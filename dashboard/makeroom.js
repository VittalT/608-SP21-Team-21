const dashBoard = document.getElementById("dashboard");

const makeroom = (roomnum) => {
    const newroom = document.createElement("div");
    newroom.classList.add("roombox");
    newroom.classList.add("roombox");
    // newroom.innerText = `Test room number ${roomnum} \\`;
    newroom.innerHTML = "<div>" + `Test room number ${roomnum.rn} \r\n` +
			`Capacity: ${roomnum.Capacity}/${roomnum.Capacity} \r\n` + 
			`Current noise level: Quiet \r\n` +
			`Volume Preferences: Quiet \r\n` + "</div>" +
                        `<button class="checkin"
                            type="button"
                            value="Check In"
                        > Check In </button>`
    dashBoard.appendChild(newroom);
}

const checkin = (roomnum) => {
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server-Side/User-Server-API.py?task=checkinpage';
    HTTP.open("GET", url);
    HTTP.send();
    HTTP.onreadystatechange = function(){
        if(this.readyState == 4 && this.status==200) {
            console.log(HTTP.responseText);
            const body = document.body;
            body.innerHTML = HTTP.responseText;
            // TODO: below code to be implemented after the Check In page is created.
            //roomnum = document.getElementById("roomnum")
            //roomnum.innerText = roomnum
        }
    }
}
