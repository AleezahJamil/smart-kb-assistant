import os
import requests
from dotenv import load_dotenv
load_dotenv()
WEATHER_KEY=os.getenv("WEATHER_API_KEY")
def get_weather(city):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params={
        "q":city,
        "appid":WEATHER_KEY,
        "units":"metric"
    }
    response=requests.get(url,params=params)
    data=response.json()
    if response.status_code!=200:
        return f"Error: {data.get('message','something went wrong')}"
    temp=data["main"]["temp"]
    description=data["weather"][0]["description"]
    city_name=data["name"]
    return f"The weather in {city_name} is {temp}°C with {description}."
if __name__=="__main__":
    result=get_weather("Gujrat")
    print(result)
  