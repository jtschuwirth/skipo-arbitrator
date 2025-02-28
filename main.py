import os
import time
from dotenv import load_dotenv
from skipo_api_client import SkipoApiClient
from functions.quotation_machine import quotation_machine
from functions.exxegutor_machine import exxegutor_machine

load_dotenv()

def get_supported_currencies(client):
    response = client.request('GET', '/v1/supported_currencies', params={'take': 50, 'page': 1})
    return response.get('data')

def main():
    url = os.getenv('API_URL')
    private_key_path = os.getenv('PRIVATE_KEY_PATH')
    api_key = os.getenv('API_KEY')

    client = SkipoApiClient(url, api_key, private_key_path)
    supported_currencies = get_supported_currencies(client)
    currencies = [currency['id'] for currency in supported_currencies if currency['type'] == 'CRYPTO']

    fiat_qty = 100000
    fiats = ['clp']
    currencies = ['BTC', 'USDT', 'ETH', 'WLD']
    while True:
        response = quotation_machine(client, currencies, fiats, fiat_qty)
        if response['action'] == 'NEXT':
            time.sleep(15)
            continue
        elif response['action'] == 'BUY':
            exxegutor_machine(client, [response['buyOrdId'], response['sellOrdId']])
            time.sleep(1)
            continue
        else:
            time.sleep(60)
            continue
            
   
main()