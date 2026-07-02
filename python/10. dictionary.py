# Dictionary
#1. Dictionary are the mutable data type
#2. Stores the values in KEY:VALUE pairs
#3. Can contain different datatypes
#4 Dictionaries are declared in {} parenthesis


# d={}
# print(type(d))

# e=dict()
# print(type(e))

a={'Name':'Palwinder','Age':25,'City':'Ludhiana','Height':5.11}
print(a)
print(a['Name'])

print(a.keys())
print(a.values())
print(a.items())

# print(a['Roll no.'])

print(a.get('Age', "Not avaliable"))



# # traversing the dictionaries
# for i,j in a.items():
#     # print(i,"-- ",j)
#     print(f"{i} -- {j}")

# print(len(a))

# creating the dictionary from the user input
# e={}
# n=int(input("Enter the lenght of the dictionary :"))
# for i in range(n):
#     key=input("Enter the key :")
#     value=input("Enter the value :")
#     e[key]=value

# print(e)

# Updating the elements in the dictionary
a={'Name':'Palwinder','Age':25,'City':'Ludhiana','Height':5.11}
print(a)
a['Name']='Aman'
print("After updation: ")
print(a)
a.update({'Name':'Sumit','Age':26})
print("After updation: ")
print(a)

# Adding elements in the dictionary
a.update({'Name':'Sumit','Scholar':'Yes'})
print(a)
a['College']='MRSPTU'
print(a)


# Deleting elements from the dictionary
a.pop('Scholar')
print(a)
a.popitem()
print(a)
del a['City'],a['Name']
print(a)

d={'Name':['Palwinder','Harjot','Sumit','Nitya'],'Age':[25,26,27,28]}
print(d)

print(d['Name'][0])
for i in range(len(d['Name'])):
    print(f"{d['Name'][i]} -- {d['Age'][i]}")


# 2d dict

dict1 = {'name': {'firstName': "Japtesh",
                    "lastName": "Singh"} ,
         'age': 21,
         'Address':{"temp": 'mohali',
                    "perm": 'Bathinda'}}

print(dict1['name'])
print(dict1['name']['firstName'])