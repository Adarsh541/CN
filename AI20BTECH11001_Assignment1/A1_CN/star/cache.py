import socket

cache_ip = '10.0.1.2'
serv_ip = '10.0.1.3'
port = 12346

dic = {}

s = socket.socket()
print("Cache socket created successfully")
s.bind((cache_ip,port))
print("Cache socket binded to %s" %(port))
s.listen(5)
print("Cache is listening")

while True:
    c,addr = s.accept()
    print("Cache got connection from ",addr)
    rm1 = c.recv(1024).decode()
    print("1 Cache recieved: "+rm1)
    c.send("Hello Client".encode())
    while True:
        rm2 = c.recv(1024).decode()
        if(len(rm2)==0):
            break
        print("2 Cache recieved "+rm2)
        if(rm2[0]=="G"):
            k = rm2[25:-13]
            #print("Adarsh: "+k)
            if k in dic.keys():
                response='HTTP /1.1 200 OK '+ dic[k]+'\r\n\r\n'
            	c.send(response.encode())
            else:
            	print("Key not in cache")
            	s1 = socket.socket()
            	s1.connect((serv_ip,port))
            	s1.send("Hello server".encode())
            	print("1.1 Cache recieved "+s1.recv(1024).decode())
            	s1.send(rm2.encode())
            	val = s1.recv(1024).decode()
            	print("1.2 Cache recieved "+val)
            	if(val[17:30] == "404 Not Found"):
            		c.send(val.encode())
            	else :
            		dic[k] = val
            		c.send(val.encode())
            	s1.close()    
        elif (rm2[0]=='P'):
            s1 = socket.socket()
            s1.connect((serv_ip,port))
            s1.send("Hello Server".encode())
            print("1.1 Cache recieved "+s1.recv(1024).decode())
            s1.send(rm2.encode())
            resp = s1.recv(1024).encode()
            print("1.2 Cache recieved "+resp)
            c.send(resp.encode())
            s1.close()
        else:
            k = rm2[20:-13]
            if k in dic.keys():
                dic.pop(k)
            s1 = socket.socket()
            s1.connect((serv_ip,port))
            s1.send("Hello Server".encode())
            print("1.1 Cache recieved "+s1.recv(1024).decode())
            s1.send(rm2.encode())
            resp = s1.recv(1024).encode()
            print("1.2 Cache recieved "+resp)
            c.send(resp.encode())
            s1.close()
            #c.send("OK no probs client".encode())

    c.close()