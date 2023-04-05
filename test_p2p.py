import subprocess
import time
import unittest
from io import StringIO
from unittest.mock import patch

from comm import server, client
from console import *


class TestConsole(unittest.TestCase):

    def test_register(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        fake_inputs = ['test1', '1.1.1.1']
        with patch('builtins.input', side_effect=fake_inputs):
            ret = register_to_db()
            self.assertEqual(ret, True)

        fake_inputs = ['test2', '1.1.1.2']
        with patch('builtins.input', side_effect=fake_inputs):
            ret = register_to_db()
            self.assertEqual(ret, True)

        fake_inputs = ['test3', '1.1.1.3']
        with patch('builtins.input', side_effect=fake_inputs):
            ret = register_to_db()
            self.assertEqual(ret, True)

    def test_list_clients(self):
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            list_clients()
            self.assertIn('test1  1.1.1.1\ttest2  1.1.1.2\ttest3  1.1.1.3', fake_stdout.getvalue())

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as fake_stdout:
            help_show()
            self.assertIn("Commands:\n\tlist: list all clients\n\tconnect <ip> <port>: connect to a "
                          "client\n\tregister: register a new client\n\tquit: quit the program\n\thistory: show "
                          "connection history\n\thelp: show help text", fake_stdout.getvalue())


# class TestCommunication(unittest.TestCase):
#     def setUp(self):
#         self.server_port = 8080
#         self.ip = '127.0.0.1'
#
#     def test_server(self):
#         def run_server():
#             subprocess.call(["python", "comm.py", "server", "127.0.0.1", str(8080)])
#
#         def run_client():
#             client("127.0.0.1", 8080)
#
#         server_thread = threading.Thread(target=run_server)
#         server_thread.start()
#
#         time.sleep(1)
#
#         fake_inputs = ['hello from client', 'test2','q']
#         with patch('builtins.input', side_effect=fake_inputs):
#             with patch('sys.stdout', new=StringIO()) as fake_stdout:
#                 client_thread = threading.Thread(target=run_client)
#                 client_thread.start()
#                 time.sleep(1)
#                 self.assertIn('13242546', fake_stdout.getvalue())
