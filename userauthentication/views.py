# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth import authenticate, login, logout


from django.template import RequestContext

from django.contrib.auth.models import User
from .models import UserProfile

from .forms import UserForm, UserProfileForm

import xlwt
# Create your views here.
def index(request):
	return render(request, 'userauthentication/index.html')

def register(request):
	context = RequestContext(request)

	registered = False #For telling templete registration success or not

	user_form = UserForm(data=request.POST)
	profile_form = UserProfileForm(data=request.POST)
	if user_form.is_valid() and profile_form.is_valid():
		
		user = user_form.save()
		user.set_password(user.password) #Hashing the password
		user.save()
		
		profile = profile_form.save(commit=False)
		profile.user = user

		if 'uimage' in request.FILES:
			profile.uimage = request.FILES['uimage']

		profile.save()

		registered = True

	else:
		print user_form.errors, profile_form.errors

	return render(request, 'userauthentication/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)		

def login_page(request):
	return render(request, 'userauthentication/login.html')

def user_login(request):
	
	username = request.POST.get('username', False)
	password = request.POST.get('password', False)

	user = authenticate(username=username, password=password)

	if user is not None:
		login(request, user)
		instance = get_object_or_404(UserProfile, user=user)
		print instance.uaddress
		print instance.uzipcode
		context = {
		"user" : instance.user,
		"instance" : instance
		}
		return render(request, 'userauthentication/details.html', context)

	else:
		return HttpResponse("Invalid login details")

def user_logout(request):
	logout(request)


	return HttpResponseRedirect('/users/')

def list(request, id):
	responce = HttpResponse(content_type='application/ms-excel')
	responce['Content-Disposition'] = 'attachment; filename=user.xls'
	wb = xlwt.Workbook(encoding='utf-8')
	ws = wb.add_sheet('Users')
	row_num = 0
	col_num = 0
	font_style = xlwt.XFStyle()

	columns = ['User name', 'Address', 'Country', 'Zipcode', 'Sex', 'Language', 'About', 'Image', 'Phone', 'Vechicle' ]
	for col_num in range(len(columns)):
		ws.write(row_num, col_num, columns[col_num], font_style)

	rows = UserProfile.objects.filter(id=id).values_list('uname', 'uaddress', 'ucountry', 'uzipcode', 'usex', 'ulanguage', 'uabout', 'uimage', 'uphone', 'uvechicle',)
	for row in rows:
		row_num += 1
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, str(row[col_num]), font_style)

	wb.save(responce)
	return responce	