import socket
import threading
import random
import os

SERVER_FOLDER = "server_folder"

host = '127.0.0.1'
port = 5566
SIZE = 1024
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []
nicknames = []

#define upload path
path = os.path.join(SERVER_FOLDER, "uploads")

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            message = message.decode(FORMAT)
            if message:
                splits = message.split(":")
            else:
                continue
            if len(splits) == 2:
                nick = splits[0]
                file_name = splits[1]
            else:
                nick = splits[0]
                file_name = splits[1]
                file_size = splits[2]
            # close to close the client
            if file_name.upper() == 'CLOSE':
                client.send('CLOSE:a'.encode(FORMAT))
                try:
                    client.close()
                except:
                    print("Error closing client")
            #list to list the name of the files avaiable to upload
            elif file_name.upper() == 'LIST':
                #store files name to give response of list command
                files = sorted(os.listdir(path))
                mess = 'LIST'
                for file in files:
                    mess = f'{mess}:{file}'
                client.send(mess.encode(FORMAT))
            elif nick.upper() == 'SEARCH':
                #store files name to give response of search command
                files = sorted(os.listdir(path))
                file_name = file_name.upper()
                mess = 'LIST'
                for file in files:
                    if file_name in file.upper():
                        mess = f'{mess}:{file}'
                client.send(mess.encode(FORMAT))
            elif nick.upper() == 'MESSAGE':
                mess = 'LIST'
                mess = f'{mess}:{file_name}'
                for client in clients:
                    if client:
                        print(client)
                        client.send(mess.encode(FORMAT))
            elif nick.upper() == 'UPLOAD':
                try:
                    size = int(file_size)
                    file_path = os.path.join(path, file_name)
                    with open(file_path, 'wb') as file:
                        while True:
                            #receiving content
                            content = client.recv(SIZE)
                            get_size = len(content)
                            size = size - get_size
                            if size == 0:
                                break
                            file.write(content)
                        file.write(content)
                        file.close()
                except:
                    print("Error in file upload")
            else:
                ok = True
                try:
                    file_path = os.path.join(path, file_name)
                    file_size = os.path.getsize(file_path)
                    #DATA is indicator to client to server sending file
                    mess = f'DATA:{file_name}:{file_size}'
                    client.send(mess.encode(FORMAT))
                    with open(file_path, "rb") as file:
                        file_data = file.read(SIZE)
                        while file_data:
                           client.send(file_data)
                           file_data = file.read(SIZE)
                        #print with file send where
                        print(f'{file_name} sent to {nick}')
                        file.close()
                except:
                   mess = f'Error:No such file'
                   ok = False
                   client.send(mess.encode(FORMAT))
                if ok:
                    print(f'{nick} {file_name} send')
        except Exception as e:
            print(f"Error in handling client: {e}")
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(f"Connected with {address} connected")

        # Request And Store Nickname
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)
        print(f'{nickname} is connected')
    
        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening...")
receive()
