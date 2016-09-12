The aim of this project is to create a simple Palindrome Web Game
(definition below). 

The idea of the game is to submit a word or string, and
gain a certain amount of points if the sentence is a palindrome. Here is what
can happen in the game:

Palindrome Definition:
A word, line, verse, number, sentence, etc, reading the same backward as
forward. E.g.
Madam, I'm Adam
Poor Dan is in a droop
Do geese see God?

The player will have the possibility to submit a sentence as well as his/her
name to the server.
  ● If the sentence is a palindrome then the user's current score must be
    increased by half of the size of the palindrome size.
  ● If the player's name is already registered in the game (if his name
    already exists), then add the score to the player. Else create a new
    record for the user. Note - The details are held in memory for a session,
    and do not need to be persisted to a file or database.
    The player also has the possibility of getting into the "Hall of Fame", which is
    displayed on a web page/api
  ● This lists the 5 best players, and ranks them by score
  
If the server is reset, the list of user-score must be empty.
The app must is thread safe, and multiple users may access it at once
