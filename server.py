import socket
import threading
import time


HOST = '127.0.0.1'
PORT = 8081
LISTENER_LIMIT = 5
active_client=[]


def listen_for_messages(client, username):

    while True:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_message_to_all(final_msg)

        else:
            print(f"The message send from client {username} is empty")


def send_message_to_all(message):

    for user in active_client:
        user[1].sendall(message.encode('utf-8'))

def client_handler(client):
    
    while True:
        username=client.recv(2048).decode('utf-8')

        if username!='':
            active_client.append((username,client))
            break
        else:
            print("Username is empty")

    threading.Thread(target=listen_for_messages,args=(client,username,)).start()

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while True:

        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == '__main__':
    main()