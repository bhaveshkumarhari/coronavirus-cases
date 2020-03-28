from django.shortcuts import render

import requests
from bs4 import BeautifulSoup

import re

def cases(request):

    r = requests.get("https://www.worldometers.info/coronavirus/")
    c = r.content

    soup = BeautifulSoup(c,"html.parser")

    all = soup.find_all("div",{"class":"container"})[1]

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
    some_news_list = news_list[:25]

    plain_news_list = []
    for item in some_news_list:
        removed_source = item.replace('[source]','')
        plain_news_list.append(removed_source)
    

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

    context = {'country': lst, 'plain_news_list': plain_news_list, 'string_total_cases': string_total_cases, 'string_total_new_cases': string_total_new_cases, 'string_total_deaths': string_total_deaths,
                'string_total_new_deaths': string_total_new_deaths, 'string_total_recovered': string_total_recovered, 'string_total_critical': string_total_critical,
                'string_total_active_cases': string_total_active_cases}

    return render(request, "dashboard.html", context)

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def terms_conditions(request):
    return render(request, "terms_conditions.html")

def terms_conditions(request):

    import requests
    from bs4 import BeautifulSoup

    r = requests.get("https://www.worldometers.info/coronavirus/")
    c = r.content

    soup = BeautifulSoup(c,"html.parser")

    all = soup.find_all("div",{"class":"container"})[1]
    fourth = all.find_all("div",{"class":"row"})[3]
    first_div_col = fourth.find_all("div",{"class":"col-md-8"})[0]
    first_innercontent = first_div_col.find_all("div",{"id":"innercontent"})[0]
    first_div_row = first_innercontent.find_all("div",{"class":"row"})[0]
    news_block = first_div_row.find_all("div",{"class":"news_post"})

    news_list = []
    for item in news_block:
        news_data = {}
        news_data["News"] = news_block.text

        news_list.append(news_data)

    print(news_list)

    return render(request, "dashboard.html")