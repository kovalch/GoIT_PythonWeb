import socket

def client_socket(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Start your conversation")
    message = input('--> ')
    while message.lower().strip() != "exit":
        client_socket.send(message.encode())
        data = client_socket.recv(1024)
        print(f'Got message from server: {data.decode()}')
        message = input('--> ')
    client_socket.close()


def main():
    SERVER_HOST = socket.gethostname() #'127.0.0.1'
    SERVER_PORT = 6000
    client_socket(SERVER_HOST, SERVER_PORT)


if __name__ == "__main__":
    main()