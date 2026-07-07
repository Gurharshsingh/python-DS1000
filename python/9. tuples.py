# Tuples and dictionary

# Tuples
#1. Tuples are the immutable data type
#2. Stores the values in ordered format
#3. Can contain different datatypes
#4 tuples are declared in () parenthesis
#5. tuples are faster than lists

a=1,2,3,4,5
print(a)
print(type(a))

b=()
print(type(b))
b=('Palwinder')
print(type(b))
print(b) 


c=(12,) # whenever we declare the tuple with the single element we have to put comma after the element

# print(type(b))

print(type(c))

# e= tuple()
# e=()
# print(type(e))

d=tuple([1,2,3,4,5,'Sumit','Gaurav',3.14,'a'])
print(d)

# # traversing the tuples
for i in d:
    print(i)

# # slicing in the tuples
print(d[::-1])
print(d[:4])
print(d[1:7])
print(d[8:2:-2])

# d.add(12)
# d.pop()


f = (1,2,3,4,5,6,7,9)

f = list(f)
f.pop()
f.append(8)
f = tuple(f)
print(f)




