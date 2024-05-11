import socket
import os

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
            print("Connected to the server.")
        except ConnectionRefusedError:
            print("Connection to the server failed. Make sure the server is running.")
            self.close_socket()
            exit()
        except Exception as e:
            print("Error:", e)
            self.close_socket()

    def send_choice(self, choice):
        try:
            self.socket.sendall(choice.encode('utf-8'))
        except Exception as e:
            print("Error sending choice:", e)
            self.close_socket()

    def send_message(self, message):
        try:
            self.send_choice("m")
            self.socket.sendall(message.encode('utf-8'))
            print("Message sent successfully.")
        except Exception as e:
            print("Error sending message:", e)
            self.close_socket()

    def send_file(self, filepath):
        try:
            self.send_choice("f")
            if not os.path.isfile(filepath):
                print("File does not exist.")
                return

            filename = os.path.basename(filepath)
            print(filename)
            self.socket.sendall(f"file:{filename}".encode('utf-8'))
            with open(filepath, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    self.socket.sendall(data)
                self.socket.send(b"FILE_TRANSMISSION_COMPLETE")    
                f.close()
            print("File sent successfully.")
        except Exception as e:
            print("Error sending file:", e)
            self.close_socket()

    def close_socket(self):
        try:
            if self.socket:
                self.socket.close()
        except Exception as e:
            print("Error while closing socket:", e)

if __name__ == "__main__":
    try:
        server_ip = input("Enter the server IP: ")
        server_port = int(input("Enter the server port: "))
        client = Client(server_ip, server_port)
        client.connect_to_server()

        while True:
            choice = input("Enter 'm' to send a message or 'f' to send a file: ")
            if choice == "m":
                message = input("Enter your message: ")
                client.send_message(message)
            elif choice == "f":
                filepath = input("Enter the path of the file to send: ")
                client.send_file(filepath)
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        print("Client stopped.")
    except Exception as e:
        print("Error:", e)
