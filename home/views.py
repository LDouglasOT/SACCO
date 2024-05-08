from django.shortcuts import redirect, render
from django.shortcuts import render

from home.form import AccountForm, UserForm
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render

from django.shortcuts import render

from datetime import date
from django.db.models import Sum 
import datetime
import hashlib
import requests
from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from django.http import HttpResponse

# Create your views here.
def Members(request):
    user = Users.objects.all()
    return render(request,"home/Members.html",{"footer":False,"header":False,"users":user,'usercount':user.count()})

def dashboard(request):
    account = Account.objects.get(accountOwner=request.user)
    User = Users.objects.get(owner=request.user)
    loan = Loan.objects.filter(loanOwner=request.user).count()
    loanpayment = LoanPayment.objects.filter(loanPaymentOwner=request.user).count()
    transaction = Transaction.objects.filter(transactionOwner=request.user).count()
    context = {
    "account":account,
    "loan":loan,

    "loanpayment":loanpayment,
    "transaction":transaction,
    
    }
    print(User.firstname)
    return render(request,"home/maindashboard.html",{"footer":False,"header":False,"account":account,
    "loan":loan,
    "loanpayment":loanpayment,
    "transaction":transaction,"user":User})

def homepage(request):
    return render(request,"home/Home.html",{"footer":True,"header":True})

def Profile(request):
    profile = Users.objects.get(owner=request.user)
    account = Account.objects.get(accountOwner=request.user)
    return render(request,"home/Profile.html",{ "profile":profile,"account":account})

def notifications(request):
    notifications = Notifications.objects.filter(notificationOwner=request.user)
    return render(request,"home/notifications.html",{"notifications":notifications})

def loans(request):
    if request.user.is_staff:
        loans = Loan.objects.all()
        return render(request,"home/loans.html",{"loans":loans})

def Transactions(request):
    transactions = Transaction.objects.filter(transactionOwner=request.user)   
    return render(request,"home/Transactions.html",{"transactions":transactions})


def CreateUser(request):

    if request.method == "POST":
       userform = UserForm(request.POST)
       accountform = AccountForm(request.POST)
       if userform.is_valid() and accountform.is_valid():
           user = userform.save()
           account = accountform.save(commit=False)
           account.user = user
           account.save()
           return redirect("dashboard")
       else:
           return JsonResponse({"status":"error"})
    if request.method == "GET":
        userform = UserForm()
        accountform = AccountForm()
        return render(request,"home/new.html",{"userform":userform,"accountform":accountform})
    

def memberinfo(request,id):
    profile = Users.objects.get(pk=id)
    account = Account.objects.get(accountOwner=profile.owner)
    return render(request,"home/memberinfo.html",{"profile":profile,"account":account})

def suspenduser(request,id):
    user = Users.objects.get(pk=id)
    user.isActive = False
    user.save()
    return redirect("members")