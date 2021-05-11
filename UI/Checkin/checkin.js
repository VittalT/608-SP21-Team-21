
if (typeof checkin === 'undefined') {
    submitcheckin = (roomno, hoursstay, noise) => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=checkin';
        const data=`roomnum=${roomno}&hours=${hoursstay}&noiselevel=${noise}`
        // {
        //     roomnum: roomno,
        //     hours: hoursstay,
        //     noiselevel: noise
        // };
        dataType='JSON';
        HTTP.open("POST", url);
        HTTP.setRequestHeader("Content-type", "application/x-www-form-urlencoded; charset=UTF-8");
        HTTP.send(data);
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                // doc.innerHTML = HTTP.responseText;
                setInnerHTML(doc, HTTP.responseText);
                // TODO: below code to be implemented after the Check In page is created.
                //roomnum = document.getElementById("roomnum")
                //roomnum.innerText = roomnum
            }
        }
    }
}
