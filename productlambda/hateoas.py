def hateoas_constraints(mul_order, host, stage, path, productid=None):
    if productid:
        if mul_order:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + path + "/" + str(productid)}]
        else:
            links = [{"rel": "self", "href": "https://" + host + "/" + stage + path}]
    else:
        links = [{"rel": "products.list", "href": "https://" + host + "/" + stage + path}]
    return links