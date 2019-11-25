import sys
import pickle

f = open(r'[file]', 'rb')
mydict = pickle.load(f)
f.close

for i in mydict:
    b=[]
    for x in i:
        b.append(x[0] * x[1])

    print("".join(b))
