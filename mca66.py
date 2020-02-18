from __future__ import absolute_import, division, print_function
import socket
import codecs
import binascii
import time, logging
import json

class mca66:


	def __init__(self, to=1):
		logging.debug("Init...")
		lines = filter(None, (line.strip() for line in open("/config/zones_list.txt")))
		self.zone_names = {int(a): b for a,b in [line.split(':') for line in lines]}
		self.input_names = list(filter(None, (line.strip() for line in open("/config/sources_list.txt"))))
		self.to = 1
		self.zonelist = {k+1:{'power':None,'input':None,'vol':None,'mute':None,'input_name':None} for k in range(6)}
	def __enter__(self):
		logging.debug("Enter...")
		self.open()
		return self
		
	def __exit__(self ,type, value, traceback):
		logging.debug("Exit...")
		
	#def test(self, command, zone, value):
		#print(command)
		#print(zone)
		#print(value)
		#logging.debug(command)
		#logging.debug(zone)
		#logging.debug(value)
		#return "off"
		
	def getZoneNames(self):
		return self.zone_names


	def checksum(self, message):
		cs = 0
		for b in message:
			cs=cs+b
		csb=cs&0xff
		return csb

	def printzonejson(self, zone):
		Zone = zone
		Power = self.zonelist[zone]['power']
		Input = self.zonelist[zone]['input']
		InputName = self.zonelist[zone]['input_name']
		Volume = self.zonelist[zone]['vol']
		Mute = self.zonelist[zone]['mute']
		print (json.dumps(
			{'Zone': Zone,
			'Power': Power,
			'Input': Input,
			'InputName': InputName,
			'Volume': Volume,
			'Mute': Mute}, indent=4, separators=(',', ': ')))
		
	def printzone(self, zone):
		print("Zone: ", zone)
		print("Power: ", self.zonelist[zone]['power'])
		print("Input: ", self.zonelist[zone]['input'])
		print("Input Name: ", self.zonelist[zone]['input_name'])
		print("Volume: ",self.zonelist[zone]['vol'])
		print("Mute: ", self.zonelist[zone]['mute'])
		#logging.debug("Zone: %s", zone)
		#logging.debug("Power: %s", self.zonelist[zone]['power'])
		#logging.debug("Input: %s", self.zonelist[zone]['input'])
		#logging.debug("Input Name: %s", self.zonelist[zone]['input_name'])
		#logging.debug("Volume: %s",self.zonelist[zone]['vol'])
		#logging.debug("Mute: %s", self.zonelist[zone]['mute'])



	def parse_reply(self, message):
		#print("ParseReply_MessagePassedIn: ", message)
		if len(message) > 14:
			Zone_List = list()
			zone0 = message[0:14]
			zone1 = message[14:28]
			#zone2 = message[28:42]
			#zone3 = message[42:56]
			#zone4 = message[56:70]
			#zone5 = message[70:84]
			#zone6 = message[84:98]
			Zone_List.append(zone1)
			#Zone_List.append(zone2)
			#Zone_List.append(zone3)
			#Zone_List.append(zone4)
			#Zone_List.append(zone5)
			#Zone_List.append(zone6)
			for i in Zone_List:
				zone = i[2]
				self.zonelist[zone]['power'] = "on" if (i[4] & 1<<7)>>7 else "off"
				self.zonelist[zone]['input'] = i[8]+1
				self.zonelist[zone]['input_name'] = self.input_names[i[8]]
				self.zonelist[zone]['vol'] = i[9]-196 if i[9] else 0
				self.zonelist[zone]['mute'] = "on" if (i[4] & 1<<6)>>6 else "off"
				self.printzonejson(zone)
			if len(message) == 14:
				zone = message[2]
				self.zonelist[zone]['power'] = "on" if (message[4] & 1<<7)>>7 else "off"
				self.zonelist[zone]['input'] = message[8]+1
				self.zonelist[zone]['input_name'] = self.input_names[message[8]]
				self.zonelist[zone]['vol'] = message[9]-196 if message[9] else 0
				self.zonelist[zone]['mute'] = "on" if (message[4] & 1<<6)>>6 else "off"
				#self.printzone(zone)
	
	def parse_reply_returndetail(self, message, zoneNumber):
		#print("ParseReply_MessagePassedIn: ", message)
		if len(message) > 14:
			Zone_List = list()
			zone0 = message[0:14]
			zone1 = message[14:28]
			#zone2 = message[28:42]
			#zone3 = message[42:56]
			#zone4 = message[56:70]
			#zone5 = message[70:84]
			#zone6 = message[84:98]
			Zone_List.append(zone1)
			#Zone_List.append(zone2)
			#Zone_List.append(zone3)
			#Zone_List.append(zone4)
			#Zone_List.append(zone5)
			#Zone_List.append(zone6)
			for i in Zone_List:
				zone = i[2]
				self.zonelist[zone]['power'] = "on" if (i[4] & 1<<7)>>7 else "off"
				self.zonelist[zone]['input'] = i[8]+1
				self.zonelist[zone]['input_name'] = self.input_names[i[8]]
				self.zonelist[zone]['vol'] = i[9]-196 if i[9] else 0
				self.zonelist[zone]['mute'] = "on" if (i[4] & 1<<6)>>6 else "off"
				#self.printzone(zone)
				
			if len(message) == 14:
				zone = message[2]
				self.zonelist[zone]['power'] = "on" if (message[4] & 1<<7)>>7 else "off"
				self.zonelist[zone]['input'] = message[8]+1
				self.zonelist[zone]['input_name'] = self.input_names[message[8]]
				self.zonelist[zone]['vol'] = message[9]-196 if message[9] else 0
				self.zonelist[zone]['mute'] = "on" if (message[4] & 1<<6)>>6 else "off"
				#self.printzone(zone)
				

		print(self.zonelist[zoneNumber]['power'])

	def setInput(self, zone, input):
		if zone not in range(1,7):
			logging.warning("Invalid Zone")
			return    
		if input not in range(1,7):
			logging.warning("invalid input number")
			return   
		cmd = bytearray([0x02,0x00,zone,0x04,input+2])
		self.send_command(cmd)

	def volUp(self, zone):
		if zone not in range(1,7):
			logging.warning("Invalid Zone")
			return    
		cmd = bytearray([0x02,0x00,zone,0x04,0x09])
		self.send_command(cmd)

	def volDwn(self, zone):
		if zone not in range(1,7):
			logging.warning("Invalid Zone")
			return    
		cmd = bytearray([0x02,0x00,zone,0x04,0x0A])
		self.send_command(cmd)

	def setVol(self, zone, vol):
		#print("_________________________")
		#print(zone,vol)
		#print(self.zonelist)
		self.queryZone(zone)
		if vol not in range(0,63):
			logging.warning("Invald Volume")
			return
		#print("Requested:",vol)
		#print("Current:", self.zonelist[zone]['vol'])
		#print("Zone:",self.zonelist[zone])
		volDiff = vol-self.zonelist[zone]['vol']
		start_time = time.time()
		if volDiff < 0:
			for k in range(abs(volDiff)):
				self.volDwn(zone)
		elif volDiff > 0:
			for k in range(volDiff):
				self.volUp(zone)
		else:
			pass
		#print("Vol Change took",time.time()-start_time,"seconds to do",volDiff,"steps")
		return
		
	def toggleMute(self, zone):
		if zone not in range(1,7):
			logging.warning("Invalid Zone")
			return    
		cmd = bytearray([0x02,0x00,zone,0x04,0x22])
		self.send_command(cmd)

	def queryZone(self, zone):
		if zone not in range(1,7):
			logging.warning("Invalid Zone")
			return
		cmd = bytearray([0x02,0x00,zone,0x06,0x00])
		self.send_command(cmd)
	
	def queryZone_returndetail(self, zone):
		if zone not in range(1,7):
			logging.warning("Invalid Zone")
			return
		cmd = bytearray([0x02,0x00,zone,0x06,0x00])
		self.send_command_returndetail(cmd, zone)

	def setPower(self, zone, pwr):
		if zone not in range(0,7):
			logging.warning("Invalid Zone")
			return
		if pwr not in [0,1]:
			logging.warning("invalid power command")
			return
		if zone==0:
			cmd = bytearray([0x02,0x00,zone,0x04,0x38 if pwr else 0x39])
		else:
			cmd = bytearray([0x02,0x00,zone,0x04,0x20 if pwr else 0x21])
		
		self.send_command(cmd)

	def send_command(self, cmd):
		#print(cmd)
		host = '10.2.40.100'
		port = 10006
		cmd.append(self.checksum(cmd))
		#print(cmd)
		mySocket = socket.socket()
		mySocket.connect((host,port))
		mySocket.send(cmd)
		data = mySocket.recv(1024)
		mySocket.close()
		self.parse_reply(data) 

	def send_command_returndetail(self, cmd, zone):
		host = '10.2.40.100'
		port = 10006
		cmd.append(self.checksum(cmd))
		#print(cmd)
		mySocket = socket.socket()
		mySocket.connect((host,port))
		mySocket.send(cmd)
		data = mySocket.recv(1024)
		mySocket.close()
		self.parse_reply_returndetail(data, zone)

	def status(self):
		return self.zonelist