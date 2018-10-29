import socket
import argparse
import os
import magic
HOST= '127.0.0.1'
parser= argparse.ArgumentParser()
parser.add_argument('-v', '--debug_msgs', action='store_true', help='Enables Debugging messages')
parser.add_argument('-p', '--port', type=int, help='thr port on which the file server connects')
parser.add_argument('-d', '--dir_path',type=str, help='path of the directory')
args=parser.parse_args()
port= int(args.port)
def_dir_path= args.dir_path
server_address= (HOST, 65431)
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
s.listen()
conn, adr= s.accept()
print('Connected by', adr)
data= conn.recv(1024)
data=data.decode()
data= data.split(" ")
req_type=data[0]
spec=data[1].split("/")
file= None
def headers(content_type, content_disposition):
    return "\n\n"+"Content-Type= "+content_type+"\nContent-Disposition= "+content_disposition

if(req_type=='get'):
    if(spec[1]==''):
        if(def_dir_path==data[2]):
            arr=os.listdir(data[2])
            response=", ".join(arr)
        else:
            response="HTTP Error 403: You are not authorized to access the contents of this file"
    else:
        if(def_dir_path==data[2]):
            path= data[2]+"\\"+spec[1]
            try:
                os.path.exists(path)
                file= open(path, "r")
                ct= magic.from_file(path,True)
                cd=data[3]
            except IOError:
                response="HTTP Error 404: File not found"
                if(args.debug_msgs):
                    print("HTTP Error 404: File not found")
            else:

                response=file.read()
                if(response==''):
                    response="HTTP Error 204: No Content in the specified file"
                    if (args.debug_msgs):
                        print("HTTP Error 204: No Content in the specified file")
                response=response+headers(ct,cd)
            finally:
                if file: file.close()
        else:
            response="HTTP Error 403: You are not authorized to access this file"
elif(req_type=='post'):
    if(spec[1]==''):
        response="HTTP Error 405: Method not allowed"
        if (args.debug_msgs):
            print("HTTP Error 405: Method not allowed")
    else:
        if(def_dir_path==data[2]):
            path= data[2]+"\\"+spec[1]+".txt"
            file= open(path, "w+")
            try:
                file.write(data[3])
                response="The data has been written onto the file"
            except IOError:
                response="HTTP Error 501: The data couldn't be written onto the file"
                if(args.debug_msgs):
                    print("HTTP Error 501: The data couldn't be written onto the file")
            finally:
                if file: file.close()
        else: response= "HTTP Error 403: You are not authorized to access the contents of the file"
else:
    response="Unspecified Error"
conn.sendall(response.encode())
s.close()
s.close()

