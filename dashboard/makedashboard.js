
var list = [
    { rn: '1-115', Capacity: 10, nl: 0, vp:0 },
    { rn: '1-134', Capacity: 10, nl: 0, vp:0 },
    { rn: '2-132', Capacity: 10, nl: 0, vp:0 },
    { rn: '2-135', Capacity: 10, nl: 0, vp:0 },
    { rn: '2-151', Capacity: 7, nl: 0, vp:0 },
    { rn: '4-149', Capacity: 10, nl: 0, vp:0 },
    { rn: '4-153', Capacity: 10, nl: 0, vp:0 },
    { rn: '4-167', Capacity: 4, nl: 0, vp:0 },
    { rn: '5-233', Capacity: 10, nl: 0, vp:0 },
    { rn: '8-119', Capacity: 8, nl: 0, vp:0 },
    { rn: '24-112', Capacity: 8, nl: 0, vp:0 },
    { rn: '26-142', Capacity: 8, nl: 0, vp:0 },
    { rn: '32-144', Capacity: 10, nl: 0, vp:0 },
    { rn: '56-154', Capacity: 10, nl: 0, vp:0 },
    { rn: '56-169', Capacity: 8, nl: 0, vp:0 },
    { rn: '66-080', Capacity: 8, nl: 0, vp:0 },
    { rn: 'E51-073', Capacity: 5, nl: 0, vp:0 },
    { rn: 'E53-120', Capacity: 7, nl: 0, vp:0 }
];


const fetchroomlist = () => {
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server-Side/User-Server-API.py?task=rooms';
    HTTP.open("GET", url);
    HTTP.send();

    HTTP.onreadystatechange = function(){
        if(this.readyState == 4 && this.status==200) {
            console.log(HTTP.responseText);
            roomlist = JSON.parse(HTTP.responseText);
            for (let room in roomlist) {
                makeroom(room);
            }
        }
    }
}


const makeloginbutton = () => {
    // TODO: change this to reflect if user is logged in
    loggedin = false;
    userid = 'test_user_id'
    // 
    const logindiv = document.getElementById("login");
    if (!loggedin) {
        logindiv.innerHTML = `<button class="loginbutton"
        type="button"
        value="Log In"
        onclick="login()"
        > Log In/Create Account </button>`
    }
    else {
        logindiv.innerText = `Logged in as ${userid}`
    }
}


const login = () => {
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server-Side/User-Server-API.py?task=loginpage';
    HTTP.open("GET", url);
    HTTP.send();
    HTTP.onreadystatechange = function(){
        if(this.readyState == 4 && this.status==200) {
            console.log(HTTP.responseText);
            const body = document.body;
            body.innerHTML = HTTP.responseText;
        }
    }
}


const main = () => {
    makeloginbutton();
    for(let i = 1; i<=18; i++) {
        makeroom(list[i]);
    }
    fetchroomlist();

}

main();