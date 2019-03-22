import sys
import socket

def get(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('whois.arin.net', 43))

    # string -> bytes
    s.send((ip + '\r\n').encode())

    response = b''
    while True:
        data = s.recv(4096)
        response += data
        if not data:
            break
    s.close()

    return response.decode()

