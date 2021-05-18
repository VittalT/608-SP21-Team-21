
if (typeof makefriend === 'undefined') {
    // fakefriends = [{"name": "bob", "inRoom":true, "room":"1-115"},
    // {"name": "rob", "inRoom":false, "room":"1-115"},
    // {"name": "tom", "inRoom":false, "room":"1-115"},
    // {"name": "aaa", "inRoom":true, "room":"2-222"},]

    makefriend = (friendobj) => {
        const friendlistdiv = document.getElementById("friendslistbox");
        const newfriend = document.createElement("div");
        onlinediv = "";
        if (friendobj.inRoom) {
            onlinediv = onlinediv + `<p>Currently checked into room: <b>${friendobj.room}</b></p>`
        }
        
        newfriend.innerHTML = `<div class="ui raised segment">` +
        "<h2>" + friendobj.name + "</h2>" +
        onlinediv +
        `<div class="ui equal width grid">` +
            `<div class="column">` +
                    `<button class="ui fluid medium orange submit button"
                    type="button"
                    value="removefriendbutton"
                    onclick="removefriend(${friendobj.name})"
                > Remove Friend </button>`
            "</div>" +
            `<div class="column"></div>` +
            `<div class="column"></div>` +
        "</div>" +
        "</div>";
        friendlistdiv.appendChild(newfriend);
    }

    makeincomingfriend = (friendobj) => {
        const friendrequestsdiv = document.getElementById("friendsrequestsbox");
        const newfriend = document.createElement("div");
        newfriend.innerHTML = `<div class="ui raised segment">` +
        "<h2>" + friendobj.name + "</h2>" +
        onlinediv +
        `<div class="ui equal width grid">` +
            `<div class="column">` +
                    `<button class="ui fluid medium orange submit button"
                    type="button"
                    value="ignorerequestbutton"
                    onclick="ignorerequest(${friendobj.name})"
                > Ignore Request </button>`
            "</div>" +
            `<div class="column">` +
                    `<button class="ui fluid medium olive submit button"
                    type="button"
                    value="addfriendbutton"
                    onclick="acceptfriend(${friendobj.name})"
                > Accept Request </button>`
            "</div>" +
            `<div class="column"></div>` +
        "</div>" +
        "</div>";
        friendrequestsdiv.appendChild(newfriend);
    }

    fetchfriendlist = () => {
        const HTTP = new XMLHttpRequest();
        const url=`http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=friends&user=${USERNAME}&token=${TOKEN}`;
        HTTP.open("GET", url);
        HTTP.send();

        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                friendlist = JSON.parse(HTTP.responseText);
                for (let i = 0; i<friendlist.length; i++) {
                    makefriend(friendlist[i]);
                }
            }
        }
    }

    fetchrequestlist = () => {
        const HTTP = new XMLHttpRequest();
        const url=`http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=friendRequests&user=${USERNAME}&token=${TOKEN}`;
        HTTP.open("GET", url);
        HTTP.send();

        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                friendrequests = JSON.parse(HTTP.responseText);
                for (let i = 0; i<friendlist.length; i++) {
                    makeincomingfriend(friendrequests[i]);
                }
            }
        }
    }

    removefriend = (frienduser) => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        const data=`task=removeFriend&user=${USERNAME}&password=${TOKEN}&friend=${frienduser}`
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.removeFriendSuccess) {
                    friendspage();
                } else {
                    el = document.getElementById("addfrienddiv");
                    const fail = document.createElement("div");
                    fail.classList.add("failedtologin");
                    fail.innerText = `Failed to remove ${frienduser}.`;
                    el.appendChild(fail);
                }
            }
        }
    }

    acceptfriend = (frienduser) => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        const data=`task=acceptFriend&user=${USERNAME}&password=${TOKEN}&friend=${frienduser}`
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.acceptFriendSuccess) {
                    friendspage();
                } else {
                    el = document.getElementById("addfrienddiv");
                    const fail = document.createElement("div");
                    fail.classList.add("failedtologin");
                    fail.innerText = `Failed to remove ${frienduser}.`;
                    el.appendChild(fail);
                }
            }
        }
    }

    addfriend = () => {
        let frienduser = document.getElementById("addfriendinput").value;
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        const data=`task=requestFriend&user=${USERNAME}&password=${TOKEN}&friend=${frienduser}`
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.requestFriendSuccess) {
                    friendspage();
                } else {
                    el = document.getElementById("addfrienddiv");
                    const fail = document.createElement("div");
                    fail.classList.add("failedtologin");
                    fail.innerText = `Failed to add ${frienduser}.`;
                    el.appendChild(fail);
                }
            }
        }
    }

    

    mainfetchfriends = () => {
        fetchfriendlist();
        // for (let i =0; i<fakefriends.length; i++) {
        //     makefriend(fakefriends[i]);
        // }
    }
}

mainfetchfriends();