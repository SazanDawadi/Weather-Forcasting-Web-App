import requests
import calendar
from datetime import datetime as dt
import json
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from django.shortcuts import render
from credentials import API_KEY
import pytz

# utc time now and later change it acc. to client's timezone
UTC = pytz.utc


def home(request):
    # RGB color for web app background
    rgb_night = [15, 32, 39,44, 83, 100]
    rgb_sunny = [255, 102, 0, 204, 204, 0]
    rgb_body = [43, 50, 178, 20, 136,204]

    geolocator = Nominatim(user_agent="weather_app")
    # if checks either form has been submitted or not
    # if yes searched is searched value
    # else searcjed is default value London,UK
    if request.POST.get('search') != None:
        searched = request.POST.get('search')
        
    else:
        searched =  "London, UK"
    
    location = geolocator.geocode(searched)
    if(location == None):
        print("hum toh cgutiye hai!!")
        msg = "oops" + " " + searched + " not found :("
        context = {
            "message":msg,
            "rb":rgb_body,
        }
        return render(request,'weather/main.html',context)



    # add your api key here
    api_key = API_KEY
    lat = location.latitude
    lon = location.longitude
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

    response = requests.get(url)
    # data is the jason file
    data = response.json()

    # checking if city found or not if error occurs exception code will run
    try:
        timezone = data["timezone"]
        today_time = pytz.timezone(timezone)
        local_time = dt.now(today_time)

        today_day_count = local_time.weekday()
        today_day_name = calendar.day_name[today_day_count]
        today_date_regular = local_time.strftime(' , %B %d')
        today_hour = int(local_time.strftime('%H'))
        # date variable outputs in format sunday,Nov 25
        date = today_day_name + today_date_regular
        

        address = searched

        current_temp = int(data["current"]["temp"])
        current_weather_desc = data["current"]["weather"][0]["description"]
        current_weather_desc_sml = data["current"]["weather"][0]["main"]
        # it displays moon and sun depending on it is either day or night
        is_it_night = (today_hour > 18 and today_hour <= 24) or (today_hour >=0 and today_hour < 6)
        
        if is_it_night:
            rgb_body = rgb_night
            
        if current_weather_desc_sml =="Clear" and is_it_night == True :
            current_weather_desc_sml += "-night"
            
        if current_weather_desc_sml =="Clear" and is_it_night == False:
            rgb_body = rgb_sunny
            

        current_weather_desc_small = 'static/icons/' + current_weather_desc_sml + '.svg'
        crnt_temp_high = int(data["daily"][0]["temp"]["max"])
        crnt_temp_low = int(data["daily"][0]["temp"]["min"])
        # api by default gives wind speed in m/s
        # to convert to miles per hr multiply by  2.237
        wind_speed = "{:.2f}".format((data["daily"][0]["wind_speed"])*2.237)
        uv_index = int(data["daily"][0]["uvi"])

        # 7 days weather forecast

        daily_weather = []
        for i in range(1,7):

            daily_high = int(data["daily"][i]["temp"]["max"])
            daily_low = int(data["daily"][i]["temp"]["min"])
            daily_wind = "{:.2f}".format((data["daily"][i]["wind_speed"])*2.237)
            daily_uvi = int(data["daily"][i]["uvi"])
            daily_weather_desc = 'static/icons/' +  data["daily"][i]["weather"][0]["main"] + '.svg'
            daily_weather_desc_long = data["daily"][i]["weather"][0]["description"] 
            
            daily_time = data["daily"][i]["dt"]
            daily_day = calendar.day_name[dt.fromtimestamp(daily_time).weekday()]
            daily_day = daily_day[:3]

            daily_weather.append((daily_high,daily_low,daily_wind,daily_uvi,daily_weather_desc,daily_day,daily_weather_desc_long))

        context ={
            'address':address,
            'date':date,
            'current_temp':current_temp,
            'current_weather_desc':current_weather_desc,
            'current_weather_desc_small':current_weather_desc_small,
            'crnt_temp_high':crnt_temp_high,
            'crnt_temp_low':crnt_temp_low,
            'wind_speed':wind_speed,
            'uv_index':uv_index,
            'daily_weather':daily_weather,
            'rb':rgb_body,
        }
        return render(request,'weather/main.html',context)
    
    except:
        msg = "oops" + " " + searched + " not found :("
        context = {
            "message":msg,
            "rb":rgb_body,
        }
        return render(request,'weather/main.html',context)



