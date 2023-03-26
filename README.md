# Binghamton University, Spring 2023

## CS428/528 Project-2: Proxy Server

### SUMMARY
Two installments-
Installment1
Where a webserver and proxy server run and server request from client
Client sends request to proxyserver, which forwards it to origin server,
and accepts response from origin and forwards it to client
Proxy is the intermediatary in this instance

Installment2

Similar to installment but proxy server maintains a cache of requested objects, 
if object exists, serves it directly to client
If it does not, then forwards request to origin server, receives the response, 
saves the file in it's cache and then forwards it to client

### NOTES, KNOWN BUGS, AND/OR INCOMPLETE PARTS

[Add any notes you have here and/or any parts of the project you were not able to complete]: #
Sometimes, error "Connections refused by peer" occurs.

### REFERENCES

[List any outside resources used]: 
StackOverflow forums
Medium Articles
https://thispointer.com/python-get-difference-between-two-datetimes-in-seconds/
https://stackoverflow.com/questions/29198122/how-to-write-proxy-program-for-resending-packets

### INSTRUCTIONS

[Provide clear and complete step-by-step instructions on how to run and test your project]: #
Part 1:
1. Change the IP address and port number as per availability in webserver.py and proxyserver1.py
2. Run webserver.py first and then proxyserver1.py. 
3. Request a proxyserver's IP address and port using URL "http://Proxy_IP:Proxy_Port/File_Name".
4. Client should receive a response and file content which is present in Web server, a print lines on proxyserver stating proxy-forward to server and then to client, a print line on web server stating the timestamp and response code sent to a proxy server.
5. Same thing will happen for the 2nd request onwards.

Part 2:
1. Change the IP address and port number as per availability in webserver.py and proxyserver1.py
2. Run webserver.py first and then proxyserver1.py. Make sure both files are in different folders.
3. Request a proxyserver's IP address and port using URL "http://Proxy_IP:Proxy_Port/File_Name".
4. Client should receive a response and file content which is present in Web server, a print lines on proxyserver stating proxy-forward to server and then to client, a print line on web server stating the timestamp and response code sent to a proxy server. Also, a file will be saved on proxyserver's folder which will be a caches file.
5. For the next request of the same file withing 120 seconds, proxy will serve the client with file content and prints a line stating proxy-cache.
6. A reqauest from client after 120 seconds will again sends this to web serveand follow steps 4 and 5.


### SUBMISSION

I have done this assignment completely on my own. I have not copied it, nor have I given my solution to anyone else. I understand that if I am involved in plagiarism or cheating I will have to sign an official form that I have cheated and that this form will be stored in my official university record. I also understand that I will receive a grade of "0" for the involved assignment and my grade will be reduced by one level (e.g., from "A" to "A-" or from "B+" to "B") for my first offense, and that I will receive a grade of "F" for the course for any additional offense of any kind.

By signing my name below and submitting the project, I confirm the above statement is true and that I have followed the course guidelines and policies.

Submission date:

Team member 1 name: Devashri Pramodrao Shirbhate

Team member 2 name: Jay Balaram Sankhe

