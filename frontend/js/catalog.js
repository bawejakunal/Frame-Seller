var orderEndpoint = "http://localhost:8000/stripe_demo/order/";
var productEndPoint = "http://localhost:8000/stripe_demo/product/";

window.addEventListener('popstate', function () {
    handler.close();
});

function processPayment(price, productID) {
    var handler = stripe_checkout(productID);
    handler.open({
        name: 'Frame Seller',
        description: 'Buy Photo Frame',
        zipCode: true,
        amount: price * 100
    });
}

function stripe_checkout(product_id) {
    var handler = StripeCheckout.configure({
        key: 'pk_test_sMAdKGvXXhzIt0h42tSNt4if',
        image: 'https://stripe.com/img/documentation/checkout/marketplace.png',
        locale: 'auto',
        token: function (token) {
            var jwttoken = getCookie("jwttoken");
            var promise = new Promise(function (success, failure) {
                var orderdetails = {'product': product_id, 'token': token.id};
                $.ajax({
                    url: orderEndpoint,
                    type: 'POST',
                    contentType: "application/json",
                    data: JSON.stringify(orderdetails),
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
                    },
                    success: function (data) {
                        success(data);
                    },
                    error: function (data) {
                        failure(data.responseText);
                    }
                });
            });
            promise.then(function (data) {
                if (data["success"] == true) {
                    showSnackbar("Your order has been submitted for processing");
                } else {
                    showSnackbar("Couldn't process your order. Please try again");
                }
            }, function (data) {
                showSnackbar("Couldn't process your order. Please try again");
            });
        }
    });
    return handler;
}


function getProducts(jwttoken) {
    var promise = new Promise(function (success, failure) {
        $.ajax({
            url: productEndPoint,
            type: 'GET',
            beforeSend: function (xhr) {
                xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
            },
            success: function (data) {
                success(data);
            },
            error: function (data) {
                failure(data.responseText);
            },
        });
    });
    promise.then(function (data) {
        if (data.length != 0) {
            fillProduct(data);
        } else {
            showSnackbar("There are no products available at this time. Please try again later.");
        }
    }, function (data) {
        showSnackbar("Can't fetch products currently. Please try again later");
    });
}

function fillProduct(data) {
    JSONArray = data;
    var numProducts = JSONArray.length;
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
                var stripeString = "<div class=\"col-sm-4\">\
                    <div class='product alert alert-info '>\
                     <img src=\"" + JSONArray[index].url + "\" class=\"img-thumbnail img-responsive\" \
                     alt=\"Image not found\"> <div class=\"caption\"> <p>" + JSONArray[index].description + "</p>\
                    </div> <script src=\"https://checkout.stripe.com/checkout.js\"></script>\
                     <button align=\"center\" class=\"btn btn-success\" id=\"customButton\"\
                     onclick=\"processPayment(" + JSONArray[index].price + "," + JSONArray[index].id + ");\">Pay $ "
                    + JSONArray[index].price + "</button></div>";

                $("#photoSection").append(stripeString);
            }
            photoSection.innerHTML += '</div>';
        }
        /////////////////////////////////////////////////////
        // Incomplete rows (having less than 3 products//////
        /////////////////////////////////////////////////////
        if (incompleteRows > 0) {
            photoSection.innerHTML += '<div class="row">';
        }
        for (var k = 0; k < incompleteRows; k++) {
            index++;
            var stripeString = "<div class=\"col-sm-4\">\
                                <div class='product alert alert-info'>\
                                 <img src=\"" + JSONArray[index].url + "\" class=\"img-thumbnail img-responsive\"\
                                 alt=\"Image not found\"> <div class=\"caption\">\
                                <p>" + JSONArray[index].description + "</p> </div> <button align=\"center\"\
                                class=\"btn btn-success\" id=\"customButton\" onclick=\"processPayment("
                                + JSONArray[index].price + "," + JSONArray[index].id + ");\">Pay $ "
                                + JSONArray[index].price + "</button></div>";
            $("#photoSection").append(stripeString);
        }
        photoSection.innerHTML += '</div>';
    }
    catch (err) {
        console.log("ERROR in getProducts.js:" + err);
    }
}