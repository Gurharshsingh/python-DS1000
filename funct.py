# pre defined functions - strip, split, print, input 

# user defined functions - def keyword

# syntax

# def functions_name():
#     return 


# # call

# functions_name()

#non - parametric
def greet():
    print("Hello")
    return "Hello Everyone"

d = greet()
print(d)



#parametric, positional arguments
def sum(a,b):
    c = a + b
    return c

result  = sum(10,30)
print(result)


#keyword arguments
def sum(a,b,c,d):
    e = a+b+c+d
    return e

result = sum(a = 30, d = 90, c = 20, b = 80)
print(result)


# default parameter
def summm(a,b,c= 0):
    d = a+b+c
    return d

result = summm(10,20,40)
print(result)


# def multi():
#     a = int(input("enter a value"))
#     b = int(input("enter a value"))
#     c = int(input("enter a value"))
#     d = a*b*c
#     return d




# result = multi()
# print(result)



def clist(m):
    d = []
    for i in m:
        d.append(i)
    return(d)

f = clist([1,2,3,4])
print(f)



def sumlist(d):
    sum = 0
    for i in d:
        sum = sum+i
    return sum

s = sumlist(f)
print(s)



# arbitrary arguments

# *a

def sumret(*a):
    sum = 0
    for i in a:
        sum +=i
    return sum

print(sumret(1,2,3))
print(sumret(9,90,7,3,4,5))

#keyword arbitrary arguments

# a = 10
# **a

def sumrettt(**a):
    sum = 0

    for i in a.keys():
        print(i)

    for i in a:
        sum +=a[i]
    return sum



print(sumrettt(a =1, b =20))
print(sumrettt(a=90, b =70, c = 45 ))












