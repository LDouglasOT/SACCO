from datetime import timezone
import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
import os
import requests
import xmltodict
from home.models import Account, Loan, Transaction, Users
from payments.models import paymentRequests
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.dateparse import parse_datetime

# Create your views here.

def withdraw(request):
    print(request.method)
    if request.method == "POST":
        amount = request.POST.get("amount")
        print(amount)
        phone = request.POST.get("phone")
        print(phone)
        account = Account.objects.get(accountOwner=request.user)
        if account.accountBalance >= float(amount):
            account.accountBalance -= float(amount)
            account.save()
            transaction = Transaction(
                transactionOwner=request.user,
                transactionAmount=float(amount),
                transactionType="Withdraw",
                transactionDescription="Withdrawal of UGX {0} to {1} Successfully executed",
                transactionDate=datetime.date.today(),
            )
            transaction.save()
            messages.success(request, 'Withdrawal Successfully executed of UGX {0} to {1}, your money should arrive in minutes'.format(amount, phone))
            return redirect("dashboard")
        else:
            messages.error(request, 'You have insufficient funds to make this transaction')
            transaction = Transaction(
                transactionOwner=request.user,
                transactionAmount=float(amount),
                transactionType="Withdraw",
                transactionDescription="Withdraw of {0} to {1} failed due to insufficient funds".format(amount, phone),
                transactionDate=datetime.date.today(),
            )
            return redirect("dashboard")
    else:
        return render(request, "home/transactions/withdraw.html", {"footer": False, "header": False})

def fetch_transactions(amount, phone, narrative):
    phone = phone[-9:]
    phone = '256' + phone
    
    payment_data = {
        "username": os.getenv('API_USERNAME'),
        "password": os.getenv('API_KEY'),
        "url": os.getenv('API_URL')
    }

    api_url = payment_data['url']
    
    request_data = {
        "AutoCreate": {
            "Request": {
                "APIUsername": payment_data['username'],
                "APIPassword": payment_data['password'],
                "Method": 'acdepositfunds',
                "NonBlocking": '', 
                "Amount": int(amount), 
                "Account": phone, 
                "AccountProviderCode": 'PROVIDER_CODE',
                "Narrative": narrative
            }
        }
    }

    xml_request = xmltodict.unparse(request_data, pretty=True)
    
    headers = {
        'Content-Type': 'application/xml',
    }

    try:
        response = requests.post(api_url, data=xml_request, headers=headers)
        response.raise_for_status()

        response_dict = xmltodict.parse(response.content)
        response_obj = response_dict['AutoCreate']['Response']
        status = response_obj['Status']

        if status == 'OK':
            return True
        else:
            return False
    except requests.RequestException as e:
        print('Error:', e)
        return False
    except xmltodict.expat.ExpatError as e:
        print('Error parsing XML:', e)
        return False




def deposit(request):
    if request.method == "POST":  
        amount = request.POST.get("amount")
        phone = request.POST.get("phone")
        
        paymentrequests = paymentRequests.objects.create(
            owner=request.user,
            amount=amount,
            phone=phone,
            narrative="Deposit of UGX {0} to {1}".format(amount, phone),
            status="Pending"
        )

        paymentrequests.save()
        messages.success(request, 'Deposit request of UGX {0} Successfully submitted to {1}, enter your pin on your phone when the mobile money prompt arrives'.format(amount, phone))
        return redirect("dashboard")
    return render(request, "home/transactions/deposit.html", {"footer": False, "header": False})
    
def loanfilter(request):
    if request.method == "POST":
        status = request.POST.get('loanstatus')
        print(status)
        startdate_str = request.POST.get('startdate')
        enddate_str = request.POST.get('enddate')
        try:
            startdate = parse_datetime(startdate_str) if startdate_str else None
            enddate = parse_datetime(enddate_str) if enddate_str else None
        except ValidationError:
            
            return render(request, "home/Loans/Loans.html", {"error": "Invalid date format. Please use YYYY-MM-DD HH:MM."})

        queryset = Loan.objects.all()

        if status and status != 'all':
            queryset = queryset.filter(loanStatus=status)

        if startdate and enddate:
            queryset = queryset.filter(createdAt__range=[startdate, enddate])
        elif startdate:
            queryset = queryset.filter(createdAt__gte=startdate)
        elif enddate:
            queryset = queryset.filter(createdAt__lte=enddate)

        loans = queryset 

        return render(request, "home/Loans/Loans.html", {"footer": False, "header": False, "loans": loans,"loancounter":loans.count()})



def canceltransaction(request,pk):
    if request.method == "GET":
        print("Request came through")
        paymentrequests = paymentRequests.objects.get(pk=pk)
        paymentrequests.status = "Cancelled"
        print(paymentRequests.status)
        paymentrequests.save()
        messages.success(request, 'Transaction Successfully cancelled')
        return redirect("dashboard")
    return redirect("dashboard")

def checktransaction(request,pk):
    if request.method == "GET":
        print("Request came through")
        paymentrequests = paymentRequests.objects.get(pk=pk)
    

        if paymentrequests.status == "Pending":
            paymentrequests.status = "Completed"
            paymentrequests.save()
            messages.success(request, 'Transaction Successfully completed')
            return redirect("dashboard")
        
        else:
            messages.error(request, 'Transaction still processing, please wait for a few minutes')
            return redirect("dashboard")
    return redirect("dashboard")

def loandetails(request,pk):
    if request.method == "GET":
        loan = Loan.objects.get(pk=pk)
        member  = Users.objects.filter(pk=loan.loanOwner.id)
        print(member)
        return render(request, "home/Loans/Details.html", {"footer": False, "header": False, "loan": loan,"member":member})
    return redirect("dashboard")