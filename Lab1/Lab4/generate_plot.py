import matplotlib.pyplot as plt

# CPU
# rinser@MININT-NIPENTJ:~/Lab1$ ./exp 5
# 690
# 0.50806413 0.52414932 0.4899262
# 690
# 0.50806421 0.52414918 0.48992610
# 5237100 bytes in 3.518000000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab1$ ./exp 10
# 976
# 0.48468079 0.49176483 0.49272187
# 976
# 0.48468104 0.49176523 0.49272200
# 10478336 bytes in 6.772000000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab1$ ./exp 50
# 2183
# 0.48893183 0.49698009 0.5014711
# 2183
# 0.48893169 0.49698004 0.50147104
# 52420379 bytes in 31.407000000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab1$ ./exp 100
# 3087
# 0.49928757 0.50158358 0.50039834
# 3087
# 0.49928761 0.50158393 0.50039852
# 104825259 bytes in 63.977000000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab1$ ./exp 500
# 6903
# 0.50095742 0.50103748 0.49857632
# 6903
# 0.50095737 0.50103742 0.49857602
# 524165499 bytes in 472.096000000 milliseconds
# rinser@MININT-NIPENTJ:~/Lab1$ ./exp 1000
# 9763
# 0.49574038 0.50273391 0.49542982
# 9763
# 0.49573973 0.50273305 0.49542955
# 1048477859 bytes in 803.526000000 milliseconds

def getAverageDifference(arr0, arr1):
    assert len(arr0) == len(arr1)
    return sum([(float(t[0] - t[1]) / t[0]) * 100 for t in zip(arr0, arr1)]) / len(arr0)


cpuTime = [
    6.772000000,
    31.407000000,
    63.977000000,
    472.096000000,
    803.526000000
]

gpuTime = [
    2.173600000,
    3.923900000,
    7.003000000,
    11.463800000,
    21.367000000
]

sizesInBytes = [ 10, 50, 100, 500, 1000 ]

avg_cpu_gpu = getAverageDifference(cpuTime, gpuTime)
print(avg_cpu_gpu)

plt.xlabel('size in megabytes')
plt.ylabel('time in milliseconds')

plt.plot(sizesInBytes, cpuTime, 'bo')
plt.plot(sizesInBytes, gpuTime, 'ro')
plt.plot(sizesInBytes, gpuTime, 'r')
plt.plot(sizesInBytes, cpuTime, 'b')

plt.show()