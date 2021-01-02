#!/bin/bash
num=${1}

for ((i=0; i<$num; i++))
do
    python Injected-"$i".py
done
