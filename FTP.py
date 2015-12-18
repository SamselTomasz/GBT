# !/usr/bin/python
# coding=utf-8
# import os
# import time
# import shutil
# import pickle
import ftplib


class FTPServer:
	"""
	This is just a skelet of an ftp access module. 
	All methods have to be filled in and functionaklity made 
	same as for LocalFolder.
	"""

	def __init__(self):
		self.items = [[], [], []]
		self.backup_local_path = ""
		self.backup_remote_path = ""
		self.ftp_user = ""
		self.ftp_PASSWORD + ""

	def __fill_table__(self, path_item):
		print "fill me up with code"

	def add_dir(self, new_path)
		print "fill me up with code"
	
	def rem_list_item(self, item):
		print "fill me up with code"
	
	def copy_to_remote(self, local_item, remote_item):
		print "fill me up with code"
	
	def copy_from_remote(sel, remote_item, local_item):
		print "fill me up with code"
	
	def delete_item(self, item_path):
		print "fill me up with code"

	def save_backup_list(self, save_file):
		print "fill me up with code"

	def load_backup_list(self, save_file):
		print "fill me up with code"

if __name__ == '__main__':
    print 'This class is not a standalone program'
