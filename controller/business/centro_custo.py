import re, json, hashlib, base64, os, sys, csv, re, jsonpickle, time
from bottle import request, response
from bottle import get, put, post, delete
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson import ObjectId
from bson import DBRef
from mongoengine import *
from ..model.models import *
from ..util.utils import CPFUtil, DateUtil
from datetime import datetime
from dateutil.parser import parse

connection = connect('faggion')

@post('/centro-custos')
def new():
	try:
		# load data from post
		post_data = json.loads(request.body.getvalue().decode('utf-8'))

		item = CentroCustos()

		item.codigo 	 = post_data['codigo'] if 'codigo' in post_data else None
		item.descricao = post_data['descricao']

		item.save()

		response.headers['Content-Type'] = 'application/json'
		response.status = 201
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@put('/centro-custos')
def update():
	try:
		request_data = json.loads(request.body.getvalue().decode('utf-8'))

		item = CentroCustos.objects(id=request_data['id'])

		item.update_one(
			codigo 		= request_data['codigo'] if 'codigo' in request_data else None,
			descricao 	= request_data['descricao']
		)

		response.status = 200
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@get('/centros-custos')
def get_all():
	try:
		response.headers['Content-Type'] = 'application/json'
		return CentroCustos.objects().filter().to_json()
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@get('/centro-custos/<id:re:[0-9a-f]{24}>')
def get_by_id(id):
	try:
		response.headers['Content-Type'] = 'application/json'
		return CentroCustos.objects(id=id).get().to_json()
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@delete('/centro-custos/<id:re:[0-9a-f]{24}>')
def delete(id):
	try:
		CentroCustos.objects(id=id).get().delete()
		response.status = 200
		return 'Registro excluido com sucesso!'
	except Exception as e:
		response.status = 500
		return str(e)