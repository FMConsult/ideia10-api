# -*- coding: utf-8 -*-
from InstagramAPI import InstagramAPI
from bottle import request, response
from bottle import get, put, post, delete

@get('/external/instagram/feed')
def get_instagram_feed():
	api = InstagramAPI("Idea10oficial", "print102030")
	if (api.login()):
		api.getSelfUserFeed()
		return api.LastJson
	else:
		return "Can't login!"