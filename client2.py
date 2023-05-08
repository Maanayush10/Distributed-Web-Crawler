import socket

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host= '127.0.0.1'
port= 12345

print("Waiting for Connections...")

try:
    s.connect((host, port))
except socket.error as e:
    print(e)

Response = s.recv(4096)
while True:
    Input= input('Choose a website to crawl : COSMOPOLITAN, IMDB:\n')
    s.send(str.encode(Input))
    Response = s.recv(4096)
    print('From Server : ' + Response.decode())
s.close()