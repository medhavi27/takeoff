Notes on the functionality:

I was able to implement everything and write tests, but encountered some issues, so please read these notes before proceeding:

1. ***Very Important*** 
Python3 does not accept leading zeros in a number, and the dataset contained a pin 0075.
Therefore, for the program to work correctly you MUST enter the pin as a string. It's a bit inefficient, but it's what I had to do.

2. VALIDATION: 
- If you enter an incorrect user ID or pin- the program ends and you have to start again.

- If you enter an invalid input (number not in the options)  on the actions menu once you are logged in, the program handles that and asks for a different input.

- If you enter a non-numeric input on the actions menu once you are logged in the program exits. This might seem inefficient but it is an ATM, and those do not have non-numeric inputs 

- If you enter a bad (or negative) input for the amount to deposit or withdraw- the program does not accept it and sets the amount to 0

- If, after completing an action, you are back on the actions menu and you enter a non-numeric, the program ends. If you enter a number not in the options it prompts you for a valid input


3. The 2 minute timeout function: I was able to implement the automatic logout after 2 minutes, but the display in the terminal stays the same until you actually try to do something. So it won't show you "you have been logged out" and exit the terminal, but it will print "session timed out" and if you try to make a withdrawal or do anything else, it will return "authorization required", which is what the instructions said to do. 

4. Time out: Once a user's active authorization ends- all functions other than logout and end return "authorization required". At this point, your only option is to end the program and log in again. Typing in any random input (or selecting the end option) will do this for you. 

5. Interaction with the input program happens through the terminal. Select numbers that map to options, and press 6 to exit.

6. Inside the "takeoff" directory, there are the following files:
- acc.csv: contains the users, pins and balances given to me in a csv file
- machine.py: contains the machine class and methods
- user.py: contains the user class and methods
- session.py: contains the session class and methods
- tests.py: contains tests
- main.py: main file, contains the code to run the program
- notes.txt: contains this information

7. To start the program, navigate into the "takeoff" directory, and type in "python3 main.py"

8. To run tests, navigate into the "takeoff" directory, and type in "python3 tests.py"


