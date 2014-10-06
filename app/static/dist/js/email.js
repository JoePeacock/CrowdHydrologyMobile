function sendMail() {
    alert("Sending");
    var link = "mailto:mtu-hci-group-6-l@mtu.edu"
             + "?cc="+escape(document.getElementById('emailAddr').value)
             + "&subject=" + escape(document.getElementById('emailSubject').value)
             + "&body=" + escape(document.getElementById('emailBody').value)
    ;

    window.location.href = link;
}

function sendMail2() {
    var link = "mailto:me@example.com"
             + "?cc=myCCaddress@example.com"
             + "&subject=" + escape("This is my subject")
             + "&body=" + escape(document.getElementById('myText').value)
    ;

    window.location.href = link;
}