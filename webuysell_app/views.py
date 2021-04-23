from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Count
from django.views.generic import DetailView
import bcrypt


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            # password = request.POST['password']
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt(8)).decode()
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['user_id'] = user.id
            request.session['greeting'] = user.first_name
            return redirect('/dashboard')
    return redirect('/')

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) >0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        users_with_email = User.objects.filter(email=request.POST['email'])
        
        if  users_with_email:
            user = users_with_email[0]
            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                request.session['user_id'] = user.id
                request.session['greeting'] = user.first_name
                return redirect('/dashboard')
        messages.error(request, "Email for password are not right")

    return redirect('/')

def product (request, product_id):
    context = {
        "this_user" : User.objects.get(id=request.session["user_id"]),
        "this_product" : Product.objects.get(id=product_id),
        "all_product" : Product.objects.all(),
    }

    return render (request, "product.html", context)