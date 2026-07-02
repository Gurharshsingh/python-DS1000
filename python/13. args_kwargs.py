# *args

def summm(*a):
    sum = 0
    for i in a:
        sum+=i
    print(sum)


summm(1,2,3,4,5,6,7,8,9,10)
summm(10,20)
summm(10,20,30)


# **kwargs 

def sumRet(**a):
    print(a)
    sum=0
    for i in a.values():
        sum+=i
    return sum

print(sumRet(a=45,b=56,c=88))
print(sumRet(a=45,b=56,c=88,d=20))
print(sumRet(a=45,b=56,c=88,d=20,e=45))
print(sumRet(a=45,b=56))