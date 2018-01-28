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
    oid         = ObjectIdField(required=True, default=ObjectId)
    file_name   = StringField()
    file_size   = StringField()
    file_type   = StringField()
    file_path   = StringField()
    description = StringField()
    uploaded_at = DateTimeField(default=datetime.datetime.now)

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