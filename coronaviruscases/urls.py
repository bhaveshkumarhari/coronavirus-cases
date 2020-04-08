from django.contrib import admin
from django.urls import path, include
from core import views
from core.views import ChartData, ChartDataCountry

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.cases, name="home"),
    path('advice-for-public/', views.advice_for_public, name="advice-for-public"),
    path('united-kingdom-cases/', views.united_kingdom_cases, name="united-kingdom-cases"),
    path('usa-cases/', views.usa_cases, name="usa-cases"),
    path('privacy-policy/', views.privacy_policy, name="privacy-policy"),
    path('terms-and-conditions/', views.terms_conditions, name="terms-and-conditions"),
    # path('world/', world.as_view(), name="world"),
    path('api/chart/data/', ChartData.as_view()),

    path('india-cases/', views.india_cases, name="india-cases"),
    path('api/chart/data/country/', ChartDataCountry.as_view()),

    path('spain-cases/', views.spain_cases, name="spain-cases"),
    path('italy-cases/', views.italy_cases, name="italy-cases"),
    path('germany-cases/', views.germany_cases, name="germany-cases"),
    path('france-cases/', views.france_cases, name="france-cases"),

]
