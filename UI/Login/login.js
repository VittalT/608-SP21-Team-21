const loginaccount = () => {
    let username = document.getElementById("u_name_login").value;
    let pass = document.getElementById("pword_login").value;
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=login';
	const data={
		user: username,
		password: pass
    };
    console.log(data);
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

const createaccount = () => {
    let username = document.getElementById("u_name_createacc").value;
    let pass1 = document.getElementById("pword_createacc").value;
    let pass2 = document.getElementById("rtpword_createacc").value;
	if (pass1 != pass2)
		//Do something about it
		pass = pass1 //For now
	else
		pass = pass1
    const HTTP = new XMLHttpRequest();
    const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=createaccount';
	const data={
		user: username,
		password: pass
	};
    console.log(data);
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