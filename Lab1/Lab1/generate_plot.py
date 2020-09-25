import matplotlib.pyplot as plt

'''
Last run data:
131006862 bytes in 7328.125 milliseconds
262070652 bytes in 15015.625 milliseconds
524172402 bytes in 31343.750 milliseconds
1048487622 bytes in 58031.250 milliseconds
2096979546 bytes in 94656.250 milliseconds
'''

sizesInBytes = [
    131006862,
    262070652,
    524172402,
    1048487622,
    2096979546
]

timeInMilliseconds = [
    7328.125,
    15015.625,
    31343.750,
    58031.250,
    94656.250
]

assert len(sizesInBytes) == len(timeInMilliseconds)

plt.plot(sizesInBytes, timeInMilliseconds, 'ro')
plt.plot(sizesInBytes, timeInMilliseconds)

plt.show()