# filehandling 



# modes - 
# r - read - read content of the files
# w - write - writes content onto files and overwrites content if already present, file creation
# a - append - adds content to the already avaliable content



# with open('students_name.txt','w') as file:
#     file.write("jasika \n")
#     file.write("sharma \n")
#     file.write("pooja \n")

# print("writing is done")


# with open('students_name.txt', 'r') as file:
#     content = file.read()
#     print(content)

# with open('students_name.txt','w') as file:
#     file.write("palwinder \n")
#     file.write("harjot \n")
#     file.write("rohit \n")


# with open('students_name.txt','a') as file:
#     file.write("sourav \n")
#     file.write("sumit \n")
#     file.write("anshul \n")



#exception handling 

try:
    with open('students_name.txt', 'r') as file:
        content = file.read()
        print(content)


except FileNotFoundError:
    print("file is not there")



print("HELLO")


try:
    a = int(input("enter a number: "))
    b = int(input("enter a number: "))
    print(a/b)


except ZeroDivisionError:
    print("You cannot divide by zero")

except ValueError:
    print("Invalid value entered")

else:
    print(a/b)

finally:
    print("Processing has ended")




try:
    with open('students.txt', 'r') as file:
        content = file.read()
        print(content)


except Exception as e:
    print(e)



    








