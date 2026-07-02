# # a=[]
# # for i in range(1,41):
# #     if(i%2!=0):
# #         a.append(i)

# # print(a)

# # in list comprehension
# # basic syntax
# # list_name= [expression for item in iterable if condition]
# # a=[i for i in range(1,41) if i%2!=0]
# # print(a)

fruits=['Apple','Mango','Papaya','Orange','PineApple']
f=[i for i in fruits if len(i)>5]
print(f)

# # c= [1,2,3,4,5,13,15,19,22,24,26]
# # d=["Even" if i%2==0 else "Odd" for i in c]
# # print(d)

# # e=['palwinder','harjot','gurminder','rajat']
# # f=[i.upper() for i in e]
# # print(f)

# #1. Create a list of squares of the list of number [6,9,10,12,25]
# #2. given a list [1,2,3,4,5] return a list in which if the 
# # number is divisible by 2 then keep the same number else multiply the 
# # number with 10

# a=[6,9,10,12,25]
# s=[i*i for i in a]
# print(s)

# b=[1,2,3,4,5]
# d=[i if i%2==0 else i*10 for i in b]
# print(d)


# aa = []
# for i in range(10):
#     aa.append(i)

a = [i*i for i in range (10) if i%2==0]
print(a)


b = ['even' if i%2==0 else 'odd' for i in range (20)]
print(b)

