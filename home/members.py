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
    user = Users.objects.filter(isActive=True)
    usercount = user.count()
    return render(request,"home/Members/Members.html",{"footer":False,"header":False,"users":user,'usercount':usercount})

def memberinfo(request,id):
    user = Users.objects.get(id=id)
    account = Account.objects.get(accountOwner=user.owner)
    return render(request,"home/Members/memberinfo.html",{"footer":False,"header":False,"user":user,"account":account})

def suspendmember(request,id):
    user = Users.objects.get(id=id)
    user.isActive = False
    user.userstatus = "Suspended"
    user.save()
    return redirect("members")

def PedningMembers(request):
    user = Users.objects.filter(isActive=False,userstatus="Pending")
    usercount = user.count()
    return render(request,"home/Members/PendingMembers.html",{"footer":False,"header":False,"users":user,'usercount':usercount})
def suspendedMembers(request):
    user = Users.objects.filter(isActive=False,userstatus="Suspended")
    usercount = user.count()
    return render(request,"home/Members/SuspendedMembers.html",{"footer":False,"header":False,"users":user,'usercount':usercount})

def reactivatemember(request,id):
    user = Users.objects.get(id=id)
    user.isActive = True
    user.userstatus = "Active"
    user.save()
    return redirect("members")

def loans(request):
    if request.user.is_staff:
        loans = Loan.objects.all()
        loancount = loans.count()
        return render(request,"home/Loans/loans.html",{"loans":loans,'loancount':loancount})