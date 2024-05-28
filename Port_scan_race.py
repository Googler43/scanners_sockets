import socket
import threading
import datetime
import time
from tqdm import tqdm
#import win32net

lock = threading.Lock()

def ip_dns(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return 'DNS Not Detect'

def bannergrabbing(sock):
    try:
        service = sock.recv(1024).decode()
        if service == 'None':
            return 'Баннер пуст'
        else:
            return service.replace(chr(10), ' ').replace(chr(13), ' ')
    except:
        return 'Баннер не удалось получить'


def find_service_name(port, sock):
    protocolname = 'tcp'
    try:
        try:
            return socket.getservbyport(port, protocolname)
        except:
            bannergrabbing(sock)
    except:
        pass

def get_share(ip:str):
    try:
        list_file = win32net.NetShareEnum(ip, 0)[0]
        return len(list_file)
    except:
        return 0


def write_file(result:str):
    lock.acquire()
    try:
        file = open('./result.txt', 'a')
        file.write(result)
        file.close()
    finally:
        lock.release()

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.2)
    try:
        connect = sock.connect((ip, port))
        result = f'{ip_dns(ip)}| {ip}| {port}| {find_service_name(port,sock)}\n'
        write_file(result)
        connect.close()
    except:
        pass

ip = str(open('./list_ip.txt','r').read()).split('\n')
print('IP in file ', len(ip))

port = range(445)
def popo(port, ip):
    for i in range(len(port)):
        t = threading.Thread(target=scan_port, kwargs={'ip': ip, 'port': port[i]})
        t.start()
        while threading.active_count() > 1800:
            time.sleep(0.1)

for p in tqdm(range(len(ip))):
    popo(port, ip[p])



print('All thread start')