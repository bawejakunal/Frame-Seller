/**
 * Created by akshay on 3/19/2017.
 */
function getUrlVars()
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    return vars;
}

function verifyUserEmail(email,token){
    parameters = {
        'uemail': email,
        'vtoken': token,
    };
    var promise = new Promise(function (success, failure) {
        $.ajax({
            url: verifyCustomerEndPoint,
            type: 'POST',
            contentType: "application/json",
            data: JSON.stringify(parameters),
            success: function (data) {
                success(data);
            },
            error: function (data) {
                failure(data.responseText);
            }
        })
    });

    promise.then(function (data) {
        console.log(data);
        document.getElementById("verifymessage").innerHTML = '<div class="page-header"><h3>Congrats! Your email has been verified successfully.</h3>' +
            '<a href="index.html">Click here to login page</a></div>';
    }, function (data) {
        var response = JSON.parse(data);
        console.log(data);
        document.getElementById("verifymessage").innerHTML = '<div class="page-header"><h3>'+response.message+'</h3></div>';
    });
}