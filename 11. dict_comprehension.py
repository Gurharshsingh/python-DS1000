# dictionary comprehension
# expression
# {key:value for item in iterable}

# write a prograam to create a dictionary as number its keys and its 
# corresponding squares as its values upto 10 numbers only

d={}
for i in range (1,11):
    d[i]=i**2
    
print(d)

d1={i:i**2 for i in range(1,11)}
print(d1)

names=['Neha','Karan','Nitika']
# create the below dictionary having values of length of the elements in the list as values

# {'Neha':4,'Karan':5,'Nitika':6 }

d3={i:len(i) for i in names}
print(d3)

# create a dictionary from 1 to 10 as its keys and corresponding values
# should tell a number is odd or even
#{1:'Odd',2:"Even"}

d4={i:"Even" if i%2==0 else "Odd" for i in range(1,11)}

print(d4)

students={'Sumit':80,'Jatin':50,'Harman':40,'Harjot':90}

# output
#{'Sumit':'Pass','Jatin':'Fail'}

d5={i:"Pass" if students[i]>50 else "Fail" for i in students}
print(d5)

# Reverse the dictionary
# {1:'Odd',2:'Even'} ==> {'Even':2,'Odd':2}
o={1:'Odd',2:'Even'}
reverse={v:k for k,v in o.items() }
print(reverse)