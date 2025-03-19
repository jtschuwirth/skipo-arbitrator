def get_supported_currencies(client):
    response = client.request('GET', '/v1/supported_currencies', params={'take': 50, 'page': 1})
    supported_currencies = response.get('data')
    currencies = [currency['id'] for currency in supported_currencies if currency['type'] == 'CRYPTO']
    return currencies