import requests

r = requests.post('http://localhost:8000/stripe_demo/api-token-auth/', data = {'username':'USERNAME','password':'PWD'})

# get data from request

response = r.json() # this will be in unicode

token = str(response)

token_splitted = token.split('.') # split header, payload, signature