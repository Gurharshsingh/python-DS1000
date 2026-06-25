# marks = int(input("Enter Your marks:"))


# if marks>=90 and marks<=100:

#     if marks>=95 and marks <=100:
#         print("Grade A+")
#     else:
#         print("Grade A")
# elif marks>=80 and marks<=89:
#     if marks>=85 and marks <=89:
#         print("Grade B+")
#     else:
#         print("grade B")
# elif marks>=70 and marks<=79:
#     if marks>=75 and marks <=79:
#         print("Grade C+")
#     else:
#         print("grade C")

# elif marks<=69 and marks>=0:
#     print("Fail")

# else:
#     print("invalid input")


# subjects = int(input("Enter number of subjects:"))
# for i in range(subjects):
#     marks = int(input("Enter Your marks:"))


#     if marks>=90 and marks<=100:
#         if marks>=95 and marks <=100:
#             print("Grade A+")
#         else:
#             print("Grade A")
#     elif marks>=80 and marks<=89:
#         if marks>=85 and marks <=89:
#             print("Grade B+")
#         else:
#             print("grade B")
#     elif marks>=70 and marks<=79:
#         if marks>=75 and marks <=79:
#             print("Grade C+")
#         else:
#             print("grade C")

#     elif marks<=69 and marks>=0:
#         print("Fail")

#     else:
#         print("invalid input")

print("==========nested Loops=============")

for i in range(1,11):
    for j in range(i):
        print("*", end = " ")
    print()

for i in range(10):
    for j in range(10,i,-1):
        print("*", end = " ")
    print()  