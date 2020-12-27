from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
import json
from django.http import HttpResponse, Http404, HttpResponseRedirect

BASE_URL='https://www.newsrain.in/petrol-diesel-prices'

def getNationalData():
    url = BASE_URL
    try:
        response = requests.get(url)
    except:
        return 'unable to reach server'
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
    res=json.dumps(x)
    return res

def getStateData(state):
    url=BASE_URL+'/'+state
    try:
        response = requests.get(url)
    except:
        return "unable to reach server"
    soup = BeautifulSoup(response.content, 'html.parser')
    district=soup.find_all('div', class_='fuel-wrapper')
    res=[]
    for i in district:
        temp={}
        distt=i.find('h2',class_="col m4 s4 fuel-title-dist center center-align").text
        temp['district']=' '.join(distt.split())
        fuel=i.find_all('div',class_="col m6")
        for j in fuel:
            fuel_type=j.find('h3',class_='block_title').text
            fuel_type=''.join(fuel_type.split())
            price=j.find('span',class_='price_tag').text
            priceChange=j.find('div',class_='price-change')
            z=str(priceChange.find('i'))
            change=z.split(' ')[3][9:]
            priceChange=j.find('div',class_='price-change').find('span').text.split()
            temp[fuel_type]={'price':price,'priceChange':priceChange[0],'change':change}
        res.append(temp)
    res=json.dumps(res)
    return res

def index(request):
    data=getNationalData()
    return HttpResponse(data)

def landing(request):
    context=request.META.get('HTTP_HOST')
    return render(request,'index.html',{'context':context})

def statewise(request,state):
    data=getStateData(state)
    return HttpResponse(data)