import matplotlib.pyplot as plt

# Last run data:
# 131006862 bytes in 7328.125 milliseconds
# 262070652 bytes in 15015.625 milliseconds
# 524172402 bytes in 31343.750 milliseconds
# 1048487622 bytes in 58031.250 milliseconds
# 2096979546 bytes in 94656.250 milliseconds


# 5 runs over TCP:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626
# 0.49075648328076077 0.49436815626045755 0.49236830136596954
# 308
# 0.49075648 0.49436816 0.49236830
# 1043812 bytes in 12515.625 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 0.4959835325160642 0.5045334064145317 0.519933801208408
# 436
# 0.49598353 0.50453341 0.51993380
# 2091492 bytes in 34687.500 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.4938110590769587 0.5035714452072664 0.49039221506690106
# 617
# 0.49381106 0.50357145 0.49039222
# 4188196 bytes in 90609.375 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.5061152238911437 0.5031572842371628 0.4980874788214309
# 873
# 0.50611522 0.50315728 0.49808748
# 8384292 bytes in 207046.875 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.4968834963651065 0.5128023894142901 0.49360725071361317
# 1234
# 0.49688350 0.51280239 0.49360725
# 16751550 bytes in 404500.000 milliseconds


# 1043812 bytes in 12515.625 milliseconds
# 2091492 bytes in 34687.500 milliseconds
# 4188196 bytes in 90609.375 milliseconds
# 8384292 bytes in 207046.875 milliseconds
# 16751550 bytes in 404500.000 milliseconds

sizesInBytes = [
    1, 2, 4, 8, 16
]

timeInMilliseconds = [
    12515,
    34687,
    90609,
    207046,
    404500
]

assert len(sizesInBytes) == len(timeInMilliseconds)

plt.xlabel('size in megabytes')
plt.ylabel('time in milliseconds')

ax = plt.plot(sizesInBytes, timeInMilliseconds, 'ro')
plt.plot(sizesInBytes, timeInMilliseconds)

plt.show()