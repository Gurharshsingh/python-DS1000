# ==========================================
# 1. File Handling (Read/Write)
# ==========================================
# print("--- 1. File Handling ---")
# print('''
# Common File Handling Modes:
# 'r'  - Read (Default): Opens a file for reading, errors if the file doesn't exist.
# 'w'  - Write: Opens a file for writing, creates the file if it does not exist or truncates the file if it exists.
# 'a'  - Append: Opens a file for appending, creates the file if it does not exist.
# 'x'  - Create: Creates the specified file, returns an error if the file exists.
# 't'  - Text (Default): Text mode.
# 'b'  - Binary: Binary mode (e.g. images).
# '+'  - Read/Write: Opens a file for updating (reading and writing).
# ''')


# # Writing to a file using 'w' mode (this creates the file or overwrites it)
# # We use the 'with' statement so the file automatically closes after we're done.

# with open("demo.txt", "w") as file:
#     file.write("Sanam ")
#     file.write("Krish\n")
#     file.write("Pooja")

# print("writing is done")
    

# with open("students.txt", "w") as file:
#     file.write("Alice\n")
#     file.write("Bob\n")
#     file.write("Charlie\n")
# print("Successfully wrote to 'students.txt'.")

# # Reading from a file using 'r' mode
# print("\nReading contents of 'students.txt':")
# with open("demo.txt", "r") as file:
#     contents = file.read()
#     print(contents)

# # Appending to a file using 'a' mode (adds to the end without overwriting)
# with open("demo.txt", "a") as file:
#     file.write("\nBalwinder\n")
# print("Appended 'Balwinder' to the file.")

# with open("demo.txt", "w") as file:
#     file.write("Vansh\n ")
#     file.write("Sujal\n")
#     file.write("Anmol")


# # with open("students.txt", "r") as file:
# #     contents = file.read()
# #     print(contents)

# # Reading line by line (useful for large files)
# print("\nReading line by line:")
# with open("demo.txt", "r") as file:
#     for line in file:
#         print("Student: {}".format(line.strip())) # .strip() removes the newline character

# # Reading all lines into a list using readlines()
# print("\nReading all lines into a list:")
# with open("demo.txt", "r") as file:
#     lines_list = file.readlines()
#     print("List of lines:", lines_list)
#     print("Total students:", len(lines_list))

# # # Writing multiple lines at once using writelines()
# print("\nWriting multiple lines at once:")
# new_students = ["Avneet\n", "Karan\n", "Rohit\n"]
# with open("demo.txt", "w") as file:
#     file.writelines(new_students)
# print("Successfully wrote new students to 'demo.txt'.")

# # # Checking if a file exists before reading
# import os
# print("\nChecking if a file exists:")
# if os.path.exists("demo.txt"):
#     print("'demo.txt' exists! We can safely read it.")
# else:
#     print("'demo.txt' does not exist.")


# # ==========================================
# # 2. Exception Handling (try / except)
# # ==========================================
print("\n--- 2. Exception Handling ---")


# with open("missing_file.txt", "r") as file:
#         data = file.read()


try:
    with open("MISSING.txt", "r") as file:
        data = file.read()
except FileNotFoundError:
    print("Error: The file 'missing_file.txt' was not found.")

# # Handling multiple exceptions and using 'else' and 'finally'
print("\nDividing numbers:")
try:
    num1 = 10
    num2 = int(input("Enter a number to divide 10 by (try 0 to see the error): "))
    result = num1 / num2
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")
except ValueError:
    print("Error: Invalid value provided, please enter an integer.")
else:
    # This runs ONLY if no exception occurred
    print(f"The result is {result}")
finally:
    # This runs ALWAYS, no matter what happens (good for cleanup)
    print("Execution of the division try/except block is complete.")

# Catching IndexError (List out of bounds)
print("\nAccessing lists:")
my_list = [1, 2, 3]
try:
    print("Trying to access index 5...")
    value = my_list[5]
except IndexError:
    print("Error: Index out of range! The list doesn't have that many elements.")

# # Catching KeyError (Dictionary key missing)
print("\nAccessing dictionaries:")
my_dict = {"name": "Alice", "age": 25}
try:
    print("Trying to access 'city'...")
    city = my_dict["city"]
except KeyError:
    print("Error: Key not found in the dictionary!")

# # Catching a generic Exception (Catch-all)
print("\nGeneric Catch-all:")
try:
    # A generic error, for example a TypeError
    result = "10" + 5
except Exception as e:
    print(e)