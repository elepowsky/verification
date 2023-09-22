import socket
import datetime

host = '##:##:##:##:##:##'
port = 7

backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((host,port))
s.listen(backlog)
print(f'Listening on {host}:{port}')

cmd = ''
try:
    client, address = s.accept()
    while True:
        cmd = input('TO PI: ')
        client.send(bytes(cmd, 'UTF-8'))
        print('Sent: ', str(datetime.datetime.now()))
        
        if cmd == 'quit':
            print("Closing socket")	
            client.close()
            s.close()
        
        data = client.recv(size)
        if data:
            data = data.decode().strip()
            if data.isnumeric():
                data = int(data)
            print('Received: ', data)

except:	
    if cmd != 'quit':
        print("Closing socket")	
        client.close()
        s.close()

