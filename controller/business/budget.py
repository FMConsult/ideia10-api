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

@get('/budget/<budget_id:re:[0-9a-f]{24}>/send/email/customer')
def send_budget_email_customer(budget_id):
	budget = Budget.objects(id = budget_id).get()

	ms = MailSender(
		host='srvwl1.virtuaserver.com.br',
		port='465',
		user='filipe.coelho@webliniaerp.com.br',
		password='f150679@Fil'
	)

	email_text = 'Agradecemos o seu pedido e ficamos a disposicao para esclarecer qualquer duvida que voce tenha a respeito dos nossos produtos e servico.<br><br>'
	email_text = email_text + 'Abaixo seguem os dados do seu pedido de orcamento realizado pelo nosso site:<br><br>'
	email_text = email_text + '<strong>Imagem escolhida:</strong> #'+ budget.image.code + ' <a href="http://201.27.1.220:7070/idea10-site/'+ budget.image.path +'">Clique aqui para visualizar a imagem</a><br>'
	email_text = email_text + '<strong>Material de Aplicacao:</strong> '+ budget.material.info.name + '<br>'
	email_text = email_text + '<strong>Tamanho do Material:</strong> '+ str(round(budget.material.dimensions.height, 2)) + 'm x '+ str(round(budget.material.dimensions.width, 2)) + 'm<br>'
	email_text = email_text + '<strong>Area de Impressao:</strong> '+ str(round(budget.local.dimensions.height, 2)) + 'm x '+ str(round(budget.local.dimensions.width, 2)) + 'm<br>'
	email_text = email_text + '<strong>Unidades necessarias p/ Impressao:</strong> '+ str(round(budget.local.dimensions.total, 2) / round(budget.material.dimensions.total, 2)) + '<br>'
	email_text = email_text + '<strong>Area Total de Impressao:</strong> '+ str(round(budget.local.dimensions.total, 2)) + 'm2<br>'
	email_text = email_text + '<strong>Valor do m2 p/ Impressao:</strong> '+ str(round(budget.material.info.cost, 2)) + '<br>'
	email_text = email_text + '<strong>Valor da Impressao:</strong> R$ '+ str(round(budget.print_value, 2)) + '<br>'

	ms.connect()
	ms.send_mail(
		subject 	= 'Idea10 | Obrigado pelo seu pedido!',
		destination = budget.customer.email,
		text 		= email_text,
		text_type 	= 'html'
	)

@get('/budget/<budget_id:re:[0-9a-f]{24}>/send/email/company')
def send_budget_email_company(budget_id):
	budget = Budget.objects(id = budget_id).get()

	ms = MailSender(
		host='srvwl1.virtuaserver.com.br',
		port='465',
		user='filipe.coelho@webliniaerp.com.br',
		password='f150679@Fil'
	)

	email_text = 'Abaixo seguem os dados do pedido de orcamento realizado pelo site:<br><br>'
	email_text = email_text + '<strong>Imagem escolhida:</strong> #'+ budget.image.code + ' <a href="http://201.27.1.220:7070/idea10-site/'+ budget.image.path +'">Clique aqui para visualizar a imagem</a><br>'
	email_text = email_text + '<strong>Material de Aplicacao:</strong> '+ budget.material.info.name + '<br>'
	email_text = email_text + '<strong>Tamanho do Material:</strong> '+ str(round(budget.material.dimensions.height, 2)) + 'm x '+ str(round(budget.material.dimensions.width, 2)) + 'm<br>'
	email_text = email_text + '<strong>Area de Impressao:</strong> '+ str(round(budget.local.dimensions.height, 2)) + 'm x '+ str(round(budget.local.dimensions.width, 2)) + 'm<br>'
	email_text = email_text + '<strong>Unidades necessarias p/ Impressao:</strong> '+ str(round(budget.local.dimensions.total, 2) / round(budget.material.dimensions.total, 2)) + '<br>'
	email_text = email_text + '<strong>Area Total de Impressao:</strong> '+ str(round(budget.local.dimensions.total, 2)) + 'm2<br>'
	email_text = email_text + '<strong>Valor do m2 p/ Impressao:</strong> '+ str(round(budget.material.info.cost, 2)) + '<br>'
	email_text = email_text + '<strong>Valor da Impressao:</strong> R$ '+ str(round(budget.print_value, 2)) + '<br><br>'

	email_text = email_text + '<h3>Dados do cliente</h3>'
	email_text = email_text + '<strong>Nome:</strong> '+ budget.customer.name + '<br>'
	email_text = email_text + '<strong>Telefone:</strong> '+ budget.customer.default_phone + '<br>'
	email_text = email_text + '<strong>Celular:</strong> '+ budget.customer.mobile_phone + '<br>'
	email_text = email_text + '<strong>E-mail:</strong> '+ budget.customer.email + '<br>'
	email_text = email_text + '<strong>CEP:</strong> '+ budget.customer.postal_code + '<br>'
	email_text = email_text + '<strong>Endereco:</strong> '+ budget.customer.address + '<br>'
	email_text = email_text + '<strong>Numero:</strong> '+ str(budget.customer.number) + '<br>'
	email_text = email_text + '<strong>Bairro:</strong> '+ budget.customer.district + '<br>'
	email_text = email_text + '<strong>Cidade:</strong> '+ budget.customer.city + '<br>'
	email_text = email_text + '<strong>Estado:</strong> '+ budget.customer.state + '<br>'
	email_text = email_text + '<strong>Observacoes:</strong> '+ budget.customer.comments

	ms.connect()
	ms.send_mail(
		subject 	= 'Idea10 | Novo pedido de orçamento pelo site!',
		destination = ['israel.barbosa@positecnologia.com.br','filipe.coelho@webliniaerp.com.br'],
		text 		= email_text,
		text_type 	= 'html'
	)

