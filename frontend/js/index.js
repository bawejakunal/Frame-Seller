var authTokenEndpoint = "http://localhost:8000/stripe_demo/api-token-auth/";
var signUpEndpoint = "http://localhost:8000/stripe_demo/signup/";

function login() {
    username = $("#loginemail");
    password = $("#loginpassword");

    bool1 = check(username);
    bool2 = check(password);

    if (bool1 && bool2) {
        parameters = {
            'username': username.val(),
            'password': password.val(),
        };
        var promise = new Promise(function (success, failure) {
            $.ajax({
                url: authTokenEndpoint,
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
            setTokenCookie(data["token"]);
            window.location.href = "catalog.html"
        }, function (data) {
            showSnackbar(data["non_field_errors"]);
        });
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
            parameters = {
                'first_name': firstname.val(),
                'last_name': lastname.val(),
                'email': email.val(),
                'password': password.val()
            };
            var promise = new Promise(function (success, failure) {
                $.ajax({
                    url: signUpEndpoint,
                    type: 'POST',
                    contentType: "application/json",
                    data: JSON.stringify(parameters),
                    success: function (data) {
                        success(data);
                    },
                    error: function (data) {
                        failure(data.responseText);
                    }
                });
            });

            promise.then(function (data) {
                if (data["success"] == true) {
                    showSnackbar("User registered successfully. You can now login");
                }
                clearSignUpForm();
            }, function (data) {
                var json = JSON.parse(data);
                if (Object.keys(json["error"]).length == 1) {
                    var errorKey = Object.keys(json["error"])[0];
                    showSnackbar(json["error"][errorKey]);
                } else {
                    showSnackbar("An error occured with your sign up. Please check your credentials.");
                }
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
