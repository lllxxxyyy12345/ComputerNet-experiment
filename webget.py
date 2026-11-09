import socket

HOST = 'www.bjfu.edu.cn'
PORT = 80
PATH = '/'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
s.connect((HOST, PORT))

req = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "User-Agent: webget/1.0 (lab2)\r\n"
    "Connection: close\r\n"
    "\r\n"
)
s.sendall(req.encode())

chunks = []
count = 0

while True:
    data = s.recv(4096)
    count += 1
    print(f'recv #{count}: {len(data)} 字节')
    if not data:
        print('对端关闭，接收结束')
        break
    chunks.append(data)

s.close()

resp = b''.join(chunks)
print('-' * 40)
print(f'recv 总次数: {count}')
print(f'响应总字节: {len(resp)}')
print('-' * 40)
print(resp[:300].decode('iso-8859-1'))
