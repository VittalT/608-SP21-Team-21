const dashBoard = document.getElementById("dashboard");

const makeroom = (room) => {
    const newroom = document.createElement("div");
    newroom.classList.add("roombox");
    newroom.classList.add("roombox");
    const roomnum = room.room_num;
    const occupants = room.occupants;
    const capacity = room.capacity;
    const noiselevel = room.noiselevel;
    const volumeprefs = room.volumeprefs;
    // newroom.innerText = `Test room number ${roomnum}`;
  
//     // newroom.innerText = `Test room number ${roomnum} \\`;
//     newroom.innerHTML = "<div>" + `Test room number ${roomnum.rn} \r\n` +
// 			`Capacity: ${roomnum.Capacity}/${roomnum.Capacity} \r\n` + 
// 			`Current noise level: Quiet \r\n` +
// 			`Volume Preferences: Quiet \r\n` + "</div>" +
    newroom.innerHTML = "<div>" + `Room number ${roomnum}` + "</div>" +
                        "<div>" + `Occupancy: ${occupants}/${capacity}` + "</div>" +
                        "<div>" + `Current Noise Level: ${noiselevel}` + "</div>" +
                        "<div>" + `Volume Preferences: ${volumeprefs}` + "</div>" +
                        `<button class="checkin"
                            type="button"
                            value="Check In"
                            onclick="checkin()"
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
