var theResult;
var TestObject;
var username;
var loveNum=0;
var hateNum=0;
//alert("hey");
function parse(){
    //alert("go");
    Parse.initialize("ZNUGpdAW35nGYe5hvleBl3IndIphZPbZjVfn8Vcn", "6Qc87mH6kNQfQ51ILACN1lz9BWwCBZpnDGpMDvUx");
    //alert("start");
    TestObject = Parse.Object.extend("Event");
    /*var testObject = new TestObject();
    testObject.set("userId","Alex");
    testObject.save(null, {
    success: function(testObject) {
        alert("yay! it worked");
        },
    error: function(testObject, error) {
        // Execute any logic that should take place if the save fails.
        // error is a Parse.Error with an error code and description.
        alert('Failed to create new object, with error code: ' + error.description);
        }
    });*/
    
    var query = new Parse.Query(TestObject);
    //alert(document.getElementById("creatorName").innerHTML);
query.equalTo("creator", document.getElementById("creatorName").innerHTML);
//alert("here");
query.find({
  success: function(results) {
     theResult=results;
    //alert("Successfully retrieved " + results.length + " scores.");
    // Do something with the returned Parse.Object values
    /*alert(results.length);
    for (var i = 0; i < results.length; i++) { 
      var object = results[i];
      //alert(object.id + ' - ' + object.get('userId'));
    }*/
    //buildHtmlTable();
    insertTable();
  },
  error: function(error) {
    alert("Error: " + error.code + " " + error.message);
  }
  
});
function insertTable()
{
    //alert("begin");
    var num_rows = theResult.length;
    var num_cols = 4;
    var width = 100;
    /*<section id="upcomming">
  <a style="display:block" href="http://google.com" style="color: #dedede;">
    <section class="event" style="background-color: #622764;">
      <div class="row" id="eventTile">
	<div class="col-xs-3">
	  <img class="img-circle" src="../static/bullhead.gif" height=50px;>
	</div>
	<div class="col-xs-9">
	  <div class="row">
	    <div class="col-xs-6">
	    <font size=1 class="text">Rekhi 117</font>
	    </div>
	    <div class="col-xs-6">
	    <font size=1 class="text">7 Attending</font>
	    </div>
	  </div>
	  <font  class="text">MTG Tournament</font>
	  <div class="row">
	    <div class="col-xs-6">
	    <font size=1 class="text">03/14/2014</font>
	    </div>
	    <div class="col-xs-6">
	    <font size=1 class="text">8:00 PM</font>
	    </div>
	  </div>
	</div>
      </div>
    </section>
  </a>*/
    var theader = "<section id=\"upcomming\">";
    var tbody = "";
    var color=0;
    for(var i = 0; i < num_rows; i++)
    {
        //tbody += "<tr>";
            var object = theResult[i];
            tbody+="<a style=\"display:bloc\" href=\"./event/"+object.id+"\" style=\"color: #dedede;\">";
            if (color==0) {
                tbody+="<section class=\"event\" style=\"background-color: #622764;\">";
                color=1;
            }else{
                tbody+="<section class=\"event\" style=\"background-color: #6e2b71;\">";
                color=0;
            }
            tbody+="<div class=\"row\" id=\"eventTile\">";
            tbody+="<div class=\"col-xs-3\">";
            tbody+="<img class=\"img-circle\" src=\"../static/bullhead.gif\" height=50px;>";
            tbody+="</div>";
            tbody+="<div class=\"col-xs-9\">";
            tbody+="<div class=\"row\">";
	    tbody+="<div class=\"col-xs-6\">";
            tbody+="<font size=1 class=\"text\">"+object.get('location_string')+"</font>";
           tbody+="</div>";
	    tbody+="<div class=\"col-xs-6\">";
	   tbody+=" <font size=1 class=\"text\">"+object.get('people_attending').length+" Attending</font>";
	  tbody+="  </div>";
	 tbody+=" </div>";
	 tbody+=" <font  class=\"text\">"+object.get('description')+"</font>";
	 tbody+=" <div class=\"row\">";
	 tbody+="   <div class=\"col-xs-6\">";
	  tbody+="  <font size=1 class=\"text\">"+object.get('date')+"</font>";
	  tbody+="  </div>";
	  tbody+="  <div class=\"col-xs-6\">";
	  tbody+="  <font size=1 class=\"text\">"+object.get('time')+"</font>";
	  tbody+="  </div>";
	 tbody+=" </div>";
	tbody+="</div>";
      tbody+="</div>";
   tbody+=" </section>";
 tbody+=" </a>";
           
    }
    var tfooter = "</section>";
    document.getElementById('theTable').innerHTML = theader + tbody + tfooter;
    
    
}   
}