# -*- coding: utf-8 -*-
'''
We can Solve this problem by using a property: ** That a median on the hypotenuse divides the right angled triangle in two isoceles triangle.** * Means AM=BM=CM * So, ∡MBC = ∡MCB
'''
import math

AB = int(input())
BC = int(input())
#AC = math.sqrt(AB**2 + BC**2)
#MC = AC/2
symbol = '°'
#d = symbol.encode('utf8')
#print(symbol)
print(str(round(math.degrees(math.atan(AB/BC)))) + symbol)
