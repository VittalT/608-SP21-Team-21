
if (typeof makeroom === 'undefined') {
    makeroom = (room) => {
        const dashBoard = document.getElementById("dashboard");
        const newroom = document.createElement("div");
        newroom.classList.add("roombox");
        const roomnum = room.roomNum;
        const occupancy = room.occupancy;
        const capacity = room.capacity;
        const noiselevel = room.noiseLevel;
        const volumepref = room.volumePref;
        const friendsinroom = room.friends;
        let friendsdiv = "";
        if (friendsinroom.length > 0) {
            friendsdiv = `<div class="friends"> Friends in this Room: `
            let i = 0;
            for (; i< friendsinroom.length-1; i++) {
                friendsdiv = friendsdiv + `${friendsinroom[i].name}, `
            }
            friendsdiv = friendsdiv + `${friendsinroom[i].name} </div>`
        }
        newroom.innerHTML = "<div>" + `Room number ${roomnum}` + "</div>" +
                            "<div>" + `Occupancy: ${occupancy}/${capacity}` + "</div>" +
                            "<div>" + `Current Noise Level: ${noiselevel}` + "</div>" +
                            "<div>" + `Volume Preferences: ${volumepref}` + "</div>" +
                            friendsdiv +
                            `<button class="checkin"
                                type="button"
                                value="Check In"
                                onclick="checkinpage()"
                            > Check In </button>`
        dashBoard.appendChild(newroom);
    }
}