var orderEndpoint = "http://localhost:8000/stripe_demo/order/";

function fillCustomerName(jwttoken) {
    var token = jwttoken.split('.')[1];
    var decodedToken = atob(token);
    var tokenjson = JSON.parse(decodedToken);
    console.log(tokenjson["first_name"] + " " + tokenjson["last_name"]);
    $("#customername").text("Hello, " + tokenjson["first_name"] + " " + tokenjson["last_name"]);
}

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
            fillOrders(data);
        } else {
            showSnackbar("You have no orders as of now");
        }
    }, function (data) {
        showSnackbar("Failed to fetch orders. Please try again later.");
    });
}

function fillOrders(data) {
    var orderSection = document.getElementById('orders');
    var numOrders = data.length;
    for (var i = 0; i < numOrders; i++) {
        try {
            var paymentinfo = getPaymentInfoTag(data[i].product.paymentstatus);
            orderSection.innerHTML +=
                '<div class="well well-lg">\
                     <div class="row">\
                           <div class="col-sm-2">\
                               <img class="img-thumbnail img-responsive" src="' + data[i].product.url + '">\
                            <div class="caption"><p>' + data[i].product.description + '</p></div>\
                        </div>\
                        <div class="col-sm-5">\
                            <strong>Date Placed on:&nbsp; </strong> ' + getDateFromString(data[i].orderdate) + '<br><br>\
                            <strong>Price:</strong> $ ' + data[i].product.price + '\
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
    }
}

function getPaymentInfoTag(orderStatus) {
    if (orderStatus == "UNPAID") {
        return '<span class="paymentinfo alert alert-warning"><strong>PAYMENT STATUS</strong> <br> ' + orderStatus + '</span>';
    } else if (orderStatus == "PAID") {
        return '<span class="paymentinfo alert alert-success"><strong>PAYMENT STATUS</strong> <br> ' + orderStatus + '</span>';
    } else {
        return '<span class="paymentinfo alert alert-danger"><strong>PAYMENT STATUS</strong> <br> ' + orderStatus + '</span>';
    }
}