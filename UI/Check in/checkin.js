const login = (roomno, hoursstay, noise) => {
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server-Side/User-Server-API.py?task=login';
	const data={
		room: roomno,
		hours: hoursstay
		noiselvl: noise
	};
	dataType='JSON';
    HTTP.open("POST", url);
	HTTP.setRequestHeader("Content-type", "application/json");
    HTTP.send(data);
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