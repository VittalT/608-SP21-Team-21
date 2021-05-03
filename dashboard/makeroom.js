const dashBoard = document.getElementById("dashboard");

const makeroom = (roomnum) => {
    const newroom = document.createElement("div");
    newroom.classList.add("roombox");
    newroom.classList.add("roombox");
    // newroom.innerText = `Test room number ${roomnum}`;
    newroom.innerHTML = "<div>" + `Test room number ${roomnum}` + "</div>" +
                        `<button class="checkin"
                            type="button"
                            value="Check In"
                        > Check In </button>`
    dashBoard.appendChild(newroom);
}