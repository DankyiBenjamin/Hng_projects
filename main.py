from flask import Flask, request, jsonify
import requests


app = Flask(__name__)


def get_weather(city):
    #
    api_key = '7a81d3c9c1b11b4cbf1a898da335b1af'
    response = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric')
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        return temperature
    else:
        return 'Unknown'


@app.route('/')
def home():
    return "welcome"


@app.route('/api/hello', methods=['GET'])
def api():
    # getting the vistor name
    visitor_name = request.args.get('visitor_name')
    client_ip = request.environ['REMOTE_ADDR']
    # getting the user ip and location
    response = requests.get(
        f'https://ipinfo.io/{client_ip}/json?token=e852942472d06c')
    data = response.json()
    location = data.get('city')
    # client_ip = data.get('ip')
    # detting the temperature
    temperature = get_weather(location)
    # greeting message
    greeting = f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {location}"
    if visitor_name:
        user_data = {
            "client_ip": client_ip,
            "location": location,
            "greeting": greeting
        }
        return jsonify(user_data)
    else:
        # without client name
        greeting = f"Hello,  the temperature is {temperature} degrees Celcius in {location}"
        user_data = {
            "client_ip": client_ip,
            "location": location,
            "greeting": greeting
        }
        return jsonify(user_data)


if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
