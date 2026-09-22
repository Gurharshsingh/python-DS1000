print("=============Special Functions============")

# 1. lambda
# 2. map
# 3. filter
# 4. enumerate



print("=============Lambda================")
# single line function
# multiple arguments 
# single return expression
# lamda keyword
# lambda arguments:expressions condition (optional)

# def sum(a,b):
#     return a+b

# sum(90,89)

add = lambda a,b: a+b

print(add(34,22))


square = lambda x: x*x

print(square(4))

check = lambda a: "even" if a%2==0 else "odd"

print(check(56))
print(check(57))


# 2. map 
#syntax - map(function,iterable)

# predefined -function

s = ['1','2','3','4','5']

convert = map(int,s)
print(convert)
print(list(convert))


d=[1,2,3,4,5,6]
print(d)

def square(x):
    return x*x

square_map = map(square,d)
print(tuple(square_map))


square_lambda_map = map(lambda x:x*x,d)
print(list(square_lambda_map))


# 3. filter
#filter - true - store

def age(a):
    if a >= 18:
        return True
    else:
        return False

ages = [12,34,5,23,21,20,56,15]

age_filter = filter(age,ages)
print(age_filter)
print(list(age_filter))


# 4. enumerate

li = ["Apple", "Mango", "banana"]
print(li)
print(enumerate(li))

for i,j in enumerate(li,1):
    print(i,j)

