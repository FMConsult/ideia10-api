import re, json, hashlib, base64, os, sys, csv, re, jsonpickle, time, urllib2
import urlparse
from bottle import request, response
from bottle import get, put, post, delete
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson import ObjectId
from bson import DBRef
from mongoengine import *
from ..model.models import *
from ..util.utils import CPFUtil, DateUtil, SeeklocWebServiceUtil, MailSender, PaginationUtil
from datetime import datetime
from dateutil.parser import parse

connection = connect('faggion')

def find_empresa_webservice(cnpj):
	res = urllib2.urlopen('http://www.receitaws.com.br/v1/cnpj/'+ cnpj)
	info = res.info()
	data = res.read()
	res.close()
	return data

@post('/pessoa')
def new(dados=None):
	try:
		if dados is None:
			post_data = jsonpickle.decode(request.body.read().decode('utf-8'))
		else:
			post_data = dados
			if post_data['tipo_cadastro'] == 'pf':
				post_data['cpf'] = post_data['cpf_cnpj']
				del post_data['cpf_cnpj']
			elif post_data['tipo_cadastro'] == 'pj':
				post_data['cnpj'] = post_data['cpf_cnpj']
				del post_data['cpf_cnpj']

		pessoa = Pessoa()

		pessoa.tipo_cadastro = post_data['tipo_cadastro']
		pessoa.perfil_cadastro = post_data['perfil_cadastro'] if 'perfil_cadastro' in post_data else None
		
		pessoa.cpf = post_data['cpf'] if 'cpf' in post_data else None
		pessoa.nome = post_data['nome'] if 'nome' in post_data else None
		pessoa.data_nascimento = post_data['data_nascimento'] if 'data_nascimento' in post_data else None
		
		pessoa.cnpj = post_data['cnpj'] if 'cnpj' in post_data else None
		pessoa.inscricao_estadual = post_data['inscricao_estadual'] if 'inscricao_estadual' in post_data else None
		pessoa.inscricao_municipal = post_data['inscricao_municipal'] if 'inscricao_municipal' in post_data else None
		pessoa.razao_social = post_data['razao_social'] if 'razao_social' in post_data else None
		pessoa.nome_fantasia = post_data['nome_fantasia'] if 'nome_fantasia' in post_data else None
		pessoa.ramo_atividade = post_data['ramo_atividade'] if 'ramo_atividade' in post_data else None
		
		pessoa.endereco = post_data['endereco'] if 'endereco' in post_data else None
		pessoa.numero_endereco = post_data['numero_endereco'] if 'numero_endereco' in post_data else None
		pessoa.complemento_endereco = post_data['complemento_endereco'] if 'complemento_endereco' in post_data else None
		pessoa.bairro = post_data['bairro'] if 'bairro' in post_data else None
		pessoa.cep = post_data['cep'] if 'cep' in post_data else None
		pessoa.cidade = post_data['cidade'] if 'cidade' in post_data else None
		pessoa.estado = post_data['estado'] if 'estado' in post_data else None

		pessoa.telefone_celular = post_data['telefone_celular'] if 'telefone_celular' in post_data else None
		pessoa.telefone_comercial = post_data['telefone_comercial'] if 'telefone_comercial' in post_data else None
		pessoa.ramal_comercial = post_data['ramal_comercial'] if 'ramal_comercial' in post_data else None
		pessoa.telefone_residencial = post_data['telefone_residencial'] if 'telefone_residencial' in post_data else None
		pessoa.email = post_data['email'] if 'email' in post_data else None

		pessoa.save()

		response.status = 201
		return str(pessoa.id)
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@put('/pessoa')
def update(dados=None):
	try:
		if dados is None:
			request_data = jsonpickle.decode(request.body.read().decode('utf-8'))
		else:
			request_data = dados
			if request_data['tipo_cadastro'] == 'pf':
				request_data['cpf'] = request_data['cpf_cnpj']
				del request_data['cpf_cnpj']
			elif request_data['tipo_cadastro'] == 'pj':
				request_data['cnpj'] = request_data['cpf_cnpj']
				del request_data['cpf_cnpj']

		pessoa = Pessoa.objects(id=request_data['id'])

		pessoa.update_one(
			tipo_cadastro = request_data['tipo_cadastro'],
			perfil_cadastro = request_data['perfil_cadastro'] if 'perfil_cadastro' in request_data else None,
			
			cpf = request_data['cpf'] if 'cpf' in request_data else None,
			nome = request_data['nome'] if 'nome' in request_data else None,
			data_nascimento = request_data['data_nascimento'] if 'data_nascimento' in request_data else None,
			
			cnpj = request_data['cnpj'] if 'cnpj' in request_data else None,
			inscricao_estadual = request_data['inscricao_estadual'] if 'inscricao_estadual' in request_data else None,
			inscricao_municipal = request_data['inscricao_municipal'] if 'inscricao_municipal' in request_data else None,
			razao_social = request_data['razao_social'] if 'razao_social' in request_data else None,
			nome_fantasia = request_data['nome_fantasia'] if 'nome_fantasia' in request_data else None,
			ramo_atividade = request_data['ramo_atividade'] if 'ramo_atividade' in request_data else None,

			endereco = request_data['endereco'] if 'endereco' in request_data else None,
			numero_endereco = request_data['numero_endereco'] if 'numero_endereco' in request_data else None,
			complemento_endereco = request_data['complemento_endereco'] if 'complemento_endereco' in request_data else None,
			bairro = request_data['bairro'] if 'bairro' in request_data else None,
			cep = request_data['cep'] if 'cep' in request_data else None,
			cidade = request_data['cidade'] if 'cidade' in request_data else None,
			estado = request_data['estado'] if 'estado' in request_data else None,

			telefone_celular = request_data['telefone_celular'] if 'telefone_celular' in request_data else None,
			telefone_comercial = request_data['telefone_comercial'] if 'telefone_comercial' in request_data else None,
			ramal_comercial = request_data['ramal_comercial'] if 'ramal_comercial' in request_data else None,
			telefone_residencial = request_data['telefone_residencial'] if 'telefone_residencial' in request_data else None,
			email = request_data['email'] if 'email' in request_data else None
		)

		response.status = 200
		return request_data['id']
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)

