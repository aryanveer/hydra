from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Keywords
from django.contrib.auth.decorators import login_required
import json
from django.views import View
from django.contrib.auth.models import Group, User


class LoginView(View):

	def get(self, request):

		if request.user.is_authenticated:
			return redirect('/dashboard/')

		return render(request, 'users/auth_login.html')

	def post(self, request):
		username = request.POST.get('username')
		password = request.POST.get('password')
		ip = request.META['REMOTE_ADDR']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			if ip in settings.ALLOWED_IP_BLOCKS:
				login(request, user)
				return redirect('/dashboard/')
		else:
			return render(request, 'users/auth_login.html', {'message': "Invalid Username or Password."})


class RegisterView(View):

	def get(self, request):
		return render(request, 'users/auth_register.html')

	def post(self, request):
		group_name = request.POST.get('group_name')
		users_count = request.POST.get('users_count')
		new_group, created = Group.objects.get_or_create(name=group_name)
		if created:
			for count in range(1, int(users_count)+1):
				username = 'test' + '_' + group_name + str(count)
				user = User.objects.create_user(username, password='test@1234')
				new_group.user_set.add(user)
		print(new_group, created)
		return render(request, 'users/index.html')


@login_required(login_url='/login/')
def logout_view(request):
	logout(request)
	return redirect('/login/')

