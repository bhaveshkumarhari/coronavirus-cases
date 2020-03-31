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

    url = "https://corona.lmao.ninja/countries"
        
    response = requests.request("GET", url)

    data_json = json.loads(response.text)

    #-------------------------------------------------------------------------

    total_cases = 0
    for item in data_json:
        for key, value in item.items():
            if key == "cases":
                # values = int(value.replace(',', ''))
                total_cases += value
                string_total_cases = f"{total_cases:,d}" # TODO: Use HUMANIZE

    total_new_cases = 0
    for item in data_json:
        for key, value in item.items():
            if key == "todayCases":
                # try:
                #     values = int(value.replace(',', ''))
                # except:
                #     pass
                total_new_cases += value
                string_total_new_cases = f"{total_new_cases:,d}"
    
    total_deaths = 0
    for item in data_json:
        for key, value in item.items():
            if key == "deaths":
                # try:
                #     values = int(value.replace(',', ''))
                # except:
                #     pass
                total_deaths += value
                string_total_deaths = f"{total_deaths:,d}"

    total_new_deaths = 0
    for item in data_json:
        for key, value in item.items():
            if key == "todayDeaths":
                # try:
                #     values = int(value.replace(',', ''))
                # except:
                #     pass
                total_new_deaths += value
                string_total_new_deaths = f"{total_new_deaths:,d}"

    total_recovered = 0
    for item in data_json:
        for key, value in item.items():
            if key == "recovered":
                # try:
                #     values = int(value.replace(',', ''))
                # except:
                #     pass
                total_recovered += value
                string_total_recovered = f"{total_recovered:,d}"
    
    total_active_cases = 0
    for item in data_json:
        for key, value in item.items():
            if key == "active":
                # try:
                #     values = int(value.replace(',', ''))
                # except:
                #     pass
                total_active_cases += value
                string_total_active_cases = f"{total_active_cases:,d}"

    total_critical = 0
    for item in data_json:
        for key, value in item.items():
            if key == "critical":
                # try:
                #     values = int(value.replace(',', ''))
                # except:
                #     pass
                total_critical += value
                string_total_critical = f"{total_critical:,d}"

#--------------------------------------------------------------------------------

    # third_div_row = all.find_all("div",{"class":"row"})[2]
    # first_div_grid = third_div_row.find_all("div",{"class":"col-md-8"})[0]
    # first_div_content = first_div_grid.find_all("div",{"class":"tab-content"})[0]
    # first_div_active = first_div_content.find_all("div",{"class":"tab-pane active"})[0]
    # first_div_countries = first_div_active.find_all("div",{"class":"main_table_countries_div"})[0]
    # first_table = first_div_countries.find_all("table",{"id":"main_table_countries_today"})[0]
    # first_table_body = first_table.find_all("tbody")[0]
    # country = first_table_body.find_all("tr")


    # lst = []
    # for item in country:
    #     data = {}
    #     data["Country"] = item.find_all("td")[0].text
    #     data["Total Cases"] = item.find_all("td")[1].text
    #     data["New Cases"] = item.find_all("td")[2].text
    #     data["Total Deaths"] = item.find_all("td")[3].text.replace(" ","")
    #     data["New Deaths"] = item.find_all("td")[4].text
    #     data["Total Recovered"] = item.find_all("td")[5].text
    #     data["Active Cases"] = item.find_all("td")[6].text
    #     data["Serious, Critical"] = item.find_all("td")[7].text
    #     data["Tot Cases/ 1M pop"] = item.find_all("td")[8].text
    #     lst.append(data)

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
    


    context = {'country': data_json, 'plain_news_list': plain_news_list, 'string_total_cases': string_total_cases, 'string_total_new_cases': string_total_new_cases, 'string_total_deaths': string_total_deaths,
                'string_total_new_deaths': string_total_new_deaths, 'string_total_recovered': string_total_recovered, 'string_total_critical': string_total_critical,
                'string_total_active_cases': string_total_active_cases}

    return render(request, "dashboard.html", context)

