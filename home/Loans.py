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


def ActiveLoans(request):
    if request.user.is_staff:
        loan = Loan.objects.filter()

        return render(
            request,
            "home/Loans/Loans.html",
            {"footer": False, "header": False, "loans": loan},
        )
    loan = Loan.objects.filter(
        loanOwner=request.user, loanStatus="Approved"
    )
    return render(
        request,
        "home/Loans/Loans.html",
        {"footer": False, "header": False, "loans": loan,"loancounter":loan.count()},
    )



def declinedLoans(request):
    if request.user.is_staff:
        loan = Loan.objects.filter(loanStatus="Declined")
        return render(
            request,
            "home/Loans/declinedLoans.html",
            {"footer": False, "header": False, "loans": loan},
        )
    loan = Loan.objects.filter(
        loanOwner=request.user, isActive=False, loanStatus="Declined"
    )
    return render(
        request,
        "home/Loans/declinedLoans.html",
        {"footer": False, "header": False, "loans": loan},
    )


def completedLoans(request):
    if request.user.is_staff:
        loan = Loan.objects.filter(loanStatus="Completed")
        return render(
            request,
            "home/Loans/completedLoans.html",
            {"footer": False, "header": False, "loans": loan},
        )
    loan = Loan.objects.filter(loanOwner=request.user, loanStatus="Completed")
    return render(
        request,
        "home/Loans/completedLoans.html",
        {"footer": False, "header": False, "loans": loan},
    )


def PendingLoans(request):
    if request.user.is_staff:
        loan = Loan.objects.filter(loanStatus="Pending")
        return render(
            request,
            "home/Loans/PendingLoans.html",
            {"footer": False, "header": False, "loans": loan},
        )
    loan = Loan.objects.filter(
        loanOwner=request.user, isActive=False, loanStatus="Pending"
    )
    return render(
        request,
        "home/Loans/PendingLoans.html",
        {"footer": False, "header": False, "loans": loan},
    )


def LoanApplication(request):
    if request.method == "POST":
        loan = Loan()
        loan.loanOwner = request.user
        loan.loanAmount = request.POST.get("loanAmount")
        loan.loanInterest = request.POST.get("loanInterest")
        loan.loanDuration = request.POST.get("loanDuration")
        loan.loanStatus = "Pending"
        loan.save()
        return redirect("dashboard")
    else:
        return render(request, "home/LoanApplication.html")


def disbursement(request):
    if request.user.is_staff:
        loan = Loan.objects.filter(loanStatus="Disburse")
        return render(
            request,
            "home/Loans/Disburse.html",
            {"footer": False, "header": False, "loans": loan},
        )
    loan = Loan.objects.filter(loanOwner=request.user, loanStatus="Disburse")
    return render(
        request,
        "home/Loans/Disburse.html",
        {"footer": False, "header": False, "loans": loan},
    )
