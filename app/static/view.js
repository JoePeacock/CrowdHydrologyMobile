
var theResult,theResult1,theResult2,theResult3,theResult4;
var TestObject
var username;

var lat,lon;
var map;
var speed1,speed2,speed3,speed4,speed5,speed6;
function getLocation()
  {
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
  //alert("finished "+lat+" "+lon);
  map();
  //initialize();
  }

function map(){
    var map = L.map('map').setView([lat, lon], 13);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 18,
      
    }).addTo(map);

                
                $.ajax("../static/location.csv", {
                    success: function(data) {
                        //alert("presuccess");
                        var jsonobject = csvJSON(data)
                        // Now use jsonobject to do some charting...
      //alert("print");
                        //$("#json").val(jsonobject);
      var json=jQuery.parseJSON( jsonobject );
      //alert(json[0]["Date and Time"]);
      //alert(json.length);
            for(var i=0;i<json.length; i++){
              //alert(json[i]["ID"]);
              L.marker([json[i]["Lat"], json[i]["Long"]]).addTo(map).bindPopup("<b>Gauge: "+json[i]["ID"]+"</b><br />"+json[i]["Location"]+"<br><a href=./data/"+json[i]["ID"]+">View Data</a>");
            }
                    },
                    error: function() {
                        // Show some error message, couldn't get the CSV file
                        alert("failed");
                    }
                });
                
    function csvJSON(csv){
 
  var lines=csv.split("\n");
 
  var result = [];
 
  var headers=lines[0].split(",");
 
  for(var i=1;i<lines.length;i++){
 
    var obj = {};
    var currentline=lines[i].split(",");
 
    for(var j=0;j<headers.length;j++){
      obj[headers[j]] = currentline[j];
    }
 
    result.push(obj);
 
  }
  //alert(JSON.stringify(result));
  //return result; //JavaScript object
  return JSON.stringify(result); //JSON
}
    
 
  var popup = L.popup();

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
      
google.maps.event.addDomListener(window, 'load', getLocation);



