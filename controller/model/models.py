import locale, re, json, hashlib, base64, os, sys, csv, re, jsonpickle, time, datetime
from mongoengine import *
from bottle import request, response
from bson import json_util, ObjectId

class CustomQuerySet(QuerySet):
    def to_json(self):
        return "[%s]" % (",".join([doc.to_json() for doc in self]))
    def to_json_all(self):
        return "[%s]" % (",".join([doc.to_json_all() for doc in self]))

class Anexo(EmbeddedDocument):
    oid         = ObjectIdField(required=True, default=ObjectId, unique=True)
    file_name   = StringField()
    file_size   = StringField()
    file_type   = StringField()
    file_path   = StringField()
    legenda     = StringField()
    data_upload = DateTimeField(default=datetime.datetime.now)

class Pessoa(Document):
    # Collection configuration
    meta = {'collection': 'pessoa', 'queryset_class': CustomQuerySet}

    # Collection fields
    email = StringField()

    def to_json(self):
        data = self.to_mongo()
        data["id"] = str(self.id)
        del data['_id']

        return json_util.dumps(data)