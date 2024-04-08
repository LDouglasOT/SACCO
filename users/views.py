from django.shortcuts import render

# Create your views here.

def Login(request):
    return render(request,"users/Login.html")