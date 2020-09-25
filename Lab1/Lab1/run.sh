#!/bin/bash
size=125
while [ $size -le 2001 ]
do
  (exec ./bin/x64/Debug/Lab1.out $size.txt result$size.txt)&
  size=$(( $size * 2 ))
done