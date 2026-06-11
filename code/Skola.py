import math

polomer = input("Zadej polomer kruhu: ")

def vypocet_kruhu(polomer):
    pi = math.pi
    obsah = pi * (float(polomer) ** 2)
    obvod = 2 * pi * float(polomer)
    print("Obsah kruhu je: " + str(obsah)) 
    print("Obvod kruhu je: " + str(obvod))
