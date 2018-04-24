#!/usr/bin/python3
# -*- coding: UTF-8 -*-# enable debugging


import os
import os.path
from pathlib import Path
import sys 
os.chdir(os.path.dirname(__file__))
# so I can load custom modules
sys.path.append(os.path.dirname(__file__))
import bottle
import bcrypt
import time
from Crypto.Cipher import AES
from Crypto import Random
from base64 import b64decode
import hmac
import hashlib
import urllib.parse

import json
from tuc.zoo import zk
from bottle import route, run, template, response, redirect

application = bottle.default_app()
# we do not need session for the file service
#application = beaker.middleware.SessionMiddleware(bottle.default_app(), session_opts)
sys.stderr.write("Fileservicepython start process at " + str(int(round(time.time() * 1000))))
sys.stderr.flush()

# do not cache templates
bottle.debug(True)	

@route('/status')
def status():
	sys.stderr.write("Python File Service status called "+ str(zk.getTest()))
	sys.stderr.flush()
	response.content_type = 'text/html; charset=utf-8'

	return ["alive " + str(zk.getTest())]
	
@route('/file/<fileId>')
def index(fileId):

	# bottle.request.environ['wsgi.errors'].write("application debug #1")
	userId = bottle.request.params.get('userId',False)
	validTill = bottle.request.params.get('validTill',False)
	hmacString = bottle.request.params.get('hmac',False)

	if validateHmac(fileId, userId, validTill, hmacString)==False:
		bottle.abort(401, "Access denied")
	
	
	fullFilePath = getRepositoryPath()+fileId
	f = Path(fullFilePath)
	if f.is_file() == False:
		# should never happen!!! 
		bottle.abort(404, "Invalid file ")


	
	filename, extension = os.path.splitext(fullFilePath)
	
	mime = "application/octet-stream";
	if extension.lower() == ".png":
		mime = "image/png"; 
	if extension.lower() == ".jpg":
		mime = "image/png"; 
	if extension.lower() == ".gif":
		mime = "image/png"; 

	#response.content_type = mime
	return bottle.static_file(fileId, root=getRepositoryPath(), mimetype=mime)


def validateHmac(fileId, userId, validTill, hmacString):
	# TODO do validation
	return True	

def getRepositoryPath():
	# outside of webapp!!
	return "/tmp/";
