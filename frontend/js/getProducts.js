/**
 * Created by akshay,siddharth on 1/28/2017.
 */
var handler = StripeCheckout.configure({
                    key: 'pk_test_HbZ2G2ELK1pvsY2iOIKStdKn',
                    image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
                    locale: 'auto',
                    token: function(token) {
                        // You can access the token ID with `token.id`.\
                        // Get the token ID to your server-side code for use.\
                    }
});
window.addEventListener('popstate', function() {
    handler.close();
});

function processPayment(price,productID){
       handler.open({
           name: 'Stripe.com',
           description: 'Buy Photo Gallery',
           zipCode: true,
           amount: price
       });
    console.log(price+" "+productID);
}
function getProducts() {
    console.log("get products demo call");
    var JSONURL = 'http://localhost:8000/stripe_demo/product/';
    var jwttoken = getCookie("jwttoken");
    console.log("jwt token: " + jwttoken);
    if (!jwttoken) {
        window.location.href = "index.html";
    } else {
        var promise = new Promise(function (success, failure) {
            $.ajax({
                url: JSONURL,
                type: 'GET',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
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
        /////////////////////////////////////////////////////
        ////// Complete rows (having 3 products /////////////
        /////////////////////////////////////////////////////
        for (var i = 0; i < fullRows; i++) {
            photoSection.innerHTML += '<div class="row">';
            for (var j = 0; j < 3; j++) {
                index++;
                var stripeString = "<div class=\"product alert alert-info col-sm-4\">\
                     <img src=\"" + JSONArray[index].url + "\" class=\"img-thumbnail img-responsive\" alt=\"Image not found\">\
                     <div class=\"caption\">\
                    <p>" + JSONArray[index].description + "</p>\
                    </div>\
                     <script src=\"https://checkout.stripe.com/checkout.js\"></script>\
                     <button align=\"center\" class=\"btn btn-success\" id=\"customButton\" onclick='processPayment(JSONArray[index].price,1)'>Pay $ " + JSONArray[index].price + "</button>";


                    //     document.getElementById('customButton').addEventListener('click', function(e) {\
                    //       // Open Checkout with further options:\
                    //       handler.open({\
                    //         name: 'Stripe.com',\
                    //         description: 'Buy Photo Gallery',\
                    //         zipCode: true,\
                    //         amount: " + JSONArray[index].price + "\
                    //     });\
                    //     e.preventDefault();\
                    // });\
                    // Close Checkout on page navigation:\
                  //   window.addEventListener('popstate', function() {\
                  //     handler.close();\
                  // });\
                  // </script>";

                $("#photoSection").append(stripeString);
            }
                    photoSection.innerHTML += '</div>';
        }
        /////////////////////////////////////////////////////
        // Incomplete rows (having less than 3 products//////
        /////////////////////////////////////////////////////
        if(incompleteRows>0){
            photoSection.innerHTML += '<div class="row">';
        }
        for (var k = 0; k < incompleteRows; k++) {
            index++;
            var stripeString = "<div class=\"product alert alert-info col-sm-4\">\
                                 <img src=\"" + JSONArray[index].url + "\" class=\"img-thumbnail img-responsive\" alt=\"Image not found\">\
                                 <div class=\"caption\">\
                                <p>" + JSONArray[index].description + "</p>\
                                </div>\
                                 <button align=\"center\" class=\"btn btn-success\" id=\"customButton\">Pay $ " + JSONArray[index].price + "</button>\
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
                                    amount: " + JSONArray[index].price + "\
                                });\
                                e.preventDefault();\
                                });\
                                // Close Checkout on page navigation:\
                                window.addEventListener('popstate', function() {\
                                      handler.close();\
                                });\
                                </script>";

            $("#photoSection").append(stripeString);
        }
                photoSection.innerHTML += '</div>';
    }
    catch (err) {
        console.log("ERROR in getProducts.js:" + err);
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