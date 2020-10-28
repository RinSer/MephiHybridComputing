import matplotlib.pyplot as plt

# OpenMPI

# 1 process results:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626
# 308
# 0.49932025 0.53350736 0.51026257
# 308
# 0.49932012 0.53350735 0.51026261
# 1043812 bytes in 2.420700000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 436
# 0.48371659 0.48365327 0.49994479
# 436
# 0.48371673 0.48365334 0.49994493
# 2091492 bytes in 6.483600000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.5068965 0.49065445 0.52581792
# 617
# 0.50689662 0.49065480 0.52581829
# 4188196 bytes in 7.524300000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.48972273 0.51447572 0.50780224
# 873
# 0.48972282 0.51447600 0.50780195
# 8384292 bytes in 12.432200000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.4974581 0.4923044 0.50742865
# 1234
# 0.49745810 0.49230492 0.50742871
# 16751550 bytes in 20.826200000 milliseconds

# 2 process results:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626
# 308
# 0.49928691 0.50022443 0.51266739
# 308
# 0.49928698 0.50022447 0.51266742
# 1043812 bytes in 2.173600000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 436
# 0.46431738 0.50014432 0.48970599
# 436
# 0.46431765 0.50014412 0.48970595
# 2091492 bytes in 3.923900000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.48119057 0.51329812 0.49663975
# 617
# 0.48119056 0.51329815 0.49663973
# 4188196 bytes in 7.003000000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.50753197 0.51250936 0.50480287
# 873
# 0.50753218 0.51250935 0.50480282
# 8384292 bytes in 11.463800000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.49878625 0.50476273 0.50596261
# 1234
# 0.49878624 0.50476277 0.50596255
# 16751550 bytes in 21.367000000 milliseconds

# 4 process results:
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 1 2525 2626
# 308
# 0.49366741 0.51324561 0.48744222
# 308
# 0.49366713 0.51324594 0.48744196
# 1043812 bytes in 2.189400000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 2 2525 2626
# 436
# 0.53411727 0.4886409 0.49255599
# 436
# 0.53411734 0.48864099 0.49255577
# 2091492 bytes in 4.750200000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 4 2525 2626
# 617
# 0.50088253 0.49774722 0.49537628
# 617
# 0.50088274 0.49774736 0.49537644
# 4188196 bytes in 10.136900000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 8 2525 2626
# 873
# 0.50557693 0.50327888 0.50448522
# 873
# 0.50557679 0.50327927 0.50448513
# 8384292 bytes in 12.645800000 milliseconds
# PS C:\Users\v-seirin\Desktop\Hybrid\Lab1\Lab1> python generate_data.py 16 2525 2626
# 1234
# 0.50276455 0.49329277 0.49392388
# 1234
# 0.50276452 0.49329272 0.49392420
# 16751550 bytes in 24.098200000 milliseconds


def getAverageDifference(arr0, arr1):
    assert len(arr0) == len(arr1)
    return sum([(float(t[0] - t[1]) / t[0]) * 100 for t in zip(arr0, arr1)]) / len(arr0)


oneThreadTime = [
    2.420700000,
    6.483600000,
    7.524300000,
    12.432200000,
    20.826200000
]

twoThreadsTime = [
    2.173600000,
    3.923900000,
    7.003000000,
    11.463800000,
    21.367000000
]

fourThreadsTime = [
    2.189400000,
    4.750200000,
    10.136900000,
    12.645800000,
    24.098200000
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