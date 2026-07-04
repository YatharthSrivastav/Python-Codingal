import requests

def get_weather(LAT, LON):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&units=metric&appid=51d05644140940cfc7f854c2c1804a3a"

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()

        return (
            f"Name: {weather_data['name']} \n"
            f"Weather: {weather_data['weather'][0]['main']} \n"
            f"Description: {weather_data['weather'][0]['description']} \n"
            f"Temp: {weather_data['main']['temp']}°C \n"
            f"Feels Like: {weather_data['main']['feels_like']}°C \n"
            f"Min Temp: {weather_data['main']['temp_min']}°C \n"
            f"Max Temp: {weather_data['main']['temp_max']}°C \n"
            f"Pressure: {weather_data['main']['pressure']} Mb \n"
            f"Wind Speed: {weather_data['wind']['speed']} m/s"
        )
    elif response.status_code == 404:
        return "Error 404: Weather data not found. Check the location or API endpoint."

    elif response.status_code == 500:
        return "Error 500: OpenWeather server encountered an internal error. Please try again later."

    else:
        return f"Error {response.status_code}: Unable to fetch weather data."
    
def main():
    print("Hello! Welcome to your Weather Tracker App")
    LAT = input("Please enter the latitude of your place\n")
    LON = input("Please enter the longitude of your place\n")
    print("Today's weather is...\n")
    weather = get_weather(LAT, LON)
    print(weather)
    print()
    print("Hope you have a nice day! Bye!")
    
if __name__ == "__main__":
    main()