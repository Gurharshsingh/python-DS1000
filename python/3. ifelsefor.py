print("=============if elif else ==============")

# age = int(input("Enter Your age:"))

# if age>=18:
#     print("You can vote")
# else:
#     print("you cannot vote")


marks = int(input("Enter Your marks:"))

if marks >90 and marks<=100 :
    print("Grade A")

elif marks>80 and marks <=90:
    print("Grade B")

elif marks>=70 and marks <=80:
    print("Grade C")

elif marks<=69 and marks>=0:
    print("fail")

else:
    print("invalid value")






# #odd even

# num = int(input("Enter a number:"))

# if num%2 ==0:
#     print("even")

# else:
#     print("odd")

# print("==============for loop=============")


for i in range(10):
    print(i)


for i in range(10):
    print("Hello")

for i in range(1,20):
    print(i)

for j in range(2,50):
    print(j)

for k in range(2,50,3):
    print(k)

for l in range(50,2,-1):
    print(l)

subjects = int(input("Enter number of subjects:"))


for i in range(subjects):
    marks = int(input("Enter Your marks:"))


    if marks>=90 and marks<=100:
        print("grade A")

    elif marks>=80 and marks<=89:
        print("grade B")

    elif marks>=70 and marks<=79:
        print("grade C")

    elif marks<=69 and marks>=0:
        print("Fail")

    else:
        print("invalid input")



