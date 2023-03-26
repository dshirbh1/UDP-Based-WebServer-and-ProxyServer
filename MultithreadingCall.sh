#!/bin/bash

for i in {1..10}
do
    #curl "http://192.168.1.103:5003/Project2-ProxyServer.pdf" &
    #curl "http://192.168.1.103:5003/Home.html" &
    #curl --output $i".html" "http://192.168.1.103:5003/Home.html" &
    curl --output $i".pdf" "http://192.168.1.103:5003/Project2-ProxyServer1.pdf" &
done
