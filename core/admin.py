from django.contrib import admin

from .models import CountriesData


class CountriesAdmin(admin.ModelAdmin):
    list_display = [
        'country',
        'cases',
        'today_cases',
        'deaths',
        'today_deaths',
        'recovered',
        'active',
        'critical',
        'tests',
    ]

admin.site.register(CountriesData, CountriesAdmin)