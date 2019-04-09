#!/usr/bin/env python
# coding: utf-8
'''
@File   :sht25.py
@Author :youxinweizhi
@Date   :2019/4/9
@Github :https://github.com/youxinweizhi
'''

import time

class SHT25:
	i2c = []
	ADDR = 64
	
	CMD_READ_TEMPERATURE = 0xF3
	CMD_READ_HUMIDITY    = 0xF5
	CMD_READ_REGISTER    = 0xE7
	CMD_WRITE_REGISTER   = 0xE6
	CMD_RESET 			 = 0xFE

	def __init__(self, _i2c):
		self.i2c = _i2c

	def toTemperature(self, buf):
		return -46.85 + 175.72 * ((buf[0] << 8) + buf[1]) /2**16

	def toHumidity(self, buf):
		return -6 + 125.0 * ((buf[0] << 8) + buf[1]) / 2**16

	def decodeUserReg(self, buf):
		reg = buf[0]
		ret = []
		if(0b10000001 & reg == 0b10000001):
			ret.append("11bits")
		elif(0b10000001 & reg == 0b10000000):
			ret.append("RH 10bit T 13bit")
		elif(0b10000001 & reg == 0b00000001):
			ret.append("RH 8bit T 12bit")
		elif(0b10000001 & reg == 0b00000000):
			ret.append("RH 12bit T 14bit")
		
		if(0b01000000 & reg == 0b01000000):
			ret.append("VDD < 2.5")
		else:
			ret.append("VDD > 2.5")

		if(0b00000100 & reg == 0b00000100):
			ret.append("heater ON")
		else:
			ret.append("heater OFF")

		if(0b00000010 & reg == 0b00000010):
			ret.append("OTP reload disabled")
		else:
			ret.append("OTP reload enabled")

		return ret

	def runI2CCommand(self, command, bytesToRead):
		b = bytearray(1)
		b[0] = command

		self.i2c.writeto(self.ADDR, b)

		if(bytesToRead > 0):
			recv = bytearray(bytesToRead)
			retryCounter = 0
			done = False
			while retryCounter < 15 and not done:
				try:
					self.i2c.readfrom_into(self.ADDR, recv)
					done = True
					retryCounter = retryCounter + 1				
				except:
					time.sleep(0.01)
			return recv

	def getTemperature(self):
		return self.toTemperature(self.runI2CCommand(self.CMD_READ_TEMPERATURE, 3))

	def getHumidity(self):
		return self.toHumidity(self.runI2CCommand(self.CMD_READ_HUMIDITY, 3))
	
	def getUserRegister(self):
		return self.decodeUserReg(self.runI2CCommand(self.CMD_READ_REGISTER, 1))

	def setUserRegister(self, register):
		b = bytearray(2)
		b[0] = self.CMD_WRITE_REGISTER
		b[1] = register & 0b11000111
		self.i2c.writeto(self.ADDR, b)

	def reset(self):
		self.runI2CCommand(self.CMD_RESET, 0)