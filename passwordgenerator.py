import random
# generate random alphabet
# generate random number
# generate random special sign 
# check lowecase
# check uppercase
# generate random password
passlen = int(input("enter length password "))
s = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#%^&*()"
p = "".join(random.sample(s, passlen))
print(p)
