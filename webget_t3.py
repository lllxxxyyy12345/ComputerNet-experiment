import socket
import sys


def usage():
    print('用法: python3 webget_t3.py <host> <path> [port]')
    print('示例: python3 webget_t3.py www.bjfu.edu.cn /')
    print('示例: python3 webget_t3.py www.bjfu.edu.cn /index.html 8080')
    sys.exit(1)


if len(sys.argv) < 3:
    usage()

host = sys.argv[1]
path = sys.argv[2]
port = int(sys.argv[3]) if len(sys.argv) >= 4 else 80

if not path.startswith('/'):
    path = '/' + path

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(10)
try:
    s.connect((host, port))
except Exception as e:
    print(f'连接 {host}:{port} 失败: {e}')
    sys.exit(2)

req = (
    f"GET {path} HTTP/1.1\r\n"
    f"Host: {host}\r\n"
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
    sys.exit(3)

lines = head.decode('iso-8859-1').split('\r\n')

print('== 请求 ==')
print(f'{host}:{port}  {path}')
print()
print('== 状态行 ==')
print(lines[0])
print('状态码:', lines[0].split()[1])
print()
print('== 响应头 ==')
for line in lines[1:]:
    if ':' in line:
        print(line)
print()
print('== 统计 ==')
print('响应头字节:', len(head) + len(sep))
print('body 字节:', len(body))
print('recv 次数:', count)

with open('body.bin', 'wb') as f:
    f.write(body)
print()
print('body 已写入 body.bin')
