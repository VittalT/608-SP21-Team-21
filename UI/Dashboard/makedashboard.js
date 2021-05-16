

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
        // TODO: change this to reflect if user is logged in
        // loggedin = false;
        // userid = 'test_user_id'
        // 
        const logindiv = document.getElementById("login");
        if (typeof loggedin === 'undefined' || !loggedin) {
            logindiv.innerHTML = `<button class="loginbutton"
            type="button"
            value="Log In"
            onclick="loginpage()"
            > Log In/Create Account </button>`
        }
        else {
            logindiv.innerText = `Logged in as ${userid}`
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
        fetchroomlist();
        for(let i = 1; i<=roomlist.length; i++) {
            makeroom(roomlist[i]);
        }
    }
}


main();
