import ssl
import OpenSSL
import threading
import time

lock = threading.Lock()

def write_data(stri: str):
    lock.acquire()
    try:
        end_file = open('./ssl_data_balance_dns.txt', 'a')
        end_file.write(stri)
        end_file.close()
    finally:
        lock.release()


def get_data_ssl_sert(url: str):
    try:
        host = url.replace('https://', '').replace('http://', '').replace('/', '')
        data = ssl.get_server_certificate((host, 443))

        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, data)
        return x509.get_issuer().get_components()
    except:
        return None

host_list = open('dns_server_list_bez_balance.txt', 'r').read().split('\n')

def main_fnc(host_i):
    ssl_data = get_data_ssl_sert(host_i)
    if ssl_data is not None:
        write_data(f"{host_i}| {ssl_data} \n")

for i in range(len(host_list)):
    print(f'{i+1} in {len(host_list)}')
    t = threading.Thread(target=main_fnc, kwargs={'host_i': host_list[i]})
    t.start()
    while threading.active_count() > 100:
        time.sleep(0.5)

