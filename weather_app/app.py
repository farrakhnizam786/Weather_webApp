from flask import Flask, render_template
import requests
import geocoder

app = Flask(__name__)

API_KEY = 'your_actual_api_key_here'  # Replace with your real API key

def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('cod') != 200:
            return None

        weather = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'].capitalize(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed']
        }
        return weather
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

@app.route('/')
def index():
    city = geocoder.ip('me').city or 'Delhi'  # fallback city
    weather_data = get_weather(city)
    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
