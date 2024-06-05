from django.db import models
import uuid

import uuid
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountNumber = models.CharField(unique=True, max_length=255, blank=True)
    accountBalance = models.FloatField()
    totalsavings = models.IntegerField(default=0)
    accountType = models.CharField(max_length=255)
    accountName = models.CharField(max_length=255)
    accountOwner = models.ForeignKey(
        "CustomUser", related_name="accounts", on_delete=models.CASCADE
    )
    userId = models.CharField(unique=True, max_length=255, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    interest = models.FloatField()
    duration = models.IntegerField()
    loanStatus = models.CharField(max_length=255)
    nextofkin = models.CharField(max_length=255)
    approvedBy = models.CharField(max_length=255)
    isActive = models.BooleanField(default=True)
    earned = models.IntegerField(default=50000)

    def save(self, *args, **kwargs):
        if not self.accountNumber:
            self.accountNumber = str(uuid.uuid4().hex)[:10]
        super().save(*args, **kwargs)


from django.db import models
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
import secrets
import base64
import os

# import qrcode
from django.utils.translation import gettext as _
from django.conf import settings


class CustomUser(AbstractUser):
    # Add custom fields here
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(_("Phone Number"), max_length=15, blank=True)
    is_verified = models.BooleanField(default=False)
    # Provide unique related_name for groups and user_permissions
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        related_name="customuser_set",  # Unique related_name for groups
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        related_name="customuser_set",  # Unique related_name for user_permissions
        related_query_name="user",
    )

    def __str__(self):
        return self.username


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        CustomUser, related_name="users", on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    phoneNumber = models.CharField(unique=True, max_length=255)
    profilepic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    account = models.OneToOneField(
        Account,
        related_name="Account",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    accountId = models.CharField(unique=True, max_length=255, null=True, blank=True)
    isAdmin = models.BooleanField(default=False)
    isActive = models.BooleanField(default=False)
    membershipNumber = models.CharField(max_length=255, null=True, blank=True)
    membershipType = models.CharField(max_length=255)
    HomeAddress = models.CharField(max_length=255, null=True, blank=True)
    dateofbirth = models.DateTimeField()
    nationality = models.CharField(max_length=255)
    nationalId = models.CharField(max_length=255)
    placeofwork = models.CharField(max_length=255)
    natureofwork = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    MaritalStatus = models.CharField(max_length=255)
    nextofkin = models.CharField(max_length=255)
    nextofkinphone = models.CharField(max_length=255)
    nextofkinaddress = models.CharField(max_length=255)
    userstatus = models.CharField(max_length=255, default="active")

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


from django.db import models
import uuid


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transactionId = models.CharField(unique=True, max_length=255)
    transactionType = models.CharField(max_length=255)
    transactionAmount = models.FloatField()
    transactionDate = models.DateTimeField(auto_now_add=True)
    transactionDescription = models.CharField(max_length=255,default="none")
    transactionStatus = models.CharField(max_length=255, default="pending")
    transactionOwner = models.ForeignKey(
        "CustomUser", related_name="transactions", on_delete=models.CASCADE
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.transactionId:
            self.transactionId = self.generate_transaction_id()
        super().save(*args, **kwargs)

    def generate_transaction_id(self):
        return uuid.uuid4().hex

    def __str__(self):
        return (
            f"{self.transactionId} - {self.transactionType} - {self.transactionAmount}"
        )


from django.db import models
import uuid


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loanId = models.CharField(unique=True, max_length=255)
    loanAmount = models.FloatField()
    loanType = models.CharField(max_length=255)
    loanOwner = models.ForeignKey(
        "CustomUser", related_name="loans", on_delete=models.CASCADE
    )
    loanStatus = models.CharField(max_length=255)
    loanInterest = models.FloatField()
    loanDuration = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    disbursement = models.DateField(null=True, blank=True)
    totalPaid = models.FloatField(default=0)
    duedate = models.DateField(null=True, blank=True)
    Referral =models.ForeignKey('CustomUser',related_name='referral',on_delete=models.CASCADE,null=True,blank=True)
    outstanding = models.FloatField(default=0)
    approvedBy = models.CharField(max_length=255,null=True,blank=True)
    isActive = models.BooleanField(default=True)
    PenaltyBalannce = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        if not self.loanId:
            self.loanId = self.generate_loan_id()
        super().save(*args, **kwargs)

    def generate_loan_id(self):
        return uuid.uuid4().hex

    def __str__(self):
        return f"{self.loanId} - {self.loanType} - {self.loanAmount}"


from django.db import models
import uuid


class LoanPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loanPaymentId = models.CharField(unique=True, max_length=255)
    loanPaymentAmount = models.FloatField()
    loanPaymentDate = models.DateTimeField()
    loanPaymentOwner = models.ForeignKey(
        "CustomUser", related_name="loan_payments", on_delete=models.CASCADE
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.loanPaymentId:
            self.loanPaymentId = self.generate_loan_payment_id()
        super().save(*args, **kwargs)

    def generate_loan_payment_id(self):
        return uuid.uuid4().hex

    def __str__(self):
        return f"{self.loanPaymentId} - {self.loanPaymentAmount}"


class Notifications(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notificationId = models.CharField(unique=True, max_length=255)
    notificationType = models.CharField(max_length=255)
    notificationOwner = models.ForeignKey(
        "CustomUser", related_name="notifications", on_delete=models.CASCADE
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    notification = models.CharField(max_length=255, default="none")

    def save(self, *args, **kwargs):

        if not self.notificationId:
            self.notificationId = self.generate_notification_id()
        super().save(*args, **kwargs)

    def generate_notification_id(self):
        return uuid.uuid4().hex

    def __str__(self):
        return f"{self.notificationId} - {self.notificationType}"
