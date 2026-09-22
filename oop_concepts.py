# Object-Oriented Programming (OOP) Concepts in Python

# 1. Inheritance
# 2. Polymorphism
# 3. Abstraction
# 4. Encapsulation

# ==========================================
# 1. INHERITANCE
# ==========================================
# Concept: Inheritance allows a new class (child class) to inherit attributes 
# and methods from an existing class (parent class). This promotes code reusability.

print("--- 1. INHERITANCE EXAMPLE ---")

# Parent Class
class Vehicle:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def start_engine(self):
        return f"The engine of {self.brand} {self.model} is starting..."

# Child Class inheriting from Vehicle
class Car(Vehicle):
    def __init__(self, brand, model, doors):
        # Call the parent class __init__ method
        super().__init__(brand, model)
        self.doors = doors

    def open_trunk(self):
        return f"Opening the trunk of the {self.brand} {self.model}."

# Demonstrating Inheritance
my_car = Car("Toyota", "Camry", 4)
print(my_car.start_engine())  # Inherited method
print(my_car.open_trunk())     # Child-specific method
print()


# # ==========================================
# # 2. POLYMORPHISM
# # ==========================================
# # Concept: Polymorphism ("many forms") allows different classes to have methods 
# # with the same name but different implementations. The correct method is 
# # called based on the object type.

# print("--- 2. POLYMORPHISM EXAMPLE ---")

class Dog:
    def make_sound(self):
        return "Woof! Woof!"

class Cat:
    def make_sound(self):
        return "Meow!"

class Duck:
    def make_sound(self):
        return "Quack!"

# # # A function that accepts any object with a make_sound method
def animal_choir(animal_object):
    print(animal_object.make_sound())

# # Demonstrating Polymorphism
dog = Dog()
cat = Cat()
duck = Duck()

print(dog.make_sound())

animal_choir(dog)
animal_choir(cat)
animal_choir(duck)
print()


# # ==========================================
# # 3. ABSTRACTION
# # ==========================================
# # Concept: Abstraction is the concept of hiding the complex implementation details 
# # and showing only the essential features of an object to the user.
# #
# # Real-World Analogy: 
# # When you drive a car, you interact with the steering wheel, accelerator, and brakes. 
# # You don't need to know the complex internal combustion details, the gear ratio, 
# # or how the engine cylinders fire to drive the car. The steering wheel is an "abstract interface".
# #
# # Why do we use Abstraction?
# # 1. Reduces Complexity: Users of your class only need to understand what it does, not how it does it.
# # 2. Safety & Security: Protects the integrity of the system by hiding internal workings.
# # 3. Enforces a Contract: It defines a template/blueprint that all derived subclasses MUST follow.
# #
# # How it is achieved in Python:
# # Python uses the 'abc' (Abstract Base Classes) module.
# # - An abstract class inherits from 'ABC'.
# # - It contains '@abstractmethod' decorators for methods that subclasses MUST override.
# # - You CANNOT create an object (instantiate) of an abstract class directly.


# print("--- 3. ABSTRACTION EXAMPLE ---")

from abc import ABC, abstractmethod

class BankApp(ABC):
    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def check_balance(self):
        pass

class MobileBankApp(BankApp):
    def login(self):
        return "Logging in via fingerprint or face ID verification."

    def check_balance(self):
        return "Retrieving account balance from mobile secure storage: $5,240"

# # Attempting to instantiate the abstract class directly would raise a TypeError:
# app = BankApp() # Error!

# # Demonstrating Abstraction using concrete subclass
my_app = MobileBankApp()
print(my_app.login())
print(my_app.check_balance())
print()


# ==========================================
# 4. ENCAPSULATION
# ==========================================
# Concept: Encapsulation wraps data (attributes) and behaviors (methods) into 
# a single unit (class), restricting direct access to some of the object's components.
# In Python, we prefix variables with one underscore (_) for protected access,
# or two underscores (__) for private access (using name mangling).

# print("--- 4. ENCAPSULATION EXAMPLE ---")

class StudentAccount:
    def __init__(self, name, roll_number):
        self.name = name                 # Public attribute
        self.roll_number = roll_number   
        self.__gpa = 3.8                 # Private attribute (restricted access)

#     # Getter method to safely access the private GPA attribute
    def get_gpa(self,code):
        if code == 1234:
            return self.__gpa
        else:
            return "Invalid code"

#     # Setter method to safely modify/validate the private GPA attribute
    def set_gpa(self, new_gpa):
        if 0.0 <= new_gpa <= 4.0:
            self.__gpa = new_gpa
        else:
            print("Invalid GPA! Must be between 0.0 and 4.0.")

# # Demonstrating Encapsulation
student = StudentAccount("Alice", "S1024")

print(f"Student Name: {student.name}")            # Direct access works (Public)
print(f"Roll Number: {student.roll_number}")     

# print(student.__gpa) # AttributeError: 'StudentAccount' object has no attribute '__gpa'

print(f"Current GPA (via getter): {student.get_gpa(1234)}") # Access via getter
student.set_gpa(3.9)                                     # Modify via setter
print(f"Updated GPA (via getter): {student.get_gpa(1234)}")
# student.set_gpa(5.5)                                     # Attempting invalid update
# print()
