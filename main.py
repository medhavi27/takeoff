from session import Session
from machine import Machine
from user import User
import csv
import time
from datetime import datetime

def main():
    """
    this is the main function- it creates a machine, and asks the user for input
    """
    machine = Machine()
    machine.set_balance(10000)
    session = Session()
    Session.set_dict(session)

    input_var = None
    try:
        input_var = eval(input("Welcome to the ATM- please enter your user id "))
        input_var = int(input_var)
    except (SyntaxError, NameError, TypeError):
        print("Not a valid input")

    if input_var in session.dic:
        bal = session.dic[input_var][1]
        try:
            pin = input("Please enter your pin ")
        except(SyntaxError, NameError, TypeError):
            print("Not a valid pin")
            pin = '0000'
        user = User(input_var, pin, bal)
        print((Session.authorize(session, user, pin)))
        amount=None
        actions = {1: ["withdraw", 4], 2: ["deposit",4], 3: ["get_user_balance", 1], 4: [ "get_history",1] , 5: ["logout", 1] , 6:["end", 0] }
        action=None
        if session.session_active:
            #Validating input so we can avoid syntaxerrors
            try:
                action = eval(input(
                    "What would you like to do today? Select a number: \n 1: Withdraw \n 2: Deposit \n 3: Check balance \n 4: Check history \n 5. Log out \n 6. Shut down "))
                action = int(action)
            except (SyntaxError, NameError, TypeError):
                print("Not a valid input")
            while action:
                session.timeout(user, time.time())
                try:
                    action=int(action)
                except (SyntaxError, NameError, TypeError):
                    print("Not a valid input")
                if action not in list(actions.keys()):
                    action = eval(input("Not a valid input, try again "))
                else:
                    func = actions[action][0]
                    params=actions[action][1]
                    if params==4:
                        if func=="withdraw":
                            # Validating input so we can avoid syntaxerrors
                            try:
                                amount = eval(input("Please enter an amount (multiple of $20) to withdraw "))
                                amount = int(amount)
                                assert(amount>0)
                            except (SyntaxError, NameError, TypeError, AssertionError):
                                amount = 0
                                print("Not a valid amount")
                        else:
                            # Validating input so we can avoid syntaxerrors
                            try:
                                amount = eval(input("Please enter an amount to deposit "))
                                amount = int(amount)
                                assert (amount > 0)
                            except (SyntaxError, NameError, AssertionError):
                                amount = 0
                                print("Not a valid amount")
                        print((getattr(Session, func)(session,machine,user,amount,datetime.now())))
                    elif params==1:
                        print((getattr(Session, func)(session,user)))
                    else:
                        print((getattr(Session, func)(session)))
                try:
                    action=eval(input("Anything else? Select a number: \n 1: Withdraw \n 2: Deposit \n 3: Check balance \n 4: Check history \n 5. Log out \n 6. End "))
                except (SyntaxError, NameError, TypeError):
                    print("Not a valid input- exiting program")
                    print(Session.end(session))


    else:
        print("Sorry, you are not a user of this bank ")


if __name__ == '__main__':
    main()
