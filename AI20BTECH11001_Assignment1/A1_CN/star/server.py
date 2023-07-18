import socket

#WRITE CODE HERE:
#1. Create a KEY-VALUE pairs (Create a dictionary OR Maintain a text file for KEY-VALUES).
dic = {}

#dst_ip = str(input("Enter Server IP: "))
serv_ip = "10.0.1.3"
s = socket.socket()
print ("Socket successfully created")

dport = 12346

s.bind((serv_ip, dport))
print ("socket binded to %s" %(dport))

s.listen(5)
print ("socket is listening")

while True:
  c, addr = s.accept()
  print ('Got connection from', addr )
  c.send('Hello client'.encode())
  while True:

    #Write your code here
    req = c.recv(1024).decode()
    if len(req)==0:
      break
    print('Server received '+req)
    if(req[0]=="G"):
      k = req[25:-13]
      response='HTTP /1.1 200 OK '+ dic[k]+'\r\n\r\n'
      c.send(response.encode())
    elif(req[0]=="P"):
      ar = []
      for i in range(5,len(req)):
        if(req[i]=='/'):
          ar.append(i)
      k = req[ar[0]+1:ar[1]]
      v = req[ar[1]+1:-13]
      dic[k]=v
      c.send("HTTP /1.1 201 CREATED\r\n\r\n".encode())
    elif(req[0]=='D'):
      k = req[20:-13]
      dic.pop(k)
      c.send("HTTP /1.1 200 OK\r\n\r\n".encode())
  #1. Uncomment c.send 
  #2. Parse the received HTTP request
  #3. Do the necessary operation depending upon whether it is GET, PUT or DELETE
  #4. Send response
  ##################

  c.close()
  #break