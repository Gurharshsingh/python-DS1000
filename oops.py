# class Phone:
#     def __init__(self, brand, model):
#         self.brand = brand
#         self.model = model

#     def call(self):
#         print(f"{self.brand} {self.model} is ringing")



# myphone = Phone("Oneplus", 11)
# print(myphone.model)
# myphone.call()


# phone = Phone("infinix", 10)
# print(phone.brand)




class BankAccount:
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount
        self.th = []
        self.th.append(f"Account Opened with ${self.amount}")

    def deposit(self,amt):
        self.amount+=amt
        self.th.append(f"Credit - ${amt}")
        print("Amount added Sucessfully!")

    def withdraw(self,amt):
        if amt > self.amount:
            print("Insufficient Balance")
        elif amt < 0:
            print("Invalid Value Entered")
        else:
            self.amount-=amt
            self.th.append(f"Debit - ${amt}")
            print("Amount withdrawn Sucessfully!")

    def check_balance(self):
        print("Account Balance: ",self.amount)

    
    def transaction(self):
        print(f'''============================
        Bank Statement\n
============================ ''')
        for i in self.th:
            print(i)

        print("Current Balance:",self.amount)
        print(f'''============================
        End of Statement
============================
         ''')


acc1 = BankAccount("Ashima", 10000)
print(acc1.amount)

acc2  = BankAccount("Inderpreet", 12000)
print(acc2.name)

acc1.deposit(2500)

acc2.withdraw(1200)
acc2.deposit(3000)

acc1.check_balance()
acc2.check_balance()

acc1.transaction()
acc2.transaction()




