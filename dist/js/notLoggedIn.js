Parse.initialize("bU0hZTlz3h2KVEhZ4GAB6xfeDywUOih0hht2qKME", "3magOH6OvOWmGmhwOcBZ1R9W996K4Gi45fH4RC5W");

  var currentUser = Parse.User.current();

  if(currentUser == null){
    window.location.replace('./index.html');
  }
