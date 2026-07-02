print("==============Operators=============")

#arithmetic - 
# + - sum, a + b
# - - subtract, a - b
# * - multiplication, a*b
# / - divide - gives division answer, a/b
# ** - exponentiation - gives power - a**b means a raised to power b,
# // - floor division - quotient,
# % - modulas - gives remainder

#logical- 
# and - check all conditions are true, returns boolean values
# a | b | Result
# 0   0   0
# 0   1   0
# 1   0   0
# 1   1   1


# #  or - returns true even if one condition is true, 
# a | b | Result
# 0   0   0
# 0   1   1
# 1   0   1
# 1   1   1

# not - gives opposite answer,returns boolean



#assignment - 
# = - assigns value to a variable, 
# +=, -=, *=, /=, %=, **=, //=


# a = 10
# a+=20
# print(a)


#comparison - Returns Boolean value 
# == - checks if values are same,  
# != - not equal 
# < - less than
# >, - greater than 
# <= - less than equal 
# >= - greater than equal




#membership - in, not in


#identity - is, is not




#arithmetic 
print("==============Arithmetic Operators==============")
a = 100
b = 50

c = a+b
print(c)
print(a+b)

print(a-b)
print(a*b)
print(a/b)
print(a**b)
print(a//b)
print(a%b)


# # # comparison operators
print ("============Comparison Operators============")
d = 20
e = 25
f = 30
g = 20

print(d==e)
print(d!=e)
print(d<e)
print(d>e)
print(d<=g)
print(d<=f)


# # # logical operators
print("============Logical Operators============")

z = (d==e)or(d<=f)
print(z)

y = (d==e)and(d<=f)
print(y)

x = (d==e)or(d!=e)
print(x)

w = not(d==e)
print(w)


# # # membership operators - in,  not in
print("============Membership Operators============")

s1 = "I am playing cricket"



print("gurharsh" in s1)
print("cricket" in s1)
print("football" not in s1)

# # # identity operators
print("==============Identity Operators==============")

p = 20
q = 20

print(id(p))
print(id(q))

print(p is q)

print(p is not q)

r = input("Enter a number: ")
print (r)
print(id(r))

print(r is p)




