#!/bin/bash
ac=$2
if [ $1 = "y" ]
then
    echo "${ac:0:8}"
else
    echo "aaa"
fi
