class Machine:
    #class to keep track of the machine
    def __init__(self):
        self.balance = 0

    def get_balance(self):
        """
        getter function for balance
        """
        return self.balance
    def set_balance(self, bal):
        """
        setter function for balance
        """
        self.balance=bal
