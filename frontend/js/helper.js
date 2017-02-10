/**
 * Deletes the JWT token cookie and returns true
 * @returns {boolean}
 */
function logoutUser() {
    document.cookie = "jwttoken=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    return true;
}

/**
 * Returns formatted data mm/dd/yyyy from date object
 * @param d
 * @returns {string}
 */
function getDateFromString(d) {
    var date = new Date(d);
    var mins = date.getMinutes();
    if (mins.length == 1) {
        mins = "0" + mins.toString();
    }
    var returnString = (date.getMonth() + 1) + "/" + date.getDate() + "/" + date.getFullYear() + "  " + date.getHours() + ":" + mins;
    return returnString;
}

/**
 * Check token checks whether the JWT token is valid and redirects to index.html if not
 * @returns {string}
 */
function checkToken() {
    var jwttoken = getCookie("jwttoken");
    console.log("jwt token: " + jwttoken);
    if (!jwttoken) {
        window.location.href = "index.html";
    } else {
        return jwttoken;
    }
}

/**
 * Retrives the cookie for the given string name
 * @param cname
 * @returns {string}
 */
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

/**
 * Shows the snackbar for 3 seconds for given div of id "snackbar"
 * @param text
 */
function showSnackbar(text) {
    $("#snackbar").text(text);
    $("#snackbar").attr("class", "show");

    // After 3 seconds, remove the show class from DIV
    setTimeout(function () {
        $("#snackbar").attr("class", "");
    }, 3000);
}

/**
 * Set the given jwttoken in cookie for the specified expiration time
 * @param jwttoken
 */
function setTokenCookie(jwttoken) {
    var jwtpayload = jwttoken.split(".")[1];
    var json = JSON.parse(window.atob(jwtpayload));
    var exptime = json["exp"];
    var d = new Date();
    d.setTime(parseInt(exptime * 1000));
    var expires = "expires=" + d.toUTCString();
    console.log(expires);
    document.cookie = "jwttoken=" + jwttoken + ";" + expires + ";path=/";
}