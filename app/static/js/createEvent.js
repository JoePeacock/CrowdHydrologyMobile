Parse.initialize("ZNUGpdAW35nGYe5hvleBl3IndIphZPbZjVfn8Vcn", "6Qc87mH6kNQfQ51ILACN1lz9BWwCBZpnDGpMDvUx");

function save(){
    var Event = Parse.Object.extend("Event");
    var newEvent = new Event();
     
    newEvent.set("creator", 1337);
    newEvent.set("name", "Sean Plott");
    newEvent.set("cheatMode", false);
     
    gameScore.save(null, {
      success: function(gameScore) {
        // Execute any logic that should take place after the object is saved.
        alert('New object created with objectId: ' + gameScore.id);
      },
      error: function(gameScore, error) {
        // Execute any logic that should take place if the save fails.
        // error is a Parse.Error with an error code and description.
        alert('Failed to create new object, with error code: ' + error.description);
      }
    });
}