# Kahoot server

from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import time
import datetime
import random as rand
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG'] = True
socketio = SocketIO(app)


pinname = 0
gamename = '' 
numplayers = 0
numquestions=15
question_num = 1
question_time_val = 10
correct_answer = 0
game_selected = 0
game_started = 0
lines = []
players = ['','','','','']
playersid = ['','','','','']
scores = [0,0,0,0,0]
answers_status = ['none','none','none','none','none']
numanswers = 0
startTime= 0
endTime= 0
microSecStart=0
microSecEnd=0
game1_first_name = 'Politics Trivia'
game2_first_name = 'Words Trivia'
game3_first_name = 'Songs Trivia'
game4_first_name = 'Music Trivia'
number=''
numQues=1
maxQuesNum=15
def reset_vars():

  global pinname
  global gamename
  global numplayers
  global numquestions
  global question_num
  global question_time_val
  global correct_answer
  global game_selected
  global game_started
  global lines
  global players
  global playersid
  global scores
  global answers_status
  global numanswers
  global number


  pinname = 0
  gamename = '' 
  numplayers = 0
  numquestions=10
  question_num = 1
  question_time_val = 10
  correct_answer = 0
  game_selected = 0;
  game_started=0;
  lines = []
  players = ['','','','','']
  playersid = ['','','','','']
  scores = [0,0,0,0,0]
  answers_status = ['none','none','none','none','none']
  numanswers = 0




@app.route('/')
def index():
    return render_template('index.html', game1_name=game1_first_name,game2_name=game2_first_name,game3_name=game3_first_name,game4_name=game4_first_name )




@app.route('/player')
def player():
    return render_template('player.html')




@app.route('/question')
def question():
    return render_template('question.html')




@app.route('/start')
def start():
    return render_template('start.html')
	
	
	
@app.route('/newGame')
def newGame():
    return render_template('newGame.html',game1_replaceName=game1_first_name,game2_replaceName=game2_first_name,game3_replaceName=game3_first_name,game4_replaceName=game4_first_name)
	
	
@app.route('/newGameQuestions')
def newGameQuestions():
    return render_template('newGameQuestions.html')

#----------------------index---------------------
# Message from HTML/JS after selecting a newgame button in index
@socketio.on('newgame selected', namespace='/')
def receive_message_from_user_newgame(message):
    print('USER MESSAGE FROM INDEX NEW GAME: {}'.format(message))

	
	
    emit('redirect from flask to index', {'url': url_for('newGame')})

# Message from HTML/JS after selecting a game 
@socketio.on('game selected', namespace='/')
def receive_message_from_user(message):
    print('USER MESSAGE FROM INDEX: {}'.format(message))
    global pinname
    global numplayers
    global game_selected
    global gamename
    global lines
    
    game_selected = 1
    
    # Load file
    
    fname = message + ".txt"
    
    filep = open(fname, "r")
    lines = filep.readlines()
    filep.close()
    gamename = lines[0]
    print('LINES INDEX: {}'.format(lines))
    
    if len(lines) > 15*6+1:
      print('ERROR!!! Too many lines in file {}'.format(fname))  
        
    pinname= rand.randint(1000,9999)
    numplayers = 0
    
    emit('redirect from flask to index', {'url': url_for('start',game=gamename,pin=pinname)}, namespace='/')
    
#----------------------start---------------------

# Message from HTML/JS after pressing Game Exit on Start page
@socketio.on('gameexit', namespace='/start')
def receive_message_from_user_start(message):
    print('USER MESSAGE EXIT GAME FROM START: {}'.format(message))

    global numplayers
    global players
    global game_selected
    global game_started

    reset_vars()

    emit('redirect from flask to start', {'url': url_for('index')},namespace='/start' )
    
    # Players --> PIN screen
    emit('redirect from flask to player', {'url': url_for('player')},broadcast=True,include_self=False,namespace='/player')

# Message from HTML/JS after pressing Game Start on Start page
@socketio.on('gamestart', namespace='/start')
def receive_message_from_user_start(message):
    print('USER MESSAGE START GAME FROM START: {}'.format(message))
     
    global gamename 
    global pinname
    global question_num
    global question_time
    global question_time_val
    global game_started
    global numplayers
    question_time = question_time_val
    question_num = 1
    game_started=1
 
    
    print('QUESTION NUMBER: {}'.format(question_num))
    
    # Display question on host screen
  
    emit('redirect from flask to question', {'url': url_for('question',game=gamename,pin=pinname,que_time=question_time,num_players=numplayers,player1=players[0],player2=players[1],player3=players[2],player4=players[3],player5=players[4])}, namespace='/question')

    # Answer screen on client screen
    p=0
    while p < numplayers:
        emit('message from flask to player', {'mode': 'waitcd','question_num':question_num,'numquestions':numquestions},room=playersid[p],include_self=False,namespace='/player')
        p=p+1

