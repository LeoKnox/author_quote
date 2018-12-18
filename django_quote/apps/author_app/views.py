from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
from .models import User, Something

def index(request):
    return render(request, "author_app/index.html")
# Create your views here.

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hpwd = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST["fname"],last_name=request.POST["lname"],password=hpwd,email=request.POST["email"])
        request.session['use'] = request.POST["fname"]
        return redirect("/welcome")

def login(request):
    errors = User.objects.pw_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name = User.objects.filter(email=request.POST["email"])
        request.session['use'] = name[0].first_name
        print(name[0].first_name)
        return redirect("/welcome")

def welcome(request):
    if 'use' not in request.session:
        return redirect("/")
    context = {
        "data":Something.objects.all().order_by("-created_at")
    }
    print(User.objects.all())
    return render(request,"author_app/welcome.html",context)

def create_quote(request):
    errors = User.objects.q_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/welcome')
    else:
        uid = User.objects.get(first_name=request.session['use'])
        Something.objects.create(quote=request.POST["quote"],author=request.POST["author"],poster=uid)
        print(Something.objects.all().values())
        return redirect("/welcome")

def poster(request, val):
    context = {
        "makes":Something.objects.filter(poster=val),
        "user":User.objects.get(id=val)
    }
    return render(request, "author_app/poster.html",context)

def delete(request, val):
    d = Something.objects.get(id=val)
    d.delete()
    return redirect("/welcome")

def edit(request):

    return render(request, "author_app/edit.html")

def update(request):
    errors = User.objects.e_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/edit")
    else:
        u=User.objects.get(first_name=request.session['use'])
        u.first_name=request.POST["first_name"]
        u.last_name=request.POST["last_name"]
        u.email=request.POST["email"]
        u.save()
    return redirect("/welcome")

def logout(request):
    request.session.clear()
    return redirect("/")

# Create your views here.
