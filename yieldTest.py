# -*- coding: utf-8 -*-

def genrator():
    mylist = range(4)
    for i in mylist:
        yield  i * i



if __name__ == '__main__':
    mygenerator = genrator()
    print(mygenerator)
    for i in mygenerator:
        print(i)
    pass