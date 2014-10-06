
google.load("visualization", "1", {packages:["corechart"]});
var theResult;
var TestObject
var username;
function parse(){
    Parse.initialize("2ICGEDAbu9xpPISmefOo6y4VvEYcw7W0oOF7Lp2T", "6tOKR4v4ERtZhk8VHahuCjoinJzZkTOcUxRPWKc5");
    TestObject = Parse.Object.extend("Pins");
    username=Parse.User.current().get("username");
    document.getElementById("welcome").innerHTML="Welcome, "+username+"!";
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
query.limit(250);
query.find({
  success: function(results) {
     theResult=results;
     document.getElementById("pin_count").innerHTML="You currently have "+results.length+" pins in our database!";
    //alert("Successfully retrieved " + results.length + " scores.");
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
            tbody += "<td style=\"text-align:center;\">";
            if (object.get('forceDisplay')) {
                tbody += "<div style=\"display:inline-block; margin:auto;\" class=\"checkbox\"><center><input type=\"checkbox\" id="+object.get('PinID')+"\"value=\"\" checked onclick=\"toggleForce('"+object.get('PinID')+"')\"></center></div>";
            } else {
                tbody += "<div style=\"display:inline-block; margin:auto;\" class=\"checkbox\"><center><input type=\"checkbox\" id="+object.get('PinID')+"\"value=\"\" onclick=\"toggleForce('"+object.get('PinID')+"')\"></center></div>";
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


function toggleForce(id){
    //alert(id);
    
    var query = new Parse.Query(TestObject);
query.equalTo("userId", username);
query.equalTo("PinID",id);

//query.descending("Repins");
query.find({
  success: function(results) {
    //alert(results.length);
    
    //alert("Results: "+results[0].get('forceDisplay'));
    results[0].set("forceDisplay",!results[0].get("forceDisplay"));
    results[0].save();
  },
  error: function(error) {
    alert("Error: " + error.code + " " + error.message);
  }
  
});
    
}

function notify(){
    //code
    alert("yolo");
}

// Builds the HTML Table out of myList.
function buildHtmlTable() {
    //parse();
//alert("Passed test");
//alert("The result is "+theResult);
    var columns = addAllColumnHeaders(theResult);
//alert("Columns is "+columns);

    for (var i = 0 ; i < theResult.length ; i++) {
        var row$ = $('<tr/>');
        for (var colIndex = 0 ; colIndex < columns.length ; colIndex++) {
            var cellValue = myList[i][columns[colIndex]];

            if (cellValue == null) { cellValue = ""; }

            row$.append($('<td/>').html(cellValue));
        }
        $("#excelDataTable").append(row$);
    }
}

// Adds a header row to the table and returns the set of columns.
// Need to do union of keys from all records as some records may not contain
// all records
function addAllColumnHeaders(myList)
{
    var columnSet = [];
    var headerTr$ = $('<tr/>');

    for (var i = 0 ; i < myList.length ; i++) {
        var rowHash = myList[i];
        for (var key in rowHash) {
            if ($.inArray(key, columnSet) == -1){
                columnSet.push(key);
                headerTr$.append($('<th/>').html(key));
            }
        }
    }
    $("#excelDataTable").append(headerTr$);

    return columnSet;
}




