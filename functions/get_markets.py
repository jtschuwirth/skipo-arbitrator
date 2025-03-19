


def get_supported_markets(client, env):
    if env != "prod":
        return [
            {'id': 'BTC-CLP', 'baseCurrencyId': 'BTC', 'quoteCurrencyId': 'CLP', 'type': 'CRYPTO-FIAT', 'minBaseQty': '0.00000005', 'minQuoteQty': '10'},
            {'id': 'BTC-USDT', 'baseCurrencyId': 'BTC', 'quoteCurrencyId': 'USDT', 'type': 'CRYPTO-CRYPTO', 'minBaseQty': '0.0001', 'minQuoteQty': '0.02'},
            {'id': 'USDT-CLP', 'baseCurrencyId': 'USDT', 'quoteCurrencyId': 'CLP', 'type': 'CRYPTO-FIAT', 'minBaseQty': '0.5', 'minQuoteQty': '100'}
        ]
    else:
        response = client.request('GET', '/v1/supported_markets', params={'take': 50, 'page': 1})
        supported_markets = response.get('data')
        return supported_markets