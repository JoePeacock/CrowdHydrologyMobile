var lat,lon;
var map;
var speed1,speed2,speed3,speed4,speed5,speed6;

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else{
      x.innerHTML="Geolocation is not supported by this browser.";
  }
}

function showPosition(position)
  {
    thePosition=position;
    lat=position.coords.latitude;
    lon=position.coords.longitude;
    map();
  }

function map(){
    var map = L.map('map').setView([lat, lon], 13);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
    }).addTo(map);
        $.ajax("/api/stations", {
            success: function(response) {
                data = response.data;
                for(var i=0;i<data.length; i++) {
                  L.marker([data[i]["latitude"], data[i]["longitgude"]]).addTo(map).bindPopup("<b>Gauge: "+data[i]["id"]+"</b><br />"+data[i]["name"]+"<br><a href=./view/"+data[i]["id"]+">View Data</a>");
                }
            }, 
            error: function() {
                alert("Sorry there seems to be an error gathering stations. Please try again later.");
            }
        });
    
    var popup = L.popup();

}


function initialize() {
    var mapOptions = {
      center: new google.maps.LatLng(lat, lon),
      zoom: 12
    };

    map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
}
      
