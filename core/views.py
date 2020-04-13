from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import View
from django.http import JsonResponse

from django.http import HttpResponseRedirect
from .forms import UploadFileForm

from django.contrib.staticfiles.storage import staticfiles_storage

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

    return country, cases_dates, cases, deaths, recovered

class ChartDataCountry(APIView):
    
    authentication_classes = []
    permission_classes = []

    def get_values(self, *args, **kwargs):
        global country, cases_dates, cases, deaths, recovered
        country = args[0]
        cases_dates = args[1]
        cases = args[2]
        deaths = args[3]
        recovered = args[4]

    def get(self, request, format=None, *args, **kwargs):
          
        data = {
            "country" : country,
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


def countryView(request, country):

#---------------GET INDIA CONTENTS FROM COUNTRY API--------------------

    country_total_cases, country_total_deaths, country_total_recovered, country_total_critical = get_specific_country_data(country)


#-------------GET COUNTRY DATA FOR CHARTS--------------------------------

    country, cases_dates, cases, deaths, recovered = get_country_data(country)

    api_obj = ChartDataCountry()
    api_obj.get_values(country, cases_dates, cases, deaths, recovered)

#-----------------------------------------------------------------

    context = {'country': country, 'plain_news_list': plain_news_list, 'country_total_cases': country_total_cases, 'country_total_deaths': country_total_deaths,
             'country_total_recovered': country_total_recovered, 'country_total_critical': country_total_critical}

    return render(request, "country_cases.html", context)


def webmap(request):
    import geopandas as gpd
    shapefile = 'static/webmap/data/countries/ne_110m_admin_0_countries.shp'

    #Read shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]
    #Rename columns.
    gdf.columns = ['country', 'country_code', 'geometry']
    gdf.head()

    print(gdf[gdf['country'] == 'Antarctica'])
    #Drop row corresponding to 'Antarctica'
    gdf = gdf.drop(gdf.index[159])

    import requests
    import json
    import pandas

    from bokeh.models import LinearColorMapper

    url = "https://corona.lmao.ninja/countries"
        
    response = requests.request("GET", url)

    data_json = json.loads(response.text)

    list_data = []
    for item in data_json:
        dict_data = {}
        dict_data['entity'] = item['country']
        dict_data['code'] = item['countryInfo']['iso3']
        dict_data['cases'] = item['cases']
        dict_data['deaths'] = item['deaths']
        dict_data['recovered'] = item['recovered']
        dict_data['year'] = 2020
        list_data.append(dict_data)

        
    df = pandas.DataFrame(list_data)
    
    df.info()
    df[df['code'].isnull()]

    #Filter data for year 2016.
    df_2020 = df[df['year'] == 2020]
    #Merge dataframes gdf and df_2016.
    merged = gdf.merge(df_2020, left_on = 'country_code', right_on = 'code')

    import json
    #Read data to json.
    merged_json = json.loads(merged.to_json())
    #Convert to String like object.
    json_data = json.dumps(merged_json)

    #Instantiate LinearColorMapper that maps numbers in a range linearly into a sequence of colors. Input nan_color.
    # color_mapper = LinearColorMapper(palette = palette, low = 0, high = 40, nan_color = '#d9d9d9')

    from bokeh.io import curdoc, output_notebook
    from bokeh.models import Slider, HoverTool
    from bokeh.layouts import widgetbox, row, column
    from bokeh.models import Column
    
    #Define function that returns json_data for year selected by user.
        
    def json_data(selectedYear):
        yr = selectedYear
        df_yr = df[df['year'] == yr]
        merged = gdf.merge(df_yr, left_on = 'country_code', right_on = 'code', how = 'left')
        merged.fillna('No data', inplace = True)
        merged_json = json.loads(merged.to_json())
        json_data = json.dumps(merged_json)
        return json_data
    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json_data(2020))

    
    #Define a sequential multi-hue color palette.
    palette = brewer['OrRd'][8]
    #Reverse color order so that dark red is highest obesity.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 90, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'0': '0%', '10':'10%', '15':'15%', '20':'20%', '25':'25%', '30':'30%','35':'35%', '40':'40%', '45':'45%', '50':'50%', '55':'55%', '60':'60%', '65':'65%', '70':'70%', '75':'75%', '80':'80%','85':'85%', '90': '>90%'}
    #Add hover tool
    hover = HoverTool(tooltips = [ ('Country/region','@country'),('Confirmed Cases', '@cases'),('Total Deaths', '@deaths'),('Total Recovered', '@recovered')])
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=8,width = 500, height = 20,
                        border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    #Create figure object.
    p = figure(title = 'Share of adults who are obese, 2016', plot_height = 600 , plot_width = 950, toolbar_location = None, tools = [hover])
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    #Add patch renderer to figure. 
    p.patches('xs','ys', source = geosource,fill_color = {'field' :'cases', 'transform' : color_mapper},
            line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify layout
    p.add_layout(color_bar, 'below')
    # Define the callback function: update_plot
    def update_plot(attr, old, new):
        yr = slider.value
        new_data = json_data(yr)
        geosource.geojson = new_data
        p.title.text = 'Share of adults who are obese, %d' %yr
        
    # Make a slider object: slider 
    slider = Slider(title = 'Year',start = 2019, end = 2020, step = 1, value = 2020)
    slider.on_change('value', update_plot)
    # # Make a column layout of widgetbox(slider) and plot, and add it to the current document
    layout = column(p,Column(slider))
    curdoc().add_root(layout)
    #Display plot inline in Jupyter notebook
    output_notebook()
    #Display plot
    show(layout)

    context = {}

    return render(request, "webmap.html", context)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('webmap.shp', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)