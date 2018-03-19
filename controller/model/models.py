import locale, re, json, hashlib, base64, os, sys, csv, re, jsonpickle, time, datetime
from mongoengine import *
from bottle import request, response
from bson import json_util, ObjectId

class CustomQuerySet(QuerySet):
	def to_json(self):
		return "[%s]" % (",".join([doc.to_json() for doc in self]))
	def to_json_all(self):
		return "[%s]" % (",".join([doc.to_json_all() for doc in self]))

class Attachment(EmbeddedDocument):
	oid 		= ObjectIdField(required=True, default=ObjectId)
	file_name   = StringField()
	file_size   = StringField()
	file_type   = StringField()
	file_path   = StringField()
	description = StringField()
	uploaded_at = DateTimeField(default=datetime.datetime.now)

class User(Document):
	# Collection configuration
	meta = {'collection': 'users', 'queryset_class': CustomQuerySet}
	
	# Collection fields
	name = StringField()
	login = StringField()
	password = StringField()

	def to_json(self):
		data = self.to_mongo()
		del data['password']
		data["id"] = str(self.id)
		del data['_id']

		return json_util.dumps(data)

class Banner(Document):
	# Collection configuration
	meta = {'collection': 'banners', 'queryset_class': CustomQuerySet}
	
	# Collection fields
	name = StringField()
	file = EmbeddedDocumentField(Attachment)

	def to_json(self):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		return json_util.dumps(data)

class Category(Document):
	# Collection configuration
	meta = {'collection': 'categories', 'queryset_class': CustomQuerySet}
	
	# Collection fields
	name = StringField()

	def to_json(self):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		return json_util.dumps(data)

class Project(Document):
	# Collection configuration
	meta = {'collection': 'projects', 'queryset_class': CustomQuerySet}
	
	# Collection fields
	title = StringField()
	category = ReferenceField('Category')
	text = StringField()

	def to_json(self):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		if not (self.category is None):
			data['category'] = self.category.to_mongo()
			data['category']["id"] = str(self.category.id)
			del data['category']['_id']

		return json_util.dumps(data)

class Material(Document):
	# Collection configuration
	meta = {'collection': 'materials', 'queryset_class': CustomQuerySet}

	# Collection fields
	name 		= StringField()
	cost 		= FloatField()
	thumbnail 	= StringField()

	def to_json(self):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		return json_util.dumps(data)

class DimensionData(EmbeddedDocument):
	oid 	= ObjectIdField(required=True, default=ObjectId)
	height 	= FloatField()
	width 	= FloatField()
	total 	= FloatField()

class MaterialSelected(EmbeddedDocument):
	oid 			= ObjectIdField(required=True, default=ObjectId)
	info 			= ReferenceField('Material')
	budget_cost 	= FloatField()
	dimensions 		= EmbeddedDocumentField(DimensionData)

class LocalInformation(EmbeddedDocument):
	oid 		= ObjectIdField(required=True, default=ObjectId)
	dimensions 	= EmbeddedDocumentField(DimensionData)

class InstalationInformation(EmbeddedDocument):
	oid 		= ObjectIdField(required=True, default=ObjectId)
	dimensions 	= EmbeddedDocumentField(DimensionData)

class CategorySelected(EmbeddedDocument):
	oid  = ObjectIdField(required=True, default=ObjectId)
	name = StringField()

class ImageSelected(EmbeddedDocument):
	oid 	= ObjectIdField(required=True, default=ObjectId)
	code 	= StringField()
	path 	= StringField()
	origin 	= StringField()

class CustomerInformation(EmbeddedDocument):
	oid 			= ObjectIdField(required=True, default=ObjectId)
	name 			= StringField()
	default_phone 	= StringField()
	mobile_phone 	= StringField()
	email 			= StringField()
	postal_code 	= StringField()
	address 		= StringField()
	number 			= IntField()
	district 		= StringField()
	city 			= StringField()
	state 			= StringField()
	comments 		= StringField()

class Budget(Document):
	# Collection configuration
	meta = {'collection': 'budgets', 'queryset_class': CustomQuerySet}

	# Collection fields
	material 			= EmbeddedDocumentField(MaterialSelected)
	local 				= EmbeddedDocumentField(LocalInformation)
	instalation			= EmbeddedDocumentField(InstalationInformation)
	category 			= EmbeddedDocumentField(CategorySelected)
	image 				= EmbeddedDocumentField(ImageSelected)
	customer 			= EmbeddedDocumentField(CustomerInformation)
	print_value 		= FloatField()

	def to_json(self):
		data = self.to_mongo()
		data["id"] = str(self.id)
		del data['_id']

		if not (self.material is None):
			data['material'] = self.material.to_mongo()
			data['material']["id"] = str(self.material.oid)
			del data['material']['oid']

		if not (self.local is None):
			data['local'] = self.local.to_mongo()
			data['local']["id"] = str(self.local.oid)
			del data['local']['oid']

		if not (self.instalation is None):
			data['instalation'] = self.instalation.to_mongo()
			data['instalation']["id"] = str(self.instalation.oid)
			del data['instalation']['oid']

		if not (self.category is None):
			data['category'] = self.category.to_mongo()
			data['category']["id"] = str(self.category.oid)
			del data['category']['oid']

		if not (self.image is None):
			data['image'] = self.image.to_mongo()
			data['image']["id"] = str(self.image.oid)
			del data['image']['oid']

		if not (self.customer is None):
			data['customer'] = self.customer.to_mongo()
			data['customer']["id"] = str(self.customer.oid)
			del data['customer']['oid']

		return json_util.dumps(data)