"""part3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path

# import url
from django.conf.urls import url

# import views
from RM import views

urlpatterns = [
    path(r'AddIncome2/', views.Add_income2, name='Add_income2'),
    path(r'AddIncome/', views.Add_income, name='Add_income'),
    path(r'AddDeduction/', views.Add_deduction, name='Add_deduction'),
    path(r'AddDeduction2/', views.Add_deduction2, name='Add_deduction2'),
    path('PayStubView', views.PayStubView, name='PayStubView'),
    path('PayStub', views.PayStub, name='PayStub'),
    path('employeeList', views.employee_list, name='employee_list'),
    path('AccCandidateList', views.ACCcandidate_list, name='ACCcandidate_list'),
    path('candidateList', views.candidate_list, name='candidate_list'),
    path('insertCan', views.insert_candidate, name='insert_candidate'),
    path('insertCan/SSN', views.candidate_ssn, name='candidate_ssn'),
    path(r'^admin/', admin.site.urls),
    path('', views.base, name='base'),
    #path('admin/', admin.site.urls),
]
