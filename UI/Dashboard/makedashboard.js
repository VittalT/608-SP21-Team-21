

if (typeof fetchroomlist === 'undefined') {
    fetchroomlist = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=rooms';
        HTTP.open("GET", url);
        HTTP.send();

        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                roomlist = JSON.parse(HTTP.responseText);
                for (let i =0 ; i<roomlist.length; i++) {
                    makeroom(roomlist[i]);
                }
            }
        }
    }


    makeloginbutton = () => {
        const logindiv = document.getElementById("login");
        if (typeof loggedin === 'undefined' || !loggedin) {
            logindiv.innerHTML = `<button class="loginbutton"
            type="button"
            value="Log In"
            onclick="loginpage()"
            > Log In/Create Account </button>`
        }
        else {
            logindiv.innerText = `Logged in as ${USERNAME}`
        }
    }

    makereservationbutton = () => {
        const reservationdiv = document.getElementById("reservation");
        if (typeof loggedin === 'undefined' || !loggedin) {
            // do nothing to the div
        }
        else {
            const HTTP = new XMLHttpRequest();
            const url=`http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=ischeckedin&user=${USERNAME}&token=${TOKEN}`;
            HTTP.open("GET", url);
            HTTP.send();
            HTTP.onreadystatechange = function(){
                if(this.readyState == 4 && this.status==200) {
                    console.log(HTTP.responseText);
                    resp = JSON.parse(HTTP.responseText);
                    if (resp.isCheckedIn) {
                        const currReservation = document.createElement("div");
                        currReservation.classList.add("currReservation");
                        reservationRoomNum = resp.roomNum;
                        currReservation.innerText = `You are currently checked in to room ${reservationRoomNum}, until ${resp.until}.`;
                        reservationdiv.appendChild(currReservation);
                        const checkoutButton = document.createElement("div");
                        checkoutButton.innerHTML = `<button class="checkoutButton"
                        type="button"
                        value="Check Out"
                        onclick="checkout()"
                        > Check Out </button>`;
                        reservationdiv.appendChild(checkoutButton);
                    } else {
                        // do nothing
                    }
                }
            }
        }
    }

    submitcheckout = () => {
        const reservationdiv = document.getElementById("reservation");
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        const data=`task=checkout&roomNum=${reservationRoomNum}&user=${USERNAME}&token=${TOKEN}`
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.checkoutSuccess) {
                    backtodashboard();
                } else {
                    const fail = document.createElement("div");
                    fail.classList.add("failedtocheckout");
                    fail.innerText = "Failed to check out, try again later.";
                    reservationdiv.appendChild(fail);
                }
            }
        }
    }


    loginpage = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=loginpage';
        HTTP.open("GET", url);
        HTTP.send();
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                setInnerHTML(doc, HTTP.responseText)
            }
        }
    }


    friendspage = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=friendspage';
        HTTP.open("GET", url);
        HTTP.send();
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                // doc.innerHTML = HTTP.responseText;
                setInnerHTML(doc, HTTP.responseText)
            }
        }
    }

    backtodashboard = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=dashboardpage';
        HTTP.open("GET", url);
        HTTP.send();
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                // doc.innerHTML = HTTP.responseText;
                setInnerHTML(doc, HTTP.responseText)
            }
        }
    }

    setInnerHTML = function(elm, html) {
        elm.innerHTML = html;
        console.log(document.documentElement.innerHTML);
        console.log(Array.from(document.head.querySelectorAll("script")));
        Array.from(document.head.querySelectorAll("script")).forEach( oldScript => {
        const newScript = document.createElement("script");
        Array.from(oldScript.attributes)
            .forEach( attr => newScript.setAttribute(attr.name, attr.value) );
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }

    main = () => {
        makeloginbutton();
        makereservationbutton();
        fetchroomlist();
        for(let i = 1; i<=roomlist.length; i++) {
            makeroom(roomlist[i]);
        }
    }
}


main();
