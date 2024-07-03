from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Function to get location data from IP


def get_location(client_ip):
    response = requests.get(f'http://ip-api.com/json/{client_ip}')
    if response.status_code == 200:
        data = response.json()
        city = data.get('city', 'Unknown')
        return city
    else:
        return 'Unknown'

# Function to get weather data


def get_weather(city):
    # Replace with your OpenWeatherMap API key
    api_key = '7a81d3c9c1b11b4cbf1a898da335b1af'
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return 'Unknown'


@app.route('/api/hello', methods=['GET'])
def hello():
    visitor_name =  request.args.get('visitor_name')
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    location = get_location(client_ip)
    temperature = get_weather(location)
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location}"
    if visitor_name:
        user_data = {
            'client_ip': client_ip,
            'location': location,
            'greeting': greeting
        }
        return jsonify(user_data), 200
    else:
        user_data = {
            'client_ip': "null",
            'location': 'null',
            'greeting': 'null'
        }
        return jsonify(user_data)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
