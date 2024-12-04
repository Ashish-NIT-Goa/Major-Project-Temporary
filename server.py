import socket

def start_server():
    """
    Starts a socket server and listens for incoming connections.
    """

    Port = 5555 # choose the port number those are free, from the range 1024 to 49151.
    Host = socket.gethostname() # Get local machine name, but it is suggested to assign IP manually
    print("HOST: ", Host)

    server = socket.socket() # By default it will take AF_INET and SOCK_STREAM
    print('socket created')
    server.bind((Host, Port))
    # server.bind(('localhost', 5555)) # bind the host and port number if it is TCP

    server.listen(5) # allows for maximum 5 connections

    print('waiting for connections')

    while True: # Unconditional loop to accept the connection continuously
        client_socket, addr = server.accept()
        sentence = client_socket.recv(1024).decode('utf-8')
        capital_sentence = sentence.upper()
        print('Connected to', addr)

        print('Message from client is:', capital_sentence)

        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if sentence.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break

    client_socket.send('Got your message, Thank you'.encode('utf-8'))
    client_socket.close()
    print('Connection is ended from', addr)

start_server()