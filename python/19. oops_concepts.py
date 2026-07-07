# 1. encapsulation - to make elments private so that it cannot be acsessed directly


from abc import abstractmethod
class Vehicle():
    def __init__(self,model,year):
        self.model = model
        self.__year = year

    def info(self):
        return self.model, self.__year
    


# 2. inheritance -  to give properties of parent class to child class
# 3. polymorphism - many forms 


class Mahindra(Vehicle):
    def engine_sound(self):
        return f"{self.model} goes Vroom"

class Tesla (Vehicle):
    def engine_sound(self):
        return f"{self.model} goes Silence"





car1 = Mahindra("Scorpio",2023)
car2 = Tesla("Model S",2023)

print(car1.engine_sound())
print(car2.info())

#abstraction - to hide unnecessary data, show only essential data
