/**
 * render first and last name of customer in header of profile.html from decoded token value.
 * @param jwttoken
 */
function fillCustomerName(jwttoken) {
    var token = jwttoken.split('.')[1];
    var decodedToken = atob(token);
    var tokenjson = JSON.parse(decodedToken);
    $("#customername").text("Hello, " + tokenjson["firstname"] + " " + tokenjson["lastname"]);
}
/**
 * GET request to orderEndpoint to get orders json for logged in user.
 * @param jwttoken
 */
function getOrdersForUser(jwttoken) {
    var promise = new Promise(function (success, failure) {
        $.ajax({
            url: orderEndpoint,
            type: 'GET',
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
        if (data.length != 0) {
            fillOrders(data, jwttoken);
        } else {
            showSnackbar("You have no orders as of now");
        }
    }, function (data) {
        showSnackbar("Failed to fetch orders. Please try again later.");
    });
}
/**
 * render orders json on HTML DOM.
 * @param data
 */
function fillOrders(orderdata, jwttoken) {
    orders = orderdata["orders"]
    var orderSection = document.getElementById('orders');
    var numOrders = orders.length;
    for (var i = 0; i < numOrders; i++) {
        for(var j=0; j <orders[i].links.length; j++){
            if(orders[i].links[j].rel == "order.product"){
                product_url = orders[i].links[j].href;
                console.log(product_url);
            }
        }

        var promise = new Promise(function (success, failure) {
            $.ajax({
                url: product_url,
                type: 'GET',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
                },
                success: function (data) {
                    success(data,orders[i]);
                },
                error: function (data) {
                    failure(data.responseText);
                }
            });
        });
        promise.then(function (data, order) {
            console.log(data);
            try {
                var paymentinfo = getPaymentInfoTag(order.paymentstatus);
                orderSection.innerHTML +=
                    '<div class="well well-lg">\
                         <div class="row">\
                               <div class="col-sm-2">\
                                   <img class="img-thumbnail img-responsive" src="' + data.url + '">\
                                <div class="caption"><p>' + data.description + '</p></div>\
                            </div>\
                            <div class="col-sm-5">\
                                <strong>Date Placed on:&nbsp; </strong> ' + getDateFromString(order.orderdate) + '<br><br>\
                                <strong>Price:</strong> $ ' + data.price + '\
                            </div>\
                            <div class="col-sm-5">\
                                ' + paymentinfo + '\
                            </div>\
                    </div>\
                 </div>';
            }
            catch (err) {
                console.log(err);
            }
        }, function (data) {
            showSnackbar("Failed to fetch orders. Please try again later.");
        });

    }
}
/**
 * decide color of container based on payment status.
 * @param orderStatus
 * @returns {string}
 */
function getPaymentInfoTag(orderStatus) {
    if (orderStatus == "UNPAID") {
        return '<span class="paymentinfo alert alert-warning"><strong>PAYMENT STATUS</strong> <br> ' + orderStatus + '</span>';
    } else if (orderStatus == "PAID") {
        return '<span class="paymentinfo alert alert-success"><strong>PAYMENT STATUS</strong> <br> ' + orderStatus + '</span>';
    } else {
        return '<span class="paymentinfo alert alert-danger"><strong>PAYMENT STATUS</strong> <br> ' + orderStatus + '</span>';
    }
}