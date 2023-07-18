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


while True:

    #wait to recieve message from the server
    data = b''
    end_flg = 0
    seq_num = 0
    while not end_flg:
        bytesAddressPair = socket_udp.recvfrom(bufferSize)
        recievedMessage = bytesAddressPair[0]
        seq_got=recievedMessage[0:2]
        # print(seq_got)
        senderAddress = bytesAddressPair[1]
        end_flg = recievedMessage[2]
        # print(end_flg)
        if(seq_got==seq_num.to_bytes(2,'big')):
            data = data + recievedMessage[3:]
            seq_num = 1-seq_num
        ack = recievedMessage[0:2] + b'vachindhi ra puha'
        socket_udp.sendto(ack,senderAddress)
    recv_data_file.write(data)
    recv_data_file.close()
