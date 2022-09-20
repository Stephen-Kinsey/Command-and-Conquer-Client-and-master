import socket
import ssl

host = '127.0.0.1'
port = 9091
HEADER_LENGTH = 10
#Use `ncat -nvlp 9099 --ssl` to listen
#Or use the server...

context = ssl.SSLContext() #Defaults to TLS 
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations('./cert.pem')

message = ""
with socket.create_connection((host, port)) as sock:
    ssock=context.wrap_socket(sock, server_hostname=host)
    while True:
        message = input("")
        if message != "":
            message = message.encode("utf-8")
                #Create secure socket
    
            ssock.send(message)
            while True:
                data = ssock.recv(1024)
                if data: 
                    print(data.decode('utf-8'))
                    #ssock.shutdown(2) #Nicely close the encrypted channel
                    break 
        message=''
