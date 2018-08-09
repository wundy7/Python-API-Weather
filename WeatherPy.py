
# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import csv

# Import API key
from config import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

## Generate Cities List

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=2000)
lngs = np.random.uniform(low=-180.000, high=180.000, size=2000)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)

#Create URL query

base_url = "http://api.openweathermap.org/data/2.5/weather?"
#api_key = config.api_key
units = "imperial"

query_url = base_url + "appid=" + api_key + "&units=" + units + "&q="

print(query_url)

# Generate loop to go through list of cities

# Creation of lists to hold values returned from API
city_info = []
city_data = []
clouds = []
humidity = []
latitude = []
longitude = []
temp = []
wind = []

# Create loop in which to tap API and get following characteristics. Use try and else so if a city doesnt have details will skip and not error out.
for city in cities:
    response = requests.get(query_url + city).json()
    
    try:
        city_id = response.get("id")
        clouds_id = response.get("clouds").get("all")
        humidity_id = response.get("main").get("humidity")
        latitude_id = response.get("coord").get("lat")
        longitude_id = response.get("coord").get("lon")
        temp_id = response.get("main")["temp"]
        wind_id = response.get("wind").get("speed")
    
        if response.get("id"):
            city_info.append(response)
            city_data.append(city)
            clouds.append(clouds_id)
            humidity.append(humidity_id)
            latitude.append(latitude_id)
            longitude.append(longitude_id)
            temp.append(temp_id)
            wind.append(wind_id)
            print(f" city is {city} and id is {city_id} and temp is {temp_id}")
        
        else:
            print(f" No details for {city}, {temp_id}")
            
    except:
        print(f"Error for {city}")  
# Print finish so know that it is done pulling details.     
print("finished")

# Create new dictionary from api 
weather_dict = {
    "City": city_data,
    "Cloudiness":clouds,
    "Humidity": humidity,
    "Latitude": latitude,
    "Longitude": longitude,
    "Temperature": temp,
    "Wind Speed": wind
}

#Count number of cities to ensure have more than 500
len(weather_dict["City"])

# Generate new DataFrame with details from openweathermap
weather_data = pd.DataFrame(weather_dict)
weather_data.head()

# Output File (CSV)
weather_data.to_csv("cities_data.csv", encoding='utf-8', index=False)

#Generate Scatter Plot
plt.scatter(weather_data["Latitude"], weather_data["Temperature"], facecolors="lightskyblue", edgecolors='black', alpha = 1)

# create chart title, labels, legends, note on driver count, and formatting
plt.title("August 9th: Temperature (F) vs Latitude")
plt.ylabel("Temperature (F)")
plt.xlabel("Latitude")


plt.savefig("Temp_vs_Lat.png")

plt.show()

# Generate Scatter Plot
plt.scatter(weather_data["Latitude"], weather_data["Humidity"], facecolors="lightskyblue", edgecolors='black', alpha = 1)

# create chart title, labels, legends, note on driver count, and formatting
plt.title("August 9th: Humidity vs Latitude")
plt.ylabel("Humidity")
plt.xlabel("Latitude")

plt.savefig("Hum_vs_Lat.png")

plt.show()

#Generate Scatter Plot
plt.scatter(weather_data["Latitude"], weather_data["Cloudiness"], facecolors="lightskyblue", edgecolors='black', alpha = 1)

# create chart title, labels, legends, note on driver count, and formatting
plt.title("August 9th: Cloudiness vs Latitude")
plt.ylabel("Cloudiness")
plt.xlabel("Latitude")

plt.savefig("Cld_vs_Lat.png")

plt.show()

# Generate Scatter Plot
plt.scatter(weather_data["Latitude"], weather_data["Wind Speed"], facecolors="lightskyblue", edgecolors='black', alpha = 1)

# create chart title, labels, legends, note on driver count, and formatting
plt.title("August 9th: Wind Speed vs Latitude")
plt.ylabel("Wind Speed")
plt.xlabel("Latitude")

plt.savefig("Cld_vs_Lat.png")

plt.show()

# Observable Trends

    #1) One assumption going in as that I assumed temperatures would be hottest at 0 degrees latitude. However,
    #   when analyzing the data it appears the hottest latitudes appear closer to the 20 degrees to 40 degrees.
    #   I would be curious if this trend is consistent throughout the year. 
    
    #2) Another trend is that once one gets 20 degrees +/- from the equator temperatures begin to drop. 
    #3) When analyzing wind speed it is hard to determine trends as the wind speed is pretty consistent throughout the 
    #   latitdudes. There do appear to be a few locations with windsppeds greater than 15 mph and more locations appear
    #   once one begins to get 20 degrees +/- from the equator. However, I would want to further investigate the data points
    #   to see if a storm was occuring at the time the data is run. Also, I would want to see how the data looks over a time
    #   period. Perhaps, looking over a period of time may show more consistent wind conditions for a specific location,
    #   thus allowing one to compare wind speed vs. latitude. 