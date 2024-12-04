import socket
import threading

def handle_client(conn, addr):
    """Handles communication with a connected client."""
    print(f"Connected by {addr}")
    try:
        while True:
            # Receive data from the client
            data = conn.recv(1024)
            if not data:
                print(f"Client {addr} disconnected")
                break
            print(f"Received from {addr}: {data.decode()}")

            # Decide the signal based on density (mock logic for now)
            # Example response to client
            conn.sendall(b"Green light for: Lane_1, Red for others\n")
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed")

def start_server():
    """Starts the server to accept connections from multiple clients."""
    host = socket.gethostname()  # Use the server's hostname or IP address
    port = 12345  # Port to listen on

    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Allow reuse of the address
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(4)  # Listen for up to 4 connections
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            # Accept a new client connection
            conn, addr = server_socket.accept()
            print(f"New connection from {addr}")
            # Create a thread for the client
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server shutting down")
    finally:
        server_socket.close()
        print("Server socket closed")

if __name__ == "__main__":
    start_server()
