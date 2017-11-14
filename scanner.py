import socket
from datagramm import *
# import numpy as np

if __name__ == '__main__':

	ip = '172.29.119.9'
	port = 2112
	sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock_client.connect((ip,port))

	sock_client.send(b'\x02sEN LMDscandata 1\x03\0')

	byte_generator = bytes_from_socket(sock_client)

	# testing bytearray function. 
	while True:
		datagram = next(byte_generator)
		print(datagram)

