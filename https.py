import socket
HOST= '127.0.0.1'
PORT= 65432
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn_param= (HOST, PORT)
s.bind(conn_param)
s.listen()
conn, adr= s.accept()
print('Connected by', adr)
print("\n")
data= conn.recv(1024)
data= data.decode()

dil= data.splitlines() #data in lines
req= dil[0].split(" ")

def post_param_calculate():
    array= data.split("\r\r") #array[0]=verbose array[1]=headers array[1]=inline_data array[2]=query parameters
    verbose=array[0]
    verbose_string= verbose.splitlines()
    url=(verbose_string[1].split(":"))[1]
    headers=array[1]
    inline_data=array[2]
    query_params=array[3]
    x = 0
    headers=headers.splitlines()
    resp_headers = ''
    if headers!='':
        while x < len(headers):
            half_header = headers[x].split(":")
            half_header[0] = f'"{half_header[0]}"'
            half_header[1] = f'"{half_header[1]}"'
            half_header = half_header[0] + ":" + half_header[1]
            resp_headers = resp_headers + half_header + "\n"
            x += 1

    resp_query_param=''
    if query_params!='':
        half_query_param= query_params.split("=")
        half_query_param[0]=f'"{half_query_param[0]}"'
        half_query_param[1]=f'"{half_query_param[1]}"'
        resp_query_param=half_query_param[0]+":"+half_query_param[1]

    post_response="""
    {
        "args": {"""+resp_query_param+"""
    }, 
        "data": {'"""+inline_data+"""'}
        "files": {}, 
        "form": {}, 
        "headers": {\n"""+resp_headers+""" 
            "Connection": "close", 
            "Content-Length": "6", 
            "Content-Type": "application/json", 
            "Host": """+HOST+""", 
        }, 
        "url": """+url+"""
    }
    """

    final_response= str(verbose)+"\n\n\n"+post_response
    conn.sendall(final_response.encode())





def get_param_calculate():
    array=data.split("\r\r")
    verbose=array[0]
    headers=array[1]
    query_params=array[2]
    verbose_string= verbose.splitlines()
    url=(verbose_string[1].split(":"))[1]
    x = 0
    headers = headers.splitlines()
    resp_headers = ''
    if headers!='':
        while x < len(headers):
            half_header = headers[x].split(":")
            half_header[0] = f'"{half_header[0]}"'
            half_header[1] = f'"{half_header[1]}"'
            half_header = half_header[0] + ":" + half_header[1]
            resp_headers = resp_headers + half_header + "\n"
            x += 1
    resp_query_param = ''
    if query_params!='':
        half_query_param = query_params.split("=")
        half_query_param[0] = f'"{half_query_param[0]}"'
        half_query_param[1] = f'"{half_query_param[1]}"'
        resp_query_param = half_query_param[0] + ":" + half_query_param[1]

    get_response="""
    {
      "args": {"""+resp_query_param+"""
      },
      "headers": {\n"""+resp_headers+"""
      "Connection":"close"
      "Host":"""+HOST+"""
      },
      "url": """+url+"""
    }  
    """
    final_response=verbose+"\n\n\n"+get_response
    conn.sendall(final_response.encode())

#final variable names are resp_headers, resp_inline_data and resp_query_param

if(req[0]=='GET'):
    get_param_calculate()
else:
    post_param_calculate()







conn.sendall(data.encode())




s.close()