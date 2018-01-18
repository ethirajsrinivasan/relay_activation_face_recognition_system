# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import requests, base64, json
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.templatetags.static import static
import os
from django.conf import settings
import os.path
import requests, base64, json, time, sys
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.core.files.storage import FileSystemStorage
#Relay can be imported and activated based on the user


def index(request):
	template = loader.get_template('facerecognition/index.html')
	return HttpResponse(template.render({}, request))

def add(request):
	error_msg = ''
	msg = ''
	template = loader.get_template('facerecognition/add.html')
	if request.method == "GET":
		return HttpResponse(template.render({}, request))
	else:
		if len(request.POST.get("name"))==0:
			return HttpResponse(template.render({'msg':msg, 'error_msg': "Name cannot be blank"}, request))	
		myfile = request.FILES.get('myfile',0)
		if myfile==0:
			return HttpResponse(template.render({'msg':msg, 'error_msg': "File cannot be blank"}, request))	
		fs = FileSystemStorage()
		file = "facerecognition/static/images/add.jpg"
		fs.delete(file)
		filename = fs.save(file, myfile)
		image_url = fs.url(filename)
		multipart_data = MultipartEncoder(
			fields={
				'file': ('myfile.jpg', open(image_url, 'rb').read(), 'image/jpeg'),
				'name': request.POST.get('name'),
			}
		)
		headers = {'content-type': multipart_data.content_type}
		url = 'http://localhost:5000/add'
		response = requests.post(url, data=multipart_data, headers=headers)
		if response.status_code == 200:
			msg = "Successfully updated"
		else:
			error_msg = 'Error Processing request'
		return HttpResponse(template.render({'msg':msg, 'error_msg': error_msg}, request))


def greet(request):
	myfile = request.FILES['myfile']
	fs = FileSystemStorage()
	file = "facerecognition/static/images/avatar.jpg"
	fs.delete(file)
	filename = fs.save(file, myfile)
	image_url = fs.url(filename)
	multipart_data = MultipartEncoder(
	  fields={
			'file': ('myfile.jpg', open(image_url, 'rb').read(), 'image/jpeg'),
		   }
	)
	headers = {'content-type': multipart_data.content_type}
	url = 'http://localhost:5000/recognize'
	response = requests.post(url, data=multipart_data,headers=headers)
	error_msg = ''
	name = ''
	if response.status_code == 200:
		data = response.content.decode("utf-8")
	else:
		error_msg = 'Error Processing request'
	template = loader.get_template('facerecognition/greet.html')
	return HttpResponse(template.render({'name': data, 'error_msg': error_msg, 'image_dir': image_url}, request))



	
	
