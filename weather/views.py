import requests
import calendar
from datetime import datetime as dt
import json
from geopy.geocoders import Nominatim
from django.shortcuts import render
from credentials import API_KEY


# Create your views here.
def home(request):
    api_key = API_KEY
    lat = "27.7172"
    lon = "85.3240"
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

    response = requests.get(url)
    # data = json.loads(response.text)
    data = response.json()
    

    today_date = data["current"]["dt"]
    # timezone_offset =data["timezone_offset"]
    local_time = dt.fromtimestamp(today_date)
    today_day_count = local_time.weekday()
    today_day_name = calendar.day_name[today_day_count]
    today_date_regular = local_time.strftime(' , %B %d')
    # date variable outputs in format sunday,Nov 25
    date = today_day_name + today_date_regular


    geolocator = Nominatim(user_agent="weather_app")
    latlong = lat + ", " + lon
    location = geolocator.reverse(latlong, language='en')
    address_raw = location.raw['address']
    city = address_raw.get('city', '')
    country = address_raw.get('country', '')
    address = city + ", " + country
    print(address)



    current_temp = int(data["current"]["temp"])
    current_weather_desc = data["current"]["weather"][0]["description"]
    current_weather_desc_small = data["current"]["weather"][0]["main"]
    crnt_temp_high = int(data["daily"][0]["temp"]["max"])
    crnt_temp_low = int(data["daily"][0]["temp"]["min"])
    # api by default gives wind speed in m/s
    # to convert to miles per hr multiply by  2.237
    wind_speed = "{:.2f}".format((data["daily"][0]["wind_speed"])*2.237)
    rain_chances = int(data["daily"][0]["rain"])

    daily_weather = []
    for i in range(1,7):

        daily_high = int(data["daily"][i]["temp"]["max"])
        daily_low = int(data["daily"][i]["temp"]["min"])
        daily_wind = "{:.2f}".format((data["daily"][i]["wind_speed"])*2.237)
        daily_rain = int(data["daily"][i]["rain"])
        daily_weather_desc = data["daily"][i]["weather"][0]["main"]
        
        daily_time = data["daily"][i]["dt"]
        daily_day = calendar.day_name[dt.fromtimestamp(daily_time).weekday()]
        daily_day = daily_day[:3]

        daily_weather.append((daily_high,daily_low,daily_wind,daily_rain,daily_weather_desc,daily_day))

    context ={
        'address':address,
        'date':date,
        'current_temp':current_temp,
        'current_weather_desc':current_weather_desc,
        'current_weather_desc_small':current_weather_desc_small,
        'crnt_temp_high':crnt_temp_high,
        'crnt_temp_low':crnt_temp_low,
        'wind_speed':wind_speed,
        'rain_chances':rain_chances,
        'daily_weather':daily_weather,
    }
    print(current_weather_desc_small)
    return render(request,'weather/main.html',context)

