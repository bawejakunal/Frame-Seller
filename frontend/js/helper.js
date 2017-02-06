/**
 * Created by akshay on 2/05/2017.
 */
function logoutUser(){
    document.cookie = "jwttoken=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    return true;
}

function fillOrders(data){
    var orderSection = document.getElementById('orders');
    var numOrders = data.length;
    for(var i=0; i< numOrders; i++){
        try{
            orderSection.innerHTML +=
             '<div class="well">\
                  <div class="row">\
                        <div class="col-md-4">\
                            <img class="img-thumbnail img-responsive" src="'+ data[i].product.url +'">\
                            <figcaption>' + data[i].product.description+'</figcaption></div>\
                        </div>\
                        <div class="col-md-4">\
                            Date Placed on:'+ data[i].orderdate+'<br>\
                            Price: $ '+ data[i].product.price+'\
                        </div>\
                        <div class="col-md-4">\
                            PAYMENT STATUS: <br> '+ data[i].paymentstatus+'\
                        </div>\
                </div>\
            </div>';
        }
        catch (err){
            console.log(err);
        }
    }
}

function getOrdersForUser() {
    var JSONURL = 'http://localhost:8000/stripe_demo/order/';
    var jwttoken = getCookie("jwttoken");
    console.log("token: "+jwttoken);
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
                }
            });
        });
        promise.then(function (data) {
            console.log(data);
            fillOrders(data);

        }, function (data) {
            console.log(data);
        });
    }
}