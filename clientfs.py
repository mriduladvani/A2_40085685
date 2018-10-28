import socket
import argparse
import getpass

from click._compat import raw_input

parser= argparse.ArgumentParser()
parser.add_argument('request_type', type=str, help='the type of request required from the user')
parser.add_argument('spec', type=str, help='specific type of action that the user wants to have done ')
parser.add_argument('-data', type=str, action='store',nargs='+', help='the data that you want to write on the file')
parser.add_argument('-URL', type=str,help='URL of the file server')
parser.add_argument('-p', '--port',type=int , help='the port on which the server is running and the one the client wants to connect to' )
parser.add_argument('-d', '--path',type=str , help='The path to which the user requires the server to connect' )
args=parser.parse_args()
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address= (str(args.URL), args.port)
client_socket.connect(server_address)

username= raw_input("Enter username ")
password= getpass.getpass("Enter Password ")

if(args.request_type=='get'):
    if(username=="mridul" and password=="advani"):
        req_to_be_sent= args.request_type+" "+args.spec+" "+args.path
    else:
        print("HTTP Error 403: Access Denied")
else:
    data="_".join(args.data)
    if(username=="mridul" and password=="advani"):
        req_to_be_sent= args.request_type+" "+args.spec+" "+args.path+" "+data
    else:
        print("HTTP Error 403: Access Denied")




client_socket.sendall(req_to_be_sent.encode())
response=client_socket.recv(1024)
response=response.decode()
print(response)