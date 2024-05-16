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


def dashboard(request):

    if not request.user.is_staff:
        account = Account.objects.get(accountOwner=request.user)
        User = Users.objects.get(owner=request.user)
        loan = Loan.objects.filter(loanOwner=request.user).count()
        loanpayment = LoanPayment.objects.filter(loanPaymentOwner=request.user).count()
        transaction = Transaction.objects.filter(transactionOwner=request.user).count()
        loantotal = Loan.objects.filter(loanOwner=request.user).aggregate(
            Sum("loanAmount")
        )
        return render(
            request,
            "home/maindashboard.html",
            {
                "footer": False,
                "header": False,
                "account": account,
                "loan": loan,
                "loanpayment": loanpayment,
                "transaction": transaction,
                "user": User,
                "loantotal": loantotal,
            },
        )
    else:
        account = Account.objects.all()

        User = Users.objects.all()
        print(User.count())
        print("Nothing to print here")
        loan = Loan.objects.filter(loanStatus="Active").count()
        pending = Loan.objects.filter(loanStatus="Pending")
        pendingCount = pending.count()
        pending = pending.aggregate(Sum("loanAmount"))

        loanpayment = LoanPayment.objects.all().count()
        transaction = Transaction.objects.all()
        transactioncount = transaction.count()
        transaction = transaction.aggregate(Sum("transactionAmount"))

        accountBalance = Account.objects.filter(accountOwner__is_active=True).aggregate(
            Sum("accountBalance")
        )
        print(accountBalance)
        loanpayment = LoanPayment.objects.filter(loanPaymentOwner=request.user).count()
        transaction = Transaction.objects.filter(transactionOwner=request.user).count()
        loantotal = Loan.objects.filter(loanOwner=request.user).aggregate(
            Sum("loanAmount")
        )

        interest = Loan.objects.filter(loanStatus="Active").aggregate(
            Sum("loanInterest")
        )
        disburse = Loan.objects.filter(loanStatus="Disburse")
        disbursecount = disburse.count()
        disburse = disburse.aggregate(Sum("loanAmount"))
        return render(
            request,
            "home/maindashboard.html",
            {
                "footer": False,
                "header": False,
                "account": account,
                "loan": loan,
                "loanpayment": loanpayment,
                "transaction": transaction,
                "transactioncount": transactioncount,
                "user": User,
                "loantotal": loantotal,
                "accountCount": account.count(),
                "userCount": User.count(),
                "loanCount": loan,
                "pending": pending,
                "pendingCount": pendingCount,
                "loanpayment": loanpayment,
                "transaction": transaction,
                "accountBalance": accountBalance,
                "interest": interest,
                "disburse": disburse,
                "disbursecount": disbursecount,
            },
        )


def homepage(request):
    return render(request, "home/Home.html", {"footer": True, "header": True})


def Profile(request):
    profile = Users.objects.get(owner=request.user)
    account = Account.objects.get(accountOwner=request.user)
    return render(
        request, "home/Profile.html", {"profile": profile, "account": account}
    )


def notifications(request):
    if request.user.is_staff:
        notifications = Notifications.objects.all()
        notificationscounter = notifications.count()
        return render(
            request,
            "home/notifications.html",
            {
                "notifications": notifications,
                "notificationscounter": notificationscounter,
            },
        )
    else:
        notifications = Notifications.objects.filter(notificationOwner=request.user)
        notificationscounter = notifications.count()
        return render(
            request,
            "home/notifications.html",
            {
                "notifications": notifications,
                "notificationscounter": notificationscounter,
            },
        )


def Transactions(request):
    transactions = Transaction.objects.filter(transactionOwner=request.user)
    return render(request, "home/Transactions.html", {"transactions": transactions})


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
            return JsonResponse({"status": "error"})
    if request.method == "GET":
        userform = UserForm()
        accountform = AccountForm()
        return render(
            request, "home/new.html", {"userform": userform, "accountform": accountform}
        )


def memberinfo(request, id):
    profile = Users.objects.get(pk=id)
    account = Account.objects.get(accountOwner=profile.owner)
    return render(
        request, "home/memberinfo.html", {"profile": profile, "account": account}
    )


def suspenduser(request, id):
    user = Users.objects.get(pk=id)
    user.isActive = False
    user.save()
    return redirect("members")


def whatsapp(request):
    return render(request, "home/whatsapp.html")
