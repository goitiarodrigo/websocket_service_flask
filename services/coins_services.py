from dotenv import load_dotenv
from requests import get, put
import os

load_dotenv()
token = os.getenv('PERMANENT_TOKEN')
headers = {
    'Authorization': f'Bearer {token}'
}
URL = os.getenv('URL_PRODUCTION') if os.getenv('ENV_PRODUCTION') else os.getenv('URL_DEVELOPMENT')

def get_coins():
    try:
        response = get(f'{URL}get_coins/', headers = headers)
        resp = response.json()
        return resp
    except ValueError as error:
        return {'error': str(error)}
    

def upload_coins(json):
    try:
        put(f'{URL}upload_coins/', json=json, headers = headers)
    except ValueError as error:
        return {'error': str(error)}