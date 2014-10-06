var theResult,theResult1,theResult2,theResult3,theResult4;
var TestObject
var username;

var lat,lon;
var map;
var speed1,speed2,speed3,speed4,speed5,speed6;
function getLocation()
{
  Parse.initialize("ZNUGpdAW35nGYe5hvleBl3IndIphZPbZjVfn8Vcn", "6Qc87mH6kNQfQ51ILACN1lz9BWwCBZpnDGpMDvUx");
  if (navigator.geolocation)
  {
        //alert("location works");
        navigator.geolocation.getCurrentPosition(showPosition);
      }
      else{x.innerHTML="Geolocation is not supported by this browser.";}
    }
    function showPosition(position)
    {
    //alert("setting...");
    thePosition=position;
    lat=position.coords.latitude;
    lon=position.coords.longitude;
  
  nearby();
  initialize();
}


function initialize() {
  var mapOptions = {
    center: new google.maps.LatLng(lat, lon),
    zoom: 12
  };
  map = new google.maps.Map(document.getElementById("map-canvas"),
    mapOptions);
         //alert("map initalized");


       }

       function nearby(){
        var point = new Parse.GeoPoint({latitude: lat, longitude: lon});
        var sEvent = Parse.Object.extend("Event");
        var place = new sEvent();
        place.set("location", point);
        var query = new Parse.Query(sEvent);

  // Interested in locations near user.
  query.near("location", point);
  // Limit what could be a lot of points.
  query.limit(10);
  // Final list of objects
  query.find({
    success: function(placesObjects) {
      for (var i = 0; i < placesObjects.length; i++){
        var Event = placesObjects[i];
        var name = Event.get("name");
        var time = Event.get("time");
        var date = Event.get("date");
      L.marker([Event.get("location").latitude,Event.get("location").longitude]).addTo(map).bindPopup("<b>"+name+"</b><br>"+date+"</br>"+time+"<br><a href=./data.html>View Data</a>").openPopup();
    }
  },
  error: function(error) {
    alert("Error: " + error.code + " " + error.message);
  }
});

}

google.maps.event.addDomListener(window, 'load', getLocation);



