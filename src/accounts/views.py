from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,)
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegistrationForm

# Create your views here.
def login_view(request):
	next =request.GET.get('next')
	title = "Login"
	#print (request.user.is_authenticated())
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")		
		user = authenticate(username=username,password=password)
		login(request,user)
		if next:
			return redirect(next)
		return redirect("/")
		#print (request.user.is_authenticated())
	return render(request, "form.html",{"form":form, "title":title})

def register_view(request):
	print (request.user.is_authenticated())
	next =request.GET.get('next')
	title = "Register"
	form = UserRegistrationForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		newuser = authenticate(username=user.username,password=password)  # authenticate() very important for login
		login(request,newuser)
		if next:
			return redirect(next)
		
		return redirect("/")

	context = {'title':title,
				'form':form
	}
	return render(request, "form.html",context)

def logout_view(request):
	logout(request)
	return redirect("/")