from django.db import models

class CountriesData(models.Model):
    flag = models.CharField(max_length=500, null=True)
    country = models.CharField(max_length=100, null=True)
    cases = models.CharField(max_length=100, null=True)
    today_cases = models.CharField(max_length=100, null=True)
    deaths = models.CharField(max_length=100, null=True)
    today_deaths = models.CharField(max_length=100, null=True)
    recovered = models.CharField(max_length=100, null=True)
    active = models.CharField(max_length=100, null=True)
    critical = models.CharField(max_length=100, null=True)
    tests = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.country
