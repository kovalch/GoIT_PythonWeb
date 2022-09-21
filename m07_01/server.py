import socket

def chat_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)
    conn, addr = server_socket.accept()
    print(f"Connected from {addr}")
    while True:
        # receive a Kilobyte data
        data = conn.recv(1024)
        if not data:
            break

        print(f'Got message from client: {data.decode()}')
        data = input("-->")

        if data == "exit":
            print('Server sent "exit" to the client')
            return False

        conn.send(data.encode())
    conn.close()


def main():
    SERVER_HOST = socket.gethostname() #'127.0.0.1'
    SERVER_PORT = 6000
    chat_server(SERVER_HOST, SERVER_PORT)


if __name__ == "__main__":
    main()