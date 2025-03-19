import os

def get_envs():
    isProd = os.getenv('ENV') == 'prod'
    print('Running in production env' if isProd else 'Running in development env')
    if isProd:
        return {
            'ENV': 'prod',
            'STRATEGY': os.getenv('STRATEGY') if os.getenv('STRATEGY') else 'default',
            'API_URL': os.getenv('API_URL_PROD'),
            'PRIVATE_KEY_PATH': os.getenv('PRIVATE_KEY_PATH_PROD'),
            'API_KEY': os.getenv('API_KEY_PROD'),
            'EXECUTE': os.getenv('EXECUTE')
        }
    else:
        return {
            'ENV': 'dev',
            'STRATEGY': os.getenv('STRATEGY') if os.getenv('STRATEGY') else 'default',
            'API_URL': os.getenv('API_URL_DEV'),
            'PRIVATE_KEY_PATH': os.getenv('PRIVATE_KEY_PATH_DEV'),
            'API_KEY': os.getenv('API_KEY_DEV'),
            'EXECUTE': os.getenv('EXECUTE')
        }