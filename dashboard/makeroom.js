const dashBoard = document.getElementById("dashboard");

const makeroom = (room) => {
    const newroom = document.createElement("div");
    newroom.classList.add("roombox");
    newroom.classList.add("roombox");
    const roomnum = room.room_num;
    const occupants = room.occupants;
    const capacity = room.capacity;
    // newroom.innerText = `Test room number ${roomnum}`;
    newroom.innerHTML = "<div>" + `Room number ${roomnum}` + "</div>" +
                        "<div>" + `Occupancy: ${occupants}/${capacity}` + "</div>" +
                        `<button class="checkin"
                            type="button"
                            value="Check In"
                        > Check In </button>`
    dashBoard.appendChild(newroom);
}