import sys
sys.setrecursionlimit(1000000)  # long type,32bit OS 4B,64bit OS 8B(1bit for sign)


def findGCD(numberA, numberB):
    if numberA == 0:
        return numberB
    if numberB == 0:
        return numberA

    numberARemainder = numberA % numberB
    return findGCD(numberB, numberARemainder)


# return (g, x, y) a*x + b*y = gcd(x, y)
def findExtendedGCD(numberA, numberB):
    if numberA == 0:
        return numberB, 0, 1
    else:
        g, x, y = findExtendedGCD(numberB % numberA, numberA)

        return g, y - (numberB // numberA) * x, x


def isCoPrime(numberA, numberB):
    return findGCD(numberA, numberB) == 1


def findCoPrimeToTotient(totient, startValue):

    for i in range(startValue+1, totient):
        if isCoPrime(totient, i):
            return i


def findDFromTotientAndE(totient, e):
    g, x, y = findExtendedGCD(totient, e)

    # the d value can't be a negative number or 0, this is solved by incrmenting by totient
    while y <= 0:
        y += totient
    return y

