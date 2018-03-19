# -*- coding: utf-8 -*-
import re, json, hashlib, base64, os, sys, csv, re, jsonpickle, time, bcrypt
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

@post('/user/login')
def login():
	try:
		post_data = json.loads(request.body.getvalue().decode('utf-8'))
		
		user = User.objects(login=post_data['login']).get()
		
		if(bcrypt.checkpw(post_data['password'].encode('utf-8'), user.password.encode('utf-8'))):
			response.headers['Content-Type'] = 'application/json'
			return user.to_json()
		else:
			response.status = 406
			return 'Senha inválida.'
	except DoesNotExist as e:
		response.status = 404
		return 'Usuário não encontrado.'

@post('/user')
def new():
	try:
		post_data = jsonpickle.decode(request.body.read().decode('utf-8'))

		item = User()
		item.name = post_data['name']
		item.login = post_data['login']
		item.password = bcrypt.hashpw(post_data['password'].encode('utf-8'), bcrypt.gensalt())
		item.save()

		response.status = 201
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@delete('/user/<id:re:[0-9a-f]{24}>')
def delete(id):
	try:
		user = User.objects(id=id).get().delete()
		response.status = 200
		return 'Registro excluido com sucesso!'
	except Exception as e:
		response.status = 500
		return str(e)