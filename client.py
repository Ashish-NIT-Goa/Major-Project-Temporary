import socket

def socket_client():
    """
    This function creates a client socket and connects to a server using the provided host and port.
    It sends a lowercase sentence to the server and receives the response from the server.
    """

    Host = 'LAPTOP-ASHISH'
    Port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((Host, Port))

    sentence = input('Enter lowercase sentences: ')

    client.send(sentence.encode('utf-8'))
    print('From receiver:')
    print(client.recv(1024).decode('utf-8'))

socket_client()