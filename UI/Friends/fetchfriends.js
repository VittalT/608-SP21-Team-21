if (typeof makefriend === 'undefined') {
    makefriend = (friendnum) => {
        const newfriend = document.createElement("div");
        newfriend.classList.add("friendbox");
        newfriend.classList.add("friendbox");
        newfriend.innerHTML = `<div class="v55_43"><div class="v55_44"></div><span class="v55_45">` + friendnum.name + `</span><span class="v55_48"> Checked in to room ` + friendnum.room + `</span></div>`;
        document.body.appendChild(newfriend);
    }
    fetchfriendlist = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=friendswithrooms&user=%27Vittal%27';
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

    backtodashboard = () => {
        const HTTP = new XMLHttpRequest();
        const url='http://608dev-2.net/sandbox/sc/team21/Server/APIs/UserServerAPI.py?task=dashboardpage';
        HTTP.open("GET", url);
        HTTP.send();
        HTTP.onreadystatechange = function(){
            if(this.readyState == 4 && this.status==200) {
                console.log(HTTP.responseText);
                const doc = document.documentElement;
                // doc.innerHTML = HTTP.responseText;
                setInnerHTML(doc, HTTP.responseText)
            }
        }
    }

    mainfetchfriends = () => {
        fetchfriendlist();
    }
}

mainfetchfriends();