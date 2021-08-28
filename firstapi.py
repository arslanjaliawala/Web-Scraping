import requests,json, scripts

#response = requests.get("https://randomfox.ca/floof")
#fox = response.json()
#print(fox["image"])
#*******************
'''
lat = input("Enter Latitude")
lon = input("Enter Longitude")
url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&appid=eb40d142570bee8397413f0fef2a9051"
jsondata = requests.get(url=url).json()
main = jsondata['current']['weather'][0]['main']
description = "//" + jsondata['current']['weather'][0]['description']
print(main + description)
'''
#nearbylocations
#originlat = input("Please enter latitude of your current destination"
originlat = '25.3960'
#originlng = input("Please enter longitude of your current destination"
originlng = '68.3578'
#places = input("Please enter places you wish to visit")
places = "restaurant"
url = url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+originlat+','+originlng+"&radius=1500&type="+places+"&key="
response = requests.get(url = url).json()
count = 0
for count in response['results']:
    name = (count['name'])
    lat = str(count['geometry']['location']['lat'])
    lng = str(count['geometry']['location']['lng'])
    newurl = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="+originlat+","+originlng+"&destinations="+ lat +"%2C"+lng+"&key="
    response2 = requests.get(url = newurl).json()
    time = response2['rows'][0]['elements'][0]['duration']['text']
    print(name + " " + time)