@get('/pessoa/<tipo_pessoa>/<cpf_cnpj>')
def get_by_cpf_or_cnpj(tipo_pessoa, cpf_cnpj):
	try:
		if tipo_pessoa == 'pf':
			result = Pessoa.objects(cpf=cpf_cnpj).filter()
		elif tipo_pessoa == 'pj':
			result = Pessoa.objects(cnpj=cpf_cnpj).filter()

		if not (result is None):
			response.headers['Content-Type'] = 'application/json'
			return result.get().to_json()
		else:
			if tipo_pessoa == 'pf':
				result = SeeklocWebServiceUtil().get_person_info(cpf_cnpj)
			elif tipo_pessoa == 'pj':
				result = find_empresa_webservice(cpf_cnpj)
			
			response.headers['Content-Type'] = 'application/json'
			if tipo_pessoa == 'pf':
				return jsonpickle.encode(result)
			elif tipo_pessoa == 'pj':
				return result
	except DoesNotExist as e:
		if tipo_pessoa == 'pf':
			result = SeeklocWebServiceUtil().get_person_info(cpf_cnpj)
		elif tipo_pessoa == 'pj':
			result = find_empresa_webservice(cpf_cnpj)

		response.headers['Content-Type'] = 'application/json'
		if tipo_pessoa == 'pf':
			return jsonpickle.encode(result)
		elif tipo_pessoa == 'pj':
			return result

@get('/pessoa')
@get('/pessoas')
@get('/pessoas/<offset>/<limit>')
def get_all(offset=None, limit=None):
	try:
		url_params = urlparse.parse_qs(request.query_string)

		for key, value in url_params.items():
			url_params[key] = value[0]

		if offset is None:
			offset = '1'

		if limit is None:
			limit = '10'

		if 'limit' in url_params:
			limit = url_params['limit']
			del url_params['limit']

		if 'nome' in url_params:
			nome = url_params['nome']
		else:
			nome = None

		if (not ('tipo_cadastro' in url_params)) and (not ('nome' in url_params)) and (not ('perfil_cadastro' in url_params)):
			query_set = Pessoa.objects().filter()
		elif ('tipo_cadastro' in url_params) and (not ('nome' in url_params)) and (not ('perfil_cadastro' in url_params)):
			query_set = Pessoa.objects(
				tipo_cadastro=url_params['tipo_cadastro']
			).filter()
		elif (not ('tipo_cadastro' in url_params)) and ('nome' in url_params) and (not ('perfil_cadastro' in url_params)):
			query_set = Pessoa.objects(
				Q(nome__icontains=nome) | Q(nome_fantasia__icontains=nome) | Q(razao_social__icontains=nome)
			).filter()
		elif (not ('tipo_cadastro' in url_params)) and (not ('nome' in url_params)) and ('perfil_cadastro' in url_params):
			query_set = Pessoa.objects(
				perfil_cadastro=url_params['perfil_cadastro']
			).filter()
		elif (not ('tipo_cadastro' in url_params)) and ('nome' in url_params) and ('perfil_cadastro' in url_params):
			query_set = Pessoa.objects(
				perfil_cadastro=url_params['perfil_cadastro']
			).filter(
				Q(nome__icontains=nome) | Q(nome_fantasia__icontains=nome) | Q(razao_social__icontains=nome)
			)
		elif ('tipo_cadastro' in url_params) and ('nome' in url_params) and (not ('perfil_cadastro' in url_params)):
			query_set = Pessoa.objects(
				tipo_cadastro=url_params['tipo_cadastro']
			).filter(
				Q(nome__icontains=nome) | Q(nome_fantasia__icontains=nome) | Q(razao_social__icontains=nome)
			)
		elif ('tipo_cadastro' in url_params) and ('nome' in url_params) and ('perfil_cadastro' in url_params):
			query_set = Pessoa.objects(
				tipo_cadastro=url_params['tipo_cadastro'],
				perfil_cadastro=url_params['perfil_cadastro']
			).filter(
				Q(nome__icontains=nome) | Q(nome_fantasia__icontains=nome) | Q(razao_social__icontains=nome)
			)

		response.headers['Content-Type'] = 'application/json'
		result = PaginationUtil().paginate(query_set, int(offset), int(limit))
		if (not (result is None)):
			return result
		else:
			response.status = 404
			return 'Nenhum registro encontrado'
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@get('/pessoa/<id:re:[0-9a-f]{24}>')
def get_by_id(id):
	try:
		response.headers['Content-Type'] = 'application/json'
		return Pessoa.objects(id=id).get().to_json()
	except DoesNotExist as e:
		response.status = 404
		return 'Nenhum registro encontrado'

@delete('/pessoa/<id:re:[0-9a-f]{24}>')
def delete(id):
	try:
		Pessoa.objects(id=id).get().delete()
		response.status = 200
		return 'Registro excluido com sucesso!'
	except Exception as e:
		response.status = 500
		return str(e)