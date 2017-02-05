function logoutUser(){
    console.log("Before deleting Cookie= " + getCookie("jwttoken"));
    document.cookie = "jwttoken=;expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    console.log("After deleting Cookie= " + getCookie("jwttoken"));
    return true;
}