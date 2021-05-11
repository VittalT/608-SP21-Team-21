const checkin = (roomno, hoursstay, noise) => {
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server-Side/User-Server-API.py?task=checkin';
	const data={
		roomnum: roomno,
		hours: hoursstay,
		noiselevel: noise
	};
	dataType='JSON';
    HTTP.open("POST", url);
	HTTP.setRequestHeader("Content-type", "application/json");
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

var setInnerHTML = function(elm, html) {
    elm.innerHTML = html;
    Array.from(elm.querySelectorAll("script")).forEach( oldScript => {
      const newScript = document.createElement("script");
      Array.from(oldScript.attributes)
        .forEach( attr => newScript.setAttribute(attr.name, attr.value) );
      newScript.appendChild(document.createTextNode(oldScript.innerHTML));
      oldScript.parentNode.replaceChild(newScript, oldScript);
    });
  }