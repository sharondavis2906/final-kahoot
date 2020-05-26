$(document).ready(function() {

	
// ====================================================================================

	var data = $.ajax({
        url: "/static/configu.txt", 
        dataType: "text",
		async: false,
        success: function (data) {
            console.log(data)
        }
    }).responseText;
	
	console.log('data: ' + data);

// Player page (enter PIN)

   var socket_player = io.connect(data+'/player');


    $('#gamepin').on('click', function() {
        
		console.log(101);
		
		var messagepin = $('#messagepin').val();

        socket_player.emit('gamepin', messagepin);

    });


    $('#nickname').on('click', function() {
        
		console.log(102);
		
		var messagenn = $('#messagenn').val();

        socket_player.emit('nickname', messagenn);

    });





// Message to Flask when button is pressed

// Red button pressed

    $('#answer-red').on('click', function() {
	
	   console.log('RED-1');
	
	   //alert ("bla");
	
	
        socket_player.emit('answer', 1);

    });


// Blue button pressed

    $('#answer-blue').on('click', function() {
	
	   console.log('BLUE-2');
	
        socket_player.emit('answer', 2);

    });


// Orange button pressed

    $('#answer-orange').on('click', function() {
	
	 console.log('ORANGE-3');
	
        socket_player.emit('answer', 3);

    });


// green button pressed

    $('#answer-green').on('click', function() {
	
	
      console.log('GREEN-4');
	
        socket_player.emit('answer', 4);

    });

 
// Message from Flask

socket_player.on('message from flask to player', function (data) {

	// Change page to "Name" if correct PIN was entered or stay on "Join" and print "wrong PIN"
	
    console.log(909);
	
	
	update_player (data.mode,data.game,data.pin,data.player,data.score,data.numquestions,data.question_num);
	
	
 
 
});


socket_player.on('redirect from flask to player', function (data) {

	// Change page to "active" once game starts or print error
	
		console.log(4515);
	
	 
	
       window.location = data.url;
 
 
	
	   //console.log(data.url);
  
});


  






    

});