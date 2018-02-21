# -*- coding: utf-8 -*-
from InstagramAPI import InstagramAPI
from bottle import request, response
from bottle import get, put, post, delete

@get('/external/instagram/feed')
def get_instagram_feed():
	# api = InstagramAPI("Idea10oficial", "print102030")
	api = InstagramAPI("idea10tambore", "Print102030")
	if (api.login()):
		api.getSelfUserFeed()
		return api.LastJson
	else:
		response.status = 500
		return "Não foi possível efetuar o login, usuário e/ou senha inválidos."