# send question time

#----------------------question---------------------
@socketio.on('gameexit', namespace='/question')
def receive_message_from_user_start(message):
    print('USER MESSAGE EXIT GAME FROM QUESTION: {}'.format(message))

    reset_vars()

    # Host --> index    
    emit('redirect from flask to question', {'url': url_for('index')},namespace='/question')

    # Players --> PIN screen
    emit('redirect from flask to player', {'url': url_for('player')},broadcast=True,include_self=False,namespace='/player')

# Question timeout (or all players answered)
@socketio.on('question timeout', namespace='/question')
def receive_message_from_user(message):
    print('USER MESSAGE FROM QUESTION TIMEOUT: {}'.format(message))
    global maxQuesNum
    global gamename 
    global pinname
    global question_num
    global question_time
    global numplayers
    global answers_status
    global playersid
    global players

    # Show results on host (question) page
    
    if(question_num<maxQuesNum):
      emit('message from flask to question',{'mode':'results','score1':scores[0],'score2':scores[1],'score3':scores[2],'score4':scores[3],'score5':scores[4]},namespace='/question')
	
    
    else:
      emit('message from flask to question',{'mode':'winTable','score1':scores[0],'score2':scores[1],'score3':scores[2],'score4':scores[3],'score5':scores[4]},namespace='/question') 
	
    # Show results on each player page
    
    p=0
    while p < numplayers:

      print('QUESTION TIMEOUT PLAYER: {}'.format(players[p]))
      print('QUESTION TIMEOUT PLAYER-ID: {}'.format(playersid[p]))
      print('QUESTION TIMEOUT ANSWER STATUS: {}'.format(answers_status[p]))
    
      if (answers_status[p] == 'correct'):
        print('QUESTION TIMEOUT ANSWER STATUS GOOD: {}'.format(answers_status[p]))
        emit('message from flask to player', {'mode': 'goodanswer','score':scores[p]},room=playersid[p],namespace='/player')
      elif (answers_status[p] == 'none'):
      
        print('QUESTION TIMEOUT ANSWER STATUS NONE: {}'.format(answers_status[p]))
        emit('message from flask to player', {'mode': 'noanswer','score':scores[p]},room=playersid[p],namespace='/player')
      else:
        emit('message from flask to player', {'mode': 'badanswer','score':scores[p]},room=playersid[p],namespace='/player')
    
      p += 1      
      
    
      
      
# Timeout before question has started      
@socketio.on('question timeoutp', namespace='/question')
def receive_message_from_user(message):
    print('USER MESSAGE FROM PRE-QUESTION TIMEOUT: {}'.format(message))
 

    global gamename 
    global pinname
    global question_num
    global question_time
    global lines
    global answers
    global correct_answer
    global answers_status
    global numanswers
    global numplayers
    
    linen = (question_num-1) * 6+1

    print('LINES QUESTION: {}'.format(lines))

    
    answers_status = ['none','none','none','none','none']
    numanswers = 0

    # Save the correct answer (from the file)
    correct_answer = lines[linen+5]

    # Display the question on Host
    startTime = datetime.datetime.now()
    microSecStart=startTime.microsecond
    print(startTime)
    print('hu')
    print('ANSWER 4: {}'.format(lines[linen+4]))
    
    emit('message from flask to question',{'mode':'question','question':lines[linen],'answer1':lines[linen+1],'answer2':lines[linen+2],'answer3':lines[linen+3],'answer4':lines[linen+4]},namespace='/question')    

    # Display the answer on Player
    p=0
    while p < numplayers:
        emit('message from flask to player', {'mode': 'answer','question_num':question_num,'numquestions':numquestions},room=playersid[p],include_self=False,namespace='/player')
        p=p+1



# Timeout before question has ended      
@socketio.on('nextquestion', namespace='/question')
def receive_message_from_user(message):
    print('USER MESSAGE FROM NEXT QUESTION: {}'.format(message))
    global numplayers
    global question_num
    question_num += 1
   
    print('NEXT QUESTION NUMBER: {}'.format(question_num))
   
    # Start the pre-question timeout counter
    emit('message from flask to question',{'mode':'prequestion','question_num':question_num},namespace='/question')    


    p=0
    while p < numplayers:
        emit('message from flask to player', {'mode': 'waitcd','question_num':question_num,'numquestions':numquestions},room=playersid[p],include_self=False,namespace='/player')
        p=p+1
	
