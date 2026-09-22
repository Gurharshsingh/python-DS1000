# oops = object oriented programming 
# 
# 

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says woof woof!")

    


dog1  = Dog('Rambo', "German Shepherd")
dog2  = Dog('Buzo', 'Labrador')

print("Name of dog:", dog1.name)
print("Breed of dog:", dog1.breed)

print("Name of dog:", dog2.name)
print("Breed of dog:", dog2.breed)

dog2.bark()
dog1.bark()



class BankAccount:
    def __init__(self,name,balance):
        self.name = name
        self.balance = balance
        self.transaction_history = []
        self.transaction_history.append("Account opened with 10000₹")

    def deposit(self,amount):
        self.balance+=amount
        self.transaction_history.append(f"Credit - \t{amount}")
        print(f"\nDeposited {amount}₹. Current Balance : {self.balance}\n")
    
    def withdraw(self,amount):
        if self.balance< amount:
            print("Insufficient Balance!")
        else:
            self.balance-=amount
            self.transaction_history.append(f"Debit - \t{amount}")
            print(f"\nWithdraw {amount}₹. Current Balance : {self.balance}\n")

    def check(self):
        print(f"\n Current Balance : {self.balance}\n")
        
    def statement(self):
        print('='*5,"Transaction History :",'='*5,"\n")
        for i in self.transaction_history:
            print(i)
        

cust1 = BankAccount("Jasika",100000)

print(cust1.name)
print(cust1.balance)
cust1.deposit(3000)
cust1.withdraw(24000)
cust1.deposit(30000)
cust1.deposit(4500)
cust1.withdraw(9000)
cust1.check()
cust1.statement()
        


