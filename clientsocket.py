import math
import socket
import threading
import random
import os
CLIENT_FOLDER = "client_folder"
folder_name = 'download'

nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5566))
SIZE = 1024
FORMAT = 'utf-8'

#define download path
folder_path = os.path.join(CLIENT_FOLDER, folder_name)
try:
    os.makedirs(folder_path)
except:
    pass

#send nick name to store user info
client.send(nickname.encode(FORMAT))


def receive():
    while True:
        try:
            #receive response sms
            msg = client.recv(SIZE).decode(FORMAT)
            if msg:
                taken = msg.split(":")
                # if response sms tag is list then print it to show the list of file
                if taken[0] == 'LIST':
                    for item in taken[1:]:
                        print(item)
                # if response sms tag is data then open a file and write bits to it
                elif taken[0] == 'DATA':
                    file_name = taken[1]
                    size = int(taken[2])
                    total_size = size
                    file_path = os.path.join(folder_path, file_name)
                    print(file_path)
                    print(size)
                    print("File download start")
                    with open(file_path, 'wb') as file:
                        while True:
                            #receiving content
                            content = client.recv(SIZE)
                            size = size - len(content)
                            percent = math.ceil(((total_size-size)/total_size)*100)
                            print(f"File download completed {percent}%")
                            if size == 0:
                                break
                            file.write(content)
                        file.write(content)
                        print("File downloaded successful")
                        print(size)
                        file.close()
                elif taken[0] == 'CLOSE':
                    break
                elif taken[0] == 'Error':
                    print(taken[1])
        except:
            print("An error occured!")
            client.close()
            break
print("""
Welcome to the File Sharing System!

Commands:
- Enter [list] to see files.
- Enter [search] to search for a file.
- Enter [file_name] to download a file.
- Enter [close] or use Ctrl+C to exit.
- Enter [message] followed by text to send an SMS to all.
""")


def write():
    while True:
        message = input()
        mess = message
        if (message.upper()=='HELP'):
            print("Commands:")
            print("- Enter [list] to see files.")
            print("- Enter [search] to search for a file.")
            print("- Enter [file_name] to download a file.")
            print("- Enter [close] or use Ctrl+C to exit.")
            print("- Enter [message] followed by text to send an SMS.")
        if(message.upper()=='SEARCH'):
            #search need to file name input to find data
            file = input('Enter file name to search  ')
            message = f'{message}:{file}'
        elif(message.upper()=='MESSAGE'):
            #search need to file name input to find data
            file = input('Enter message to send all  ')
            message = f'{message}:{nickname};- {file}'
        elif(message.upper()=='UPLOAD'):
            path = input("Enter file path ")
            file_name = input("Enter file name ")
            message = f'{message}:{file_name}'
        #     client.send()
        else:
            #to download and list command we need only one type data so i add nickname with it to make it two split
            message = f'{nickname}:{message}'
        if (mess.upper()!='UPLOAD'):
            client.send(message.encode(FORMAT))

        elif (mess.upper()=='UPLOAD'):
            try:
                file_path = os.path.join(path,file_name)
                file_size = os.path.getsize(file_path)
                print(f'{file_name} upload start that is {file_size} bit')
                size = 0
                message = f'{message}:{file_size}'
                client.send(message.encode(FORMAT))
                with open(file_path, "rb") as file:
                    file_data = file.read(SIZE)
                    while file_data:
                        client.send(file_data)
                        size = size + len(file_data)
                        percent = math.ceil((size/file_size)*100)
                        print(f'File upload complete {percent}%')
                        file_data = file.read(SIZE)
                    #ensure complete of transmission
                    file.close()
                    print("File Upload Succesful")
            except:
                print("Error in file upload")
        elif(mess.upper()=='CLOSE'):
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
