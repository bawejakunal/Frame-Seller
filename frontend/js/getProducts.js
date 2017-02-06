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
     photoSection.innerHTML += '<div class="col-sm-4">\
     <img src="' + JSONArray[index].url + '" class="img-thumbnail img-responsive" alt="Image not found">\
     <figcaption>' + JSONArray[index].description + '</figcaption>\
     <div class="alert alert-info">\
     <strong>' + JSONArray[index].price + '</strong> \
     </div>\
     <form action="http://e4fb795b.ngrok.io/stripe_demo/order/" method="POST">\
     \x3Cscript\
     src="https://checkout.stripe.com/checkout.js" class="stripe-button"\
     data-key="pk_test_HbZ2G2ELK1pvsY2iOIKStdKn"\
     data-amount="' + JSONArray[index].price + '"\
     data-name="Photo Gallery Buy"\
     data-description="' + JSONArray[index].description + '"\
     data-image="https://stripe.com/img/documentation/checkout/marketplace.png"\
     data-locale="auto"\
     data-zip-code="true">\x3C/script>\
     <input type="hidden" value="' + JSONArray[index].id + '" name="productid">\
     </form>\
     </div>';
     }
     photoSection.innerHTML += '</div>';
     }
     photoSection.innerHTML += '<div class="row">';
     for (var k = 0; k < incompleteRows; k++) {
     index++;
     console.log(index);
     photoSection.innerHTML += '<div class="col-sm-4">\
     <img src="' + JSONArray[index].url + '" class="img-thumbnail img-responsive" alt="Image not found">\
     <figcaption>' + JSONArray[index].description + '</figcaption>\
     <div class="alert alert-info">\
     <strong>' + JSONArray[index].price + '</strong> \
     </div>\
     <form action="http://e4fb795b.ngrok.io/stripe_demo/order/" method="POST">\
     \x3Cscript\
     src="https://checkout.stripe.com/checkout.js" class="stripe-button"\
     data-key="pk_test_HbZ2G2ELK1pvsY2iOIKStdKn"\
     data-amount="' + JSONArray[index].price + '"\
     data-name="Photo Gallery Buy"\
     data-description="' + JSONArray[index].description + '"\
     data-image="https://stripe.com/img/documentation/checkout/marketplace.png"\
     data-locale="auto"\
     data-zip-code="true">\x3C/script>\
     <input type="hidden" value="' + JSONArray[index].id + '" name="productid">\
     </form>\
     </div>';
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