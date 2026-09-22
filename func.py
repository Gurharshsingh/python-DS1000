print("=======Functions======")


# functions - pre-defined, input, print, int
# user defined - def keyword
# 
# 


# def greet(name):
#     print("hello!",name)


# user = input("Enter name: ")


# greet(user)
# greet("yash")



def sum():    #non - parametric function
    a = 20
    b = 30
    print(a+b)
    return a+b

print(sum())

def sum(a,b):   #parametric function
    return a+b

print(sum(90,50))
print(sum(100,300))



#positional arguments
def multi(a,b,c):
    print(a)
    print(b)
    print(c)
    return a*b*c

print(multi(10,200,300))
result = multi(10,200,300)
print(result)

#default parameter
#keyword arguments

def summ(a,b,c=0,d=0):
    print(a)
    print(b)
    print(c)
    print(d)
    return a+b+c+d

# print(summ(a=30,b=11,d=50,c=90))
print(summ(4,4,0,0))
print(summ(4,5,5))


def clist(n):
    d = []
    for i in range(n):
        d.append(i)
    return d

user = int(input("Enter a number: "))

print(clist(user))
f = clist(user)
print(f)

def sumlist(l):
    sum=0
    for i in l:
        sum+=i
    return sum

print("SUM OF LIST ELEMENTS IS: ", sumlist(f))

#args - arbitrary arguments (*a) - tuple 
#kwargs - keyword arbitrary arguments (**a) - dictionary


def summret(*a):
    sum = 0
    for i in a:
        sum+=i
    return sum

print(summret(1,2,3))
print(summret(2,4,5,6,3,2))


def sumret(**a):
    print(a.keys())
    print(a.values())
    sum=0
    for i in a.values():
        sum +=i
    return sum

print(sumret(a=10,b=40,c=35))
print(sumret(m1=40,m2=76,m3=90,m4=100,m5=32))        



