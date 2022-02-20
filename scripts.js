src = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"

function login() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("noaccountlabel").innerHTML = this.responseText;
        }
    };
    const testUser = document.getElementByClass("usernameform");
    const passUser = document.getElementByClass("passwordform");
    xhttp.open("GET", "http://172.28.121.145:5000/login?user=" + testUser + "&pass=" + passUser, true);
    xhttp.send();
}


function signup() {
    const xhttp = new XMLHttpRequest();
    xhttp.onload = function () {
        document.getElementById("noaccountlabel").innerHTML = this.responseText;
    }
    xhttp.open("GET", "http://172.28.121.145:5000/login?user=testUser&pass=", true);
    // xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();
}

function noAccount() {

} // noAccount
