from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import Users
import bcrypt, re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your views here.
def index(request):
	return render(request, 'login_app/index.html')
def success(request):
	data = {
		'username': request.POST['username'],
		'email': request.POST['email'],
		'password': request.POST['pass'],
		'cpass': request.POST['conpass'],
		}
	results = Users.objects.validate(data)

	if results[0]:
		request.session['user_id'] = results[1].id
		context = {
		'win': 'Thank you for Registering!'
		}
		return render(request,'login_app/index.html',context)
	else:
		for err in results[1]:
 			messages.error(request, err)
 		
		return redirect("/")

def login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		if not Users.objects.filter(email = email):
			context = {
				'nouser':"This User does not exits"
			}
			return render(request,'login_app/index.html',context)

		user = Users.objects.filter(email = email)

		if not EMAIL_REGEX.match(email):
			context = {
			'email':'Sorry, your email did not match our records'
			}
			return render(request,'login_app/index.html',context)
	if bcrypt.hashpw(str(password),str(user[0].password)) == user[0].password:
		request.session['log_user_id'] = user[0].id
		request.session['log_user_name'] = user[0].name
	
		return redirect(reverse('puppy:index'))
	else:
		context = {
			'notmatch':'Sorry, your password did not match our records'
		}
		return render(request,'login_app/index.html',context)
def logout(request):
	request.session.clear()
	return redirect('/')


