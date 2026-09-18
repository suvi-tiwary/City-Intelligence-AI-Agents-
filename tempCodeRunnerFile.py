from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool
from tavily import TavilyClient
import os
import requests
from langchain_groq import ChatGroq


load_dotenv()

@tool
def get_weather(city:str)->str:#
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

# result = get_weather.invoke({"city":"Raxaul"})
# print(result)

@tool
def get_news(city:str)->str:
    """
    Get the Lastest news about your personalized city
    """
    tavily_search = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response=tavily_search.search(
        max_results=1,
        search_depth="basic",
        query=f"{city}"
    )

    results = response["results"]
    news=[]
    for result in results:
        title=result.get("title")
        discription=result.get("content")
        url = result.get("url")

        news.append(
             f"Title : {title} \n"
             f"Description : {discription} \n"
             f"Url : {url}\n"
        )
    return "\n\n".join(news) 

# res = get_news.invoke({'city':"jaipur"})
# print(res)

llm = ChatGroq(
    model_name="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY")
    )

llm_with_tools = llm.bind_tools([get_weather,get_news])
messages =[]
tools={
    "get_weather":get_weather,
    "get_news":get_news
}

print("123123 WELCOME TO CITY INTELLIGENCE SYSTEM 321321")
print("Press exit ")

while True:
    query=input("You : ")
    if query.lower() == "exit":
        break
    messages.append(HumanMessage(query))

    while True:
        result = llm_with_tools.invoke(messages)
        messages.append(result)

        if not result.tool_calls:
            break

        for tool_call in result.tool_calls:
            tool_name = tool_call["name"]
            tool_arg = tool_call["args"]
            print(tool_call)

            confirm = input(f"Agents Want to use this tool {tool_name}. Approve (y/n) ")
            if confirm.lower() == "n":
                print("Tool access denied")
                messages.append(ToolMessage(
                    content="Tool access denied by the user.",
                    tool_call_id=tool_call["id"]
                ))
                continue

            tool_result = tools[tool_name].invoke(tool_arg)
            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))

        # Error fixed: `continue` here unconditionally restarted the inner loop,
        # making the final response code unreachable; loop only while tools are called.

    print(result.content)
                
            

            


    



