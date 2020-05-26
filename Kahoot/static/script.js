
$(document).ready(function() {

// Index page


	var data = $.ajax({
        url: "/static/configu.txt", 
        dataType: "text",
		async: false,
        success: function (data) {
            console.log(data)
        }
    }).responseText;
	
	console.log("data: " + data);





// -------------------------------------------------------------------------
// index page
    var socket = io.connect(data);

// Message to Flask when button is pressed

// Game 1 button pressed

    $('#game1').on('click', function() {
		
        socket.emit('game selected', "Trivia1");

    });


// Game 2 button pressed

    $('#game2').on('click', function() {
		
        socket.emit('game selected', "Trivia2");

    });


// Game 3 button pressed

    $('#game3').on('click', function() {
		
        socket.emit('game selected', "Trivia3");

    });


// Game 4 button pressed

    $('#game4').on('click', function() {
		
        socket.emit('game selected', "Trivia4");

    });

	
// new game button pressed

    $('#newgame').on('click', function() {

        socket.emit('newgame selected',"redirect");

    });




// Message from Flask

socket.on('redirect from flask to index', function (data) {

	// Change page to "Start Page" after game selection/ new game
		
    window.location = data.url;
 
});


// -------------------------------------------------------------------------
// Start page

   var socket_start = io.connect(data+'/start');

 


    $('#gamestart').on('click', function() {
        
	

        socket_start.emit('gamestart', "Game Start");
		
		
		

    });


    $('#gameexit').on('click', function() {
        

        console.log(3);

        socket_start.emit('gameexit', "Game Exit");

    });




socket_start.on('redirect from flask to start', function (data) {

	
		console.log(700);
	
    window.location = data.url;
 
});


socket_start.on('message from flask to start', function (data) {
	
	console.log(99);
	
   
   update_start(data.numplayers,data.player1,data.player2,data.player3,data.player4,data.player5);
   
  
    console.log(100);

});






// -------------------------------------------------------------------------
// Question page 

   var socket_question = io.connect(data+'/question');
 
 
     // Dummy button to simulate timeout
     $('#question_timeout').on('click', function() {
        
		console.log(302);
		
        socket_question.emit('question timeout', 'timeout');

    });


     // Dummy button to simulate timeout for pre-question count
     $('#question_timeoutp').on('click', function() {
        
		console.log(306);
		
        socket_question.emit('question timeoutp', 'timeout');

    });



     // Next question
     $('#nextquestion').on('click', function() {
        
		console.log(336);
		
        socket_question.emit('nextquestion', 'next');

    });


     // exit game
     $('#gameexit').on('click', function() {
        
		console.log(336);
		
        socket_question.emit('gameexit', 'Game Exit');

    });




 
// Message from Flask

socket_question.on('redirect from flask to question', function (data) {

	// Change page to "active" once game starts or print error
	
		console.log(215);
	
	 
	
       window.location = data.url;
 
 
	
	   console.log(data.url);
  
});

	
socket_question.on('message from flask to question', function (data) {

	
	
    console.log(9690);
	
	update_question (data.mode,data.question, data.question_num,data.answer1, data.answer2, data.answer3, data.answer4,data.score1,data.score2,data.score3,data.score4,data.score5);
	

});
//-----------------------------------------
//new game

 var socket_newGame = io.connect(data+'/newGame');
 
 // Message from Flask

socket_newGame.on('redirect from flask to newGame', function (data) {

	// Change page to "Start Page" after game selection
		
    window.location = data.url;
 
});

	// Enter 1 button pressed

    $('#enter1').on('click', function() {
		
		var text = document.getElementById("game1replace").value;
		var message = text + "1";
		
		
        socket_newGame.emit('gameChange selected', message);

    });
	
	// Enter 2 button pressed

    $('#enter2').on('click', function() {
		
		var text = document.getElementById("game2replace").value;
		var message = text + "2";
		
		
        socket_newGame.emit('gameChange selected', message);


    });
	
		// Enter 3 button pressed

    $('#enter3').on('click', function() {
		var text = document.getElementById("game3replace").value;
		var message = text + "3";
		
		
        socket_newGame.emit('gameChange selected', message);


    });
	
		// Enter 4 button pressed

    $('#enter4').on('click', function() {
		
	var text = document.getElementById("game4replace").value;
		var message = text + "4";
		
		
        socket_newGame('gameChange selected', message);


    });
	
     // exit game
     $('#gameexit').on('click', function() {
        
		console.log(336);
		
        socket_newGame.emit('gameexit', 'exit');

    });
	
	socket_newGame.on('message from flask to newGame', function (data) {

	
	
    console.log(9690);
	
	update_newGame (data.mode);
	

});



//-----------------------------------------
//new game questions
var socket_newGameQuestions = io.connect(data+'/newGameQuestions');
	// questionEnter button pressed

socket_newGameQuestions.on('redirect from flask to newGameQuestions', function (data) {

	// Change page to "Start Page" after game selection
		
    window.location = data.url;
 
});
    $('#questionEnter').on('click', function() {
		
		var text1 = document.getElementById("question").value;
		var text2 = document.getElementById("answer1replace").value;
		var text3 = document.getElementById("answer2replace").value;
		var text4 = document.getElementById("answer3replace").value;
		var text5 = document.getElementById("answer4replace").value;
		var text6 = document.getElementById("correctAnswerNum").value;
		var message = text1+"/n"+ text2+"/n"+ text3+"/n"+ text4+"/n"+ text5+"/n"+ text6;
		
        socket_newGameQuestions.emit('questionChange selected', message);

    });
	
	

	socket_newGameQuestions.on('message from flask to newGameQuestions', function (data) {
	
	console.log(666);
	console.log(data.numQuestion)
   
   update_numQues(data.numQuestion);
   update_newGameQuestions(data.mode);
    console.log(100);

});
	

    

});