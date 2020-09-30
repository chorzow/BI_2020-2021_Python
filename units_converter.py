# degrees (deg) to radians (rad) and vice-versa
from math import pi
value = round(float(input('Enter value to convert:')), ndigits=3)
units = input('Enter units to convert:')
if units == 'deg':
    print(f"{value} deg = {round(value * pi / 180, ndigits=3)} rad")
elif units == 'rad':
    print(f"{value} rad = {round(value * 180 / pi, ndigits=3)} deg")
