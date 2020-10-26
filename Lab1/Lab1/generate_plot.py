import matplotlib.pyplot as plt

# 1 thread results:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626
# 308
# 0.4613626 0.52603047 0.46309684
# 308
# 0.46136260 0.52603054 0.46309674
# 1043812 bytes in 1.668500000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 436
# 0.5056086 0.50566764 0.51554511
# 436
# 0.50560844 0.50566781 0.51554531
# 2091492 bytes in 2.915200000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.52983585 0.49824401 0.50085811
# 617
# 0.52983588 0.49824405 0.50085819
# 4188196 bytes in 5.765700000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.49465644 0.47979742 0.49815887
# 873
# 0.49465638 0.47979701 0.49815899
# 8384292 bytes in 13.783100001 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.5113332 0.50899978 0.50178553
# 1234
# 0.51133347 0.50899976 0.50178528
# 16751550 bytes in 22.432100000 milliseconds

# 2 threads results:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626
# 308
# 0.47594819 0.52039959 0.5158941
# 308
# 0.47594810 0.52039951 0.51589411
# 1043812 bytes in 0.972800000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 436
# 0.50585847 0.51674108 0.48966757
# 436
# 0.50585866 0.51674098 0.48966789
# 2091492 bytes in 2.911700000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.50412305 0.51392987 0.50484703
# 617
# 0.50412309 0.51392978 0.50484705
# 4188196 bytes in 5.071800000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.50001795 0.49961894 0.48665471
# 873
# 0.50001788 0.49961916 0.48665482
# 8384292 bytes in 14.927800000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.51029687 0.49435182 0.49386062
# 1234
# 0.51029700 0.49435151 0.49386057
# 16751550 bytes in 18.192900000 milliseconds

# 4 threads results:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626 
# 308
# 0.53922382 0.50925454 0.49865183
# 308
# 0.53922379 0.50925469 0.49865180
# 1043812 bytes in 0.823400000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 436
# 0.49615192 0.52400826 0.4994548
# 436
# 0.49615213 0.52400815 0.49945468
# 2091492 bytes in 2.445100000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.49601666 0.49591181 0.48039506
# 617
# 0.49601668 0.49591187 0.48039526
# 4188196 bytes in 4.128100000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.50674862 0.50571937 0.49971588
# 873
# 0.50674838 0.50571954 0.49971589
# 8384292 bytes in 8.642700000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.49573987 0.4961339 0.4941281
# 1197
# 0.49573916 0.49613386 0.49412847
# 16241710 bytes in 17.244100000 milliseconds


def getAverageDifference(arr0, arr1):
    assert len(arr0) == len(arr1)
    return sum([(float(t[0] - t[1]) / t[0]) * 100 for t in zip(arr0, arr1)]) / len(arr0)


oneThreadTime = [
    1.668500000,
    2.915200000,
    5.765700000,
    13.783100001,
    22.432100000
]

twoThreadsTime = [
    0.972800000,
    2.911700000,
    5.071800000,
    14.927800000,
    18.192900000
]

fourThreadsTime = [
    0.823400000,
    2.445100000,
    4.128100000,
    8.642700000,
    17.244100000
]

sizesInBytes = [2**i for i in range(5)]

avg_one_two = getAverageDifference(oneThreadTime, twoThreadsTime)
print(avg_one_two)
avg_one_four = getAverageDifference(oneThreadTime, fourThreadsTime)
print(avg_one_four)
avg_two_four = getAverageDifference(twoThreadsTime, fourThreadsTime)
print(avg_two_four)

plt.xlabel('size in megabytes')
plt.ylabel('time in milliseconds')

plt.plot(sizesInBytes, oneThreadTime, 'bo')
plt.plot(sizesInBytes, twoThreadsTime, 'yo')
plt.plot(sizesInBytes, fourThreadsTime, 'ro')
plt.plot(sizesInBytes, fourThreadsTime, 'r')
plt.plot(sizesInBytes, twoThreadsTime, 'y')
plt.plot(sizesInBytes, oneThreadTime, 'b')

plt.show()