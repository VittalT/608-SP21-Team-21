const makefriend = (friendnum) => {
    const newfriend = document.createElement("div");
    newfriend.classList.add("friendbox");
    newfriend.classList.add("friendbox");
    newfriend.innerHTML = "<div class="v55_43">" + 
		"<div class="v55_44">" + "</div>" + 
		"<span class="v55_45">" + ${friendnum.name} + "</span>" + 
		"<span class="v55_48">" `Checked in to room ` + ${friendnum.room} + "</span>" + "</div>";
    dashBoard.appendChild(newfriend);
}
const fetchfriendlist = () => {
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=friends&user=%27Vittal%27';
    HTTP.open("GET", url);
    HTTP.send();

    HTTP.onreadystatechange = function(){
        if(this.readyState == 4 && this.status==200) {
            console.log(HTTP.responseText);
            freindlist = JSON.parse(HTTP.responseText);
            for (let friend in friendlist) {
                makefriend(friend);
            }
        }
    }
}

const main = () => {
    // checkin
    // for(let i = 1; i<=18; i++) {
    //     makefriend(list[i]);
    // }
    fetchfriendlist();
}

main();