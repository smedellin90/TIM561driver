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
			yield bytearray(data)

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

# function shall split the datagram by space
# from then the values will be assigned to 
# corresponding key/value pair. 
def decode_datagram(datagram):
    items = datagram.split(b' ')

    header = {}
    header['TypeOfCommand'] = items[0].decode('ascii')
    if header['TypeOfCommand'] != 'sSN':
        return None
    header['Command'] = items[1].decode('ascii')
    if header['Command'] != 'LMDscandata':
        return None
    header['VersionNumber'] = parse_number(items[2])
    header['DeviceNumber'] = parse_number(items[3])
    header['SerialNumber'] = items[4].decode('ascii')
    header['DeviceStatus1'] = parse_number(items[5])
    header['DeviceStatus2'] = parse_number(items[6])
    if header['DeviceStatus1'] != 0 or header['DeviceStatus2'] != 0:
        return None
    header['TelegramCounter'] = parse_number(items[7])
    header['TimeSinceStartup'] = parse_number(items[9])
    header['TimeOfTransmission'] = parse_number(items[10])
    header['AngularStepWidth'] = parse_number(items[24])
    header['NumberOfData'] = parse_number(items[25])
    header['Data'] = [parse_number(x) / 1000 for x in items[26:26+header['NumberOfData']]]

    return header

