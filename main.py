import time
from dotenv import load_dotenv
from functions.get_markets import get_supported_markets
from skipo_api_client import SkipoApiClient
from functions.quotation_machine import quotation_machine
from functions.exxegutor_machine import exxegutor_machine
from functions.get_envs import get_envs

load_dotenv()

strategies = set(['quote_for_max', 'quote_for_min'])

def main():
    envs = get_envs()
    env = envs['ENV']
    url = envs['API_URL']
    private_key_path = envs['PRIVATE_KEY_PATH']
    api_key = envs['API_KEY']
    execute = True if envs['EXECUTE'] == 'true' else False

    strategy = envs['STRATEGY']
    if strategy not in strategies:
        print(f"Invalid strategy: {strategy}")
        return
    
    max_quote = {
        'CLP': {
            'symbol': 'CLP',
            'qty': 30000
        },
        'USDT': {
                'symbol': 'USDT',
                'qty': 30
            }
    }        

    client = SkipoApiClient(url, api_key, private_key_path)
    markets = get_supported_markets(client, env)
    while True:
        response = quotation_machine(client, markets, max_quote, env, strategy)
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