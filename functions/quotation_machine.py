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
    return response

def quotation_machine(client, currencies, fiats):
    for currency in currencies:
        for fiat in fiats:
            fiat_currency = fiat['name']
            qty = fiat['qty']
            print("--------------------")
            try:
                if currency == fiat_currency:
                    continue
                print(f'Checking market: [{currency}-{fiat_currency}]')
                market = get_markets_prices(client, currency, fiat_currency, qty)
                difference = analyse_market_difference(market)
                if (difference['rate_difference'] > 0):
                    print(f"EXECUTE, earn: {difference['gains']} {fiat_currency} with trading volume {qty} {fiat_currency}")
                    print(f"orders: buy: {market['buy']['ordId']} sell: {market['sell']['ordId']}")
                    return {
                        'status': 200,
                        'action': 'EXECUTE',
                        'buyOrdId': market['buy']['ordId'],
                        'sellOrdId': market['sell']['ordId']
                    }
                else:
                    print(f"NEXT, loose: {difference['gains']} {fiat_currency} with trading volume {qty} {fiat_currency}")
                    print(f"orders: buy: {market['buy']['ordId']} sell: {market['sell']['ordId']}")
            except:
                print(f"Error checking market: [{currency}-{fiat_currency}]")
                continue
    
    return {
        'status': 200,
        'action': 'NEXT'
    }