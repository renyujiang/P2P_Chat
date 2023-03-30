import os
import queue
import random
import socket
import sys
import threading
import applescript
from time import sleep

from applescript import tell

my_info = {'id': 0, 'name': 'client0', 'ip': '127.0.0.1'}

client_list = [{'id': 0, 'name': 'client0', 'ip': '127.0.0.1'},
               {'id': 1, 'name': 'client1', 'ip': '127.0.0.1'},
               {'id': 2, 'name': 'client2', 'ip': '127.0.0.1'},
               {'id': 3, 'name': 'client3', 'ip': '127.0.0.1'},
               {'id': 4, 'name': 'client4', 'ip': '127.0.0.1'},
               {'id': 5, 'name': 'client5', 'ip': '127.0.0.1'},
               {'id': 6, 'name': 'client6', 'ip': '127.0.0.1'}]

help_text = 'Commands:\n' \
            '\tlist: list all clients\n' \
            '\tconnect <client_id>: connect to a client\n' \
            '\tquit: quit the program\n' \
            '\thelp: show help text\n'

# listen to the port
listen_port = 8080

listen_thread_input_queue = queue.Queue()
listen_thread_input_sign = queue.Queue()


# console thread's function
def console_thread():
    print('Welcome to chat console!')
    print('Type "help" to see all commands.\n')
    print('This app is ONLY available on MacOS for now, DO NOT run it on other platforms!\n')

    # create a thread to listen to the port
    listen_thread_console = threading.Thread(target=listen_thread)
    listen_thread_console.start()
    sleep(1)
    # loop forever until receive quit command
    while True:
        print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
        # read a line from the console
        user_input = input()
        cmd = user_input.split()
        if not listen_thread_input_sign.empty():
            listen_thread_input_queue.put(cmd[0])
            continue
        elif cmd[0] == 'connect':
            if len(cmd) != 3:
                print('Missing argument')
            else:
                connect_to_client(cmd[1])
        elif cmd[0] == 'help':
            print(help_text)
        elif cmd[0] == 'quit':
            print('Bye!')
            return 0
        else:
            print('Unknown command')


# identify current platform
def identify_platform():
    if sys.platform == 'darwin':
        return 'open -a Terminal'
    # elif sys.platform == 'win32':
    #     return 'start cmd'
    # elif sys.platform == 'linux':
    #     return 'gnome-terminal'
    else:
        return False


# open new terminal for server
def new_terminal_server(ip, port):
    # Get the absolute path of the current file
    current_file = os.path.abspath(__file__)

    # Get the absolute path of the directory containing the current file
    current_dir = os.path.dirname(current_file)

    cmd = 'python ' + current_dir + '/comm.py ' + 'server ' + ip + ' ' + str(port)

    tell.app('Terminal', 'do script "' + cmd + '"')


# open new terminal for client
def new_terminal_client(ip, port):
    # Get the absolute path of the current file
    current_file = os.path.abspath(__file__)

    # Get the absolute path of the directory containing the current file
    current_dir = os.path.dirname(current_file)

    cmd = 'python ' + current_dir + '/comm.py ' + 'client ' + ip + ' ' + str(port)

    tell.app('Terminal', 'do script "' + cmd + '"')


# list all clients
def list_clients():
    tmp = 0
    for i in client_list:
        print(i['name'], end='\t')
        tmp += 1
        if tmp % 5 == 0:
            print('')
    print('')
    return 0


# send thread's function
def send_message(sock):
    try:
        while True:
            message = input("Enter message: ")
            sock.send(message.encode())
            if message == 'quit_this':
                sock.close()
                break
    except OSError:
        print('Connection reset by peer')
        sock.close()
        return 0


# receive thread's function
def receive_message(sock):
    try:
        while True:
            message = sock.recv(1024).decode()
            if message == 'quit_this':
                sock.close()
                print('Connection reset by peer')
                break
            print("Received message: " + message)
    except OSError:
        print('Connection reset by peer')
        sock.close()
        return 0


# connect to a client
def connect_to_client(client_ip):
    # get local ip address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # use the port that the server is listening on
    server_address = (client_ip, listen_port)
    print('connecting to %s port %s' % server_address)
    # send a connection request to the server
    sock.connect(server_address)
    # receive a confirmation message from the server
    message = sock.recv(1024).decode()
    message_split = message.split()
    if message_split[0] == 'confirm':
        # create two threads to send and receive messages
        print("\x1b[1A\x1b[2K", end="")
        print('Connection established')
        new_terminal_client(client_ip, message_split[1])
        print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
        return True
    elif message_split[0] == 'reject':
        print("\x1b[1A\x1b[2K", end="")
        print('Connection rejected')
        print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
        return False
    else:
        print("\x1b[1A\x1b[2K", end="")
        print('Unknown message, connection closed')
        print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
        return False


# handle the connection
def handle_connection(conn, ip_address):
    # create a new thread to open a new terminal
    open_terminal_cmd = identify_platform()
    if not open_terminal_cmd:
        print('Unknown platform')
        return 0

    # wait for user input to confirm the connection
    print("\x1b[1A\x1b[2K", end="")
    print('Do you want to connect to ' + str(conn.getpeername()) + '? (y/n)')
    listen_thread_input_sign.put(True)
    user_input = listen_thread_input_queue.get()
    listen_thread_input_sign.queue.clear()
    if user_input == 'y' or user_input == 'Y':
        # send a confirmation message to the client
        random_port = random.randint(1024, 65535)
        message = 'confirm ' + str(random_port)
        conn.send(message.encode())
        # open a new terminal
        new_terminal_server(ip_address, random_port)
        print("\x1b[1A\x1b[2K", end="")
        print('Connection established')
        print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
    elif user_input == 'n' or user_input == 'N':
        # send a rejection message to the client
        conn.send('reject'.encode())
        conn.close()
        print("\x1b[1A\x1b[2K", end="")
        print('Connection closed')
        print(my_info['name'] + '@' + my_info['ip'] + ':~$ ', end='')
    else:
        print("\x1b[1A\x1b[2K", end="")
        print('Unknown command, connection closed')
        conn.send('reject'.encode())
        conn.close()


# listen thread's function
def listen_thread():
    # get local ip address
    hostname = socket.gethostname()
    # ip_address = socket.gethostbyname(hostname)
    ip_address = '127.0.0.1'
    print("Local IP address: " + ip_address)
    # create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the port
    server_address = (ip_address, listen_port)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)
    # listen for incoming connections
    sock.listen(1)
    conn_list = []
    while True:
        # wait for a connection
        conn, addr = sock.accept()
        conn_list.append(conn)
        print("\nListen thread:~$ " + str(addr) + " want to connect to you")

        # handle the connection
        handle_connection(conn, ip_address)


# console thread starts
if __name__ == '__main__':
    # create a new chat console
    console_thread()
