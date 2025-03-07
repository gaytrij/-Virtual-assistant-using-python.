import requests
import datetime
import logging
import sqlite3
import os

# Configure logging
logging.basicConfig(filename='assistant.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# OpenWeatherMap API key
API_KEY = '0d6f4e457bebd2b98f0aa8428ab640a3'
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

# SQLite database setup
if not os.path.exists('assistant.db'):
    conn = sqlite3.connect('assistant.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE history (id INTEGER PRIMARY KEY, operation TEXT, result TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

def log_operation(operation, result):
    """Logs operations to the database."""
    conn = sqlite3.connect('assistant.db')
    c = conn.cursor()
    c.execute("INSERT INTO history (operation, result, timestamp) VALUES (?, ?, ?)",
              (operation, result, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_weather(city):
    """Fetches weather information for a given city."""
    try:
        url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return f"Error: {data['message']}"
        weather = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        return f"Weather in {city}: {weather}, Temperature: {temperature}°C"
    except Exception as e:
        return f"Error fetching weather: {e}"

def set_reminder(reminder_text, reminder_time):
    """Sets a reminder for a specific time."""
    try:
        reminder_time = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        now = datetime.datetime.now()
        if reminder_time < now:
            return "Error: Reminder time must be in the future."
        return f"Reminder set for {reminder_time}: {reminder_text}"
    except ValueError:
        return "Error: Invalid date format. Use YYYY-MM-DD HH:MM."

def calculate(expression):
    """Performs basic arithmetic operations."""
    try:
        result = eval(expression)
        log_operation(expression, str(result))
        return f"Result: {result}"
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error: Invalid expression. {e}"

def main():
    print("Welcome to the Virtual Assistant!")
    while True:
        print("\nOptions:")
        print("1. Perform Calculation")
        print("2. Get Weather")
        print("3. Set Reminder")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            expression = input("Enter an arithmetic expression (e.g., 2 + 3 * 4): ")
            print(calculate(expression))
        elif choice == '2':
            city = input("Enter city name: ")
            print(get_weather(city))
        elif choice == '3':
            reminder_text = input("Enter reminder text: ")
            reminder_time = input("Enter reminder time (YYYY-MM-DD HH:MM): ")
            print(set_reminder(reminder_text, reminder_time))
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
