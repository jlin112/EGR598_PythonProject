import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

def get_weather_data(api_key, location, days):
    """
    Request the weather data (historical, real-time, or forecasting) based on user's input (Location, and number of days).
    """
    if days < 0:
        # Historical Weather
        date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        url = f"http://api.weatherapi.com/v1/history.json?key={api_key}&q={location}&dt={date}"
        data_type = "Historical"
    elif days == 0:
        # Real-time Weather
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        data_type = "Real-time"
    else:
        # Forecasting Weather
        url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days={days}"
        data_type = "Forecast"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data, data_type
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return None, None

def display_weather(data, data_type):
    """
    Demonstrate the weather data based on the number type (negative, 0, positive) (historical, real-time, or forecast).
    """
    if not data:
        messagebox.showinfo("Weather Data", "No data available.")
        return
    
    if data_type == "Real-time":
        location = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        temp_c = data['current']['temp_c']
        condition = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']
        message = (
            f"Real-time Weather in {location}, {region}, {country}:\n"
            f"  Temperature: {temp_c}°C\n"
            f"  Condition: {condition}\n"
            f"  Humidity: {humidity}%\n"
            f"  Wind Speed: {wind_kph} kph\n"
        )
    elif data_type == "Historical":
        location = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        date = data['forecast']['forecastday'][0]['date']
        condition = data['forecast']['forecastday'][0]['day']['condition']['text']
        max_temp = data['forecast']['forecastday'][0]['day']['maxtemp_c']
        min_temp = data['forecast']['forecastday'][0]['day']['mintemp_c']
        message = (
            f"Historical Weather in {location}, {region}, {country} on {date}:\n"
            f"  Condition: {condition}\n"
            f"  Max Temp: {max_temp}°C\n"
            f"  Min Temp: {min_temp}°C\n"
        )
    elif data_type == "Forecast":
        location = data['location']['name']
        region = data['location']['region']
        country = data['location']['country']
        forecast_message = f"Forecast Weather for {location}, {region}, {country}:\n\n"
        for day in data['forecast']['forecastday']:
            date = day['date']
            condition = day['day']['condition']['text']
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            avg_humidity = day['day']['avghumidity']
            forecast_message += (
                f"Date: {date}\n"
                f"  Condition: {condition}\n"
                f"  Max Temp: {max_temp}°C\n"
                f"  Min Temp: {min_temp}°C\n"
                f"  Avg Humidity: {avg_humidity}%\n\n"
            )
        message = forecast_message
    else:
        message = "Invalid data type."
    
    messagebox.showinfo(f"{data_type} Weather Data", message)

def fetch_weather():
    """
    Fetches weather data based on user input from the GUI.
    """
    location = location_entry.get()
    days = days_entry.get()
    
    if not location:
        messagebox.showerror("Input Error", "Please enter a location.")
        return
    
    try:
        days = int(days)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number of days (integer).")
        return
    
    data, data_type = get_weather_data(api_key, location, days)
    display_weather(data, data_type)

# API Key from https://www.weatherapi.com/
api_key = "c9f776706b1740d2b8f214136240512"

root = tk.Tk()
root.title("Weather Data Analyzer")

tk.Label(root, text="Enter Location:").grid(row=0, column=0, padx=10, pady=10)
location_entry = tk.Entry(root, width=30)
location_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Enter Days (negative for history, 0 for real-time, positive for forecast):").grid(row=1, column=0, padx=10, pady=10)
days_entry = tk.Entry(root, width=30)
days_entry.grid(row=1, column=1, padx=10, pady=10)

fetch_button = tk.Button(root, text="Get Weather Data", command=fetch_weather)
fetch_button.grid(row=2, column=0, columnspan=2, pady=20)

root.mainloop()


