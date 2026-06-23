print("==============Operators=============")

#arithmetic - 
# + - sum, 
# - - subtract,
# * - multiplication, 
# / - divide - gives division answer, 
# ** - exponentiation - gives power - a**b means a raised to power b,
# // - floor division - quotient,
# % - modulas - gives remainder

#logical- 
# and - check all conditions are true, returns boolean values
#  or - returns true even if one condition is true, 
# not - gives opposite answer,returns boolean



#assignment - 
# = - assigns value to a variable, 
# +=, -=, *=, /=, %=, **=, //=


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

x  = a+b

print(x)
print("sum =", a+b)
print("diff =", a-b)
print("mul =", a*b)
print("div =", a/b)
print("pow =", a**b)
print("floor =", a//b)
print("mod =", a%b)

# # comparison operators
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


# # logical operators
print("============Logical Operators============")

z = (d==e)or(d<=f)and(d!=e)
print(z)

y = (d!=e)and(d<=f)
print(y)

x = (d==e)or(d!=e)
print(x)

w = not(d==e)
print(w)


# # membership operators
print("============Membership Operators============")

s1 = "I am playing cricket"

print("gurharsh" in s1)
print("cricket" in s1)
print("football" not in s1)

# # identity operators
# print("==============Identity Operators==============")

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




