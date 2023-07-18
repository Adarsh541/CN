import socket
import time
senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#msg = '1001011'
# big data to be sent
#data = b'savaranadattareddyadarshsaiadepu'
img_file = open("testFile.jpg","rb")
data = img_file.read()
#data = str(data)
packet_size = bufferSize-3
# number of packets to be sent to transfer whole data
num_pkts = len(data)//packet_size
rem = len(data)%packet_size
number_of_ret =0
if(rem==0):
	num_pkts = num_pkts
else:
	num_pkts = num_pkts+1
seq_num = 0
end_flg = 0
tmt = int(input("Timeout in ms:"))
tmt/=1000
#tmt = 5/1000
# send each pkt
start=time.time()
for i in range(num_pkts):
	print(i)
	if(i+1 == num_pkts):
		pkt_data = data[packet_size*i:]
		end_flg = 1
	else:
		pkt_data = data[packet_size*i:packet_size*i+packet_size]
	# make pkt
	pkt = seq_num.to_bytes(2,'big')+end_flg.to_bytes(1,'big')+pkt_data
	# print(len(pkt))
	# send pkt and start deadline
	socket_udp.sendto(pkt,recieverAddressPort)
	# print(pkt)
	deadline = time.time()+tmt
	# process till the current pkt is aknowledged
	is_ack = False
	while not is_ack:
		try:
			socket_udp.settimeout(deadline-time.time())
			recv_msg = socket_udp.recvfrom(bufferSize)
			ack = recv_msg[0]
			ack_seq_num_bytes = ack[0:2]
			while ack_seq_num_bytes!=seq_num.to_bytes(2,'big'):
				socket_udp.settimeout(deadline-time.time())
				recv_msg1 = socket_udp.recvfrom(bufferSize)
				ack1 = recv_msg1[0]
				ack_seq_num_bytes = ack1[0:2]
			is_ack = True
		except:
			# resend pkt
			print('Timeout Resending...')
			number_of_ret +=1
			socket_udp.sendto(pkt,recieverAddressPort)
			deadline = time.time()+tmt
	seq_num = 1-seq_num

img_file.close()
end=time.time()
time_diff=end-start
print('Number of Re transmissions:',number_of_ret)
print('Throughput is : ',len(data)/(1024*time_diff))
'''while True:

    # Send to server using created UDP socket
    msg = input("Please enter message to send: ")
    message = str.encode(msg)

    socket_udp.sendto(message, recieverAddressPort)
    try:
    #wait for reply message from reciever
    	msgFromServer = socket_udp.recvfrom(bufferSize)
    	print("Printing the whole recieved msg: ",msgFromServer)
    	msgString = "Message from Server {}".format(msgFromServer[0])
    	print(msgString)'''
