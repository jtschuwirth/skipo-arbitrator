import time

def get_markets_prices(client, currency, fiat, qty):
    quotation_buy = get_quotation(client, currency, fiat, False, 'BUY', qty)
    quotation_sell = get_quotation(client, currency, fiat, False, 'SELL', qty)

    return {
        'buy': quotation_buy,
        'sell': quotation_sell
    }

def analyse_market_difference(market):
    buy_rate = float(market['buy']['rate'])
    sell_rate = float(market['sell']['rate'])
    base_qty = float(market['buy']['baseQty'])
    difference = sell_rate - buy_rate

    gains = difference * base_qty
    return {
        'buy_rate': buy_rate,
        'sell_rate': sell_rate,
        'rate_difference': difference,
        'gains': gains
    }

def get_quotation(client, base_currency, quote_currency, is_base_qty, side, qty):
    response = client.request('POST', '/v1/converts/quotations', body={
        'baseCurrencyId': base_currency, 
        'quoteCurrencyId': quote_currency,
        'qtyCurrencyId': base_currency if is_base_qty else quote_currency,
        'side': side,
        'quantity': str(qty)
    })
    status_code = response['statusCode'] if 'statusCode' in response else 200
    if status_code == 429:
        raise Exception('Too many requests')
    return response

def quotation_machine(client, markets, max_quote, env, strategy):
    for market in markets:
            quote_symbol = market['quoteCurrencyId']
            base_symbol = market['baseCurrencyId']

            quote_qty = 0
            max_quote_qty = float(max_quote[quote_symbol]['qty'])
            min_quote_qty = float(market['minQuoteQty'])

            if strategy == 'quote_for_min':
                quote_qty = min_quote_qty
            elif strategy == 'quote_for_max':
                quote_qty = max_quote_qty

            if quote_qty < min_quote_qty:
                print(f"Skipping market: [{base_symbol}-{quote_symbol}] because quote qty is less than min quote qty")
                continue

            try:
                print("---------------------------------")
                print(f'Checking market: [{base_symbol}-{quote_symbol}] in {env} with strategy {strategy}')
                market = get_markets_prices(client, base_symbol, quote_symbol, quote_qty)
                difference = analyse_market_difference(market)
                if (difference['rate_difference'] > 0):
                    print(f"EXECUTE, earn: {difference['gains']} {quote_symbol} with trading volume {quote_qty} {quote_symbol}")
                    print(f"orders: buy: {market['buy']['ordId']} sell: {market['sell']['ordId']}")
                    return {
                        'status': 200,
                        'action': 'EXECUTE',
                        'buyOrdId': market['buy']['ordId'],
                        'sellOrdId': market['sell']['ordId']
                    }
                else:
                    print(f"NEXT, loose: {difference['gains']} {quote_symbol} with trading volume {quote_qty} {quote_symbol}")
                    print(f"orders: buy: {market['buy']['ordId']} sell: {market['sell']['ordId']}")
                    time.sleep(2)
            except Exception as e:

                print(f"Error checking market: [{base_symbol}-{quote_symbol}], {e}")
                time.sleep(2)
                continue
    
    return {
        'status': 200,
        'action': 'NEXT'
    }