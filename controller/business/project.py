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

@post('/project')
def new():
	try:
		# load data from post
		post_data = jsonpickle.decode(request.body.read().decode('utf-8'))

		item = Project()
		item.title = post_data['title']
		item.category = DBRef('category', ObjectId(post_data['category']['id']))
		item.text = post_data['text']
		item.save()

		response.status = 201
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@get('/projects')
def get_all():
	try:
		response.headers['Content-Type'] = 'application/json'
		return Project.objects().filter().to_json()
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@delete('/project/<id:re:[0-9a-f]{24}>')
def delete(id):
	try:
		# get specified record from database
		item = Project.objects(id=id).get()

		# remove record from database
		item.delete()
		
		response.status = 200
		return 'Registro excluido com sucesso!'
	except Exception as e:
		response.status = 500
		return str(e)