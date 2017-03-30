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

function verifyUserEmail(email, token, taskToken, verify){
    var verifyurl;
    if(verify == "succeed") {
        verifyurl = verifyCustomerSucceedEndPoint;
    } else {
        verifyurl = verifyCustomerFailEndPoint;
    }

    parameters = {
        'uemail': email,
        'vtoken': token,
        'taskToken':taskToken,
    };
    var promise = new Promise(function (success, failure) {
        $.ajax({
            url: verifyurl,
            type: 'GET',
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
        document.getElementById("verifymessage").innerHTML = '<div class="page-header"><h3>Congrats! Your email has been verified successfully.</h3>' +
            '<a href="index.html">Click here to login page</a></div>';
    }, function (data) {
        var response = JSON.parse(data);
        document.getElementById("verifymessage").innerHTML = '<div class="page-header"><h3>'+response.message+'</h3></div>';
    });
}