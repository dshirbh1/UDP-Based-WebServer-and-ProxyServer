#!/bin/bash

for i in {1..10}
do
    curl "http://149.125.41.213:5003/home.html" &
done
