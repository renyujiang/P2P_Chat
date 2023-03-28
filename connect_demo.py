import socket
import threading


# send thread's function
def send_message(sock):
    try:
        while True:
            message = input("Enter message: ")
            sock.send(message.encode())
            if message == "quit":
                sock.close()
                break
    except OSError:
        print("Connection reset by peer")
        sock.close()
        return 0


# receive thread's function
def receive_message(sock):
    try:
        while True:
            message = sock.recv(1024).decode()
            if message == "quit":
                sock.close()
                break
            print("Received message: " + message)
    except OSError:
        print("Connection reset by peer")
        sock.close()
        return 0


def main():
    # 定义服务器的 IP 地址和端口号
    server_ip = "10.239.81.4"
    server_port = 8080

    # 创建 Socket 对象
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 连接到服务器
    sock.connect((server_ip, server_port))
    print(sock)
    print("Connected to server")

    # create two new thread to send and receive message
    t1 = threading.Thread(target=send_message, args=(sock,))
    t2 = threading.Thread(target=receive_message, args=(sock,))
    t1.start()
    t2.start()


if __name__ == "__main__":
    main()
