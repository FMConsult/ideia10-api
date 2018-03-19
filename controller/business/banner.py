# -*- coding: utf-8 -*-
import re, json, hashlib, base64, os, sys, csv, re, jsonpickle, time
from bottle import request, response
from bottle import get, put, post, delete
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson import ObjectId
from bson import DBRef
from mongoengine import *
from ..model.models import *
from ..util.utils import *
from datetime import datetime
from dateutil.parser import parse

@post('/banner')
def new():
	try:
		# load data from post
		post_data = jsonpickle.decode(request.body.read().decode('utf-8'))

		item = Banner()
		item.name = post_data['name']
		
		if 'attachment' in post_data:
			attachment = Attachment()
			attachment.file_name = post_data['attachment']['name']
			attachment.file_size = post_data['attachment']['size']
			attachment.file_type = post_data['attachment']['type']

			# replaces the multipart file information
			post_data['attachment']['path'] = post_data['attachment']['path'][(post_data['attachment']['path'].find('base64,')+7) : len(post_data['attachment']['path'])]
			# generate file name
			file_path = 'images/'+ str(ObjectId()) +'.'+ post_data['attachment']['type']
			# create file point
			file = open(file_path, 'wb')
			# write data in file
			file.write(base64.decodestring(post_data['attachment']['path']))
			# closes file
			file.close()
			
			attachment.file_path = file_path

			item.file = attachment
		item.save()

		response.status = 201
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@get('/banners')
def get_all():
	try:
		response.headers['Content-Type'] = 'application/json'
		return Banner.objects().filter().to_json()
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@delete('/banner/<id:re:[0-9a-f]{24}>')
def delete(id):
	try:
		# get specified record from database
		banner = Banner.objects(id=id).get()

		# remove the file from the FileSystem
		os.remove(banner.file.file_path)

		# remove record from database
		banner.delete()
		
		response.status = 200
		return 'Registro excluido com sucesso!'
	except Exception as e:
		response.status = 500
		return str(e)