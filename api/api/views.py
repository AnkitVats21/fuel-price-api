from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect

BASE_URL='https://www.newsrain.in/petrol-diesel-prices'

def getNationalData():
    url = BASE_URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    result=soup.find_all('article')

    x=[]
    for i in result:
        temp=i.find('div',class_='col m4 s4 fuel-title center center-align')
        stateData=temp.text
        city=temp.find('small', class_='center').text
        city=' '.join(city.split())
        state=' '.join(stateData.split())
        state=state.replace(city,'')
        t={
            'state':state,
            'city':city
        }
        fuel=i.find_all('div',class_='col m6')
        for k,j in enumerate(fuel):
            fuel_type=j.find('h3', class_='block_title').text
            fuel_type=''.join(fuel_type.split())
            price=''.join((j.find('span',class_='price_tag').text).split())
            price_change=j.find('div',class_='price-change')
            z=str(price_change.find('i'))
            price_change=''.join((price_change.text).split())
            change=z.split(' ')[3][9:]
            t[fuel_type]={'price':price,'priceChange':price_change,'change':change}
        x.append(t)
    ans=json.dumps(x)
    return ans

def index(request):
    data=getNationalData()
    return HttpResponse(data)



