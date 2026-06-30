#built in functions
# enumerate(), zip(), map(), filter(),print(),len()

# user defined functions
# that are defined byt he user for its specific purpose

# USER DEFINED FUNCTIONS
# def function_name(parameters):
    #statemen--1
    #steament -- n
    
    # return value
    
def greet():
    # print("Good Morning!!")
    return "Good morning!!"


a=greet()
print(a)

def table(n):
    l=[]
    for i in range(1,11):
        l.append(n*i)
    return l
    
    
l=table(13)
print(l)

# function to check whether a number is prime or not
def check_prime(n):
    count=0
    for i in range(2,n):
         if(n%i==0):
             count=1
             break
    if count==0:
        return "The number is prime"
    else:
        return "The number is not prime"
    
a=check_prime(47)
print(a)

a=[1,1,1,2,2,4,5,6,8,8,6]
# create a function that return the list in sorted order
# and return the list without duplicate values
def remove_duplicate(a):
    a.sort()
    i=0,j=0
    while(i<len(a)):
        if(a[i]==a[i-1]):
            del a[i-1]
        
        i+=1
    return a

l=remove_duplicate(a)
print(l)