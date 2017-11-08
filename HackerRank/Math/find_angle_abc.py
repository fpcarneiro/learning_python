# -*- coding: utf-8 -*-
import math

AB = int(input())
BC = int(input())
AC = math.sqrt(AB**2 + BC**2)
MC = AC/2
symbol = '°'
d = symbol.encode('utf8')
print(symbol)
#print(str(d, encoding='utf8'))
#print(str(round(math.degrees(math.asin(MC/BC)))) + u'\u00b0')