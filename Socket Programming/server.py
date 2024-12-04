import socket
import threading

def handle_client(conn, addr):
    print(f"Connected by {addr}")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                # Client has disconnected
                print(f"Client {addr} disconnected")
                break
            print(f"Received from {addr}: {data.decode()}")
            conn.send(b"Message received\n")
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()

def start_server():
    # host = '0.0.0.0'  # Listen on all available interfaces
    host = socket.gethostname()
    port = 12345       # Port to listen on

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(2)  # Accepting up to 2 clients

    print(f"Server listening on {host}:{port}")

    # Accept connections from 2 clients
    for _ in range(2):
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

    # Once two clients are connected, close the server socket
    server_socket.close()

if __name__ == "__main__":
    start_server()