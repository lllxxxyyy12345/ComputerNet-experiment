from socket import *
clientSocket = socket(AF_INET, SOCK_DGRAM)
with open('/etc/services', 'rb') as f:
    data = f.read(2000)
print('发送字节数:', len(data))
clientSocket.sendto(data, ('127.0.0.1', 5201))
msg, addr = clientSocket.recvfrom(4096)
print('回包长度:', len(msg))
clientSocket.close()
