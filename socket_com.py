# create two new thread to send and receive message
import socket
import sys
import threading


# send thread's function
def send_message(sock):
    while True:
        message = input("Enter message: ")
        sock.send(message.encode())


# receive thread's function
def receive_message(sock):
    while True:
        message = sock.recv(1024).decode()
        print("Received message: " + message)


conn = sys.argv[1]
fd = int(conn.split('[')[1].split(']')[0])
client_socket_obj = socket.fromfd(fd, socket.AF_INET, socket.SOCK_STREAM)

t1 = threading.Thread(target=send_message, args=(client_socket_obj,))
t2 = threading.Thread(target=receive_message, args=(client_socket_obj,))
t1.start()
t2.start()
