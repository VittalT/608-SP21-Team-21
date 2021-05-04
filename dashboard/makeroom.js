const dashBoard = document.getElementById("dashboard");

const makeroom = (roomnum) => {
    const newroom = document.createElement("div");
    newroom.classList.add("roombox");
    newroom.classList.add("roombox");
    // newroom.innerText = `Test room number ${roomnum} \\`;
    newroom.innerHTML = "<div>" + `Test room number ${roomnum} \r\n` +
			`Capacity: 10/10 \r\n` + 
			`Current noise level: Quiet \r\n` +
			`Volume Preferences: Quiet \r\n` + "</div>" +
                        `<button class="checkin"
                            type="button"
                            value="Check In"
                        > Check In </button>`
    dashBoard.appendChild(newroom);
}