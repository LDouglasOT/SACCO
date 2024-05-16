"""
URL configuration for sacc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from users.views import *
from home.views import *
from django.conf.urls.static import static
from django.conf import settings
from home.members import *
from home.Loans import *


urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("", homepage, name="index"),
    path("dashboard/", dashboard, name="dashboard"),
    path("home/", homepage, name="home"),
    path("profile/", Profile, name="profile"),
    path("notifications/", notifications, name="notifications"),
    path("transactions/", Transactions, name="transactions"),
    path("createuser/", CreateUser, name="createuser"),
    path("login/", custom_login, name="login"),
    path("logout/", custom_logout, name="logout"),
    path("register/", custom_registration, name="register"),
    # Members inforamation, suspension, active ones and activation
    path("members/active/", Members, name="members"),
    path("member/<uuid:id>/", memberinfo, name="memberinfo"),
    path("membersuspend/<uuid:id>/", suspendmember, name="suspendmember"),
    path("members/pendingmembers/", PedningMembers, name="pendingmembers"),
    path("memebers/suspendedmembers/", suspendedMembers, name="suspendedmembers"),
    path("reactivatemember/<uuid:id>/", reactivatemember, name="reactivatemember"),
    # This is where the loan applications,activation,deletion,dues,views are done
    path("application/", LoanApplication, name="loanapplication"),
    path("loans/activeloans", ActiveLoans, name="loans"),
    path("loans/declined", declinedLoans, name="declinedLoans"),
    path("loans/disburse", disbursement, name="disburse"),
    path("loans/completed", completedLoans, name="completedLoans"),
    path("loans/pending", PendingLoans, name="pendingLoans"),
    # This is where the loan payments are done
    path("whatsapp/", whatsapp, name="whatsapp"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
