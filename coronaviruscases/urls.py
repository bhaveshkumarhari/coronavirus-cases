from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import ChartData, ChartDataCountry

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cases, name="home"),
    path('advice-for-public/', views.advice_for_public, name="advice-for-public"),
    path('country/UK/', views.united_kingdom_cases, name="united-kingdom-cases"),
    path('country/USA/', views.usa_cases, name="usa-cases"),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('terms-and-conditions/', views.terms_conditions, name="terms-and-conditions"),

    path('api/chart/data/', ChartData.as_view()),

    path('country/<str:country>/', views.countryView, name="country"),
    path('api/chart/data/country/<str:country>/', ChartDataCountry.as_view()),

    path('country/data/<str:country>/', views.countryWithoutChart, name="country-without-chart"),

]
