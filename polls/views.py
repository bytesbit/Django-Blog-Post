from django.shortcuts import render, redirect
from django.http import HttpResponse		#import httpresponse method from module
from .models import Post
from django.contrib import messages
from django.contrib.auth.models import User, auth

def index(request):
	context = {
		'posts': Post.objects.order_by('date_posted')[::-1],
		'title': 'Home',
	}
	return render(request, 'polls/index.html', context)
def about(request):
	return render(request, 'polls/about.html', context={'title': 'About'})

def signin(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			messages.success(request, f'Welcome {user.username}')
			return redirect('polls-home')
		else:
			messages.info(request, f'Invalid credentials')
			return render(request, 'polls/signin.html', {'username': username})
	elif not request.user.is_authenticated:
		return render(request, 'polls/signin.html', context={'title': 'Sign in'})
	else:
		return redirect('polls-home')