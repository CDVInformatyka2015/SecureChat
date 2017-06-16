import rsa
import argparse
import socket
import pickle

# obsługa argumentu --host
parser = argparse.ArgumentParser()
parser.add_argument("--host", help="If given, connects to host instead of listening for connection.")
args = parser.parse_args()

# tworzenie gniazda + dane serwera
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = args.host
port = 5555


# Generowanie klucza RSA
def rsagen():
    print("Trwa generowanie klucza!")
    return rsa.newkeys(2048)


# obsługa klienta
def client(host):
    print("Connecting to server...")
    s.connect((host, 5555))
    print("Connected to server...")

    data = {
        'nickname': nickname,
        'message': '',
        'pubkey': pubkey
    }
    s.send(pickle.dumps(data))

    while True:
        data = s.recv(1024)
        info = pickle.loads(data)
        print("{0} > {1}".format(info['nickname'], rsa.decrypt(info['message'], privkey).decode('utf8')))
        message = input("Me > ")
        data = {
            'nickname': nickname,
            'message': rsa.encrypt(message.encode('utf8'), info['pubkey']),
            'pubkey': pubkey
        }
        s.send(pickle.dumps(data))


# obsługa serwera
def server():
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
            info = pickle.loads(data)
            print("{0} > {1}".format(info['nickname'], rsa.decrypt(info['message'], privkey).decode('utf8')))
            message = input("Me > ")
            data = {
                'nickname': nickname,
                'message': rsa.encrypt(message.encode('utf8'), info['pubkey']),
                'pubkey': pubkey
            }
            conn.send(pickle.dumps(data))


# jeżeli podane ip hosta to ruszamy jako klient
def main():
    if hostname:
        try:
            client(hostname)
        except socket.error as e:
            print(str(e))
    else:
        server()


if __name__ == "__main__":
    nickname = input("Set your nickname: ")
    (pubkey, privkey) = rsagen()
    main()
