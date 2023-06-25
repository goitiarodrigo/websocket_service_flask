from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
from services.coins_services import get_coins, upload_coins
import random
import logging
import os

load_dotenv()

app = Flask('__name__')

socketio = SocketIO(app, cors_allowed_origins = '*')
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
URL = os.getenv('URL_PRODUCTION') if os.getenv('ENV_PRODUCTION') else os.getenv('URL_DEVELOPMENT')

@app.route('/')
def index():
    return 'Websocket server is running'

@socketio.on('connect')
def handle_connect():
    print('New connection')


def generate_alert_price():

    while True:
        try:
            json_data = get_coins()
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
                    logger.exception(f'An error occurred with current currencies data {error}')

            upload_coins(list_prices_changed_data)
            socketio.emit('price_alert', list_prices_changed_data)
            socketio.sleep(10)
        except ValueError as error:
            socketio.emit('error', { 'message': f'An error has occurred in HTTP requests: {error}' })

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
if __name__ == '__main__' :
    socketio.start_background_task(generate_alert_price)
    socketio.run(app, host='0.0.0.0', debug=True)
