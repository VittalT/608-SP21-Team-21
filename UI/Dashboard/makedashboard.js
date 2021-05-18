if (typeof fetchroomlist === 'undefined') {
    fetchroomlist = () => {
        const HTTP = new XMLHttpRequest();
        let url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=rooms';
        if (typeof loggedin != 'undefined' && loggedin) {
            url=`http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=rooms&user=${USERNAME}&token=${TOKEN}`;
        }
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
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                // doc.innerHTML = HTTP.responseText;
                setInnerHTML(doc, HTTP.responseText)
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
                    console.log(HTTP.responseText);
                    const doc = document.documentElement;
                    // doc.innerHTML = HTTP.responseText;
                    setInnerHTML(doc, HTTP.responseText)
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
                    console.log(HTTP.responseText);
                    const doc = document.documentElement;
                    // doc.innerHTML = HTTP.responseText;
                    setInnerHTML(doc, HTTP.responseText);
                    // TODO: below code to be implemented after the Check In page is created.
                    //roomnum = document.getElementById("roomnum")
                    //roomnum.innerText = roomnum
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
        let friendsdiv = "";
        // if (friendsinroom.length > 0) {
        //     friendsdiv = `<div class="header"> Friends in this Room: `
        //     let i = 0;
        //     for (; i< friendsinroom.length-1; i++) {
        //         friendsdiv = friendsdiv + `${friendsinroom[i].name}, `
        //     }
        //     friendsdiv = friendsdiv + `${friendsinroom[i].name} </div>`
        // }
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
                                    `<p>` + `Volume Preferences: <b>${volumepref}</b>` + `</p>` +
                                "</div>" +
                            "</div>" +
                            friendsdiv +
                            `<button class="ui fluid medium teal submit button"
                                type="button"
                                value="Check In"
                                onclick="checkinpage()"
                            > Check In </button>`
        dashBoard.appendChild(newroom);
    }
}


dashboardmain();
