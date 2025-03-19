import os
import time
from dotenv import load_dotenv
from skipo_api_client import SkipoApiClient
from functions.quotation_machine import quotation_machine
from functions.exxegutor_machine import exxegutor_machine

load_dotenv()

def get_envs():
    isProd = os.getenv('ENV') == 'prod'
    print('Running in production env' if isProd else 'Running in development env')
    if isProd:
        return {
            'API_URL': os.getenv('API_URL_PROD'),
            'PRIVATE_KEY_PATH': os.getenv('PRIVATE_KEY_PATH_PROD'),
            'API_KEY': os.getenv('API_KEY_PROD'),
            'EXECUTE': os.getenv('EXECUTE'),
            'CURRENCIES': ['BTC', 'USDT', 'ETH', 'BNB', 'DOGE', 'ADA', 'LTC', 'SOL', 'TRX', 'USDC', 'XRP'],
            'FIATS': [{
                'name': 'CLP',
                'qty': 30000
            },
            {
                'name': 'USDT',
                'qty': 30
            }]
        }
    else:
        return {
            'API_URL': os.getenv('API_URL_DEV'),
            'PRIVATE_KEY_PATH': os.getenv('PRIVATE_KEY_PATH_DEV'),
            'API_KEY': os.getenv('API_KEY_DEV'),
            'EXECUTE': os.getenv('EXECUTE'),
            'CURRENCIES': ['BTC', 'USDT'],
            'FIATS': [{
                'name': 'CLP',
                'qty': 30000
            },
            {
                'name': 'USDT',
                'qty': 30
            }]
        }

def main():
    envs = get_envs()
    url = envs['API_URL']
    private_key_path = envs['PRIVATE_KEY_PATH']
    api_key = envs['API_KEY']
    execute = True if envs['EXECUTE'] == 'true' else False
    currencies = envs['CURRENCIES']
    fiats = envs['FIATS']

    client = SkipoApiClient(url, api_key, private_key_path)
    while True:
        response = quotation_machine(client, currencies, fiats)
        if response['action'] == 'NEXT':
            time.sleep(15)
            continue
        elif response['action'] == 'EXECUTE' and execute:
            exxegutor_machine(client, [response['buyOrdId'], response['sellOrdId']])
            time.sleep(1)
            continue
        else:
            time.sleep(60)
            continue
            
   
main()