import matplotlib.pyplot as plt

timeInMilliseconds = [
    15328,
    44406,
    106218,
    228812,
    383203
]

paralleledTimeInMilliseconds = [
    10359,
    27281,
    72812,
    155187,
    324125
]

avg = sum([(float(t[0] - t[1]) / t[0]) * 100 for t in zip(timeInMilliseconds, paralleledTimeInMilliseconds)]) / len(timeInMilliseconds)
print(avg)

sizesInBytes = [2**i for i in range(len(timeInMilliseconds))]

assert len(sizesInBytes) == len(timeInMilliseconds)
assert len(sizesInBytes) == len(paralleledTimeInMilliseconds)

plt.xlabel('size in megabytes')
plt.ylabel('time in milliseconds')

ax = plt.plot(sizesInBytes, timeInMilliseconds, 'ro')
plt.plot(sizesInBytes, paralleledTimeInMilliseconds, 'yo')
plt.plot(sizesInBytes, paralleledTimeInMilliseconds, 'g')
plt.plot(sizesInBytes, timeInMilliseconds)

plt.show()