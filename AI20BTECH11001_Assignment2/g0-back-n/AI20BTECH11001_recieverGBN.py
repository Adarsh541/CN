import socket
import time
recieverIP = "10.0.0.2"
recieverPort   = 20002
bufferSize  = 1024 #Message Buffer Size

# bytesToSend = str.encode(msgFromServer)

# Create a UDP socket
socket_udp = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind socket to localIP and localPort
socket_udp.bind((recieverIP, recieverPort))

print("UDP socket created successfully....." )
recv_data_file = open("recv_tst_img.jpg","wb")

# while True:
    #wait to recieve message from the server
data = b''
end_flg = 0
exp_seq_num = 0
while not end_flg:
    rcv_pkt = socket_udp.recvfrom(bufferSize)
    # print("reciever recieved: ",rcv_pkt[0][0:2]) #print recieved message
    recievedMessage = rcv_pkt[0]
    senderAddress = rcv_pkt[1]
    
    if(recievedMessage[0:2]==exp_seq_num.to_bytes(2,'big')):
        data = data + recievedMessage[3:]
        ack = exp_seq_num.to_bytes(2,'big') + b'ack'
        exp_seq_num +=1
        print(exp_seq_num)
        end_flg = recievedMessage[2]
    else:
        ack= (exp_seq_num-1).to_bytes(2,'big') + b'ack'
    socket_udp.sendto(ack,senderAddress)

print("len byte data:",len(data))
recv_data_file.write(data)
recv_data_file.close()
