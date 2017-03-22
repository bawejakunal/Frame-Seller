function loadVerifyPage() {
    var url = window.location.href;
    url = url.split('#').pop().split('?').pop();
    var pageurl = url.substring(0, url.lastIndexOf('/'));
    pageurl = pageurl + "/verify.html";
    document.getElementById("suvpage").value = pageurl;
}

/**
 * Check login credentials by sending them to authTokenEndpoint and receiving response inside Promise.
 */
function login() {
    username = $("#loginemail");
    password = $("#loginpassword");

    bool1 = check(username);
    bool2 = check(password);

    if (bool1 && bool2) {
        parameters = {
            'email': username.val(),
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
            var response = JSON.parse(data);
            showSnackbar(response["message"]);
        });
    }
}
/**
 * Check sign up credentials of new user by sending them to signUpEndpoint and receiving response inside Promise.
 */
    function signUp() {
        firstname = $("#sufirstname");
        lastname = $("#sulastname");
        email = $("#suemail");
        password = $("#supassword");
        repeatpassword = $("#surepeatpassword");
        verify_page = $("#suvpage");

        var bool1 = check(firstname);
        var bool2 = check(lastname);
        var bool3 = check(email);
        var bool4 = check(password);
        var bool5 = check(repeatpassword);
        var bool6 = check(verify_page);

        if (bool1 && bool2 && bool3 && bool4 && bool5 && bool6) {
            parameters = {
                'firstname': firstname.val(),
                'lastname': lastname.val(),
                'email': email.val(),
                'password': password.val(),
                'verify_page': verify_page.val()
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
                    showSnackbar("User registered successfully. You will receive verification mail shortly.");
                }
                clearSignUpForm();
            }, function (data) {
                var json = JSON.parse(data);
                showSnackbar(json["message"]);
            });
        }
    }

/**
 * clears signup form's fields when user presses sign up button
 */
    function clearSignUpForm() {
        $("#sufirstname").val("");
        $("#sulastname").val("");
        $("#suemail").val("");
        $("#supassword").val("");
        $("#surepeatpassword").val("");
    }
/**
 * check if a form field is submitted with blank input.
 * @param element
 * @return {Boolean} bool
 */
    function check(element) {
        var bool;
        var re_email = /^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
        var re_password = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$/;

        if (element.val() == "") {
            element.addClass("invalid");
            bool = false;
        } else {
            element.removeClass("invalid");
            bool = true;
        }

        if (element.attr('id') == "suemail" &&  !re_email.test(element.val())){
            element.addClass("invalid");
            bool = false;
            showSnackbar("Email id should be of format user@domain.com");
        } else if (element.attr('id') == "supassword"){
            bool = re_password.test(element.val());
            if(!bool){
                element.addClass("invalid");
                showSnackbar("Password must have 1 Special, Numeric, Uppercase and Lowercase Character and of length 8 to 20");
            }
        } else if (element.attr('id') == "surepeatpassword" && element.val() !== "") {
            if ($("#supassword").val() !== element.val()) {
                showSnackbar("Passwords do not match");
                element.addClass("invalid");
                $("supassword").addClass("invalid");
            }
        }
        return bool
    }
