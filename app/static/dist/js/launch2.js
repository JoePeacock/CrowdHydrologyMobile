
google.load("visualization", "1", {packages:["corechart"]});
var theResult;
var TestObject
var username;
alert("butts");
function parse(){
    alert("#butts");
    Parse.initialize("2ICGEDAbu9xpPISmefOo6y4VvEYcw7W0oOF7Lp2T", "6tOKR4v4ERtZhk8VHahuCjoinJzZkTOcUxRPWKc5");
    alert("woring");
    TestObject = Parse.Object.extend("Pins");
    username=Parse.User.current().get("username");
    //document.getElementById("welcome").innerHTML="Welcome, "+username+"!";
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
query.equalTo("userId", username);
query.descending("Repins");
alert("yoyoyo");
query.limit(10);
query.find({
  success: function(results) {
     theResult=results;
     document.getElementById("pin_count").innerHTML="You currently have "+results.length+" pins in our database!";
    alert("Successfully retrieved " + results.length + " scores.");
    // Do something with the returned Parse.Object values
    
    for (var i = 0; i < results.length; i++) { 
      var object = results[i];
      //alert(object.id + ' - ' + object.get('userId'));
    }
    //buildHtmlTable();
    insertTable();
  },
  error: function(error) {
    alert("Error: " + error.code + " " + error.message);
  }
  
});

//alert("completed");
}

function insertTable()
{
    
    var num_rows = theResult.length;
    var num_cols = 4;
    var width = 100;
    var theader = "<table border=\"1\" id='table1' width = ' "+ width +"% '>";
    var tbody = "";

    //theader += "<th>Date Added</th>";
    theader += "<th><center>Pin ID</center></th>";
    theader += "<th><center>Name</center></th>";
    theader += "<th><center>Number of Repins</center></th>";
    theader += "<th><center>URL of Image</center></th>";
     theader += "<th><center>Force Display?</center></th>";

    for(var i = 0; i < num_rows; i++)
    {
        tbody += "<tr>";
            var object = theResult[i];
            //tbody += "<td>";
            //tbody += object.get('createdAt') ;
            //tbody += "</td>"
            tbody += "<td>";
            tbody += object.get('PinID');
            tbody += "</td>"
            tbody += "<td>";
            tbody += object.get('Name');
            tbody += "</td>"
            tbody += "<td>";
            tbody += object.get('Repins');
            tbody += "</td>"
            tbody += "<td>";
            tbody += "<center><a href=\""+object.get('Image')+"\">link</a></center>";
            tbody += "</td>"
            tbody += "<td>";
            if (object.get('forceDisplay')) {
                tbody += "<div class=\"checkbox\"><center><input type=\"checkbox\" id="+object.get('PinID')+"\"value=\"\" checked onclick=\"toggleForce('"+object.get('PinID')+"')\"></center></div>";
            } else {
                tbody += "<div class=\"checkbox\"><center><input type=\"checkbox\" id="+object.get('PinID')+"\"value=\"\" onclick=\"toggleForce('"+object.get('PinID')+"')\"></center></div>";
            }
            tbody += "</td>"
            /*tbody += "<td>";
            if(object.get('type')==0)
                tbody += "Compliment";
            else
                tbody += "Hateful";
            tbody += "</td>"
            tbody += "<td>";
            tbody += "<center><button id="+object.id+">Delete</button></center>";
            tbody += "</td>"*/
        
        tbody += "</tr>";
    }
    var tfooter = "</table>";
    document.getElementById('theTable').innerHTML = theader + tbody + tfooter;
    $("button").click(function() {
        //alert(this.id); // or alert($(this).attr('id'));
        var query = new Parse.Query(TestObject);
        query.get(this.id, {
            success: function(gameScore) {
                // The object was retrieved successfully.
                //alert("THIS IS SUCCESS");
                    gameScore.destroy({
                        success: function(gameScore) {
                          // The object was deleted from the Parse Cloud.
                          //alert("Works");
                          window.location.replace("./main.html");
                        },
                        error: function(gameScore, error) {
                          // The delete failed.
                          // error is a Parse.Error with an error code and description.
                          //alert("doesn't work");
                        }
                    });
                },
            error: function(object, error) {
                alert("YOU FAIL");
                // The object was not retrieved successfully.
                // error is a Parse.Error with an error code and description.
            }
        });
    });
    
    
}






