def hateoas_constraints(mul_order, host, stage, path, productid=None):
    if productid:
        host = host.strip().strip('/')
        stage = stage.strip().strip('/')
        path = path.strip().strip('/')
        if mul_order:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + "/" + path + "/" + str(productid)}]
        else:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + "/" + path}]
    else:
        links = [{"rel": "products.list", "href": "https://" + host + "/" + stage + "/" + path}]
    return links