def united_kingdom_cases(request):

#----------------GET NEWS UPDATES---------------------------------------

    fourth = all.find_all("div",{"class":"row"})[3]
    first_div_col = fourth.find_all("div",{"class":"col-md-8"})[0]
    first_innercontent = first_div_col.find_all("div",{"id":"innercontent"})[0]
    first_div_row = first_innercontent.find_all("div",{"class":"row"})[0].text
    # news_block = first_div_row.find_all("div",{"class":"news_post"})

    news_list = []
    news_list = first_div_row.splitlines() #Separate every sentence and add to list

    for item in news_list:
        news_list.remove('') #Remove blank values from list
    
    news_list.remove('Latest Updates')
    some_news_list = news_list[:50] #Get first 50 news list

    plain_news_list = []
    for item in some_news_list:
        removed_source = item.replace('[source]','') #Remove word contains in sentence
        plain_news_list.append(removed_source)
    
#-------------------------------------------------------------------------

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

    # Filter table with specific value
    uk_value = df[df['Country'] == 'UK']

    # Convert to string without index value
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
        
        # Separate two values and create list
        list_data = ukdata.split(': ')

        # Create dictionary with key and value
        dict_data["City"] = list_data[0]
        dict_data["Cases"] = list_data[1]
        
        # Create list of dictionary
        uk_list.append(dict_data)

    context = {'uk_list': uk_list, 'plain_news_list': plain_news_list, 'uk_total_cases': uk_total_cases, 'uk_total_deaths': uk_total_deaths, 'uk_total_recovered': uk_total_recovered, 'uk_total_critical': uk_total_critical}

    return render(request, "united_kingdom_cases.html", context)

# def world_map(request):
#     return render(request, "world.html")

#------------------------------------------------------------------------------------------------

def usa_cases(request):

    url = "https://corona.lmao.ninja/states"
    
    response = requests.request("GET", url)

    data_json = json.loads(response.text)

#-------------GET NEWS UPDATES----------------------------------

    fourth = all.find_all("div",{"class":"row"})[3]
    first_div_col = fourth.find_all("div",{"class":"col-md-8"})[0]
    first_innercontent = first_div_col.find_all("div",{"id":"innercontent"})[0]
    first_div_row = first_innercontent.find_all("div",{"class":"row"})[0].text
    # news_block = first_div_row.find_all("div",{"class":"news_post"})

    news_list = []
    news_list = first_div_row.splitlines() #Separate every sentence and add to list

    for item in news_list:
        news_list.remove('') #Remove blank values from list
    
    news_list.remove('Latest Updates')
    some_news_list = news_list[:50] #Get first 50 news list

    plain_news_list = []
    for item in some_news_list:
        removed_source = item.replace('[source]','') #Remove word contains in sentence
        plain_news_list.append(removed_source)

#---------------GET USA CONTENTS FROM COUNTRY API--------------------

    url = "https://corona.lmao.ninja/countries"
        
    response = requests.request("GET", url)

    country_data_json = json.loads(response.text)

    df=pandas.DataFrame(country_data_json)

    # Filter table with specific value
    usa_value = df[df['country'] == 'USA']

    # Convert to string without index value
    usa_total_cases = usa_value.cases.to_string(index=False)
    usa_total_deaths = usa_value.deaths.to_string(index=False)
    usa_total_recovered = usa_value.recovered.to_string(index=False)
    usa_total_critical = usa_value.critical.to_string(index=False)

#-----------------------------------------------------------------
      
    context = {'states': data_json, 'plain_news_list': plain_news_list, 'usa_total_cases': usa_total_cases, 'usa_total_deaths': usa_total_deaths, 'usa_total_recovered': usa_total_recovered, 'usa_total_critical': usa_total_critical}

    return render(request, "usa_cases.html", context)

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def terms_conditions(request):
    return render(request, "terms_conditions.html")