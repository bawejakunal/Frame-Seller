function logoutUser(){
    document.cookie = "jwttoken=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    return true;
}

function getDateFromString(d){
    var date = new Date(d);
    var mins = date.getMinutes();
    if(mins.length==1){
        mins = "0"+mins.toString();
    }
    var returnString = (date.getMonth()+1)+"/"+date.getDate()+"/"+date.getFullYear()+"  "+date.getHours()+":"+mins;
    return returnString;
}

function checkToken(){
    var jwttoken = getCookie("jwttoken");
    console.log("jwt token: " + jwttoken);
    if (!jwttoken) {
        window.location.href = "index.html";
    } else {
        return jwttoken;
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