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

function verifyUserEmail(vToken, taskToken){
    parameters = {
        'vToken': vToken,
        'taskToken':taskToken,
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
        window.location.href = "index.html";
    }, function (data) {
        var response = JSON.parse(data);
        document.getElementById("verifymessage").innerHTML = '<div class="page-header"><h3> Verification Failed </h3></div>';
    });
}