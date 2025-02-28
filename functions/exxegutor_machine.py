def exxegutor_machine(client, ordIds):
    for id in ordIds:
        client.request('POST', '/v1/converts/quotations:confirm', body={
            'ordId': id
        })
        print(f'Order {id} executed')

    return
