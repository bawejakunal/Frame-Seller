def validate_json_createorder(json):
    print(json)
    payload_fields = ['event', 'data']

    for field in payload_fields:
        if field not in json:
            print(field)
            return False
        if not isinstance(json[field], dict):
            print 1, json[field], type(json[field])
            return False

    event_fields = ['principal-id', 'host', 'stage']
    event_json = json['event']
    for field in event_fields:
        if field not in event_json:
            print field
            return False
        if not isinstance(event_json[field],unicode):
            print 2, event_json[field], type(event_json[field])
            return False

    if 'product' not in json['data'] or not isinstance(json['data']['product'], dict):
        print('product')
        print json['data']['product'], type(json['data']['product'])
        return False

    if 'stripe_token' not in json['data'] or not isinstance(json['data']['stripe_token'], unicode):
        print('stripe_token')
        print json['data']['stripe_token'], type(json['data']['stripe_token'])
        return False

    product_fields = ['url', 'price', 'id', 'links']
    product_json = json['data']['product']
    for field in product_fields:

        if field not in product_json:
            print(field)
            return False
        if field == product_fields[0] and not isinstance(product_json[field], unicode):
            print(field)
            print(type(product_json[field]))
            return False
        if field == product_fields[1] and not isinstance(product_json[field], int):
            print(field)
            print(type(product_json[field]))
            return False
        if field == product_fields[2] and not isinstance(product_json[field], int):
            print(field)
            print(type(product_json[field]))
            return False
        if field == product_fields[3] and not isinstance(product_json[field], list):
            print(field)
            print(type(product_json[field]))
            return False

    return True


def validate_json_updatepayment(json):
    print(json)

    payload_fields = ['type', 'data']

    for field in payload_fields:
        if field not in json:
            print(field+"not in json")
            return False
        if field == payload_fields[0] and not isinstance(json[field], unicode):
            print(json[field])
            print(type(json[field]))
            return False
        if field == payload_fields[1] and not isinstance(json[field], dict):
            print(json[field])
            print(type(json[field]))
            return False

    return True

    data_fields = ['order_url', 'user_id', 'order_id', 'payment_status', 'order_amount', 'product_url', 'stripe_token', 'order_date']
    data_json = json['data']

    for field in data_fields:
        if field not in data_json:
            print(field+"not in data json")
            return False
        if field == data_fields[0] and not isinstance(data_json[field], unicode):
            return False
        if field == data_fields[1] and not isinstance(data_json[field], unicode):
            return False
        if field == data_fields[2] and not isinstance(data_json[field], unicode):
            return False
        if field == data_fields[3] and not isinstance(data_json[field], int):
            return False
        if field == data_fields[4] and not isinstance(data_json[field], (int, long, float)):
            return False
        if field == data_fields[5] and not isinstance(data_json[field], unicode):
            return False
        if field == data_fields[6] and not isinstance(data_json[field], unicode):
            return False
        if field == data_fields[7] and not isinstance(data_json[field], unicode):
            return False


