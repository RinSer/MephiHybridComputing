import matplotlib.pyplot as plt

'''
Last run data:
131006862 bytes in 5421.875 milliseconds
262070652 bytes in 11296.875 milliseconds
524172402 bytes in 24875.000 milliseconds
1048487622 bytes in 47640.625 milliseconds
2096979546 bytes in 96203.125 milliseconds
'''

sizesInBytes = [
    131006862,
    262070652,
    524172402,
    1048487622,
    2096979546
]

timeInMilliseconds = [
    5421.875,
    11296.875,
    24875.000,
    47640.625,
    96203.125
]

assert len(sizesInBytes) == len(timeInMilliseconds)

plt.plot(sizesInBytes, timeInMilliseconds, 'ro')
plt.plot(sizesInBytes, timeInMilliseconds)

plt.show()