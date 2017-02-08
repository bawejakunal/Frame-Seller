/**
 * Created by akshay on 2/05/2017.
 */
function logoutUser(){
    document.cookie = "jwttoken=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    return true;
}

function getDateFromString(d){
    var date = new Date(d);
    var mins = date.getMinutes();
    if(mins.length==1){
        mins = "0"+mins.toString();
    }
    var returnString = (date.getMonth()+1)+"/"+date.getDate()+"/"+date.getFullYear()+"  "+date.getHours()+":"+mins;
    return returnString;
}

function fillOrders(data){
    var orderSection = document.getElementById('orders');
    var numOrders = data.length;
    for(var i=0; i< numOrders; i++){
        try{
            orderSection.innerHTML +=
             '<div class="well well-lg">\
                  <div class="row">\
                        <div class="col-sm-2">\
                            <img class="img-thumbnail img-responsive" src="'+ data[i].product.url +'">\
                            <div class="caption"><p>' + data[i].product.description + '</p></div>\
                        </div>\
                        <div class="col-sm-5">\
                            <strong>Date Placed on:&nbsp; </strong> '+ getDateFromString(data[i].orderdate)+'<br><br>\
                            <strong>Price:</strong> $ '+ data[i].product.price+'\
                        </div>\
                        <div class="col-sm-5">\
                            <strong>PAYMENT STATUS</strong> <br> '+ data[i].paymentstatus+'\
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
            getNameFromToken();
            fillOrders(data);

        }, function (data) {
            console.log(data);
        });
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

function getNameFromToken(){
    var token = getCookie("jwttoken").split('.')[1];
    var decodedToken =  atob(token);
    console.log(decodedToken);
}