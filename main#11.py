class Bankaccaunt:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance

    @property
    def my_balance(self):
        return self.balance

client1 = Bankaccaunt(name='Pasha')
print(client1.my_balance)
client1.balance = 5000
print(client1.my_balance)
