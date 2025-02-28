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
        'baseCurrency': base_currency, 
        'quoteCurrency': quote_currency,
        'isBaseQty': is_base_qty,
        'side': side,
        'qty': str(qty)
    })
    return response

def quotation_machine(client, currencies, fiats, qty):
    for currency in currencies:
        for fiat in fiats:
            print("--------------------")
            try:
                print(f'Checking market: [{currency.lower()}-{fiat}]')
                market = get_markets_prices(client, currency.lower(), fiat, qty)
                difference = analyse_market_difference(market)
                if (difference['rate_difference'] > 0):
                    print(f"BUY, earn: {difference['gains']} {fiat.upper()} with trading volume {qty} {fiat.upper()}")
                    print(f"orders: buy: {market['buy']['ordId']} sell: {market['sell']['ordId']}")
                    return {
                        'status': 200,
                        'action': 'BUY',
                        'buyOrdId': market['buy']['ordId'],
                        'sellOrdId': market['sell']['ordId']
                    }
                else:
                    print(f"SELL, loose: {difference['gains']} {fiat.upper()} with trading volume {qty} {fiat.upper()}")
                    print(f"orders: buy: {market['buy']['ordId']} sell: {market['sell']['ordId']}")
            except:
                print(f"Error checking market: [{currency.lower()}-{fiat}]")
                continue
    
    return {
        'status': 200,
        'action': 'NEXT'
    }