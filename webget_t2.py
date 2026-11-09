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
    if not data:
        break
    chunks.append(data)
s.close()

resp = b''.join(chunks)

head, sep, body = resp.partition(b'\r\n\r\n')
if not sep:
    print('错误：响应里找不到 \\r\\n\\r\\n')
    raise SystemExit(1)

lines = head.decode('iso-8859-1').split('\r\n')

print('== 状态行 ==')
print(lines[0])
print('状态码:', lines[0].split()[1])

print()
print('== 响应头 ==')
headers = {}
for line in lines[1:]:
    if ':' in line:
        k, v = line.split(':', 1)
        headers[k.strip()] = v.strip()
        print(f'{k.strip()}: {v.strip()}')

print()
print('== 统计 ==')
print('响应头字节:', len(head) + len(sep))
print('body 字节:', len(body))
print('recv 次数:', count)

with open('body.bin', 'wb') as f:
    f.write(body)

print()
print('body 已写入 body.bin')
