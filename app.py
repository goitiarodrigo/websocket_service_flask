from flask import Flask
from flask_socketio import SocketIO
import requests
import random

app = Flask('__name__')

socketio = SocketIO(app, cors_allowed_origins = '*')

@app.route('/')
def index():
    return 'Websocket server is running'

@socketio.on('connect')
def handle_connect():
    print('New connection')


def generate_alert_price():

    while True:
        try:
            token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJ1c2VybmFtZSI6InRlc3QiLCJleHAiOjE2ODc0NDQ1NDJ9.fq8cxu_1R7ctTk3BrLYAya_x1GsLZITLuo4Szte7RJU'
            headers = {
                'Authorization': f'Bearer {token}'
            }

            response = requests.get('http://localhost:3000/api/get_coins/', headers = headers)
            json_data = response.json()
            if 'message' in json_data: raise ValueError(json_data['message'])
            quantity_coins = random.randint(1, 10)
            selected_coins = random.sample(json_data, quantity_coins)

            list_prices_changed_data = []
            for coin in selected_coins:
                try:
                    new_price = coin['current_price'] + random.uniform(-0.1 if coin['current_price'] < 0.5 else -0.5 , 0.5)
                    prices_changed_data = {
                        'name': coin['name'],
                        'abbreviation': coin['abbreviation'],
                        'old_price': coin['current_price'],
                        'image': coin['image'],
                        'current_price': new_price,
                        'id': coin['id'],
                        'previous_day_price': coin['previous_day_price']
                    }

                    list_prices_changed_data.append(prices_changed_data)
                except ValueError as error:
                    raise f'An error has occurred with current currencies data: {error}'

            requests.put('http://localhost:3000/api/upload_coins/', json = list_prices_changed_data, headers = headers)
            socketio.emit('price_alert', list_prices_changed_data)
            socketio.sleep(10)
        except ValueError as error:
            socketio.emit('error', { 'message': f'An error has occurred in HTTP requests: {error}' })

@socketio.on('disconnect')
def handle_disconnect():
    print('Clien disconnected')

if __name__ == '__main__' :
    socketio.start_background_task(generate_alert_price)
    socketio.run(app, debug=True)
