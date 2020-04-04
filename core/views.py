from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

import re
import pandas
import json

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

#--------------------------------------------------------------

url = "https://corona.lmao.ninja/countries"
        
response = requests.request("GET", url)

world_data_json = json.loads(response.text)

#-------------------------------------------------------------------------

def cases(request):

    # total_cases = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "cases":
    #             total_cases += value
    #             string_total_cases = f"{total_cases:,d}"

    # total_new_cases = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "todayCases":
    #             total_new_cases += value
    #             string_total_new_cases = f"{total_new_cases:,d}"
    
    # total_deaths = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "deaths":
    #             total_deaths += value
    #             string_total_deaths = f"{total_deaths:,d}"

    # total_new_deaths = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "todayDeaths":
    #             total_new_deaths += value
    #             string_total_new_deaths = f"{total_new_deaths:,d}"

    # total_recovered = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "recovered":
    #             total_recovered += value
    #             string_total_recovered = f"{total_recovered:,d}"
    
    # total_active_cases = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "active":
    #             total_active_cases += value
    #             string_total_active_cases = f"{total_active_cases:,d}"

    # total_critical = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "critical":
    #             total_critical += value
    #             string_total_critical = f"{total_critical:,d}"

            
    # total_casesPerOneMillion = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "casesPerOneMillion":
    #             try:
    #                 float_value = float(value)
    #             except:
    #                 float_value = 0.0
    #             total_casesPerOneMillion += float_value
                # print(type(float_value))
                    
                # string_total_casesPerOneMillion = f"{total_casesPerOneMillion:,d}"

    # total_casesPerOneMillion = 0
    # for item in world_data_json:
    #     for key, value in item.items():
    #         if key == "deathsPerOneMillion":
    #             total_casesPerOneMillion += float(value)
    #             string_total_casesPerOneMillion = f"{total_casesPerOneMillion:,d}"

    df=pandas.DataFrame(world_data_json)

    # Filter table with specific value
    world_value = df[df['country'] == 'World']

    # Convert to string without index value
    world_total_cases = world_value.cases.to_string(index=False)
    world_total_deaths = world_value.deaths.to_string(index=False)
    world_total_recovered = world_value.recovered.to_string(index=False)
    world_total_critical = world_value.critical.to_string(index=False)

    world_total_todayCases = world_value.todayCases.to_string(index=False)
    world_total_todayDeaths = world_value.todayDeaths.to_string(index=False)
    world_total_active = world_value.active.to_string(index=False)

    context = {'country': world_data_json, 'plain_news_list': plain_news_list, 'world_total_cases': world_total_cases, 'world_total_deaths': world_total_deaths, 'world_total_recovered': world_total_recovered, 
    'world_total_critical': world_total_critical,'world_total_todayCases':world_total_todayCases, 'world_total_todayDeaths': world_total_todayDeaths, 'world_total_active':world_total_active}

    return render(request, "dashboard.html", context)

def united_kingdom_cases(request):
    
#------------------UK data from world cases API-------------------------------

    df=pandas.DataFrame(world_data_json)

    # Filter table with specific value
    uk_value = df[df['country'] == 'UK']

    # Convert to string without index value
    uk_total_cases = uk_value.cases.to_string(index=False)
    uk_total_deaths = uk_value.deaths.to_string(index=False)
    uk_total_recovered = uk_value.recovered.to_string(index=False)
    uk_total_critical = uk_value.critical.to_string(index=False)


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

    context = {'uk_list': uk_list, 'plain_news_list': plain_news_list, 'uk_total_cases': uk_total_cases, 'uk_total_deaths': uk_total_deaths, 'uk_total_recovered': uk_total_recovered, 'uk_total_critical': uk_total_critical}

    return render(request, "united_kingdom_cases.html", context)

def usa_cases(request):

    url = "https://corona.lmao.ninja/states"
    
    response = requests.request("GET", url)

    states_data_json = json.loads(response.text)

#---------------GET USA CONTENTS FROM COUNTRY API--------------------

    df=pandas.DataFrame(world_data_json)

    # Filter table with specific value
    usa_value = df[df['country'] == 'USA']

    # Convert to string without index value
    usa_total_cases = usa_value.cases.to_string(index=False)
    usa_total_deaths = usa_value.deaths.to_string(index=False)
    usa_total_recovered = usa_value.recovered.to_string(index=False)
    usa_total_critical = usa_value.critical.to_string(index=False)

#-----------------------------------------------------------------

    context = {'states': states_data_json, 'plain_news_list': plain_news_list, 'usa_total_cases': usa_total_cases, 'usa_total_deaths': usa_total_deaths, 'usa_total_recovered': usa_total_recovered, 'usa_total_critical': usa_total_critical}

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