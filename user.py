class User:
    #class to keep track of a user, account id, pin, balance
    #and transaction history
    def __init__(self, id, pin, bal):
        self.account_id = id
        self.pin = pin
        self.balance = bal
        self.overdrawn=False
        self.trans_history = []

    def get_trans_history(self):
        """
        getter function for a user's transaction history
        """
        return self.trans_history

    def get_overdrawn(self):
        """
        getter function for a user's overdraft history
        """
        return self.overdrawn

    def set_overdrawn(self):
        """
        setter function for a user's overdraft history
        """
        self.overdrawn = True


