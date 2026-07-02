''' 
1. Sets are the mutable data type
2. It stores the values in unordered format
3. It does not store the duplicate values
4. Sets are stored in {} braces
5. It can store heterogenous type of data
'''

# a={} # it will by default make the variable a as dictionary
# print(type(a))

# s=set()
# print(type(s))

d={1,2,3,4,5}
print(d)
e={1,'Hello',25,26,26.8,'Hello'}
print(e)
# print("--------------------------------")

# Adding elements in the set

s={'Hello',1,2,3,56.8}
print(s)
s.add(22)
# print("After ADd")
# print(s)
s.update([1,3,4,5])
print("After update")
print(s)

# traversing in the sets
# for i in s:
#     print(i,end=" ")

# Removing elements from the set
# 1. pop() 2. remove() 3.discard()

# print()
# print("-"*50)
s.pop()
# print("After using the pop function")
# print(s)

# s.remove(22)
# print("Afte using remove")
# print(s)

# # s.remove(6) # it will create an error when the input element is not present in the set
# s.discard(5)
# s.discard(6) # it will not create when the input element is not present
# print("After using discard")
# print(s)

# #frozen sets
# a=frozenset([1,2,3,4,5]) # it will make the sets immutable
# print(a)
# a.add(8)

# # set operations
a={1,2,3,4,5}
b={4,5,6,7,8}

# union , intersection , difference , symmetric differenc , subsets
print(a | b)
print(a.union(b))  # union  
print(a & b)
print(a.intersection(b))  # intersection
print(a - b)
print(a.difference(b))  # difference
print(a ^ b)
print(a.symmetric_difference(b))  # symmetric difference

# d={4,5,6}
# print(d.issubset(b))
# print(d.issuperset(b))
# print(d.isdisjoint(b))
