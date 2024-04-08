from django.shortcuts import render
from django.shortcuts import render
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
def Home(request):
    
    return render(request,"home/Home.html",{"footer":True,"header":True})

def dashboard(request):
    return render(request,"home/dashview.html",{"footer":False,"header":False})

def homepage(request):
    return render(request,"home/homepage.html")