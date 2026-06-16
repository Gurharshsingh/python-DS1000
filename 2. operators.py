print("==============Operators=============")

#arithmetic - +, -, *, /, **,//,%
#logical- and, or, not
#assignment - =, +=, -=, *=, /=, %=, **=, //=
#comparison - ==, !=, <, >, <=, >=

#membership - in, not in
#identity - is, is not

#arithmetic 
print("==============Arithmetic Operators==============")
a = 10
b = 5
x  = a+b

print(x)
print("sum =", a+b)
print("diff =", a-b)
print("mul =", a*b)
print("div =", a/b)
print("pow =", a**b)
print("floor =", a//b)
print("mod =", a%b)

# comparison operators
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


# logical operators
print("============Logical Operators============")

z = (d==e)and(d!=e)
print(z)

y = (d!=e)and(d<=f)
print(y)

x = (d==e)or(d!=e)
print(x)

w = not(d==e)
print(w)


# membership operators
print("============Membership Operators============")

s1 = "I am playing cricket"

print("gurharsh" in s1)
print("cricket" in s1)
print("football" not in s1)

# identity operators
print("==============Identity Operators==============")

p = 20
q = 20

print(id(p))
print(id(q))

print(p is q)

print(p is not q)

r = int(input("Enter a number: "))
print (r)
print(id(r))

print(r is p)




