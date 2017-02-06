/**
 * Created by akshay,siddharth on 1/28/2017.
 */
 function getProducts() {
    console.log("get products demo call");
    var JSONURL = 'http://localhost:8000/stripe_demo/product/';
    var jwttoken = getCookie("jwttoken");
    // var JSONstring = '[{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"},{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"},{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"},{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"}]';
    console.log("token");
    console.log(jwttoken);
    if (!jwttoken) {
        window.location.href = "index.html";
    } else {
        var promise = new Promise(function (success, failure) {
            $.ajax({
                url: JSONURL,
                type: 'GET',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', 'JWT '+jwttoken);
                },
                success: function (data) {
                    success(data);
                },
                fail: function (data) {
                    failure(data.responseText);
                },
            });
        });
        promise.then(function (data) {
            console.log(data);
            fillProduct(data);
        }, function (data) {
            console.log(data);
        });
    }

    function fillProduct(data) {
     JSONArray = data;
     var numProducts = JSONArray.length;
     console.log("Number of products=" + numProducts);
     var fullRows = Math.floor(numProducts / 3);
     var incompleteRows = Math.floor(numProducts % 3);
     var index = -1;
     var photoSection = document.getElementById('photoSection');
     try {
         photoSection.innerHTML += '<div class="container">';
         for (var i = 0; i < fullRows; i++) {
             photoSection.innerHTML += '<div class="row">';
             for (var j = 0; j < 3; j++) {
                 index++;
                 console.log(index);

                 var stripeString = "<div class=\"product alert alert-info col-sm-4\">\
                 <img src=\"" + JSONArray[index].url + "\" class=\"img-thumbnail img-responsive\" alt=\"Image not found\">\
                 <div class=\"caption\">\
                <p>"+ JSONArray[index].description + "</p>\
                </div>\
                 <script src=\"https://checkout.stripe.com/checkout.js\"></script>\
                 <button align=\"center\" class=\"btn btn-success\" id=\"customButton\">Pay $ "+JSONArray[index].price+"</button>\
                 <script>\
                 var handler = StripeCheckout.configure({\
                  key: 'pk_test_HbZ2G2ELK1pvsY2iOIKStdKn',\
                  image: 'https://stripe.com/img/documentation/checkout/marketplace.png',\
                  locale: 'auto',\
                  token: function(token) {\
                    // You can access the token ID with `token.id`.\
                    // Get the token ID to your server-side code for use.\
                }\
            });\
            document.getElementById('customButton').addEventListener('click', function(e) {\
              // Open Checkout with further options:\
              handler.open({\
                name: 'Stripe.com',\
                description: 'Buy Photo Gallery',\
                zipCode: true,\
                amount: "+JSONArray[index].price+"\
            });\
            e.preventDefault();\
        });\
        // Close Checkout on page navigation:\
        window.addEventListener('popstate', function() {\
          handler.close();\
      });\
      </script>";

      $("#photoSection" ).append(stripeString);
  }
  photoSection.innerHTML += '</div>';
}
photoSection.innerHTML += '<div class="row">';
for (var k = 0; k < incompleteRows; k++) {
 index++;
 console.log(index);
 var stripeString = "<div class=\"product alert alert-info col-sm-4\">\
                 <img src=\"" + JSONArray[index].url + "\" class=\"img-thumbnail img-responsive\" alt=\"Image not found\">\
                 <div class=\"caption\">\
                <p>"+ JSONArray[index].description + "</p>\
                </div>\
                 <script src=\"https://checkout.stripe.com/checkout.js\"></script>\
                 <button align=\"center\" class=\"btn btn-success\" id=\"customButton\">Pay $ "+JSONArray[index].price+"</button>\
                 <script>\
                 var handler = StripeCheckout.configure({\
                  key: 'pk_test_HbZ2G2ELK1pvsY2iOIKStdKn',\
                  image: 'https://stripe.com/img/documentation/checkout/marketplace.png',\
                  locale: 'auto',\
                  token: function(token) {\
                    // You can access the token ID with `token.id`.\
                    // Get the token ID to your server-side code for use.\
                }\
            });\
            document.getElementById('customButton').addEventListener('click', function(e) {\
              // Open Checkout with further options:\
              handler.open({\
                name: 'Stripe.com',\
                description: 'Buy Photo Gallery',\
                zipCode: true,\
                amount: "+JSONArray[index].price+"\
            });\
            e.preventDefault();\
        });\
        // Close Checkout on page navigation:\
        window.addEventListener('popstate', function() {\
          handler.close();\
      });\
      </script>";

      $("#photoSection" ).append(stripeString);
}
photoSection.innerHTML += '</div>';
}
catch (err) {
 console.log("ERROR in getProducts.js:" + err);
}
}
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}