import socket
import threading
import os

CLIENT_FOLDER = "client_folder"
folder_name = 'download'

nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55558))
SIZE = 1024
FORMAT = 'utf-8'  # Changed 'utf' to 'utf-8'

folder_path = os.path.join(CLIENT_FOLDER, folder_name)
try:
    os.makedirs(folder_path)
except FileExistsError:
    print(f"Already exists")

client.send(nickname.encode(FORMAT))


def receive():
    while True:
        try:
            msg = client.recv(SIZE).decode(FORMAT)
            if not msg:
               continue
            cmd, data = msg.split(":")
            print(f'{cmd} {data}')
            # Uncomment and complete the sections related to file handling based on your requirements.
            # if cmd == "FILENAME":
            #     """ Recv the file name """
            #     print(f"[CLIENT] Received the filename: {data}.")
            #     file_path = os.path.join(folder_path, data)
            #     file = open(file_path, "w")
            #     print("Filename received.")
            # elif cmd == "DATA":
            #     """ Recv data from client """
            #     print(f"[CLIENT] Receiving the file data.")
            #     file.write(data)
            #     print("File data received")
            # elif cmd == "FINISH":
            #     file.close()
            #     print("The data is saved.")
            # elif cmd == 'Error':
            #     print(data)
            # elif cmd == "CLOSE":
            #     break
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break


def write():
    while True:
        try:
            message = input("Enter file name or [close] to stop ")
            message = f'{nickname}:{message}'
            client.send(message.encode(FORMAT))
            if message.upper() == 'CLOSE':
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
