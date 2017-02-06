function logoutUser(){
    console.log("Before deleting Cookie= " + getCookie("jwttoken"));
    document.cookie = "jwttoken=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    console.log("After deleting Cookie= " + getCookie("jwttoken"));
    return true;
}

function getOrdersForUser() {
    console.log("getOrdersForUser() demo call");
    var JSONURL = 'http://localhost:8000/stripe_demo/order/';
    var jwttoken = getCookie("jwttoken");
    console.log("token: "+jwttoken);
    if (!jwttoken) {
        // window.location.href = "index.html";
    } else {
        var promise = new Promise(function (success, failure) {
            $.ajax({
                url: JSONURL,
                type: 'GET',
                beforeSend: function (xhr) {
                    xhr.setRequestHeader('Authorization', 'JWT ' + jwttoken);
                },
                dataType: 'jsonp',
                done: function (data, textStatus, request) {
                    success(data);
                },
                fail: function (data, textStatus, request) {
                    failure(data.responseText);
                }
            });
        });
        promise.then(function (data) {
            console.log(data);
        }, function (data) {
            console.log(data);
        });
    }
}