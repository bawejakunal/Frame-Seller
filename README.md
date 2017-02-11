# Stripe Demo

## A Team Has No Name

### Team Members
1. Abhijeet Mehrotra (am4586)
2. Akshay Nagpal (an2756)
3. Kunal Baweja (kb2896)
4. Siddharth Shah (sas2387)

## URLs
1. **S3 frontend**: http://s3-us-west-2.amazonaws.com/stripe6998/index.html
2. **Elastic Beanstalk (API URL)**: http://stripedeploy.pmi6pbp3mg.us-west-2.elasticbeanstalk.com/api/

## API endpoints
### Auth service
<dl>
  <dt>POST api/api-token-auth/</dt>
  
  ```json
  {
   "username": "dummy@user.com",
   "password": "password"
}
   ```
  #####Response: Success
   ```json
{"token":"JWT_TOKEN_HERE"}
```
#####Response: Failure
```json
{"detail":"authorization failure"}
```
  ### SignUp service
  <dt>POST api/signup/</dt>
  
  #####Request parameter
  ```json
  parameters = {
                'first_name': "foo",
                'last_name': "bar",
                'email': "foobar@gmail.com",
                'password': "password"
            };
  ```
  #####Response: Success
  ```json
    {"success":true}
```
#####Response: Failure
```json
{
   "success": false,
   "error": "failure message here"
}
```
  ### Fetch product catalog service
  <dt>GET api/product/</dt>
  
 #####Response: Success
 
  ```json
  [
  {
    "id": 1,
    "price": 100,
    "description": "Brooklyn Bridge",
    "url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg"
  },
  {
    "id": 2,
    "price": 150,
    "description": "Singapore Grand Prix",
    "url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg"
  }
]
  ```
  ###Fetch orders of logged in user
  <dt>GET api/order/</dt>
  
  #####Response: Success
  
  ```json
[
  {
    "id": 14,
    "user": 5,
    "orderdate": "2017-02-11T02:40:24.333429Z",
    "paymentstatus": "PAID",
    "product": {
      "id": 1,
      "price": 100,
      "description": "Brooklyn Bridge",
      "url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg"
    }
  },
  {
    "id": 15,
    "user": 5,
    "orderdate": "2017-02-11T02:40:56.373584Z",
    "paymentstatus": "PAID",
    "product": {
      "id": 2,
      "price": 150,
      "description": "Singapore Grand Prix",
      "url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg"
    }
  }
]
```

  ### Submit order &amp; stripe token to backend
  <dt>POST api/order/</dt>
  
  ```json
{
    "token": "STRIPE_CLIENT_TOKEN",
    "product": "PRODUCT_ID"
}
   ```
  #####Response: Success
   ```json
{
  "success": true
}
```
</dl>

## Architecture
![Architecture Diagram](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/Architecture.jpg?token=AEfjci-OnBMNofT_MGshD_k4ilopAdSkks5Yp6fwwA%3D%3D "Architecture Diagram")

## Tech Stack
1. Python (Django REST Framework)
2. HTML5, CSS, Javascript
3. jQuery, Bootstrap
4. MySQL

## Deployment
1. Front end static files hosted on S3 bucket
2. Database hosted on Amazon RDS
3. Backend server hosted on Elastic Beanstalk (Load Balancer + EC2 instance)

## Communication with the Stripe Service
### Client Side
Stripe.js was used to integrate payment popup on client side'
### Server Side
Server end uses the Charge API to communicate with the Stripe service and store the order **meta data** on Stripe and the order status in the database
```python
charge = stripe.Charge.create(
            amount=int(product.price*100),
            currency="usd",
            metadata={"order_id": order_id},
            source=stripe_token);
```
## Screenshots
![Homepage](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/home.png?token=AEfjcjQ9VMv2yIekNWJe5cetgrbk856Rks5Yp6qQwA%3D%3D "Homepage")

![Catalog](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/card_popup.png?token=AEfjcvJmBo945Nja1luvW5o3EFUZdVOTks5Yp6gLwA%3D%3D "Catalog")

![Card Popup](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/card_popup.png?token=AEfjcj_5Y3tZOmL6VHWmy5Rw9fxFKj1Aks5Yp6s9wA%3D%3D "Card Popup")

![Payment submitted](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/payment_submitted.png?token=AEfjcuVDduoWWE_6YJ-WqK6GiiBtPrIfks5Yp6r7wA%3D%3D "Payment submitted")

![Orders](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/orders.png?token=AEfjcn3LhHthr4Ahlv7TUCTd4r6143HKks5Yp6rOwA%3D%3D "Orders by user")

![Stripe Oder Meta](https://raw.githubusercontent.com/bawejakunal/stripe-demo/master/screenshots/stripe_order_meta.png?token=AEfjcqrMeDc4srLO5PE9fCWJVPQQ61SKks5Yp6sRwA%3D%3D "Stripe Metadata")


## Further Improvements
1. Use AngularJS in future assignments
2. As suggested by Prof. Donald Ferguson, segregate the microservices further into Order, Payment and User.
3. Add randomly generated `idempotency_key` in `stripe.Charge.create()` method call to implement [Stripe Idempotent Requests](https://stripe.com/docs/api/python#idempotent_requests) for retrying payment requests that fail due to network errors. 