from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Account)
admin.site.register(CustomUser)
admin.site.register(Loan)
admin.site.register(Users)
admin.site.register(LoanPayment)
admin.site.register(Notifications)
admin.site.register(Transaction)
