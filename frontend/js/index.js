function login() {
    username = $("#loginemail");
    password = $("#loginpassword");

    bool1 = check(username);
    bool2 = check(password);

    if (bool1 && bool2) {
        var promise = new Promise(function (success, failure) {
            parameters = {
                'username': username.val(),
                'password': password.val(),
            };
            //console.log(parameters);
            var request = $.post("http://localhost:8000/stripe_demo/api-token-auth/", parameters, function (data) {
                //console.log(data);
            })
                .done(function (data, textStatus, request) {
                    //console.log(data);
                    //console.log(request.getAllResponseHeaders());
                    success(data);
                })
                .fail(function (data, textStatus, request) {
                    //console.log(data);
                    //console.log(data.getAllResponseHeaders())
                    failure(data.responseText);
                })
        });
        promise.then(function (data) {
            console.log(data);
            var jwttoken = data["token"];
            var jwtpayload = jwttoken.split(".")[1];
            var json = JSON.parse(window.atob(jwtpayload));
            var exptime = json["exp"];
            var d = new Date();
            d.setTime(parseInt(exptime*1000));
            var expires = "expires=" + d.toUTCString();
            console.log(expires);
            document.cookie = "jwttoken=" + jwttoken + ";" + expires + ";path=/";
            window.location.href = "catalog.html"
        }, function (data) {
            alert(data);
        });
    }
}

function signUp() {
    firstname = $("#sufirstname");
    lastname = $("#sulastname");
    email = $("#suemail");
    password = $("#supassword");
    repeatpassword = $("#surepeatpassword");

    var bool1 = check(firstname);
    var bool2 = check(lastname);
    var bool3 = check(email);
    var bool4 = check(password);
    var bool5 = check(repeatpassword);

    if (bool1 && bool2 && bool3 && bool4 && bool5) {
        var promise = new Promise(function (success, failure) {
            parameters = {
                'first_name': firstname.val(),
                'last_name': lastname.val(),
                'email': email.val(),
                'password': password.val()
            };
            console.log(parameters);
            $.ajax({
                url: 'http://localhost:8000/stripe_demo/signup/',
                type: 'POST',
                contentType: "application/json",
                data: JSON.stringify(parameters),
                success: function (data) {
                    success(data);
                },
                error: function (data) {
                    console.log(data);
                    failure(data);
                }
            });
        });

        promise.then(function (data) {
            alert("User registered successfully. You can now login");
            clearSignUpForm();
        }, function (data) {
            var json = JSON.parse(data);
            alert(json["error"]);
        });
    }
}

function clearSignUpForm() {
    $("#sufirstname").val("");
    $("#sulastname").val("");
    $("#suemail").val("");
    $("#supassword").val("");
    $("#surepeatpassword").val("");
}

function check(element) {
    var bool;
    console.log(element.val());
    if (element.val() == "") {
        element.addClass("invalid");
        bool = false;
    } else {
        element.removeClass("invalid");
        bool = true;

    }

    if (element.attr('id') == "surepeatpassword" && element.val() !== "") {
        if ($("#supassword").val() !== element.val()) {
            alert("Passwords do not match");
            element.addClass("invalid");
            $("supassword").addClass("invalid");
        }
    }
    return bool
}
