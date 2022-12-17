import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 8081

def listen_messages_from_server(client):
    while True:
        message=client.recv(2048).decode('utf-8')

        print(message)

def send_message_to_server(client):

    while True:
        message=input("Message")
        if message!='':
            client.sendall(message.encode())
        else:
            print("Message can not empty")

def main():

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print(f"connected to the server on {HOST} {PORT}")
    except:
        print(f"Unable to connect to host {HOST} and port {PORT}")

    while True:
        username=input("Enter Username")

        if username!='':
            client.sendall(username.encode())
            break
        else:
            print("Username can not be empty")
            exit(0)

    
    threading.Thread(target=listen_messages_from_server,args=(client,)).start()
    send_message_to_server(client)

if __name__ == '__main__':
    main()