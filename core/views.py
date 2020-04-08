from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

import requests
from bs4 import BeautifulSoup

import re
import pandas
import json

User = get_user_model()

r = requests.get("https://www.worldometers.info/coronavirus/")
c = r.content

soup = BeautifulSoup(c,"html.parser")

all = soup.find_all("div",{"class":"container"})[1]

#-------------GET NEWS UPDATES--------------------------------------

fourth = all.find_all("div",{"class":"row"})[3]
first_div_col = fourth.find_all("div",{"class":"col-md-8"})[0]
first_innercontent = first_div_col.find_all("div",{"id":"innercontent"})[0]
first_div_row = first_innercontent.find_all("div",{"class":"row"})[0].text
# news_block = first_div_row.find_all("div",{"class":"news_post"})


news_list = []
news_list = first_div_row.splitlines()

for item in news_list:
    news_list.remove('')

news_list.remove('Latest Updates')
some_news_list = news_list[:50]

plain_news_list = []
for item in some_news_list:
    removed_source = item.replace('[source]','')
    plain_news_list.append(removed_source)

#-------------Live Data of all countries----------------------

url = "https://corona.lmao.ninja/countries"
        
response = requests.request("GET", url)

world_data_json = json.loads(response.text)

def cases(request):

#-----------------New List of dictionaries--------------------

    new_list = []
    for dict_item in world_data_json:
        new_dict = {}
        new_dict['flag'] = dict_item['countryInfo']['flag']
        new_dict['country'] = dict_item['country']
        new_dict['cases'] = dict_item['cases']
        new_dict['todayCases'] = dict_item['todayCases']
        new_dict['deaths'] = dict_item['deaths']
        new_dict['todayDeaths'] = dict_item['todayDeaths']
        new_dict['recovered'] = dict_item['recovered']
        new_dict['active'] = dict_item['active']
        new_dict['critical'] = dict_item['critical']
    
        new_list.append(new_dict)

    now_df=pandas.DataFrame(new_list)

    sorted_now_df = now_df.sort_values(by='cases', ascending=False)

    converted_now_to_list = sorted_now_df.T.to_dict().values()

#-----------------Total Live Data of the world----------------

    url = "https://corona.lmao.ninja/all"
        
    response = requests.request("GET", url)

    total_data_json = json.loads(response.text)

    cases = total_data_json['cases']
    deaths = total_data_json['deaths']
    recovered = total_data_json['recovered']
    critical = total_data_json['critical']

    todayCases = total_data_json['todayCases']
    todayDeaths = total_data_json['todayDeaths']
    active = total_data_json['active']

    #------------------Yesterday's Data---------------------------

    url = "https://corona.lmao.ninja/yesterday"
    
    response = requests.request("GET", url)

    yesterday_data_json = json.loads(response.text)

    yesterday_new_list = []
    for dict_item in yesterday_data_json:
        new_dict = {}
        new_dict['flag'] = dict_item['countryInfo']['flag']
        new_dict['country'] = dict_item['country']
        new_dict['cases'] = dict_item['cases']
        new_dict['todayCases'] = dict_item['todayCases']
        new_dict['deaths'] = dict_item['deaths']
        new_dict['todayDeaths'] = dict_item['todayDeaths']
        new_dict['recovered'] = dict_item['recovered']
        new_dict['active'] = dict_item['active']
        new_dict['critical'] = dict_item['critical']
    
        yesterday_new_list.append(new_dict)

    yesterday_df=pandas.DataFrame(yesterday_new_list)

    yesterday_sorted_df = yesterday_df.sort_values(by='cases', ascending=False)

    yesterday_converted_to_list = yesterday_sorted_df.T.to_dict().values()


    total_cases = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "cases":
                total_cases += value

    total_todayCases = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "todayCases":
                total_todayCases += value

    total_deaths = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "deaths":
                total_deaths += value

    total_todayDeaths = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "todayDeaths":
                total_todayDeaths += value

    total_recovered = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "recovered":
                total_recovered += value

    total_active = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "active":
                total_active += value
    
    total_critical = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "critical":
                total_critical += value

    context = {'country': converted_now_to_list, 'plain_news_list': plain_news_list, 'cases': cases,
                'deaths': deaths, 'recovered': recovered, 'critical': critical,
                'todayCases': todayCases, 'todayDeaths': todayDeaths, 'active': active,
                'yesterday_data':yesterday_converted_to_list, 'total_cases':total_cases, 'total_todayCases':total_todayCases, 
                'total_deaths':total_deaths, 'total_todayDeaths':total_todayDeaths, 'total_recovered':total_recovered, 'total_active':total_active, 
                'total_critical':total_critical}

    return render(request, "dashboard.html", context)

def united_kingdom_cases(request):
    
#------------------UK Flag----------------------------------------

    for dict_item in world_data_json:
        new_dict = {}
        if dict_item['country'] == 'UK':
            new_dict['flag'] = dict_item['countryInfo']['flag']
            uk_flag = new_dict.get('flag')

#------------------UK data from world cases API-------------------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('UK')

