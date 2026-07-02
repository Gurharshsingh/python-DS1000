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
if len(sys.argv) > 1:
    print(f"  Script name: {sys.argv[0]}")
    print("  Additional arguments:")
    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"    Arg {i}: {arg}")
else:
    print(f"  Script name: {sys.argv[0]}")
    print('  No additional arguments were passed. Try running: python "15. modules.py" arg1 arg2')

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
