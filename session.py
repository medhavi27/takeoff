import sys
from machine import Machine
from user import User
import csv
import time
from datetime import datetime

class Session:
    def __init__(self):
        self.current_user = None
        self.session_active = False
        self.last_func_time = None
        self.current_time=None
        self.dic = {}


    def set_current_time(self, time):
        """
        setter function for current time
        """
        self.current_time=time

    def get_current_time(self):
        """
        getter function for current time
        """
        return self.current_time


    def set_dict(self):
        """
        setter function for dictionary- key: account_id, value: [pin, balance]
        """
        reader = csv.reader(open('acc.csv', 'r'))
        # adding the users' account id, pin and balance to a dictionary for easy lookup
        next(reader, None)
        for row in reader:
            id = int(row[0])
            pin = row[1]
            bal = float(row[2])
            self.dic[id] = [pin, bal]

    def create_session(self, user):
        """
        @param user: User
        @return type: None
        """
        # input: a User object
        # creates a session, and user for the session
        # rtype: none
        self.current_user = user
        self.session_active = True
        self.last_func_time = time.time()
        return

    def timeout(self, user, time):
        # @param user: User 
        # calls the logout function there has been no activity for over 2 minutes
        # @return type: None
        self.set_current_time(time)
        if self.get_current_time() - self.last_func_time > 120:
            self.logout(user)
            print("SESSION TIMED OUT- end program and log in again")
        return

    def authorize(self, user, pin):
        """
        @param user: User
        @param pin: string
        @return type: string
        """
        self.last_func_time = time.time()
        k = user.account_id
        if k in self.dic:
            if self.dic[k][0] == pin:
                self.create_session(user)
                return "%s successfully authorized" % (user.account_id)
            else:
                return "Authorization failed"
        return "Authorization failed"

    def get_user_balance(self, user):
        """
        @param user: User
        @return type: string
        """
        if not self.current_user:
            return "Authorization required"
        self.last_func_time = time.time()
        return "Current balance: %s" % (user.balance)

    def get_history(self, user):
        """
        @param user: User
        @return type: string
        """
        if not self.current_user:
            return "Authorization required"
        self.last_func_time = time.time()
        if user.get_trans_history() == []:
            return "No history found"
        else:
            ret = ""
            hist = user.get_trans_history()
            for x in reversed(hist):
                ret = ret + "\n" + x
            return ret

    def withdraw(self, machine, user, amount, now):
        """
        @param machine: Machine
        @param user: User
        @param amount: int
        @param now: datetime
        @return type: string
        """
        self.last_func_time = time.time()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        if not self.current_user:
            return "Authorization required"
        if user.get_overdrawn():
            return "Your account is overdrawn! You may not make withdrawals at this time."
        if machine.get_balance() == 0 or amount % 20 != 0:
            return "Unable to process your withdrawal at this time."
        if user.balance < amount:
            user.set_overdrawn(True)
            if machine.get_balance() < amount:
                amount = machine.get_balance()
                bal = user.balance - amount - 5
                machine.set_balance(0)
                user.balance = bal
                ret = "Unable to dispense full amount requested at this time\n Amount dispensed: %s \n You have been charged an overdraft fee of $5. Current balance: %s" % (
                amount, str(user.balance))
                user.trans_history.append("%s -%s %s" % (dt_string, amount, user.balance))
                return ret

            else:
                bal = user.balance - amount - 5
                user.balance = bal
                machine.set_balance(machine.get_balance() - amount)
                ret = "Amount dispensed: %s \n You have been charged an overdraft fee of $5. Current balance: %s" % (
                amount, str(user.balance))
                user.trans_history.append("%s -%s %s" % (dt_string, amount, user.balance))
                return ret

        if machine.get_balance() < amount:
            amount = machine.get_balance()
            bal = user.balance - amount
            user.balance = bal
            machine.set_balance(0)
            ret = "Unable to dispense full amount requested at this time\n Amount dispensed: %s \. Current balance: %s" % (
            amount, str(user.balance))
            user.trans_history.append("%s -%s %s" % (dt_string, amount, user.balance))
        else:
            bal = user.balance - amount
            user.balance = bal
            machine.set_balance(machine.get_balance() - amount)
            ret = "Amount dispensed: %s \n Current balance: %s" % (amount, str(user.balance))
            user.trans_history.append("%s -%s %s" % (dt_string, amount, user.balance))
        return ret

    def deposit(self, machine, user, amount, now):
        """
        @param machine:
        @param user:
        @param amount:
        @return type: string
        """
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        self.last_func_time = time.time()
        if not self.current_user:
            return "Authorization required"
        curr_bal = user.balance
        if amount+curr_bal>0:
            user.set_overdrawn(False)
        bal = user.balance + amount
        user.balance = bal
        machine.set_balance(machine.get_balance() + amount)
        user.trans_history.append("%s %s %s" % (dt_string, amount, user.balance))
        return "Current balance: %s" % (user.balance)


    def logout(self, user):
        """
        @param user: User
        @return type: string
        """
        if self.current_user:
            self.current_user = None
            self.session_active == False
            return "Account %s logged out" % (user.account_id)

        else:
            return "No account is currently authorized"


    def end(self):
        sys.exit()
