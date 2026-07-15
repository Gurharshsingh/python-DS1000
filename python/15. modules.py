import sys
import os
import datetime
import math


def separate_section(title):
    print("\n" + "="*20 + " " + title + " " + "="*20)

# =====================================================================
# 1. THE SYS MODULE
# =====================================================================
separate_section("1. sys Module")
# The sys module provides access to some variables used or maintained by the
# interpreter and to functions that interact strongly with the interpreter.

# 1.1 sys.argv - Command Line Arguments
print("sys.argv (Arguments passed to script):", sys.argv)
# if len(sys.argv) > 1:
#     print(f"  Script name: {sys.argv[0]}")
#     print("  Additional arguments:")
#     for i, arg in enumerate(sys.argv[1:], start=1):
#         print(f"    Arg {i}: {arg}")
# else:
#     print(f"  Script name: {sys.argv[0]}")
#     print('  No additional arguments were passed. Try running: python "15. modules.py" arg1 arg2')

# # 1.2 sys.platform - Platform Identifier
print("sys.platform (Operating System):", sys.platform)

# # 1.3 sys.version - Python Version
print("sys.version (Python Version):", sys.version)


# # 1.4 sys.getsizeof() - Memory Footprint of Objects
num = 42
text = "Hello, World!"
lst = [1, 2, 3, 4, 5]
tup = (1, 2, 3, 4, 5)
print(f"\nMemory consumption (getsizeof):")
print(f"  Integer (42): {sys.getsizeof(num)} bytes")
print(f"  String ('Hello, World!'): {sys.getsizeof(text)} bytes")
print(f"  List [1, 2, 3, 4, 5]: {sys.getsizeof(lst)} bytes")
print(f"  Tuple (1, 2, 3, 4, 5): {sys.getsizeof(tup)} bytes")


# # # =====================================================================
# # # 2. THE OS MODULE
# # # =====================================================================
# separate_section("2. os Module")
# The os module provides a portable way of using operating system dependent functionality.


print("My directory name is: ", os.getcwd())

cwd = os.getcwd()
print(cwd)

dirs = os.listdir()
print(dirs)

for i in range(5):
    print(dirs[i])


path1 = os.path.join(cwd,"new_folder","new.txt")
print(path1)

#makedir, rmdir 
if os.path.exists(path1):
    print("File exists:",path1)
    os.rmdir(path1)
    print("removing path")
    
    
else:
    print("File does not exist:",path1)
    print("creating path.....")
    os.makedirs(path1)
    print("path created successfully")
    

print(os.name)


# # # =====================================================================
# # # 3. THE DATETIME MODULE
# # # =====================================================================
# # separate_section("3. datetime Module")
# # # The datetime module supplies classes for manipulating dates and times.

# # 3.1 Getting Current Date and Time
now = datetime.datetime.now()
print("Current Date & Time (datetime.now()):", now)

# # # 3.2 Date Objects (Year, Month, Day)
today = datetime.date.today()
print("Today's Date (date.today()):", today)
print(f"Year: {today.year}, Month: {today.month}, Day: {today.day}")
s = "26-07-02"

print(s.split("-"))


specific_datetime = datetime.datetime(2025, 12, 25, 18, 30, 0)
print("Specific Date/Time (Christmas 2025 6:30 PM):", specific_datetime)

# # # =====================================================================
# # # 4. THE MATH MODULE
# # # =====================================================================
# # separate_section("4. math Module")
# # # The math module provides access to mathematical functions defined by the C standard.

# # 4.1 Constants
print("Math Constants:")
print("  math.pi (Pi):", math.pi)
print("  math.e (Euler's number):", math.e)
print("  math.tau (Tau = 2 * Pi):", math.tau)

# # # 4.2 Numeric Representations (ceil, floor, trunc, fabs)
val = -5.67
print("\nRounding & Absolute Values:")
print(f"  Original value: {val}")
print(f"  math.ceil({val}) (Smallest integer >= val):", math.ceil(val))
print(f"  math.floor({val}) (Largest integer <= val):", math.floor(val))
print(f"  math.trunc({val}) (Truncates decimal part):", math.trunc(val))

# # # 4.3 Operations (factorial, gcd, isclose)
# print("\nMathematical Operations:")
print("  math.factorial(5) (5! = 5*4*3*2*1):", math.factorial(5))
print("  math.gcd(24, 36) (Greatest Common Divisor):", math.gcd(24, 36))


# # # 4.4 Power & Logarithmic Functions
print("\nPower & Logarithmic Functions:")
print("  math.sqrt(64) (Square root):", math.sqrt(64))
print("  math.pow(2, 5) (2 raised to power of 5):", math.pow(2, 5))

# # # 4.5 Trigonometry & Angle Conversion
# print("\nTrigonometry:")
angle_deg = 45
angle_rad = math.radians(angle_deg)
print(f"  Converting {angle_deg}° to radians: {angle_rad:.4f} radians")
print(f"  math.sin(math.radians(45)) (Sine of 45°):", math.sin(angle_rad))
print(f"  math.cos(math.radians(45)) (Cosine of 45°):", math.cos(angle_rad))
print(f"  Converting {angle_rad:.4f} radians back to degrees: {math.degrees(angle_rad)}°")
