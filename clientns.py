import socket
import argparse

parser= argparse.ArgumentParser()
parser.add_argument('request_type', type=str, help='the type of request that the user wants to send')
parser.add_argument('URL', type=str, help='signifies the request URL')
parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
parser.add_argument('-k', '--header', action='append', help='the headers that are intended to be passed request' )
parser.add_argument('-d', '--data', action='append', help='the inline data intended to be passed in request')
parser.add_argument('-f', '--readfile', action='store', help='reads the content of the file to be passed in the request')
parser.add_argument('-o', '--writefile', action='store', help='to write the response of the body on a new file')
args=parser.parse_args()
actual_url=args.URL.split("/")
url=''.join(actual_url[0])
client_socket= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((url, 65432))
query_param=''
query= (args.URL).split("/?")
if(len(query)>1):
 query_param= query[1] #get data query param
get_request= "GET /get "+args.URL+" HTTP/1.0\r\nHost:"+args.URL+"\r\n" #get data request

aheaders=''
if args.header:
    for x in args.header:
        aheaders= aheaders+x+"""\r\n""" #get data all headers

#condition check for -d and -f to not be used simultaneously
#data for post
data=''
if (args.readfile) and (args.data):
    print('you cant use -d and -f together')
    exit(0)
elif (args.data) and (args.readfile!=True):
    y= '&'.join(args.data)
    data=y
elif (args.data!=True) and (args.readfile):
    file=open(args.readfile, "r")
    data= file.read()


get_send= get_request+"\r\r"+aheaders+"\r\r"+query_param #items to be sent in a get request: 1. request 2.query parameters 3.headers

post_send = """\
POST http://"""+args.URL+""" HTTP/1.1\r
Host: """+args.URL+"""\r
Content-Type: application/json\r
Content-Length: """+str(len(data)+1)+"""\r
Connection: close"""+"""\r\r"""+aheaders+"""\r\r"""+data+"""\r\r"""+query_param+""""""



if args.request_type!='get':
    client_socket.sendall(post_send.encode())
else:
    client_socket.sendall(get_send.encode())

response= client_socket.recv(1024)
response=response.decode()

response=response.split("\n\n\n")
if(args.verbose):
    print(response[0]+"\n\n"+response[1])
else:
    print(response[1])


if(args.verbose) and (args.writefile):
    file = open(args.writefile, "w+")
    file.write(response[0]+"\n\n"+response[1])
    print("The above response has been written onto the file")
elif(args.verbose!=True) and  (args.writefile):
    file=open(args.writefile, "w+")
    file.write(response[1])
    print("The above response has been written onto the file")

client_socket.close()