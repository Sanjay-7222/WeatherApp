from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City
import requests
from django.contrib import messages

# Create your views here.

def home(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={},&appid=5efa88ba6a3f50ac03a648f56b82c433&units=metric'
    if request.method=='POST':
        form=CityForm(request.POST)
        if form.is_valid():
            NCity=form.cleaned_data['name']
            CCity=City.objects.filter(name=NCity).count()
            if CCity==0:
                res=requests.get(url.format(NCity)).json()
                if res['cod']==200:
                    form.save()
                    messages.success(request,""+NCity+" Added Succesfully....!!!")
                else:
                    messages.error(request,"City Does Not Exists....!!!")
            else:
                messages.error(request,"City Already Exists....!!!")
    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        weather={
            'City':city,
            'Temperature': res['main']['temp'],
            'Description': res['weather'][0]['description'],
            'Country': res['sys']['country'],
            'Icon': res['weather'][0]['icon'],
        }
        data.append(weather)
    context={'data':data,'form':form}
    return render(request,"weatherapp.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request,""+CName+" Removed Successfully....!!!")
    return redirect('Home')