#----------------------newGame---------------------	
@socketio.on('gameexit', namespace='/newGame')
def receive_message_from_user_start(message):
    print('USER MESSAGE EXIT GAME FROM QUESTION: {}'.format(message))

    reset_vars()

    # Host --> index    
    emit('redirect from flask to newGame', {'url': url_for('index')},namespace='/newGame')

	

@socketio.on('gameChange selected', namespace='/newGame')
def receive_message_from_user_gameChange(message):
    global game1_first_name
    global game2_first_name
    global game3_first_name
    global game4_first_name
    global number
    global numQues
    print('USER MESSAGE FROM INDEX GAME CHANGE: {}'.format(message))	

    number = message[-1]	
    if message[:-1]=='':
        emit('message from flask to newGame', {'mode': 'badGameName'})
    elif len(message)>18:
        emit('message from flask to newGame', {'mode': 'badGameName'})
    else:
        if number == '1':
	
          game1_first_name = message[:-1]
        elif number == '2':
	
          game2_first_name = message[:-1]
        elif number == '3':
	
          game3_first_name = message[:-1]		
        elif number == '4':
	    
            game4_first_name = message[:-1]		
	
	# with is like your try .. finally block in this case
        with open('Trivia' + number + '.txt', 'r') as file:
		# read a list of lines into data
            data = file.readlines()

	# and write everything back
        with open('Trivia' + number + '.txt', 'w') as file:
	    # now change the 2nd line, note that you have to add a newline
            data[0] = message[:-1] + '\n'
            file.writelines( data )
        numQues=1
        emit('redirect from flask to newGame', {'url': url_for('newGameQuestions')},  namespace='/newGame')
		

#----------------------newGameQuestions---------------------	
	
@socketio.on('questionChange selected', namespace='/newGameQuestions')
def receive_message_from_user_questionChange(message):
    global question
    global answer1
    global answer2
    global answer3
    global answer4
    global correctAns
    global number
    global numQues
    print('USER MESSAGE FROM INDEX Question CHANGE: {}'.format(message))	
	
    list= message.split("/n")
    question=list[0]
    answer1=list[1]
    answer2=list[2]	
    answer3=list[3]
    answer4=list[4]
    correctAns=list[5]	

	# with is like your try .. finally block in this case
    with open('Trivia' + number + '.txt', 'r') as file:
		# read a list of lines into data
        data = file.readlines()
    if question=='':
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})
    elif answer1=='':
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})
    elif answer2=='':
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})
    elif answer3=='':
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})
    elif answer4=='':
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})
    elif correctAns=='':
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})
    elif len(question)>75:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	
    elif len(answer1)>20:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	  
    elif len(answer2)>20:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	
    elif len(answer3)>20:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	  
    elif len(answer4)>20:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	
    elif int(correctAns)>4:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	
    elif int(correctAns)<1:
        emit('message from flask to newGameQuestions', {'mode': 'badQuestion', 'numQuestion': numQues})	


    else:
        if(numQues<15):
                with open('Trivia' + number + '.txt', 'w') as file:
	        # now change the 2nd line, note that you have to add a newline
                    data[(numQues-1)*6+1] = question + '\n'
                    data[(numQues-1)*6+2] = answer1 + '\n'
                    data[(numQues-1)*6+3] = answer2 + '\n'
                    data[(numQues-1)*6+4] = answer3 + '\n'
                    data[(numQues-1)*6+5] = answer4 + '\n'
                    data[(numQues-1)*6+6] = correctAns + '\n'
                    file.writelines( data )
                numQues= numQues+1	
                emit('message from flask to newGameQuestions', {'numQuestion': numQues})		
        else:
	
                emit('redirect from flask to newGameQuestions', 	{'url': url_for('index')},namespace='/newGameQuestions')			

@socketio.on('gameexit', namespace='/newGameQuestions')
def receive_message_from_user_start(message):
    print('USER MESSAGE EXIT GAME FROM QUESTION: {}'.format(message))

    reset_vars()

    # Host --> index    
    emit('redirect from flask to newGameQuestions', {'url': url_for('index')},namespace='/newGameQuestions')
#----------------------player---------------------	    
   
