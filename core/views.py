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


def cases(request):

    third_div_row = all.find_all("div",{"class":"row"})[2]
    first_div_grid = third_div_row.find_all("div",{"class":"col-md-8"})[0]
    first_div_content = first_div_grid.find_all("div",{"class":"tab-content"})[0]
    first_div_active = first_div_content.find_all("div",{"class":"tab-pane active"})[0]
    first_div_countries = first_div_active.find_all("div",{"class":"main_table_countries_div"})[0]
    first_table = first_div_countries.find_all("table",{"id":"main_table_countries_today"})[0]
    first_table_body = first_table.find_all("tbody")[0]
    country = first_table_body.find_all("tr")


    lst = []
    for item in country:
        data = {}
        data["Country"] = item.find_all("td")[0].text
        data["Total Cases"] = item.find_all("td")[1].text
        data["New Cases"] = item.find_all("td")[2].text
        data["Total Deaths"] = item.find_all("td")[3].text.replace(" ","")
        data["New Deaths"] = item.find_all("td")[4].text
        data["Total Recovered"] = item.find_all("td")[5].text
        data["Active Cases"] = item.find_all("td")[6].text
        data["Serious, Critical"] = item.find_all("td")[7].text
        data["Tot Cases/ 1M pop"] = item.find_all("td")[8].text
        lst.append(data)

#-------------------------------------------------------------------------------

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
    
#-------------------------------------------------------------------------

    total_cases = 0
    for item in lst:
        for key, value in item.items():
            if key == "Total Cases":
                values = int(value.replace(',', ''))
                total_cases += values
                string_total_cases = f"{total_cases:,d}"

    total_new_cases = 0
    for item in lst:
        for key, value in item.items():
            if key == "New Cases":
                try:
                    values = int(value.replace(',', ''))
                except:
                    values = 0
                total_new_cases += values
                string_total_new_cases = f"{total_new_cases:,d}"
    
    total_deaths = 0
    for item in lst:
        for key, value in item.items():
            if key == "Total Deaths":
                try:
                    values = int(value.replace(',', ''))
                except:
                    values = 0
                total_deaths += values
                string_total_deaths = f"{total_deaths:,d}"

    total_new_deaths = 0
    for item in lst:
        for key, value in item.items():
            if key == "New Deaths":
                try:
                    values = int(value.replace(',', ''))
                except:
                    values = 0
                total_new_deaths += values
                string_total_new_deaths = f"{total_new_deaths:,d}"

    total_recovered = 0
    for item in lst:
        for key, value in item.items():
            if key == "Total Recovered":
                try:
                    values = int(value.replace(',', ''))
                except:
                    values = 0
                total_recovered += values
                string_total_recovered = f"{total_recovered:,d}"
    
    total_active_cases = 0
    for item in lst:
        for key, value in item.items():
            if key == "Active Cases":
                try:
                    values = int(value.replace(',', ''))
                except:
                    values = 0
                total_active_cases += values
                string_total_active_cases = f"{total_active_cases:,d}"

    total_critical = 0
    for item in lst:
        for key, value in item.items():
            if key == "Serious, Critical":
                try:
                    values = int(value.replace(',', ''))
                except:
                    values = 0
                total_critical += values
                string_total_critical = f"{total_critical:,d}"

#--------------------------------------------------------------------------------

    context = {'country': lst, 'plain_news_list': plain_news_list, 'string_total_cases': string_total_cases, 'string_total_new_cases': string_total_new_cases, 'string_total_deaths': string_total_deaths,
                'string_total_new_deaths': string_total_new_deaths, 'string_total_recovered': string_total_recovered, 'string_total_critical': string_total_critical,
                'string_total_active_cases': string_total_active_cases}

    return render(request, "dashboard.html", context)

def united_kingdom_cases(request):

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
    
#-------------------------------------------------------------------------

    # url = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/stats"

    # querystring = {"country":"United Kingdom"}

    # headers = {
    #     'x-rapidapi-host': "covid-19-coronavirus-statistics.p.rapidapi.com",
    #     'x-rapidapi-key': "b366e49ea8mshd793e280f2aa844p1f4bc1jsn63e668661ccf"
    #     }

    # response = requests.request("GET", url, headers=headers, params=querystring)

    # data_json = json.loads(response.text)['data']
    # covid_stats = data_json['covid19Stats']
    # last_covid_stats = covid_stats[-1]

    third_div_row = all.find_all("div",{"class":"row"})[2]
    first_div_grid = third_div_row.find_all("div",{"class":"col-md-8"})[0]
    first_div_content = first_div_grid.find_all("div",{"class":"tab-content"})[0]
    first_div_active = first_div_content.find_all("div",{"class":"tab-pane active"})[0]
    first_div_countries = first_div_active.find_all("div",{"class":"main_table_countries_div"})[0]
    first_table = first_div_countries.find_all("table",{"id":"main_table_countries_today"})[0]
    first_table_body = first_table.find_all("tbody")[0]
    country = first_table_body.find_all("tr")


    lst = []
    for item in country:
        data = {}
        data["Country"] = item.find_all("td")[0].text
        data["Total_Cases"] = item.find_all("td")[1].text
        data["New_Cases"] = item.find_all("td")[2].text
        data["Total_Deaths"] = item.find_all("td")[3].text.replace(" ","")
        data["New_Deaths"] = item.find_all("td")[4].text
        data["Total_Recovered"] = item.find_all("td")[5].text
        data["Active_Cases"] = item.find_all("td")[6].text
        data["Critical"] = item.find_all("td")[7].text
        # data["Tot Cases/ 1M pop"] = item.find_all("td")[8].text
        lst.append(data)

    df=pandas.DataFrame(lst)
    uk_value = df[df['Country'] == 'UK']
    uk_total_cases = uk_value.Total_Cases.to_string(index=False)
    uk_total_deaths = uk_value.Total_Deaths.to_string(index=False)
    uk_total_recovered = uk_value.Total_Recovered.to_string(index=False)
    uk_total_critical = uk_value.Critical.to_string(index=False)


#-----------------------------------------------------------------------------------

    r_uk = requests.get("https://www.portsmouth.co.uk/health/coronavirus/coronavirus-full-list-places-covid-19-cases-england-and-how-many-have-tested-positive-uk-so-far-2457616", headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c_uk = r_uk.content

    uk_soup = BeautifulSoup(c_uk,"html.parser")

    uk_all = uk_soup.find_all("div",{"id":"content-wrapper"})[0]

    uk_data = uk_all.find_all("div",{"class":"markup sc-bbkauy leZDRt"})


    uk_list = []
    for count in range(11,160):
        dict_data = {}
        ukdata = uk_data[count].text
        list_data = ukdata.split(': ')

        dict_data["City"] = list_data[0]
        dict_data["Cases"] = list_data[1]
        
        uk_list.append(dict_data)

    context = {'uk_list': uk_list, 'plain_news_list': plain_news_list, 'uk_total_cases': uk_total_cases, 'uk_total_deaths': uk_total_deaths, 'uk_total_recovered': uk_total_recovered, 'uk_total_critical': uk_total_critical}

    return render(request, "united_kingdom_cases.html", context)

def world_map(request):
    return render(request, "world.html")

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def terms_conditions(request):
    return render(request, "terms_conditions.html")