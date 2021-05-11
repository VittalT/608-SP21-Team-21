var roomlist = [
    { roomnum: '1-115', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '1-134', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '2-132', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '2-135', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '2-151', capacity: 7, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '4-149', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '4-153', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '4-167', capacity: 4, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '5-233', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '8-119', capacity: 8, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '24-112', capacity: 8, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '26-142', capacity: 8, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '32-144', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '56-154', capacity: 10, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '56-169', capacity: 8, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: '66-080', capacity: 8, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: 'E51-073', capacity: 5, occupants: 0, noiselevel: 0, volumeprefs:0 },
    { roomnum: 'E53-120', capacity: 7, occupants: 0, noiselevel: 0, volumeprefs:0 }
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
    const url='http://608dev-2.net/sandbox/sc/team21/Server/UserServerAPI.py?task=loginpage';
    HTTP.open("GET", url);
    HTTP.send();
    HTTP.onreadystatechange = function(){
        if(this.readyState == 4 && this.status==200) {
            console.log(HTTP.responseText);
            const doc = document.documentElement;
            doc.innerHTML = HTTP.responseText;
        }
    }
}


const main = () => {
    makeloginbutton();
    for(let i = 1; i<=18; i++) {
        makeroom(roomlist[i]);
    }
    fetchroomlist();

}

main();