@socketio.on('gamepin', namespace='/player')
def receive_message_from_user_join(message):

    global pinname
    global game_selected
    global numplayers
    global game_started	
    print('USER MESSAGE PIN ENTERED FROM PLAYER: {}'.format(message))
    print('pin name: {}'.format(pinname))
    if game_selected == 0:
      # Game not selected
      emit('message from flask to player', {'mode': 'nogame'})
	  
    else:  
      if int(message) == int(pinname):  
          print(numplayers)
          if(numplayers>4):
              print('ooooooooof')
              emit('message from flask to player', {'mode': 'tooManyPlayers'})
          elif game_started==1:
              emit('message from flask to player', {'mode': 'late2game'})
          else:
              emit('message from flask to player', {'mode': 'pinok'})
      else:
        emit('message from flask to player', {'mode': 'badpin'})
   
   
   
   
   # Message from HTML/JS after entering the nickname 
@socketio.on('nickname', namespace='/player')
def receive_message_from_user_join(message):
    print('USER MESSAGE NICKNAME: {}'.format(message))

    global pinname
    global gamename
    global numplayers
    global players
    global playersid
    global numquestions
    global question_num


    print('QUESTION NUMBER: {}'.format(question_num))

    if message == '':
      # Error
      emit('message from flask to player', {'mode': 'badname'})
    elif len(message) >10:
      # Error
      emit('message from flask to player', {'mode': 'badname'})
    elif(numplayers>4):
        print('ooooooooof')
        emit('message from flask to player', {'mode': 'tooManyPlayers'})
    elif game_started==1:
         emit('message from flask to player', {'mode': 'late2game'})
    else:     
    
      players[numplayers] = message     # Name of player
      playersid[numplayers] = request.sid
      
      print('NICKNAME PLAYER ID: {}'.format(playersid[numplayers]))
      
      numplayers += 1
                 
      # Host
      # Doesn't work without broadcast. Why?
      emit('message from flask to start',{'numplayers':numplayers,'player1':players[0],'player2':players[1],'player3':players[2],'player4':players[3],'player5':players[4]},broadcast=True,include_self=False,namespace='/start')
      
      # Players (sent to each player), message = player name
      emit('message from flask to player', {'mode': 'nameok','game':gamename,'pin':pinname,'player':message,'score':'0','numquestions':numquestions,'question_num':question_num})

   
   
@socketio.on('answer', namespace='/player')
def receive_message_from_user_join(message):
    print('USER MESSAGE ANSWER: {}'.format(message))
         
    global numplayers
    global players
    global playersid
    global scores    
    global numanswers
    global correct_answer
    global answers_status

    print('USER MESSAGE ANSWER CORRECT ANSWER: {}'.format(correct_answer))          

    numanswers += 1

    id = request.sid 
    
    # Find the player whose ID was sent in the message    
    p=0
    en=0
    while (p < numplayers) and (en == 0):
      
      
      if id == playersid[p]:
         en=1
         # Player found using request ID. Now check if his/her answer was correct (message == answer from player)
         
         print('USER MESSAGE ANSWER PLAYER: {}'.format(players[p]))
         
         
         # correct_answer is a string (from file)
         # message == player answer
         if message == int(correct_answer):
           endTime = datetime.datetime.now()
           microSecEnd=endTime.microsecond
           print(startTime)
           print(endTime)
		   
           MicroTimePast=microSecEnd-microSecStart
           miliSecPast= MicroTimePast/1000
           print('USER MESSAGE ANSWER CORRECT ANSWER INSIDE: {}'.format(correct_answer))        
           print('USER MESSAGE ANSWER PLAYER ANSWER: {}'.format(message))
         
           answers_status[p] = 'correct'
           scoreAdd= int(10000 - miliSecPast)
           print(scoreAdd)
           scores[p] += scoreAdd  
         else:
           answers_status[p] = 'wrong'
           
      else:
         p += 1      
   
    print('USER MESSAGE NUMPLAYERS: {}'.format(numplayers))
    print('USER MESSAGE NUMANSWERS: {}'.format(numanswers))
   
    if numanswers < numplayers:
      # If not last answer then move player into "wait"
      
      print('USER MESSAGE WAIT4ALL: {}'.format(numanswers))
      
      emit('message from flask to player', {'mode': 'wait4all'}) 
    else:
      # Move host into "statistics" view (done via emulating a "question timeout")
      
      print('USER MESSAGE DONE: {}'.format(numanswers))
      
      # Doesn't work without broadcast. Why?
      emit('message from flask to question',{'mode':'done'},broadcast=True,include_self=False,namespace='/question')
     


if __name__ == '__main__':
    socketio.run(app)
