import argparse
import socket

# obsługa argumentu --host
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="If given, connects to host instead of listening for connection.")
args = parser.parse_args()

# tworzenie gniazda + dane serwera
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = args.host
port = 5555


# obsługa klienta
def client(host):
    nickname = input("Set your nickname: ")
    print("Connecting to server ...")
    s.connect((host, 5555))
    print("Connected to server ...")

    while True:
        message = input("Me > ")
        s.send(str.encode("{0} > {1}".format(nickname, message)))
        data = s.recv(1024)
        print(data.decode('utf-8'))


# obsługa serwera
def server():
    nickname = input("Set your nickname: ")
    try:  # zajęcie portu
        s.bind(("", port))
    except socket.error as exception:
        print(str(exception))

    s.listen(2)
    conn = None

    while True:
        if conn is None:
            print("Waiting for connection...")
            conn, addr = s.accept()
            print('Got connection from ', addr)
        else:
            data = conn.recv(1024)
            print(data.decode("utf-8"))
            message = input("Me > ")
            conn.send(str.encode("{0} > {1}".format(nickname, message)))


# jeżeli podane ip hosta to ruszamy jako klient
if hostname:
    try:
        client(hostname)
    except socket.error as e:
        print(str(e))
else:
    server()
