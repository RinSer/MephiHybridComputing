import matplotlib.pyplot as plt

'''
Last run data:
5890533 bytes in 218.750 milliseconds
23557471 bytes in 890.625 milliseconds
94226163 bytes in 3171.875 milliseconds
376898208 bytes in 14609.375 milliseconds
1507579894 bytes in 60171.875 milliseconds
'''

sizesInBytes = [
    5890533,
    23557471,
    94226163,
    376898208,
    1507579894,
]

timeInMilliseconds = [
    218.750,
    890.625,
    3171.875,
    14609.375,
    60171.875
]

assert len(sizesInBytes) == len(timeInMilliseconds)

plt.plot(sizesInBytes, timeInMilliseconds, 'ro')
plt.plot(sizesInBytes, timeInMilliseconds)

plt.show()