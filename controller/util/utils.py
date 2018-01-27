import re, smtplib, sys, string, random, urlparse, jsonpickle
import suds, xmltodict, logging, string
from email.mime.text import MIMEText
from bottle import request, response
from dateutil import parser
from datetime import datetime
from datetime import date
from math import ceil
from controller.model.models import *

class StringUtil(object):
	def __init__(self):
		pass

	def id_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))

class MailSender(object):
	_host = None
	_port = None
	_user = None
	_pass = None
	_smtp_server = None

	def __init__(self, host=None, port=None, user=None, password=None):
		self._host = host
		self._port = port
		self._user = user
		self._pass = password
		pass

	def connect(self):
		try:
			self._smtp_server = smtplib.SMTP_SSL(self._host +':'+ self._port)
			self._smtp_server.set_debuglevel(True)
			self._smtp_server.login(self._user, self._pass)
		except Exception as e:
			raise e

	def send_mail(self, destination, subject, text, text_type):
		try:
			message = MIMEText(text, text_type, 'utf-8')
			message['From'] = self._user
			message['Subject'] = subject
			
			self._smtp_server.sendmail(self._user, destination, message.as_string())
			self._smtp_server.quit()
		except Exception as e:
			raise e

class DateUtil:
	def is_date(self, string):
		try:
			parser.parse(string)
			return True
		except ValueError:
			return False

	def calculate_age(self, born):
		today = date.today()
		return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

class CPFUtil:
	def __init__( self ):
		""" 
		Class to interact with CPF numbers
		"""
		pass

	def format( self, cpf ):
		""" 
		Method that formats a brazilian CPF

		Tests:
		>>> print CPFUtil().format('91289037736')
		912.890.377-36
		"""
		return "%s.%s.%s-%s" % ( cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11] )

	def validate(self,cpf):
		cpf_invalidos = [11*str(i) for i in range(10)]
		if cpf in cpf_invalidos:
			return False
		if not cpf.isdigit():
			cpf = cpf.replace(".", "")
			cpf = cpf.replace("-", "")
		if len(cpf) < 11:
			return False
		if len(cpf) > 11:
			return False
		selfcpf = [int(x) for x in cpf]
		cpf = selfcpf[:9]
		while len(cpf) < 11:
			r =  sum([(len(cpf)+1-i)*v for i, v in [(x, cpf[x]) for x in range(len(cpf))]]) % 11
			if r > 1:
				f = 11 - r
			else:
				f = 0
			cpf.append(f)
		return bool(cpf == selfcpf)

class CNPJUtil:
	def __init__( self ):
		pass

	def validate(self, cnpj):
		cnpj = ''.join(re.findall('\d', str(cnpj)))

		if (not cnpj) or (len(cnpj) < 14):
			return False

		inteiros = map(int, cnpj)
		novo = inteiros[:12]
		prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

		while len(novo) < 14:
			r = sum([x*y for (x, y) in zip(novo, prod)]) % 11
			if r > 1:
				f = 11 - r
			else:
				f = 0
				novo.append(f)
				prod.insert(0, 6)

		if novo == inteiros:
			return cnpj

		return False

class PaginationUtil(object):
	def __init(self):
		pass

	def paginate(self, query, offset, limit):
		count = len(query)
		num_pages = ceil(float(count) / float(limit))

		if offset > num_pages:
			return None

		prev    = (offset - 1) if offset > 1 else None
		next    = (offset + 1) if offset < num_pages else None
		start   = (offset - 1) * limit
		end     = start + limit

		objects = []

		for item in query[start:end]:
			try:
				objects.append(jsonpickle.decode(item.to_json()))
			except AttributeError as e:
				print('erro ao serializar o item type: '+ str(type(item)) +' com id: '+ str(item.id))
				pass
			except Exception as e:
				print('erro ao serializar o item type: '+ str(type(item)) +' com id: '+ str(item.id))
				pass

		pagination = {
			'pagination': {
				'offset': offset,
				'prev'  : prev,
				'next'  : next,
				'total' : num_pages
			},
			'records': objects
		}

		return pagination

class UrlUtil:
	def __init(self):
		pass

	def url_parse(self, query_string):
		url_params = {}
		url_params['params'] = urlparse.parse_qs(query_string)

		for key, value in url_params['params'].items():
			if key == 'offset':
				url_params['offset'] = int(value[0])
				del url_params['params']['offset']
			elif key == 'limit':
				url_params['limit'] = int(value[0])
				del url_params['params']['limit']
			else:
				url_params['params'][key] = value[0]

		return url_params
