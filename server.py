import socket
import ssl
import subprocess
import threading
from io import StringIO
import sys

port = 9091
host= "127.0.0.1"
cert="./cert.pem" #./cert.
key="./key.pem"

#Needs cert and key generated:
#openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365

def client_thread(Tconn, Taddr):        
    data = ""
    while True:
        data = Tconn.recv(1024).decode('utf-8')
        if not data:
            break
        if data == "ls -l":
            print(f"Recieved: {data} From: {Taddr}")
            Tconn.send(subprocess.check_output(['ls','-l']))
        elif data == "pwd":
            print(f"Recieved: {data} From: {Taddr}")
            Tconn.send(subprocess.check_output(['pwd']))
        else:
            try:
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()
                exec("print('test')")
                var = redirected_output.getvalue()
                sys.stdout = old_stdout
                print(var)
                if var:
                    Tconn.send(var)
                    print(f"Recieved: {data} From: {Taddr}")
                else:
                    print("else")
                    raise Exception
            except:  
                sys.stdout = old_stdout
                print("im over here")
                print(f"Recieved: {data} From: {Taddr}")
                Tconn.send(b'Invalid Command')




context = ssl.SSLContext()
context.load_cert_chain(certfile=cert, keyfile=key)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind((host, port))
    print(f"Server Started on {host}:{port}")
    while True:
        sock.listen(5)
        with context.wrap_socket(sock, server_side=True) as ssock:
            while True:
                
                conn, addr = ssock.accept()
                print('Connected by', addr)
                threading.Thread(target=client_thread, args=(conn,addr,)).start()
            
            
            
