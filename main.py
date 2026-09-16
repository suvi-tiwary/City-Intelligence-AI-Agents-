from dotenv import load_dotenv
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage
from langchain.tools import tool
from tavily import TavilyClient
import os
import requests

load_dotenv()

@tool
def get_weather(city:str)->str:
    """ 
    Get weather of the particular city 
    """
    weather_api_key= os.getenv("WEATHER_API_KEY")
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric")
    data = response.json()
    temperature = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]

    condition = data["weather"][0]["main"]
    description = data["weather"][0]["description"]

    wind_speed = data["wind"]["speed"]
    visibility = data["visibility"]

    city_name = data["name"]
    country = data["sys"]["country"]

    return (
        f"Weather in {city_name}, {country}:\n"
        f"Temperature: {temperature}°C\n"
        f"Feels like: {feels_like}°C\n"
        f"Condition: {condition} ({description})\n"
        f"Humidity: {humidity}%\n"
        f"Wind speed: {wind_speed} m/s\n"
        f"Visibility: {visibility / 1000} km"
    )

result = get_weather.invoke({"city":"Raxaul"})
print(result)
