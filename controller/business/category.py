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

@post('/category')
def new():
	try:
		# load data from post
		post_data = jsonpickle.decode(request.body.read().decode('utf-8'))

		item = Category()
		item.name = post_data['name']
		item.save()

		response.status = 201
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@put('/category/<id:re:[0-9a-f]{24}>')
def update(id):
	try:
		# load data from post
		request_data = jsonpickle.decode(request.body.read().decode('utf-8'))

		item = Category.objects(id=id)
		item.update_one(
			name = request_data['name']
		)

		response.status = 200
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@get('/categories')
def get_all():
	try:
		response.headers['Content-Type'] = 'application/json'
		return Category.objects().filter().to_json()
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@delete('/category/<id:re:[0-9a-f]{24}>')
def delete(id):
	try:
		# get specified record from database
		item = Category.objects(id=id).get()

		# remove record from database
		item.delete()
		
		response.status = 200
		return 'Registro excluido com sucesso!'
	except Exception as e:
		response.status = 500
		return str(e)