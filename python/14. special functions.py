def section(title):
    print("\n" + "="*20 + " " + title + " " + "="*20)

print("===============functions====================")

# # 1. Lambda Functions
section("1. Lambda Functions")
# A lambda function is a small anonymous function.
# A lambda function can take any number of arguments, but can only have one expression.
# Syntax: lambda arguments : expression

#double
 
double = lambda x:x*2

print(double(4))

# add

add = lambda a,b,c:a+b+c
print(add(5,5,5))

# check

check = lambda a:"even" if a%2==0 else "odd"
print(check(5))



# # 2. Map Function
section("2. Map Function")
# The map() function executes a specified function for each item in an iterable.
# The item is sent to the function as a parameter.
# Syntax: map(function, iterables)


li = ['1','2','3','4','5','6','7','8','9','10']


convert = map(int,li)

print(tuple(convert))

def square(n):
    return n*n


t1 = (1,2,3,4,5)
square1 = map(square,t1)

print(list(square1))


square2 = map(lambda x:x*x,t1)
print(tuple(square2))









# 3. Filter Function
section("3. Filter Function")
# The filter() function returns an iterator where the items are filtered through a function to test if the item is accepted or not.
# Syntax: filter(function, iterable)

def age(a):
    if a >=18:
        return True
    else:
        return False

li1 = [12,34,5,23,21,20,56,15]

li2 = filter(age,li1)
print(list(li2))

check1 = filter(lambda x:True if x%2==0 else False,li1)
print(list(check1))


# 4. Enumerate Function
section("4. Enumerate Function")
# The enumerate() funct ion takes a collection (e.g. a tuple) and returns it as an enumerate object.
# The enumerate object yields pairs containing a count (from start, which defaults to 0) and a value yielded by the iterable argument.
# Syntax: enumerate(iterable, start=0)

fruits = ["banana", "apple", "cherry"]

# print(list(enumerate(fruits)))

for i in enumerate(fruits):
    print(i)


for i,j in enumerate(fruits,start= 1):
    print(i,j)



