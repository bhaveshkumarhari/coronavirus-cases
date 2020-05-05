from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import View, TemplateView
from django.http import JsonResponse

from django.http import HttpResponseRedirect

from .forms import ContactForm

from django.contrib.staticfiles.storage import staticfiles_storage

from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import get_user_model

import requests
from bs4 import BeautifulSoup

import re
import pandas
import json

from . import plots

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

news_list.remove('Latest News')
some_news_list = news_list[:50]

plain_news_list = []
for item in some_news_list:
    removed_source = item.replace('[source]','')
    plain_news_list.append(removed_source)

# Remove empty string from list
plain_news_list = [i for i in plain_news_list if i]

#-------------Live Data of all countries----------------------

url = "https://corona.lmao.ninja/v2/countries"
        
response = requests.request("GET", url)

world_data_json = json.loads(response.text)


#-----------------Total Live Data of the world----------------

url = "https://corona.lmao.ninja/v2/all"
    
response = requests.request("GET", url)

total_data_json = json.loads(response.text)

#--------------FOR GLOBAL TRACKER AND BAR CHART--------------

now_confirmed_cases = total_data_json['cases']
now_total_deaths = total_data_json['deaths']
now_total_recovered = total_data_json['recovered']
now_total_critical = total_data_json['critical']

now_todayCases = total_data_json['todayCases']
now_todayDeaths = total_data_json['todayDeaths']
now_total_active = total_data_json['active']
now_total_tests = total_data_json['tests']

global_bar_chart = []

global_bar_chart.append(now_confirmed_cases)
global_bar_chart.append(now_total_deaths)
global_bar_chart.append(now_total_recovered)
global_bar_chart.append(now_total_critical)
global_bar_chart.append(now_total_active)


def get_flag(country):

    url = "https://corona.lmao.ninja/v2/countries"
        
    response = requests.request("GET", url)

    world_data_json = json.loads(response.text)

    new_list = []
    for dict_item in world_data_json:
        new_dict = {}
        new_dict['flag'] = dict_item['countryInfo']['flag']
        new_dict['country'] = dict_item['country']

        new_list.append(new_dict)

    for dictl in new_list:
        if dictl['country'] == country:
            return dictl['flag']



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
        new_dict['tests'] = dict_item['tests']
    
        new_list.append(new_dict)

    now_df=pandas.DataFrame(new_list)

    sorted_now_df = now_df.sort_values(by='cases', ascending=False)

    converted_now_to_list = sorted_now_df.T.to_dict().values()


    #------------------Yesterday's Data---------------------------

    url = "https://corona.lmao.ninja/v2/countries?yesterday=true"
    
    response = requests.request("GET", url)

    yesterday_data_json = json.loads(response.text)

    # print(yesterday_data_json)

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
        new_dict['tests'] = dict_item['tests']
    
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

    total_tests = 0
    for item in yesterday_data_json:
        for key, value in item.items():
            if key == "tests":
                total_tests += value
            
    #--------FOR MAP PLOTS---------------------------

    plot = plots.plotworld()

    context = {'plot': plot, 'country': converted_now_to_list, 'plain_news_list': plain_news_list, 'cases': now_confirmed_cases,
                'deaths': now_total_deaths, 'recovered': now_total_recovered, 'critical': now_total_critical,
                'todayCases': now_todayCases, 'todayDeaths': now_todayDeaths, 'active': now_total_active, 'tests': now_total_tests,
                'yesterday_data':yesterday_converted_to_list, 'total_cases':total_cases, 'total_todayCases':total_todayCases, 
                'total_deaths':total_deaths, 'total_todayDeaths':total_todayDeaths, 'total_recovered':total_recovered, 'total_active':total_active, 
                'total_critical':total_critical, 'total_tests':total_tests}

    return render(request, "dashboard.html", context)

def united_kingdom_cases(request):
    
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

#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    country, cases_dates, cases, deaths, recovered = get_country_data("United Kingdom")

    api_obj = ChartDataCountry()
    api_obj.get_values(country, cases_dates, cases, deaths, recovered, country_total_cases, country_total_deaths, country_total_recovered)

