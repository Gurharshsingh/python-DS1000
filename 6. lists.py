print("=================Lists====================")

# lists (collection of items ) - mutable , ordered, indexed, heterogeneous



li = [10,20,30,40,"apple","banana",40.5, True]

print(li)

# slicing
print(li[4])
print(li[0:4])
print(li[4:6])
print(li[::-1])
print(li[-1])

li1 = [20,30,50,60,30,100,90]

#adding elements

li1.extend([99,100,78909])
print(li1)

li1.append([20,30,40])
li1.append(900)
print(li1)

print(li1[10][1])

li1.insert(5,650)
print(li1)


#removing elements

li1.pop()
print(li1)

li1.pop(5)
print(li1)


li1.remove(100)
print(li1)

li1.pop()
print(li1)


li1.sort()
print(li1)
li1.sort(reverse = True)
print(li1)


li1.reverse()
print(li1)

#count

print(li1.count(99))

l = []

for i in range(20):
    l.append(i)


print(l)


for i in l:
    print(l[i])


#zip function
a = [1,2,3,4]
b = ["a","b","c","d"]

for i in zip(a,b):
    print(i)

for i,j in zip(a,b):
    print(str(i)+".", j )


d = [1,2,3,4]
c = [5,6,7,8]



for i,j in zip(d,c):
    print(i+j)

#join












 




