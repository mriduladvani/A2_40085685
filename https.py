import socket
HOST= '127.0.0.1'
PORT= 65432
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_param= (HOST, PORT)
s.bind(conn_param)
s.listen()
conn, adr= s.accept()
print('Connected by', adr)
while True:
    data= conn.recv(1024)
    if not data:
       break
    conn.sendall(data)

s.close()