#---------------------------------------------------------------------------

    context = {'country': "United Kingdom", 'uk_list': uk_list, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 
            'country_total_deaths': country_total_deaths, 'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "united_kingdom_cases.html", context)

def usa_cases(request):

    url = "https://corona.lmao.ninja/v2/states"
    
    response = requests.request("GET", url)

    states_data_json = json.loads(response.text)

#---------------GET USA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('USA')

#--------FOR MAP PLOTS---------------------------

    plot = plots.plot1d()

#---------------GET COUNTRY CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('USA')

#-------------GET COUNTRY DATA FOR LINE CHARTS--------------------------------

    country, cases_dates, cases, deaths, recovered = get_country_data('US')

    chart_available = True
    if cases_dates == []:
        chart_available = False

    api_obj = ChartDataCountry()
    api_obj.get_values(country, cases_dates, cases, deaths, recovered, country_total_cases, country_total_deaths, country_total_recovered)


    context = {'plot': plot, 'states': states_data_json, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
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

        labels = ['Confirmed cases', 'Deaths', 'Recovered', 'Critical', 'Active']

        # labels = ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange']
        # default_items = [234, 134, 133, 32, 34, 5]


        data = {
            "cases_date": cases_date,
            "confirmed_cases": confirmed_cases,
            "deaths_date": deaths_date,
            "deaths": deaths,
            "recovered_date": recovered_date,
            "recovered": recovered,

            "global_bar_chart": global_bar_chart,
            "labels": labels,
            
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

    # print(cases_dates)

    return country, cases_dates, cases, deaths, recovered

class ChartDataCountry(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get_values(self, *args, **kwargs):
        global labels, bar_chart_data, country, cases_dates, cases, deaths, recovered, country_total_cases, country_total_deaths, country_total_recovered
        country = args[0]
        cases_dates = args[1]
        cases = args[2]
        deaths = args[3]
        recovered = args[4]

        labels = ["Confirmed Cases", "Deaths", "Recovered"]
        bar_chart_data = []
        country_total_cases = args[5]
        country_total_deaths = args[6]
        country_total_recovered = args[7]

        bar_chart_data.append(int(country_total_cases.replace(' ','')))
        bar_chart_data.append(int(country_total_deaths.replace(' ','')))
        bar_chart_data.append(int(country_total_recovered.replace(' ','')))

    def get(self, request, format=None, *args, **kwargs):
          
        data = {
            "country" : country,
            "cases_dates": cases_dates,
            "cases": cases,
            "deaths": deaths, 
            "recovered": recovered,

            "labels": labels,
            "bar_chart_data": bar_chart_data, 
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


def countryView(request, country):

    country_flag = get_flag(country)

    country_bar = country
    country_line = country

    if country_line == "UK":
        country_line = "United Kingdom"

    if country_line == "USA":
        country_line = "US"

#---------------GET COUNTRY CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data(country_bar)

#-------------GET COUNTRY DATA FOR LINE CHARTS--------------------------------

    country, cases_dates, cases, deaths, recovered = get_country_data(country_line)

    chart_available = True
    if cases_dates == []:
        chart_available = False

    api_obj = ChartDataCountry()
    api_obj.get_values(country, cases_dates, cases, deaths, recovered, country_total_cases, country_total_deaths, country_total_recovered)

#-----------------------------------------------------------------

    context = {'country_flag':country_flag, 'chart_available': chart_available, 'country': country, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "country_cases.html", context)
    

class ChartDataCompareCountry(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get_values(self, *args, **kwargs):
        global country1, cases_dates1, cases1, deaths1, recovered1, country2, cases_dates2, cases2, deaths2, recovered2
        global labels, country_bar_chart1, country_bar_chart2
        
        country1 = args[0]
        cases_dates1 = args[1]
        cases1 = args[2]
        deaths1 = args[3]
        recovered1 = args[4]

        country2 = args[5]
        cases_dates2 = args[6]
        cases2 = args[7]
        deaths2 = args[8]
        recovered2 = args[9]


        country_total_cases1 = args[10]
        country_total_deaths1 = args[11]
        country_total_recovered1 = args[12]
        country_total_critical1 = args[13]

        country_bar_chart1 = []
        country_bar_chart1.append(country_total_cases1)
        country_bar_chart1.append(country_total_deaths1)
        country_bar_chart1.append(country_total_recovered1)
        country_bar_chart1.append(country_total_critical1)

        country_total_cases2 = args[14]
        country_total_deaths2 = args[15]
        country_total_recovered2 = args[16]
        country_total_critical2 = args[17]

        country_bar_chart2 = []
        country_bar_chart2.append(country_total_cases2)
        country_bar_chart2.append(country_total_deaths2)
        country_bar_chart2.append(country_total_recovered2)
        country_bar_chart2.append(country_total_critical2)

        labels = ["Confirmed Cases", "Deaths", "Recovered", "Critical"]

    def get(self, request, format=None, *args, **kwargs):
          
        data = {
            "country1" : country1,
            "cases_dates1": cases_dates1,
            "cases1": cases1,
            "deaths1": deaths1, 
            "recovered1": recovered1,

            "country2" : country2,
            "cases_dates2": cases_dates2,
            "cases2": cases2,
            "deaths2": deaths2, 
            "recovered2": recovered2,

            "labels": labels,
            "country_bar_chart1": country_bar_chart1, 
            "country_bar_chart2": country_bar_chart2,
        }
        return Response(data)


class compareCountriesView(View):

    def get(self, *args, **kwargs):

        country1 = 'Afghanistan'
        country2 = 'Afghanistan'

        url = "https://pomber.github.io/covid19/timeseries.json"
            
        response = requests.request("GET", url)
        dict_data = json.loads(response.text)

        #------------GET FLAG---------------------------
        country1_flag = get_flag(country1)
        country2_flag = get_flag(country2)

        #---------------GET COUNTRY CONTENTS FROM COUNTRY API--------------------

        country_total_cases1, country_total_deaths1, country_total_recovered1, country_total_critical1 = get_specific_country_data(country1)
        country_total_cases2, country_total_deaths2, country_total_recovered2, country_total_critical2 = get_specific_country_data(country2)

        #-------------GET COUNTRY DATA FOR CHARTS--------------------------------
        

        country1, cases_dates1, cases1, deaths1, recovered1 = get_country_data(country1)

        country2, cases_dates2, cases2, deaths2, recovered2 = get_country_data(country2)


        compare_api_obj = ChartDataCompareCountry()
        compare_api_obj.get_values(country1, cases_dates1, cases1, deaths1, recovered1, country2, cases_dates2, cases2, deaths2, recovered2,
                                country_total_cases1, country_total_deaths1, country_total_recovered1, country_total_critical1, country_total_cases2, country_total_deaths2, country_total_recovered2, country_total_critical2)

        #----------------------------------------------------------------------

        context = {'dict_data':dict_data, 'country1': country1, 'country2': country2, 'country1_flag': country1_flag, 'country2_flag': country2_flag, 'plain_news_list': plain_news_list, 'country_total_cases1': country_total_cases1, 'country_total_deaths1': country_total_deaths1,
                'country_total_recovered1': country_total_recovered1, 'country_total_critical1': country_total_critical1, 'country_total_cases2': country_total_cases2, 'country_total_deaths2': country_total_deaths2,
                'country_total_recovered2': country_total_recovered2, 'country_total_critical2': country_total_critical2}

        return render(self.request, "compare_countries.html", context)
    
    def post(self, *args, **kwargs):

        url = "https://pomber.github.io/covid19/timeseries.json"
            
        response = requests.request("GET", url)
        dict_data = json.loads(response.text)

        form = ContactForm(self.request.POST or None)
        # print(self.request.POST)

        if form.is_valid():
            country1 = form.cleaned_data.get('country1')
            country2 = form.cleaned_data.get('country2')

            country1_bar = country1
            country2_bar = country2

            if country1_bar == "United Kingdom":
                country1_bar = "UK"

            if country1_bar == "US":
                country1_bar = "USA"

            if country2_bar == "United Kingdom":
                country2_bar = "UK"

            if country2_bar == "US":
                country2_bar = "USA"

            #------------GET FLAG--------------------
            country1_flag = get_flag(country1_bar)
            country2_flag = get_flag(country2_bar)

            country1_chart = country1
            country2_chart = country2

            #---------------GET COUNTRY CONTENTS FROM COUNTRY API--------------------

            country_total_cases1, country_total_deaths1, country_total_recovered1, country_total_critical1 = get_specific_country_data(country1_bar)
            country_total_cases2, country_total_deaths2, country_total_recovered2, country_total_critical2 = get_specific_country_data(country2_bar)

            #-------------GET COUNTRY DATA FOR CHARTS--------------------------------
        

            country1, cases_dates1, cases1, deaths1, recovered1 = get_country_data(country1_chart)
            country2, cases_dates2, cases2, deaths2, recovered2 = get_country_data(country2_chart)


            compare_api_obj = ChartDataCompareCountry()
            compare_api_obj.get_values(country1, cases_dates1, cases1, deaths1, recovered1, country2, cases_dates2, cases2, deaths2, recovered2,
                                country_total_cases1, country_total_deaths1, country_total_recovered1, country_total_critical1, country_total_cases2, country_total_deaths2, country_total_recovered2, country_total_critical2)


            context = {'dict_data':dict_data, 'country1': country1, 'country2': country2, 'country1_flag': country1_flag, 'country2_flag': country2_flag, 'plain_news_list': plain_news_list, 'country_total_cases1': country_total_cases1, 'country_total_deaths1': country_total_deaths1,
                    'country_total_recovered1': country_total_recovered1, 'country_total_critical1': country_total_critical1, 'country_total_cases2': country_total_cases2, 'country_total_deaths2': country_total_deaths2,
                    'country_total_recovered2': country_total_recovered2, 'country_total_critical2': country_total_critical2}

            return render(self.request, "compare_countries.html", context)

        
class Plot1DView(TemplateView):
    template_name = "worldmap.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(Plot1DView, self).get_context_data(**kwargs)
        context['plot'] = plots.plotworld()
        return context

    #--------FOR MAP PLOTS---------------------------

def worldmap(request):

    plot = plots.plotworld()

    context = {'plot': plot, 'plain_news_list': plain_news_list, 'cases': now_confirmed_cases,
                'deaths': now_total_deaths, 'recovered': now_total_recovered, 'critical': now_total_critical,
                'todayCases': now_todayCases, 'todayDeaths': now_todayDeaths, 'active': now_total_active, 'tests': now_total_tests}

    return render(request, "worldmap.html", context)

def india_cases(request):

    url = "http://covid19-india-adhikansh.herokuapp.com/states"
        
    response = requests.request("GET", url)

    data_json = json.loads(response.text)

    df=pandas.DataFrame(data_json['state'])

    converted_to_list = df.T.to_dict().values()

    # total_cases = 0
    # for item in converted_to_list:
    #     for key, value in item.items():
    #         if key == "total":
    #             total_cases += value

    # print(total_cases)

    #---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data('India')

    context = {'df': converted_to_list, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "india_cases.html", context)