#!/usr/bin/env bash
num=${1}
for ((j=1; j<$num; j++))
do
    cp Injected-0.py Injected-"$j".py
done

for ((j=1; j<$num; j++))
do
    sed -i "s/0-conf.yaml/$j-conf.yaml/g" Injected-"$j".py
done

