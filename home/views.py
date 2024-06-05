from django.shortcuts import redirect, render
from django.shortcuts import render

from home.form import AccountForm, UserForm
from payments.models import paymentRequests
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
import uuid
from .models import CustomUser, Account, Users
from django.contrib import messages
from django.db.models.functions import TruncMonth

from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Transaction

def get_monthly_transaction_totals(user):
    # Initialize a dictionary with all months set to 0
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly_totals_dict = {month: 0 for month in month_names}
    
    # Fetch and aggregate the data
    monthly_totals = (
        Transaction.objects.filter(transactionOwner=user,transactionType='Deposit')
        .annotate(month=TruncMonth('transactionDate'))
        .values('month')
        .annotate(total_amount=Sum('transactionAmount'))
        .order_by('month')
    )
    
    # Update the dictionary with actual totals
    for record in monthly_totals:
        month_key = record['month'].strftime('%B')  # Get full month name
        monthly_totals_dict[month_key] = record['total_amount']
    
    return monthly_totals_dict

def get_monthly_transaction_totals_for_withdraws(user):
    # Initialize a dictionary with all months set to 0
    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    monthly_totals_dict = {month: 0 for month in month_names}
    
    # Fetch and aggregate the data
    monthly_totals = (
        Transaction.objects.filter(transactionOwner=user,transactionType='Withdraw')
        .annotate(month=TruncMonth('transactionDate'))
        .values('month')
        .annotate(total_amount=Sum('transactionAmount'))
        .order_by('month')
    )
    
 
    for record in monthly_totals:
        month_key = record['month'].strftime('%B')  # Get full month name
        monthly_totals_dict[month_key] = record['total_amount']
    
    return monthly_totals_dict


def dashboard(request):

    if not request.user.is_staff:
        print(get_monthly_transaction_totals(request.user))
        account = Account.objects.get(accountOwner=request.user)
        User = Users.objects.get(owner=request.user)
        loan = Loan.objects.filter(loanOwner=request.user).count()
        loanpayment = LoanPayment.objects.filter(loanPaymentOwner=request.user).count()
        transaction = Transaction.objects.filter(transactionOwner=request.user).count()
        loantotal = Loan.objects.filter(loanOwner=request.user).aggregate(
            Sum("loanAmount")
        )
        paymentRequest = paymentRequests.objects.filter(status="Pending")
        print(paymentRequest)
        activeloan = Loan.objects.filter(loanOwner=request.user, loanStatus="Active").first()
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
                "paymentRequests": paymentRequest.count,
                "actual":paymentRequest,
                "monthly_totals": get_monthly_transaction_totals(request.user),
                "monthly_withdraws": get_monthly_transaction_totals_for_withdraws(request.user),
                "activeloan": activeloan,
            },
        )
    else:


        account = Account.objects.all()

        User = Users.objects.all()

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
        withdraws = Transaction.objects.filter(transactionType="Withdraw")
        withdeawcount = withdraws.count()
        withdrawstotal=Transaction.objects.filter(transactionType="Withdraw").aggregate(Sum("transactionAmount"))
        
        totals = Loan.objects.filter(loanStatus="Active").aggregate(
        total_loan_amount=Sum('loanAmount'),
        total_loan_interest=Sum('loanInterest')
        )
    
        combined_total = (totals['total_loan_amount'] or 0) + (totals['total_loan_interest'] or 0)
        print(combined_total)
        # combined_total = (totals['total_loan_amount'] or 0) + (totals['total_loan_interest'] or 0)
        
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
                "withdraws": withdrawstotal,
                "withdeawcount":withdeawcount,
                'combined_total': combined_total,
            
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
    if request.user.is_staff:
        transactions = Transaction.objects.all()
        return render(request, "home/Transactions.html", {"transactions": transactions})
    else:
        transactions = Transaction.objects.filter(transactionOwner=request.user)
        return render(request, "home/Transactions.html", {"transactions": transactions})

    

# @login_required
def CreateUser(request):
    if request.method == "POST":
        username = request.POST.get('phoneNumber')
        password = request.POST.get('password')
        email = request.POST.get('email')  
        user = CustomUser.objects.create_user(username=username, password=password, email=email)
        
        account = Account(
            accountBalance=0.0,  # Initialize balance
            totalsavings=0,
            accountType=request.POST['accountType'],
            accountName="{0} {1}".format(request.POST['firstname'], request.POST['lastname']),
            accountOwner=user,
            userId=str(uuid.uuid4()),
            interest=1.1,
            duration=0,
            loanStatus="None",
            nextofkin=request.POST['nextofkin'],
            approvedBy=request.POST['id_approvedBy'],
            earned=0
        )
        account.save()

        mainuser = Users(
            owner=user,
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            location=request.POST['location'],
            phoneNumber=request.POST['phoneNumber'],
            profilepic=request.POST['profilepic'],
            email=request.POST['email'],
            password=request.POST['password'],
            account=account,
            accountId=str(uuid.uuid4()),
            isActive=True,
            membershipType=request.POST['accountType'][0],
            HomeAddress=request.POST['location'],
            dateofbirth=request.POST['birthday'],
            nationality='Uganda',
            nationalId=request.POST['nationalId'],
            placeofwork=request.POST['placeofwork'],
            natureofwork=request.POST['natureofwork'],
            gender=request.POST['accountType'][1],
            MaritalStatus=request.POST['id_MaritalStatus'],
            nextofkin=request.POST['nextofkin'],
            nextofkinphone=request.POST['nextofkinphone'],
            nextofkinaddress=request.POST['nextofkinaddress']
        )
        mainuser.save()

        return redirect('member')
    elif request.method == "GET":
        userform = UserForm()
        accountform = AccountForm()
        members = CustomUser.objects.filter(is_staff=True)
        return render(
            request, "home/new.html", {"userform": userform, "accountform": accountform, "members": members}
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

