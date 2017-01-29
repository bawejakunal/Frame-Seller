/**
 * Created by akshay on 1/28/2017.
 */
function getProducts() {
var JSONstring = '[{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"},{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"},{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"},{"url": "https://c1.staticflickr.com/1/728/31226388014_5558604d0f_k.jpg", "price": 50.0, "id": 1, "description": "Brooklyn Bridge"}, {"url": "https://c1.staticflickr.com/6/5763/20977162524_c8931fe2d3_k.jpg", "price": 25.0, "id": 2, "description": "F1 Racing"}]';

var JSONArray = JSON.parse(JSONstring);

JSONArray.forEach(function(product) {
    console.log(product.id);
    console.log(product.description);
    console.log(product.url);
    console.log(product.price);
});

var numProducts = JSONArray.length;
console.log(numProducts);

var fullRows = numProducts/3;
var incompleteRows = numProducts%3;
var index = -1;
document.body.innerHTML += '<div class="container">';
    for(var i=0;i<fullRows;i++){
        document.body.innerHTML += '<div class="row">';
        for(var j=0;j<3;j++){
            index++;
            document.body.innerHTML += '<div class="col-sm-4">\
                <img src="'+JSONArray[index].url+'" class="img-thumbnail img-responsive" alt="Image not found">\
                <figcaption>'+JSONArray[index].description+'</figcaption>\
                <div class="alert alert-info">\
                    <strong>'+JSONArray[index].price+'</strong> <button type="button" class="btn btn-success">Buy</button>\
                </div>\
            </div>';
        }
        document.body.innerHTML += '</div>';
    }
    document.body.innerHTML += '<div class="row">';
    for(var k=0;k<incompleteRows;k++){
        index++;
        document.body.innerHTML += '<div class="col-sm-4">\
                <img src="'+JSONArray[index].url+'" class="img-thumbnail img-responsive" alt="Image not found">\
                <figcaption>'+JSONArray[index].description+'</figcaption>\
                <div class="alert alert-info">\
                    <strong>'+JSONArray[index].price+'</strong> <button type="button" class="btn btn-success">Buy</button>\
                </div>\
            </div>';
    }
    document.body.innerHTML += '</div>';
}