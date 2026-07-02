print("==========Strings==========") #indexed

s = "Karanveer Singh"

print(len(s))

print(s)

#slicing

print(s[0])
print(s[0:9])
print(s[3:13])
print(s[2:12:3]) # start stop step
print(s[::-1])
print(s[12:3:-2])

#methods

print(s.lower())
print(s.upper())
print(s.title())
print(s.capitalize())
print(s.swapcase())
print(s.startswith("Karan"))
print(s.endswith("igh"))


# striping

s1 = "     hello          hi      "

print(s1)
print(s1.strip())
print(s1.rstrip())
print(s1.lstrip())

# replace

s2 = "I am playing cricket"


print(s2)

s2 = s2.replace("playing","coding")
print(s2)

s2 = s2.replace("I am", "Balwinder")
print(s2)


#splitting

new = "Hello How are you"

print(new.split(" "))

print(new.split("o"))


neww = "bdbisdbibdsij3jksd#vjhsdvhdch#bjbdjbjasbibcai#"

print(neww.split("#"))

s = neww.split("#")
print(s)