#-----------------------UK Cities Cases------------------------------------

    r_uk = requests.get("https://www.portsmouth.co.uk/health/coronavirus/coronavirus-full-list-places-covid-19-cases-england-and-how-many-have-tested-positive-uk-so-far-2457616", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c_uk = r_uk.content

    uk_soup = BeautifulSoup(c_uk,"html.parser")

    uk_all = uk_soup.find_all("div",{"id":"content-wrapper"})[0]

    uk_data = uk_all.find_all("div",{"class":"markup sc-bbkauy leZDRt"})


    uk_list = []
    for count in range(11,160):
        dict_data = {}
        ukdata = uk_data[count].text
        
        # Separate two values and create list
        list_data = ukdata.split(': ')

        # Create dictionary with key and value
        dict_data["City"] = list_data[0]
        dict_data["Cases"] = list_data[1]
        
        # Create list of dictionary
        uk_list.append(dict_data)

#---------------------------------------------------------------------------

    context = {'uk_flag': uk_flag, 'uk_list': uk_list, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 
            'country_total_deaths': country_total_deaths, 'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "united_kingdom_cases.html", context)

def usa_cases(request):

    url = "https://corona.lmao.ninja/states"
    
    response = requests.request("GET", url)

    states_data_json = json.loads(response.text)

#---------------GET USA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('USA')

#-----------------------------------------------------------------

    context = {'states': states_data_json, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "usa_cases.html", context)

def advice_for_public(request):

    context = {'plain_news_list': plain_news_list}

    return render(request, "advice_for_public.html", context)

def privacy_policy(request):

    context = {'plain_news_list': plain_news_list}

    return render(request, "privacy_policy.html", context)

def terms_conditions(request):

    context = {'plain_news_list': plain_news_list}

    return render(request, "terms_conditions.html", context)

# class world(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'world.html')

class ChartData(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        url = "https://corona.lmao.ninja/v2/historical/all"
                
        response = requests.request("GET", url)

        world_data_json = json.loads(response.text)

        cases_date =[]
        confirmed_cases = []
        cases_dict = world_data_json['cases']
        for key, value in cases_dict.items():
            cases_date.append(key)
            confirmed_cases.append(value)

        deaths_date =[]
        deaths = []
        cases_dict = world_data_json['deaths']
        for key, value in cases_dict.items():
            deaths_date.append(key)
            deaths.append(value)

        recovered_date =[]
        recovered = []
        cases_dict = world_data_json['recovered']
        for key, value in cases_dict.items():
            recovered_date.append(key)
            recovered.append(value)

        # labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        # default_items = [234, 134, 133, 32, 34, 5]

        data = {
            "cases_date": cases_date,
            "confirmed_cases": confirmed_cases,
            "deaths_date": deaths_date,
            "deaths": deaths,
            "recovered_date": recovered_date,
            "recovered": recovered,
            
        }
        return Response(data)

def get_country_data(country):

    url = "https://pomber.github.io/covid19/timeseries.json"
    
    response = requests.request("GET", url)

    data_json = json.loads(response.text)

    cases_dates = []
    cases = []
    deaths = []
    recovered = []
    for key, value in data_json.items():
        if key == country:
            counts = len(value)
            for count in range(counts):
                cases_dates.append(value[count]['date'])
                cases.append(value[count]['confirmed'])
                deaths.append(value[count]['deaths'])
                recovered.append(value[count]['recovered'])

    return cases_dates, cases, deaths, recovered

class ChartDataCountry(APIView):

    authentication_classes = []
    permission_classes = []

    def get_values(self, *args, **kwargs):
        global cases_dates, cases, deaths, recovered
        cases_dates = args[0]
        cases = args[1]
        deaths = args[2]
        recovered = args[3]

    def get(self, request, format=None):
          
        data = {
            "cases_dates": cases_dates,
            "cases": cases,
            "deaths": deaths, 
            "recovered": recovered,
        }
        return Response(data)


def get_specific_country_data(country):

    df=pandas.DataFrame(world_data_json)

    # Filter table with specific value
    country_value = df[df['country'] == country]

    # Convert to string without index value
    country_total_cases = country_value.cases.to_string(index=False)
    country_total_deaths = country_value.deaths.to_string(index=False)
    country_total_recovered = country_value.recovered.to_string(index=False)
    country_total_critical = country_value.critical.to_string(index=False)

    return country_total_cases, country_total_deaths, country_total_recovered, country_total_critical


def india_cases(request):

#---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('India')


#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    cases_dates, cases, deaths, recovered = get_country_data('India')

    api_obj = ChartDataCountry()
    api_obj.get_values(cases_dates, cases, deaths, recovered)

#-----------------------------------------------------------------

    context = {'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "india_cases.html", context)

def spain_cases(request):

#---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('Spain')

#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    cases_dates, cases, deaths, recovered = get_country_data('Spain')

    api_obj = ChartDataCountry()
    api_obj.get_values(cases_dates, cases, deaths, recovered)

#-----------------------------------------------------------------

    context = {'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "spain_cases.html", context)

def italy_cases(request):

#---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('Italy')

#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    cases_dates, cases, deaths, recovered = get_country_data('Italy')

    api_obj = ChartDataCountry()
    api_obj.get_values(cases_dates, cases, deaths, recovered)

#-----------------------------------------------------------------------

    context = {'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "italy_cases.html", context)


def germany_cases(request):

#---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('Germany')

#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    cases_dates, cases, deaths, recovered = get_country_data('Germany')

    api_obj = ChartDataCountry()
    api_obj.get_values(cases_dates, cases, deaths, recovered)

#-----------------------------------------------------------------------

    context = {'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "germany_cases.html", context)

def france_cases(request):

#---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('France')

#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    cases_dates, cases, deaths, recovered = get_country_data('France')

    api_obj = ChartDataCountry()
    api_obj.get_values(cases_dates, cases, deaths, recovered)

#-----------------------------------------------------------------------

    context = {'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "france_cases.html", context)