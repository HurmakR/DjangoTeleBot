import requests, os
from dotenv import load_dotenv

def get_token():
    load_dotenv()
    API_KEY=os.getenv('API_KEY')
    url = 'https://api.remonline.ua/token/new'
    myobj = {'api_key': API_KEY}
    return requests.post(url, myobj).json()['token']

def get_repair_by_id(repnum):
    url = 'https://api.remonline.app/order/'
    myobj = {'token': get_token(), 'id_labels[]': f'ВО{repnum}'}
    result = requests.get(url, myobj).json()
    return result

