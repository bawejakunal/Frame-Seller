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
 * GET request to pendingOrderEndpoint to get pending orders json for logged in user.
 * @param jwttoken
 */
function getPendingOrdersForUser(jwttoken) {
    var promise = new Promise(function (success, failure) {
        $.ajax({
            url: pendingOrderEndpoint,
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
            fillPendingOrders(data, jwttoken);
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
    var orders = orderdata["orders"];
    var orderSection = document.getElementById('orders');
    var numOrders = orders.length;
    var producturls = new Set();
    var allproductinfo = {};

    // fill product URLs to producturls
    for (var i = 0; i < numOrders; i++) {
        for (var j = 0; j < orders[i].links.length; j++) {
            if (orders[i].links[j].rel == "order.product") {
                producturls.add(orders[i].links[j].href);
            }
        }
    }
    // fill product info into allproductinfo
    var getAllProductsPromise = new Promise(function (success1, failure1) {
        var productfetchcount = 0;
        producturls.forEach(function(producturl) {
            var getSingleProductPromise = new Promise(function (success2, failure2) {
                $.ajax({
                    url: producturl,
                    type: 'GET',
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
                    },
                    success: function (data) {
                        success2(data);
                    },
                    error: function (data) {
                        failure2(data.responseText);
                    }
                });
            });

            getSingleProductPromise.then(function (data) {
                allproductinfo[data.id] = data;
                productfetchcount++;
                if(productfetchcount == producturls.size){
                    success1();
                }
            }, function (data){
                // ignore if few products are not loaded
            });
        });
    });

    getAllProductsPromise.then(function () {
        for(var k=0; k < numOrders; k++) {
            var paymentinfo = getPaymentInfoTag(orders[k].payment_status);
            var productinfo = allproductinfo[orders[k].product_id];
            orderSection.innerHTML +=
                '<div class="well well-lg">\
                     <div class="row">\
                           <div class="col-sm-2">\
                               <img class="img-thumbnail img-responsive" src="' + productinfo.url + '">\
                        <div class="caption"><p>' + productinfo.description + '</p></div>\
                    </div>\
                    <div class="col-sm-5">\
                        <strong>Date Placed on:&nbsp; </strong> ' + getDateFromString(orders[k].order_date) + '<br><br>\
                        <strong>Price:</strong> $ ' + productinfo.price + '\
                    </div>\
                    <div class="col-sm-5">\
                        ' + paymentinfo + '\
                    </div>\
                </div>\
             </div>';
        }
    }, function () {
            showSnackbar("Failed to fetch completed orders. Please try again later.");
    });
}

/**
 * render pending orders json on HTML DOM.
 * @param data
 */
function fillPendingOrders(orderdata, jwttoken) {
    var orders_p = orderdata["orders"];
    var orderSection = document.getElementById('pending-orders');
    var numOrders = orders_p.length;
    var producturls = new Set();
    var allproductinfo = {};
    for (var i = 0; i < numOrders; i++) {
        for (var j = 0; j < orders_p[i].links.length; j++) {
            if (orders_p[i].links[j].rel == "order.product") {
                producturls.add(orders_p[i].links[j].href);
            }
        }
    }

    var getAllProductsPromise = new Promise(function (success1, failure1) {
        var productfetchcount = 0;
        producturls.forEach(function(producturl) {
            var getSingleProductPromise = new Promise(function (success2, failure2) {
                $.ajax({
                    url: producturl,
                    type: 'GET',
                    beforeSend: function (xhr) {
                        xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
                    },
                    success: function (data) {
                        success2(data);
                    },
                    error: function (data) {
                        failure2(data.responseText);
                    }
                });
            });

            getSingleProductPromise.then(function (data) {
                allproductinfo[data.id] = data;
                productfetchcount++;
                if(productfetchcount == producturls.size){
                    success1();
                }
            }, function (data){
                // ignore if few products are not loaded
            });
        });
    });

    getAllProductsPromise.then(function () {
        for(var k=0; k < numOrders; k++) {
            var productinfo = allproductinfo[orders_p[k].product_id];
            orderSection.innerHTML +=
                '<div class="well well-lg">\
                     <div class="row">\
                           <div class="col-sm-2">\
                               <img class="img-thumbnail img-responsive" src="' + productinfo.url + '">\
                        <div class="caption"><p>' + productinfo.description + '</p></div>\
                    </div>\
                    <div class="col-sm-5">\
                        <strong>Price:</strong> $ ' + productinfo.price + '\
                    </div>\
                    <div class="col-sm-5">\
                    </div>\
                </div>\
             </div>';
        }
    }, function () {
            showSnackbar("Failed to fetch pending orders. Please try again later.");
    });
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