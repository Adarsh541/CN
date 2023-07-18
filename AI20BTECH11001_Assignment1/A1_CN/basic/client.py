import socket

serverIP = "10.0.1.2"

#dst_ip = raw_input("Enter dstIP: ")
dst_ip = "10.0.1.2"
s = socket.socket()

print(dst_ip)

port = 12346

s.connect((dst_ip, port))

s.send('Hello server\r\n'.encode())
print ('Client received '+s.recv(1024).decode())
#Write your code here:
#1. Add code to send HTTP GET / PUT / DELETE request. The request should also include KEY.
while True:
	req_type = raw_input("Enter the type of request: ")
	if(req_type=='g'):
		key = raw_input("Enter the value of key: ")
		req = "GET /assignment1?request="+key+" HTTP/1.1\r\n\r\n"
		s.send(req.encode())
		
	elif(req_type=='p'):
		key = raw_input("Enter the value of key: ")
		val = raw_input("Enter value corresponding to the key: ")
		req = "PUT /assignment1/"+key+'/'+val+' HTTP/1.1\r\n\r\n'
		s.send(req.encode())
	elif(req_type=='d'):
		key = raw_input("Enter the value of key: ")
		req = "DELETE"+" /assignment1/"+key+" HTTP/1.1\r\n\r\n"
		s.send(req.encode())
	else:
		break
	print("Clinet received "+s.recv(1024).decode())
	#2. Add the code to parse the response you get from the server.


s.close()
