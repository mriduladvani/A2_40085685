import socket
import argparse
import os
import magic


def headers(content_type, content_disposition):
    return "\n\n" + "Content-Type= " + content_type + "\nContent-Disposition= " + content_disposition

HOST = '127.0.0.1'
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--debug_msgs', action='store_true', help='Enables Debugging messages')
parser.add_argument('-p', '--port', type=int, help='thr port on which the file server connects')
parser.add_argument('-d', '--dir_path', type=str, help='path of the directory')
args = parser.parse_args()
port = int(args.port)
def_dir_path = args.dir_path
server_address = (HOST, 65431)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(server_address)
try:
    while True:
        s.listen()
        conn, adr = s.accept()
        print('Connected by', adr)
        data = conn.recv(1024)
        data = data.decode()
        data = data.split(" ")
        req_type = data[0]
        spec = data[1]
        path=def_dir_path+spec
        n_array=path.rsplit('/',1)
        file = None





        if req_type == 'get':
            if n_array[1] == '':
                arr = os.listdir(path)
                response = "\n".join(arr)
            else:
                if '..' in path:
                    response="HTTP Error 403: Access Denied"
                else:
                    try:
                        os.path.exists(path)
                        file = open(path, "r")
                        ct = magic.from_file(path, True)
                        if(len(data)>=2):
                            cd = data[2]
                        else:
                            cd='inline'
                    except IOError:
                        response = "HTTP Error 404: File not found"
                        if args.debug_msgs:
                            print("HTTP Error 404: File not found")
                    else:
                        response = file.read()
                        if response == '':
                            response = "HTTP Error 204: No Content in the specified file"
                            if args.debug_msgs: print("HTTP Error 204: No Content in the specified file")
                        else: response=response+headers(ct,cd)
                    finally:
                        if file: file.close()


        elif req_type == 'post':
            if n_array[1] == '':
                response = "HTTP Error 405: Method not allowed"
                if args.debug_msgs:
                    print("HTTP Error 405: Method not allowed")
            else:
                if(os.path.exists(os.path.dirname(path))):
                    file = open(path, "w+")
                    try:
                        file.write(data[2])
                        response = "The data has been written onto the file"
                    except IOError:
                        response = "HTTP Error 501: The data couldn't be written onto the file"
                        if args.debug_msgs:
                            print("HTTP Error 501: The data couldn't be written onto the file")
                    finally:
                        if file:
                            file.close()
                else:
                    os.mkdir(os.path.dirname(path))
                    file = open(path, "w+")
                    try:
                        file.write(data[2])
                        response = "The data has been written onto the file"
                    except IOError:
                        response = "HTTP Error 501: The data couldn't be written onto the file"
                        if args.debug_msgs:
                            print("HTTP Error 501: The data couldn't be written onto the file")
                    finally:
                        if file:
                            file.close()
        else:
            response = "Unspecified Error"
        conn.sendall(response.encode())
finally:
        s.close()
