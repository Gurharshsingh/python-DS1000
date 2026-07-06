# ==========================================
# Formatted Strings (f-strings) in Python
# ==========================================
# F-strings (introduced in Python 3.6) provide a concise and 
# readable way to embed expressions inside string literals.


print("--- 1. Basic Variable Insertion ---")
name = "Alice"
age = 25
# Put an 'f' before the opening quote, and use { } for variables.
greeting = f"Hello, my name is {name} and I am {age} years old."
print(greeting)


print("\n--- 2. Math and Expressions inside f-strings ---")
# You can put actual Python code and math inside the curly braces!
num1 = 10
num2 = 5
print(f"If you add {num1} and {num2}, you get {num1 + num2}.")
print(f"Is {num1} greater than 15? {num1 > 15}")


print("\n--- 3. Calling Methods inside f-strings ---")
# You can call string methods or object methods directly inside.
word = "python is awesome"
print(f"Capitalized: {word.upper()}")


# print("\n--- 4. Formatting Numbers (Decimals) ---")
# # You can control how numbers are displayed using a colon ':'
price = 49.9
tax = 0.075

# Example: force 2 decimal places using ':.2f'
# The 'f' stands for float (decimal number).
total = price + (price * tax)
print(f"Raw total: {total}")
print(f"Formatted total (2 decimals): ${total:.2f}")

# Example: Formatting large numbers with commas
large_number = 1000000000
print(f"Large number with commas: {large_number:,}")


print("\n--- 5. Multi-line f-strings ---")
# You can use triple quotes for multi-line f-strings
character = "Knight"
health = 100
inventory = ["Sword", "Shield", "Potion"]

character_sheet = f"""
=======================
CHARACTER SHEET
=======================
Class:    {character}
HP:       {health}/100
Items:    {len(inventory)} items in bag
Weapon:   {inventory[0]}
=======================
"""
print(character_sheet)
