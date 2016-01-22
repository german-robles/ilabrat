#!/usr/bin/python
# -*- coding: utf-8 -*-
import gnupg
import yaml
import os
import optparse

class Encrypter :
	def getConfig(self):
		imHere = os.path.dirname(os.path.abspath(__file__))
		with open("%s/ilabrat.conf" % (imHere), 'r') as ymlfile:
			cfg = yaml.load(ymlfile)
		home = (cfg['home'])
		passphrase = (cfg['passphrase'])
		emailKey = (cfg['emailKey'])
		bind = (cfg['bind'])
		port = (cfg['port'])
		debug = (cfg['debug'])
		sslcrt = (cfg['sslcrt'])
		sslkey = (cfg['sslkey'])
		accesslog = (cfg['accesslog'])
		logfile = (cfg['logfile'])
		upload_folder = (cfg['uploadFolder'])
		

		return home, passphrase, emailKey, bind, port, debug, sslcrt, sslkey, accesslog, logfile, upload_folder
		
	# String methods
	def decrypt(self, home, passphrase, string):
		gpg = gnupg.GPG(gnupghome='%s'%(home))
		decrypted_data = gpg.decrypt(string, passphrase='%s'%(passphrase))
		return decrypted_data.data

	def encrypt(self, home, emailKey, string):
		gpg = gnupg.GPG(gnupghome='%s'%(home))
		encrypted_data = gpg.encrypt(string, '%s'%(emailKey))
		encrypted_string = str(encrypted_data)
		return encrypted_string	
	
	# File methods
	def encrypt_file(self, home, emailKey, filename, upload_folder):
		gpg = gnupg.GPG(gnupghome='%s'%(home))
		with open('%s/%s'%(upload_folder, filename), 'rb') as f:
			status = gpg.encrypt_file(
				f, recipients=['%s'%(emailKey)],
				output='%s/%s.gpg'%(upload_folder, filename))
		print 'ok: ', status.ok
		print 'status: ', status.status
		print 'stderr: ', status.stderr

	def decrypt_file(self, home, filename, upload_folder, passphrase):
		gpg = gnupg.GPG(gnupghome='%s'%(home))
		filenameStriped = filename.replace('.gpg' , '')
		with open('%s/%s'%(upload_folder, filename), 'rb') as f:
			status = gpg.decrypt_file(
				f, passphrase='%s'%(passphrase),
				output='%s/%s'%(upload_folder, filenameStriped))
		print 'ok: ', status.ok
		print 'status: ', status.status
		print 'stderr: ', status.stderr

if __name__ == '__main__':
	Encrypter()