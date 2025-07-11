from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_login(request):
    pass

def user_logout(request):
    pass

def user_register(request):
    pass