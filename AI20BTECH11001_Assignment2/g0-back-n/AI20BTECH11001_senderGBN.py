import socket
import time
senderIP = "10.0.0.1"
senderPort   = 20001
recieverAddressPort = ("10.0.0.2", 20002)
bufferSize  = 1024 #Message Buffer Size

N = int(input("Enter window size: "))
#N=4

# Create a UDP socket at reciever side
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

tmt = int(input("Timeout in ms:"))
#tmt=25
socket_udp.settimeout(tmt/1000)

end_flg = 0
img_file = open("testFile.jpg","rb")
data = img_file.read()
print("data length: ",len(data))

# splitting data into chunks
packet_size = bufferSize-3
num_pkts = len(data)//packet_size
rem = len(data)%packet_size
if(rem==0):
	num_pkts = num_pkts
else:
	num_pkts = num_pkts+1
chunk_data = []
for i in range(num_pkts):
	if(i+1 == num_pkts):
		chunk_data.append(data[packet_size*i:])
	else: 
		chunk_data.append(data[packet_size*i:packet_size*i+packet_size])

start=time.time()
window_buffer=[]
for i in range(N):
	if(i==num_pkts-1):
		end_flg = 1
	pkt = i.to_bytes(2,'big')+end_flg.to_bytes(1,'big')+chunk_data[i]
	socket_udp.sendto(pkt,recieverAddressPort)
	window_buffer.append(pkt)
base = 0
next_seq_num = N

while base<num_pkts:
	while(len(window_buffer)<N and next_seq_num<len(chunk_data)):
		if(next_seq_num==(len(chunk_data)-1)):
			end_flg=1
		pkt = next_seq_num.to_bytes(2,'big')+end_flg.to_bytes(1,'big')+chunk_data[next_seq_num]
		socket_udp.sendto(pkt,recieverAddressPort)
		window_buffer.append(pkt)
		next_seq_num+=1

	try:
		recv_pkt = socket_udp.recvfrom(bufferSize)
		recv_msg = recv_pkt[0]
		if(recv_msg[0:2]>=(base).to_bytes(2,'big')):
			new_base = int.from_bytes(recv_msg[0:2],'big') + 1
			while base!=new_base:
				window_buffer.pop(0)
				base+=1

	except socket.timeout:
		print("timeout")
		# for j in range(base,next_seq_num):
		# 	if(j==num_pkts-1):
		# 		end_flg = 1
		# 	pkt = (j%N).to_bytes(2,'big')+end_flg.to_bytes(1,'big')+chunk_data[j]
		# 	socket_udp.sendto(pkt,recieverAddressPort)
		for pkt in window_buffer:
			socket_udp.sendto(pkt,recieverAddressPort)

end=time.time()
time_diff=end-start
print("Throughput is :",len(data)/(1024* time_diff))
