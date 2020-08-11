from django.shortcuts import render, redirect, HttpResponse, reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from polls.models import Post

'''
types of django messages--------->
messgaes.success
messgaes.error
messgaes.warning
messgaes.info
messgaes.debug
'''

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		fname = request.POST['fname']
		fname = fname.capitalize()
		lname = request.POST['lname']
		lname = lname.capitalize()
		if password1 == password2:
			if not User.objects.filter(username=username).exists():
				user = User.objects.create_user(username=username, password=password1, first_name=fname, last_name=lname, email=email)
				user.save()
				print(f"{username} User created")
				messages.success(request, f'{fname} your account created successfully. Now you can login here.')
				return redirect('polls-signin')
			else:
				messages.info(request, f'Username {username} already taken')
				return render(request, 'users/register.html', {'fname': fname, 'lname': lname})
		else:
			print("password not match")
			return render(request, 'users/register.html')
	elif request.user.is_authenticated:
		return redirect("polls-home")

	else:
		return render(request, 'users/register.html', {'title': 'Register'})

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)
		messages.info(request, f'Loggout successfully')
		return redirect('polls-home')
	else:
		return redirect('polls-home')

def newPost(request):
	if request.method == 'POST':
		ttl = request.POST['title']
		content = request.POST['content']
		author = request.user.username
		author = User.objects.get(username=author)
		post = Post(title=ttl, content=content, author=author)
		post.save()
		messages.success(request, 'Post created successfully.')
		return redirect('polls-home')
	elif not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		return render(request, 'users/newpost.html')

def profile(request):
	if not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		user = User.objects.filter(username=request.user.username).first()
		posts = Post.objects.filter(author=user)
		context = {
			'title': request.user.first_name,
			'posts': posts,
		}
		return render(request, 'users/profile.html', context)

def edit(request, pk):
	if request.method == "POST":
		newTitle = request.POST['title']
		newContent = request.POST['content']
		user = User.objects.get(username=request.user.username)
		post = Post.objects.get(id=pk, author=user)
		post.title = newTitle
		post.content = newContent
		post.save()


	elif not request.user.is_authenticated:
		return redirect('polls-home')
	else:
		print(pk)
		user = User.objects.filter(username=request.user.username).first()
		try:
			post = Post.objects.get(id=pk, author=user)
		except:
			return redirect('polls-home')
		context = {
			'post_title': post.title,
			#'content':	post.content,
			'title': 'edit',
		}
		return render(request, 'users/editPost.html')

# def fetchProfile(request, user):
# 	u = User.objecrs.get(username=user)
# 	posts = Post.objects.filter(author=u).all()
# 	context ={
# 		'u': u,
# 		'posts': posts,
# 	}
# 	return render(request, 'users/fetchProfile.html', context)
