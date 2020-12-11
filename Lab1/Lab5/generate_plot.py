import matplotlib.pyplot as plt

# One OpenMPI process

# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 1
# 308
# 0.46166129 0.50106315 0.49147693
# 308
# 0.46166134 0.50106323 0.49147686
# 1043504 bytes in 1289.124800000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 5
# 690
# 0.48604823 0.51869241 0.50259717
# 690
# 0.48604834 0.51869243 0.50259757
# 5237100 bytes in 57.601900000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 10
# 976
# 0.49813632 0.51469754 0.51626886
# 976
# 0.49813640 0.51469767 0.51626867
# 10478336 bytes in 40.721600000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 100
# 3087
# 0.50280586 0.51193567 0.50895846
# 3087
# 0.50280482 0.51193506 0.50895834
# 104825259 bytes in 804.684900000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 1000
# 9763
# 0.49650353 0.50200694 0.49524842
# 9763
# 0.49650362 0.50200504 0.49524739
# 1048477859 bytes in 2366.760300000 milliseconds

# Two OpenMPI processes

# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 1
# 308
# 0.4985006 0.51396652 0.50058429
# 308
# 0.49850070 0.51396668 0.50058436
# 1043504 bytes in 980.606600000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 5
# 690
# 0.48979811 0.50551494 0.49966603
# 690
# 0.48979834 0.50551486 0.49966609
# 5237100 bytes in 60.952000000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 10
# 976
# 0.49785014 0.50211968 0.49680553
# 976
# 0.49785012 0.50211990 0.49680564
# 10478336 bytes in 275.292800000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 100
# 3087
# 0.50365805 0.49631892 0.49592513
# 3087
# 0.50365770 0.49631900 0.49592495
# 104825259 bytes in 779.910700000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 1000
# 9763
# 0.49649581 0.49878219 0.49887213
# 9763
# 0.49649522 0.49878165 0.49887180
# 1048477859 bytes in 1926.970600000 milliseconds

# Four OpenMPI processes

# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 1
# 308
# 0.51118888 0.48902356 0.51353446
# 308
# 0.51118869 0.48902369 0.51353449
# 1043504 bytes in 474.475900000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 5
# 690
# 0.50125153 0.52512853 0.4933337
# 690
# 0.50125134 0.52512860 0.49333379
# 5237100 bytes in 289.917800000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 10
# 976
# 0.50871937 0.48464081 0.50073687
# 976
# 0.50871927 0.48464081 0.50073642
# 10478336 bytes in 100.448900000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 100
# 3087
# 0.49903273 0.4960186 0.49331348
# 3087
# 0.49903208 0.49601915 0.49331394
# 104825259 bytes in 805.243600000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab5$ ./exp 1000
# 9763
# 0.50337539 0.4978823 0.49928694
# 9763
# 0.50337529 0.49788222 0.49928582
# 1048477859 bytes in 1821.021800000 milliseconds

def getAverageDifference(arr0, arr1):
    assert len(arr0) == len(arr1)
    return sum([(float(t[0] - t[1]) / t[0]) * 100 for t in zip(arr0, arr1)]) / len(arr0)


oneThreadTime = [
    1289.1248,
    57.6019,
    40.7216,
    804.6849,
    2366.7603
]

twoThreadsTime = [
    980.6066,
    60.952,
    275.2928,
    779.9107,
    1926.9706
]

fourThreadsTime = [
    474.4759,
    289.9178,
    100.4489,
    805.2436,
    1821.0218
]

sizesInBytes = [ 1, 5, 10, 100, 1000 ]

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