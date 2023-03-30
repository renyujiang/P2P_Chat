import socket
import sys
import threading
from time import sleep


def receive_message(conn, addr):
    while True:
        # Receive message from the other side
        data = conn.recv(1024)

        if not data:
            # If the other side closes the connection, break the loop
            break

        # Print the message received from the other side
        print(f"Message from {addr[0]}:{addr[1]}: {data.decode()}")

    # Close the socket connection
    conn.close()


def server(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind IP address and port number
    s.bind((ip, port))

    # Listen on the port and wait for connections
    s.listen(1)
    print(f"Listening on port {port}...")

    while True:
        # Wait for a client connection
        conn, addr = s.accept()
        print(f"Connected to client {addr[0]}:{addr[1]}")

        # Start a new thread to handle client communication
        t = threading.Thread(target=receive_message, args=(conn, addr))
        t.start()

        # Send message to the client
        while True:
            message = input("Enter message (enter q to quit): ")

            if message == "q":
                # If user enters q, break the loop
                break

            # Send message to the client
            conn.sendall(message.encode())

        # Close the socket connection
        conn.close()
        return 0


def client(ip, port):
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    s.connect((ip, port))

    # Start a new thread to handle server communication
    t = threading.Thread(target=receive_message, args=(s, (ip, port)))
    t.start()

    # Send message to the server
    while True:
        message = input("Enter message (enter q to quit): ")

        if message == "q":
            # If user enters q, break the loop
            break

        # Send message to the server
        s.sendall(message.encode())

    # Close the socket connection
    s.close()
    return 0


if __name__ == "__main__":
    # Get command line arguments
    if len(sys.argv) != 4:
        print("Usage: python communication.py <server/client> <ip> <port>")
        sys.exit()

    mode = sys.argv[1]
    ip = sys.argv[2]
    port = int(sys.argv[3])

    if mode == "server":
        server(ip, port)
    elif mode == "client":
        sleep(2)
        client(ip, port)
    else:
        print("Invalid mode, please use 'server' or 'client'")
        sys.exit()
