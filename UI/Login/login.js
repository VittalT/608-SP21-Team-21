
if (typeof loginaccount === 'undefined') {
    loginaccount = () => {
        let usernm = document.getElementById("userlogin").value;
        let pass = document.getElementById("pwordlogin").value;
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        const data=`task=login&user=${usernm}&password=${pass}`
        // {
        //     task: "login",
        // 	user: username,
        // 	password: pass
        // };
        console.log(data);
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                // const doc = document.documentElement;
                // // doc.innerHTML = HTTP.responseText;
                // setInnerHTML(doc, HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.loginSuccess) {
                    USERNAME = usernm;
                    TOKEN = resp.token;
                    loggedin = true;
                    backtodashboard();
                } else {
                    el = document.getElementById("loginform");
                    const fail = document.createElement("div");
                    fail.classList.add("failedtologin");
                    fail.innerText = "Incorrect username or password";
                    el.appendChild(fail);
                }
                // TODO: below code to be implemented after the Check In page is created.
                //roomnum = document.getElementById("roomnum")
                //roomnum.innerText = roomnum
            }
        }
    }

    createaccount = () => {
        let username = document.getElementById("usercreateacc").value;
        let pass1 = document.getElementById("pwordcreateacc").value;
        let pass2 = document.getElementById("rtpwordcreateacc").value;
        if (pass1 != pass2)
            //Do something about it
            pass = pass1 //For now
        else
            pass = pass1
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        const data=`task=createAccount&user=${username}&password=${pass}`
        // {
        //     task: "creataccount",
        // 	user: username,
        // 	password: pass
        // };
        console.log(data);
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                // const doc = document.documentElement;
                // // doc.innerHTML = HTTP.responseText;
                // setInnerHTML(doc, HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.createAccountSuccess) {
                    USERNAME = usernm;
                    TOKEN = resp.token;
                    loggedin = true;
                    backtodashboard();
                } else {
                    el = document.getElementById("createaccountform");
                    const fail = document.createElement("div");
                    fail.classList.add("failedtologin");
                    fail.innerText = "Failed to Create Account";
                    el.appendChild(fail);
                }


                // TODO: below code to be implemented after the Check In page is created.
                //roomnum = document.getElementById("roomnum")
                //roomnum.innerText = roomnum
            }
        }
    }

    // var setInnerHTML = function(elm, html) {
    //     elm.innerHTML = html;
    //     Array.from(elm.querySelectorAll("script")).forEach( oldScript => {
    //       const newScript = document.createElement("script");
    //       Array.from(oldScript.attributes)
    //         .forEach( attr => newScript.setAttribute(attr.name, attr.value) );
    //       newScript.appendChild(document.createTextNode(oldScript.innerHTML));
    //       oldScript.parentNode.replaceChild(newScript, oldScript);
    //     });
    //   }
}