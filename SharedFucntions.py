from math import *

def nearestFibo(val):
    n=round(val)
    fibo=0
    if sqrt(5*n**2+4)%1==0 or sqrt(5*n**2-4)%1==0:
        # print("Your number is a Fibonacci number!")
        fibo=n
    else:
        # print("Your number is not a Fibonacci number.")
        c = 0
        while 1:
            c += 1
            if sqrt(5*(n+c)**2+4)%1==0 or sqrt(5*(n+c)**2-4)%1==0:
                # print("%s is the closest Fibonacci number to your entry." % str(n+c))
                fibo=n+c
                break
            if sqrt(5*(n-c)**2+4)%1==0 or sqrt(5*(n-c)**2-4)%1==0:
                # print("%s is the closest Fibonacci number to your entry." % str(n-c))
                fibo=n-c
                break
    return fibo