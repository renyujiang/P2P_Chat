import subprocess
import time

import comm
import threading


def run_server():
    subprocess.call(["python", "comm.py", "server", "127.0.0.1", str(8080)])


def run_client():
    comm.client("127.0.0.1", 8080)


if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    time.sleep(1)
    client_thread = threading.Thread(target=run_client)
    client_thread.start()
