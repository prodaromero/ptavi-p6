#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Lectura por shell
try:
    METHOD = sys.argv[1]
    LOGIN = sys.argv[2].split('@')[0]
    IP = sys.argv[2].split('@')[1].split(':')[0]
    PORT = int(sys.argv[2].split('@')[1].split(':')[1])
except:
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

#Creamos el mensaje que vamos a enviar

MESSAGE = METHOD + ' ' + 'sip:' + LOGIN + ' ' + 'SIP/2.0'


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((IP, PORT))

print("Enviando: " + MESSAGE)
my_socket.send(bytes(MESSAGE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

RECIEVE = data.decode('utf8')

print('Recibido -- ', RECIEVE)
RECIEVE = RECIEVE.split()
print(RECIEVE)

TRYING = RECIEVE[2]
RING = RECIEVE[5]
OK = RECIEVE[8]

if TRYING == 'Trying' and RING == 'Ring' and OK == 'OK':
    MESSAGE = 'ACK' + ' ' + 'sip:' + LOGIN + ' ' + 'SIP/2.0'
    print("Enviando: " + MESSAGE)
    my_socket.send(bytes(MESSAGE, 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)

print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
