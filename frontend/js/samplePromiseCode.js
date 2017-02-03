/**
 * Created by akshay on 2/3/2017.
 */
// Simple code to understand promises and their syntax
var productsJson = new Promise(function(resolve,reject){
	var numProducts = 3 //JSON recieved
	if(numProducts>0){
  	resolve(numProducts); //we got product json successsfully
  }
  else{
  	reject("Sorry could not get JSON from endpoint. Either there are no more products or there is some error.");
  }
});

productsJson
	.then(
		function(data){
			console.log("recieved "+data+" products");
		})
  .catch(
  	function(data){
    	console.log(data);
    });