@post('/budget')
def new():
	try:
		# load data from post
		post_data = jsonpickle.decode(request.body.read().decode('utf-8'))

		# initialize budget object data
		budget = Budget()
		
		# fill material field
		budget.material = MaterialSelected()
		budget.material.info = DBRef('materials', ObjectId(post_data['material']['id']))
		budget.material.budget_cost = float(post_data['material']['cost'])
		budget.material.dimensions = DimensionData()
		budget.material.dimensions.height = float(post_data['material']['dimensions']['height']);
		budget.material.dimensions.width = float(post_data['material']['dimensions']['width']);
		budget.material.dimensions.total = float(post_data['material']['dimensions']['total']);
		
		# fill local field
		budget.local = LocalInformation()
		budget.local.dimensions = DimensionData()
		budget.local.dimensions.height = float(post_data['local']['dimensions']['height']);
		budget.local.dimensions.width = float(post_data['local']['dimensions']['width']);
		budget.local.dimensions.total = float(post_data['local']['dimensions']['total']);
		
		# fill category selected field
		if ('category' in post_data) and (not (post_data['category'] is None)):
			budget.category = CategorySelected()
			budget.category.name = post_data['category']['name'] if 'name' in post_data['category'] else None

		# fill image selected field
		budget.image = ImageSelected()
		budget.image.code = post_data['image']['code'];
		budget.image.path = post_data['image']['path'];
		budget.image.origin = post_data['image']['origin'];

		# fill customer field
		budget.customer = CustomerInformation()
		budget.customer.name = post_data['customer']['name']
		budget.customer.default_phone = post_data['customer']['default_phone'] if 'default_phone' in post_data['customer'] else None
		budget.customer.mobile_phone = post_data['customer']['mobile_phone'] if 'mobile_phone' in post_data['customer'] else None
		budget.customer.email = post_data['customer']['email'] if 'email' in post_data['customer'] else None
		budget.customer.postal_code = post_data['customer']['postal_code'] if 'postal_code' in post_data['customer'] else None
		budget.customer.address = post_data['customer']['address'] if 'address' in post_data['customer'] else None
		budget.customer.number = post_data['customer']['number'] if 'number' in post_data['customer'] else None
		budget.customer.district = post_data['customer']['district'] if 'district' in post_data['customer'] else None
		budget.customer.city = post_data['customer']['city'] if 'city' in post_data['customer'] else None
		budget.customer.state = post_data['customer']['state'] if 'state' in post_data['customer'] else None
		budget.customer.comments = post_data['customer']['comments'] if 'comments' in post_data['customer'] else None

		# fill other relevant fields
		budget.print_value = float(post_data['print_value'])

		# save budget record in database
		budget.save()

		# send a copy of budget to customer
		send_budget_email_customer(budget.id)

		# send a copy of budget to company process the budget request
		send_budget_email_company(budget.id)

		response.status = 201
	except Exception as e:
		response.status = 500
		return 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)