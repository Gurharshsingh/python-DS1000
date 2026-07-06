#oops - object oriented programming

class Dog:
    def __init__(self,name,age,breed):
        self.name = name
        self.age = age
        self.breed = breed

    def bark(self):
        print(f"{self.name} says Woof!")

    def info(self):
        print("Name is: ", self.name,"Age is:",self.age)


    # updating values

    def birthday(self):
        self.age +=1
        print("You are", self.age, "years old")



dog1 = Dog("Buddy",5,"Golden Retriever")
dog2 = Dog("Lucy",3,"Labrador")


print(dog1.name, dog2.name)
print(dog1.age)
print(dog1.breed)

#method calling

dog1.bark()
dog2.info()

dog2.birthday()
dog2.info()


class BankAccount:
    
    def __init__(self, owner_name, initial_balance=0.0):
        self.owner = owner_name
        
        # 'balance' is the state of the account.
        # We start it with an initial value provided during creation.
        self.balance = initial_balance
        
        # We can also keep a transaction history as a list attribute
        self.transaction_history = []
        
        # Log the initial creation
        self.transaction_history.append(f"Account opened with ${self.balance:.2f}")

    def deposit(self, amount):
        """Adds money to the account balance."""
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Credit: +${amount:.2f}")
            print(f"Success: ${amount:.2f} deposited into {self.owner}'s account.")
        else:
            print("Error: Deposit amount must be positive.")

    def withdraw(self, amount):
        """Removes money from the account if funds are sufficient."""
        if amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return

        if amount > self.balance:
            print(f"Error: Insufficient funds! You only have ${self.balance:.2f}.")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Debit: -${amount:.2f}")
            print(f"Success: ${amount:.2f} withdrawn from {self.owner}'s account.")

    def show_balance(self):
        """Displays the current account balance."""
        print(f"--- {self.owner}'s Current Balance: ${self.balance:.2f} ---")

    def print_statement(self):
        """Prints out the entire history of transactions."""
        print(f"\n========== BANK STATEMENT FOR {self.owner.upper()} ==========")
        for transaction in self.transaction_history:
            print(transaction)
        print(f"Final Balance: ${self.balance:.2f}")
        print("====================================================\n")


# ==========================================
# Main Program: Testing the BankAccount Class
# ==========================================

print("1. Creating Accounts")
# We can create accounts with or without an initial balance
b_account = BankAccount("Balwinder", 50000.0)


print("\n2. Making Transactions")
b_account.deposit(2000.0)
b_account.withdraw(10000.0)
b_account.withdraw(100000.0) # This should fail due to logic in the method!



# print("\n3. Showing Individual Balances")
b_account.show_balance()

# print("\n4. Printing Statements (Showing stored complex state)")
b_account.print_statement()



    


