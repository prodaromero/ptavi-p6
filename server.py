#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        #self.wfile.write(b"Hemos recibido tu peticion" + b'\r\n\r\n')
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if not line:
                break
            MESSAGE = line.decode('utf-8')
            print("El cliente nos manda " + MESSAGE)
            METHOD = MESSAGE.split(' ')[0]

            if METHOD == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 Trying" + b"\r\n\r\n" +
                                 b"SIP/2.0 180 Ring" + b"\r\n\r\n" +
                                 b"SIP/2.0 200 OK" + b"\r\n\r\n")
            elif METHOD == 'BYE':
                self.wfile.write(b"SIP/2.0 200 OK" + b"\r\n\r\n")
            elif METHOD == 'ACK':
                #cuando se nos envie la confirmacion reproduciremos
                aEjecutar = './mp32rtp -i 127.0.0.1 -p 23032 <' + FILE
                print("Vamos a ejecutar" + aEjecutar)
                os.system(aEjecutar)
            elif METHOD not in ['INVITE','BYE', 'ACK']:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            

if __name__ == "__main__":

    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        FILE = sys.argv[3]
    except:
        sys.exit("Usage: python server.py IP port audio_file")
    # Creamos servidor de eco y escuchamos
    print("Listening...")

    serv = socketserver.UDPServer(('', PORT), EchoHandler)
    print("Lanzando servidor UDP de eco...")

    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print()
        print("Servidor finalizado")
