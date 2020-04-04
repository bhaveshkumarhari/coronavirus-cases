"""coronaviruscases URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cases, name="home"),
    path('advice-for-public/', views.advice_for_public, name="advice-for-public"),
    path('united-kingdom-cases/', views.united_kingdom_cases, name="united-kingdom-cases"),
    path('usa-cases/', views.usa_cases, name="usa-cases"),
    # path('world/', views.world, name="world"),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('terms-and-conditions/', views.terms_conditions, name="terms-and-conditions"),
]
