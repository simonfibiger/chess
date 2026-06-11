import socket
from _thread import * 
import sys


server = ""
port = 5555

socet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socet.bind((server, port))
except socet.error as e:
    print(str(e))
    
socet.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")
            if not data:
                print("No data received, closing connection.")
                break  # No data means the client has disconnected
            else:
                print("Received: " + reply)
                print("Sending: " + reply)
                
            conn.sendall(str.encode(reply))  # Echo back the received data
        except Exception as e:
            print("Error: " + str(e))
            break
        data = conn.recv(2048)
while True:
    conn, addr = socet.accept()
    print("Connected to: " + addr[0] + ":" + str(addr[1]))

