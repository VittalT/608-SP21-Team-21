
if (typeof submitcheckin === 'undefined') {
    submitcheckin = () => {
        let roomnum = document.getElementById("roominput").value;
        let hoursstay = document.getElementById("hoursinput").value;
        let volumepref = document.getElementById("volumeprefinput").value;
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py';
        // TODO : add user
        const data=`task=checkin&roomNum=${roomnum}&duration=${hoursstay}&volumePref=${volumepref}&user=${USERNAME}&token=${TOKEN}`;
        console.log(data)
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                // const doc = document.documentElement;
                // doc.innerHTML = HTTP.responseText;
                // setInnerHTML(doc, HTTP.responseText);
                resp = JSON.parse(HTTP.responseText);
                if (resp.checkinSuccess) {
                    backtodashboard();
                } else {
                    el = document.body;
                    const fail = document.createElement("div");
                    fail.classList.add("checkinFail");
                    fail.innerText = "Failed to Check In. Check that info is correct and try again.";
                    el.appendChild(fail);
                }
                // TODO: below code to be implemented after the Check In page is created.
                //roomnum = document.getElementById("roomnum")
                //roomnum.innerText = roomnum
            }
        }
    }
}
