# datagram.py 

import collections

tim561Datagram = collections.namedtuple("tim561Datagram",["CommandType", 
															"Command", 
															"VersionNumber",
															"DeviceNumber", 
															"SerialNumber", 
															"DeviceStatus", 
															"TelegramCounter", 
															"ScanCounter",
															"TimeSinceStartup", 
															"TimeOfTransmission", 
															"StatusOfDigitalInput",
															"StatusOfDigitalOutput",
															"LayerAngle",
															"ScanFrequency",
															"MeasurementFrequency",
															"EncoderPosition",
															"EncoderSpeed",
															"OutputChannel16bit",
															"ScaleFactor",
															"ScaleFactorOffset",
															"StartAngle",
															"SizeofAngleStep",
															"Data"
															])

# creation of Byte generator from data stream
def bytes_from_socket(socket):
	while True:
		data = socket.recv(256)
		for byte in data:
			yield bytes([data])

# from constant data stream, creation of 
# datagram generator from complete telegrams
def datagram_from_socket(socket):
	STX = b'\x02'
	ETX = b'\x03'

	byte_generator = bytes_from_socket(socket)

	while True:
		datagram = b''

		for byte in byte_generator:
			if byte == STX: 
				break

		for byte in byte_generator:
			if byte == ETX:
				break
			datagram += byte
		yield datagram

def parse_nmumber(nbr_str):
	# decimal numbers are encoded with leading '+' and '-'
	# if above condition met, cast byte to integer
	# else cast byte to hex 
	if b'+' in nbr_str or b'-' in nbr_str:
		return int(nbr_str)
	else:
		return int(nbr_str, 16)
