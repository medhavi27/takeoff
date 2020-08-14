import unittest
from session import Session
from machine import Machine
from user import User
import main as Main
from datetime import datetime

class TestStringMethods(unittest.TestCase):
    session = Session()
    Session.set_dict(session)
    machine = Machine()
    machine.set_balance(10000)

    def test_authorize(self):
        """
        Tests the authorize function- pass, fail and does not exist
        """
        user1 = User(2001377812, '5950', 0)
        user2 = User(2001377812, '0075', 0)
        user3 = User(1203939932, '0075', 0)
        pas = Session.authorize(self.session, user1, '5950')
        fail = Session.authorize(self.session, user2, '0075')
        notexist = Session.authorize(self.session, user3, '0075')
        self.assertEqual(pas, "2001377812 successfully authorized")
        self.assertEqual(fail, "Authorization failed")
        self.assertEqual(notexist, "Authorization failed")

    def test_balance(self):
        """
        tests the get_user_balance function- positive, negative and zero balance
        also when authorization is required
        """
        user1 = User(2001377812, '5950', 10000)
        Session.authorize(self.session, user1, '5950')
        Session.withdraw(self.session, self.machine, user1, 400,datetime.now())
        Session.withdraw(self.session,self.machine, user1, 160, datetime.now())
        Session.deposit(self.session, self.machine, user1, 400, datetime.now())
        self.assertEqual('Current balance: 9840', Session.get_user_balance(self.session, user1))
        user2= User(2001377812, '5950', 0)
        Session.authorize(self.session, user2, '5950')
        self.assertEqual('Current balance: 0', Session.get_user_balance(self.session, user2))
        user3 = User(2001377812, '5950', -2020)
        Session.authorize(self.session, user2, '5950')
        self.assertEqual('Current balance: -2020', Session.get_user_balance(self.session, user3))
        Session.logout(self.session, user3)
        self.assertEqual("Authorization required", Session.get_user_balance(self.session, user3))

    def test_get_history(self):
        """
        tests the get_history function- for empty and valid history, and for authorization required
        """
        user1 = User(2001377812, '5950', 10000)
        Session.authorize(self.session, user1, '5950')
        self.assertEqual("No history found", Session.get_history(self.session, user1))
        a=datetime.now()
        Session.withdraw(self.session, self.machine, user1, 400, a)
        a= a.strftime("%d/%m/%Y %H:%M:%S")
        b=datetime.now()
        Session.withdraw(self.session, self.machine, user1, 160, b)
        b= b.strftime("%d/%m/%Y %H:%M:%S")
        c=datetime.now()
        Session.deposit(self.session, self.machine, user1, 400, c)
        c= c.strftime("%d/%m/%Y %H:%M:%S")
        x = Session.get_history(self.session, user1)
        string = "\n%s 400 9840\n%s -160 9440\n%s -400 9600" %(a,b,c)
        self.assertEqual(string, x)
        Session.logout(self.session, user1)
        self.assertEqual("Authorization required", Session.get_history(self.session, user1))



    def test_deposit(self):
        """
        tests the deposit function- if everything goes well and if authorization is required
        """
        user1 = User(2001377812, '5950', 10000)
        Session.authorize(self.session, user1, '5950')
        a=datetime.now()
        success = Session.deposit(self.session, self.machine, user1, 50, a)
        self.assertEqual(success, "Current balance: 10050")
        Session.logout(self.session, user1)
        self.assertEqual("Authorization required", Session.deposit(self.session, self.machine, user1, 50, a))

    def test_withdrawal(self):
        """
        tests the deposit function- check overdraft, not multiple of 200, whether the machine is empty,
        whether the machine has enough money, whether the user has enough money
        """
        user1 = User(7089382418, '0075', 100)
        Session.authorize(self.session, user1,'0075')
        a = datetime.now()
        Session.withdraw(self.session, self.machine, user1, 400, a)
        b = datetime.now()
        overdrawn = Session.withdraw(self.session, self.machine, user1, 160, b)
        self.assertEqual("Your account is overdrawn! You may not make withdrawals at this time.", overdrawn)

        user2 = User(2001377812, '5950', 100)
        Session.authorize(self.session, user2,'5950')
        c = datetime.now()
        not_multiple = Session.withdraw(self.session, self.machine, user2, 412, c)
        self.assertEqual("Unable to process your withdrawal at this time.", not_multiple)

        self.machine.set_balance(0)
        empty_machine = Session.withdraw(self.session, self.machine, user2, 412, c)
        self.assertEqual("Unable to process your withdrawal at this time.", empty_machine)

        #overdraft tests
        user3 = User(2001377812, '5950', 100)
        Session.authorize(self.session, user3,'5950')
        self.machine.set_balance(120)
        not_enough_in_machine_or_user = Session.withdraw(self.session, self.machine, user3, 400, c)
        string= "Unable to dispense full amount requested at this time\n Amount dispensed: 120 \n You have been charged an overdraft fee of $5. Current balance: -25"
        self.assertEqual(not_enough_in_machine_or_user, string)

        user4= User(2001377812, '5950', 100)
        Session.authorize(self.session, user4,'5950')
        self.machine.set_balance(10000)
        not_enough_in_user = Session.withdraw(self.session, self.machine, user4, 300, c)
        string = "Amount dispensed: 300 \n You have been charged an overdraft fee of $5. Current balance: -205"
        self.assertEqual(not_enough_in_user, string)

        user5= User(2001377812, '5950', 10000)
        Session.authorize(self.session, user5,'5950')
        self.machine.set_balance(300)
        not_enough_money_in_machine = Session.withdraw(self.session, self.machine, user5, 600, c)
        string="Unable to dispense full amount requested at this time\n Amount dispensed: 300 \. Current balance: 9700"
        self.assertEqual(not_enough_money_in_machine, string)

        #all goes well
        user6= User(2001377812, '5950', 10000)
        Session.authorize(self.session, user6,'5950')
        self.machine.set_balance(10000)
        success = Session.withdraw(self.session, self.machine, user6, 600, c)
        string="Amount dispensed: 600 \n Current balance: 9400"
        self.assertEqual(success, string)

        #authorization required
        Session.logout(self.session, user6)
        self.assertEqual("Authorization required", Session.withdraw(self.session, self.machine, user6, 20, c))


    def test_logout(self):
        """
        tests logout function- simple logout, and logout when no one is logged in
        """
        user6= User(2859459814, '7386', 10000)
        Session.authorize(self.session, user6, '7386')
        msg = Session.logout(self.session, user6)
        self.assertEqual("Account 2859459814 logged out", msg)
        self.assertEqual("No account is currently authorized", Session.logout(self.session, user6))

    def test_timeout(self):
        """
        tests timeout function- includes a print message
        """
        user6= User(2859459814, '7386', 10000)
        Session.authorize(self.session, user6, '7386')
        Session.timeout(self.session, user6, 1597428189999999990.6783)
        self.assertEqual("Authorization required", Session.get_user_balance(self.session, user6))




























if __name__ == '__main__':
    unittest.main()