if (typeof fetchroomlist === 'undefined') {
    fetchroomlist = () => {
        const HTTP = new XMLHttpRequest();
        let url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=rooms';
        if (typeof loggedin != 'undefined' && loggedin) {
            url=`http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=rooms&user=${USERNAME}&token=${TOKEN}`;
        }
        // console.log(url)
        HTTP.open("GET", url);
        HTTP.send();

        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                roomlist = JSON.parse(HTTP.responseText).rooms;
                for (let i =0 ; i<roomlist.length; i++) {
                    makeroom(roomlist[i]);
                }
            }
        }
    }


    makeloginbutton = () => {
        const logindiv = document.getElementById("login");
        if (typeof loggedin === 'undefined' || !loggedin) {
            logindiv.innerHTML = `<button class="ui basic button"
            type="button"
            value="Log In"
            onclick="loginpage()"
            >  
                <i class="icon user"></i>
                Log In/Create Account 
            </button>`
        }
        else {
            logindiv.innerText = `Logged in as ${USERNAME}`
        }
    }

    makereservationbutton = () => {
        const reservationdiv = document.getElementById("reservation");
        isCheckedIn = false;
        if (typeof loggedin === 'undefined' || !loggedin) {
            // do nothing to the div
        }
        else {
            const HTTP = new XMLHttpRequest();
            const url=`http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=isCheckedIn&user=${USERNAME}&token=${TOKEN}`;
            HTTP.open("GET", url);
            HTTP.send();
            HTTP.onreadystatechange = function(){
                if(this.readyState == 4 && this.status==200) {
                    console.log(HTTP.responseText);
                    resp = JSON.parse(HTTP.responseText);
                    if (resp.isCheckedIn) {
                        isCheckedIn = true;
                        const currReservation = document.createElement("div");
                        currReservation.classList.add("currReservation");
                        reservationRoomNum = resp.roomNum;
                        currReservation.innerHTML = `<b> You are currently checked in to room ${reservationRoomNum}, until ${resp.until}.</b>`;
                        reservationdiv.appendChild(currReservation);
                        const checkoutButton = document.createElement("div");
                        checkoutButton.innerHTML = `<button class="ui basic button"
                        type="button"
                        value="Check Out"
                        onclick="submitcheckout()"
                        > 
                            <i class="icon user"></i>
                            Check Out 
                        </button>`;
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
                    isCheckedIn = false;
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


    backtodashboard = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=dashboardPage';
        HTTP.open("GET", url);
        HTTP.send();
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                const doc = document.documentElement;
                setInnerHTML(doc, HTTP.responseText);
                hidenavbarbuttons();
            }
        }
    }

    friendspage = () => {
        if (typeof loggedin === 'undefined' || !loggedin) {
            // not logged in, so go to login page
            loginpage();
        } else {
            const HTTP = new XMLHttpRequest();
            const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=friendsPage';
            HTTP.open("GET", url);
            HTTP.send();
            HTTP.onreadystatechange = function(){
                if(this.readyState == 4 && this.status==200) {
                    const doc = document.documentElement;
                    setInnerHTML(doc, HTTP.responseText);
                    hidenavbarbuttons();
                }
            }
        }
    }

    checkinpage = (roomnum) => {
        if (typeof loggedin === 'undefined' || !loggedin) {
            // not logged in, so go to login page
            loginpage();
        } else {
            const HTTP = new XMLHttpRequest();
            const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=checkinPage';
            HTTP.open("GET", url);
            HTTP.send();
            HTTP.onreadystatechange = function(){
                if(this.readyState == 4 && this.status==200) {
                    const doc = document.documentElement;
                    setInnerHTML(doc, HTTP.responseText);
                    hidenavbarbuttons();
                }
            }
        }
    }

    loginpage = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=loginPage';
        HTTP.open("GET", url);
        HTTP.send();
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                setInnerHTML(doc, HTTP.responseText);
                hidenavbarbuttons();
            }
        }
    }


    setInnerHTML = function(elm, html) {
        elm.innerHTML = html;
        // console.log(document.documentElement.innerHTML);
        // console.log(Array.from(document.head.querySelectorAll("script")));
        Array.from(document.head.querySelectorAll("script")).forEach( oldScript => {
        const newScript = document.createElement("script");
        Array.from(oldScript.attributes)
            .forEach( attr => newScript.setAttribute(attr.name, attr.value) );
        newScript.appendChild(document.createTextNode(oldScript.innerHTML));
        oldScript.parentNode.replaceChild(newScript, oldScript);
        });
    }

    dashboardmain = () => {
        makeloginbutton();
        makereservationbutton();
        fetchroomlist();
        // for(let i = 1; i<=roomlist.length; i++) {
        //     makeroom(roomlist[i]);
        // }
    }

    makeroom = (room) => {
        const dashBoard = document.getElementById("dashboard");
        const newroom = document.createElement("div");
        newroom.className = "ui raised segment";
        const roomnum = room.roomNum;
        const occupancy = room.occupancy;
        const capacity = room.capacity;
        const noiselevel = room.noiseLevel;
        const volumepref = room.volumePref;
        const friendsinroom = room.friends;
        console.log(friendsinroom)
        let friendsdiv = "";
        if (friendsinroom.length > 0) {
            friendsdiv = `<div class="header"> Friends in this Room: `
            let i = 0;
            for (; i< friendsinroom.length-1; i++) {
                friendsdiv = friendsdiv + `${friendsinroom[i]}, `
            }
            friendsdiv = friendsdiv + `${friendsinroom[i]} </div>`
        }

        let volprefdiv = `<p>` + `Volume Preferences: <b>${volumepref.volume}</b>` + `</p>`
        if (volumepref.volume != "none") {
            let numpeople = volumepref.numPeople;
            if (numpeople > 1) {
                volprefdiv = `<p>` + `${numpeople} people prefer: <b>${volumepref.volume}</b>` + `</p>`
            } else {
                volprefdiv = `<p>` + `1 person prefers: <b>${volumepref.volume}</b>` + `</p>`
            }
        }
        let checkinbutton = (typeof isCheckedIn === 'undefined' || !isCheckedIn) ? 
        `<button class="ui fluid medium teal submit button"
            type="button"
            value="Check In"
            onclick="checkinpage()"
        > Check In </button>` : "";
        
        newroom.innerHTML = "<h2>" + `Room ${roomnum}` + "</h2>" +
                            `<div class="ui equal width grid">` +
                                `<div class="column">` +
                                    `<i class="users icon"></i>` +
                                    `<p>` + `Occupancy: ${occupancy}/${capacity}` + "</p>" +
                                "</div>" +
                                `<div class="column">` + 
                                    `<i class="volume up icon"></i>` +
                                    `<p>` + `Current Noise Level: <b>${noiselevel}</b>` + `</p>` +
                                "</div>" +
                                `<div class="column">` + 
                                    `<i class="volume up icon"></i>` +
                                    volprefdiv +
                                "</div>" +
                            "</div>" +
                            friendsdiv +
                            checkinbutton
        dashBoard.appendChild(newroom);
    }

    hidenavbarbuttons = () => {
        if (typeof loggedin === 'undefined' || !loggedin) {
            // not logged in, so show login button
        } else {
            // logged in, so hide login button
            document.getElementById("navbarloginbutton").style.display = "none";
        }
    }
}


dashboardmain();
