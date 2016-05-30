#!/usr/bin/python
#coding=utf-8
#-*- coding: utf-8 -*-

#TITLE  : Arduino Control
#DATE   : 2016.03.03
#AUTHOR : KwangEun, An
#DESC	: program requires the pyserial.

import serial

class Arduino():
	#--init--
	
	#Arduino connection containers
	connections = None
	
	#device 
	devicePath = '/dev/tty.usbserial'
	#--init--
	
	#Initialize a connections
	def __init__(self, numberOfConnections):
		#self.connections = [0 for x in range(0, numberOfConnections)]
		self.connections = []
		
		#Creats instnaces of serial channels with arduinos
		for x in range(0, numberOfConnections):
			self.connections[x] = serial.Serial(devicePath+x,9600)
	#Read signal from arduino in return value.
	def ArduinoReadSignal(self, connectionId):
		return self.connections[connectionId]
		
	#Send signal to Arduino 
	def ArduinoSendSignal(self, connectionId, data):
		self.connections[connectionId].write(data)
	
	
