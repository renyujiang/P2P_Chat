import os
import socket
import sys
import threading
import applescript
from time import sleep

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
            '\tquit: quit the program\n' \
            '\thelp: show help text\n'


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
        if cmd[0] == 'quit':
            print('Bye!')
            return 0
        elif cmd[0] == 'list':
            list_clients()
        elif cmd[0] == 'help':
            print(help_text)
        else:
            print('Unknown command')


# identify current platform
def identify_platform():
    if sys.platform == 'win32':
        return 'start cmd'
    elif sys.platform == 'darwin':
        return 'open -a Terminal'
    elif sys.platform == 'linux':
        return 'gnome-terminal'
    else:
        return False


# open new terminal for different system
def open_new_terminal(open_terminal_cmd):
    os.system(open_terminal_cmd)


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


# listen thread's function
def listen_thread():
    # get local ip address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print("Local IP address: " + ip_address)
    # create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind the socket to the port
    server_address = (ip_address, 8080)
    print('starting up on %s port %s' % server_address)
    sock.bind(server_address)
    # listen for incoming connections
    sock.listen(1)
    while True:
        # wait for a connection
        conn, addr = sock.accept()
        print("\nListen thread:~$ Connected by " + str(addr))

        # create a new thread to open a new terminal
        open_terminal_cmd = identify_platform()
        if not open_terminal_cmd:
            print('Unknown platform')
            continue

        # create a new terminal to communicate
        command = 'python /Users/renyujiang/Desktop/EC530/Assignments/P2P-Chat/socket_com.py ' + str(conn)
        applescript.tell.app('Terminal', 'do script"' + command + '"', background=False)


# console thread starts
if __name__ == '__main__':
    # create a new chat console
    console_thread()
