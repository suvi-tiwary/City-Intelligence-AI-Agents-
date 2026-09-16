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
    weather_api= os.getenv("WEATHER_API_KEY")
    response = requests.get(weather_api)
    data = response.json()
    print(data)
   

get_weather.invoke("what is the weather of Raxaul")
