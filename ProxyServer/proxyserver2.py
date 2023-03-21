# Import socket module
from socket import *
# In order to terminate the program
import sys
import os
# Import thread module, datetime for timestamp
import threading
import datetime
import time

webserverName = "149.125.156.149"
webserverPort = 5002
proxyserverPort = 5003
proxyserverAddress = "149.125.156.149"

cachePath = "ProxyServer"

class myThread (threading.Thread):
   def __init__(self, connectionSocket, proxyclientSocket):
      threading.Thread.__init__(self)
      self.socket = connectionSocket
      self.proxysocket = proxyclientSocket

   def run(self):
      # Get lock to synchronize threads
      threadLock.acquire()
      sendFile(self.socket, self.proxysocket)
      # Free lock to release next thread
      threadLock.release()

threadLock = threading.Lock()
threads = list()

# thread function
def sendFile(connectionSocket, proxyclientSocket):
    while True:
        message = connectionSocket.recv(2048).decode()
        filename = message.split()[1]
        if os.path.exists(os.path.join(cachePath, filename[1:])):
            with open(os.path.join(cachePath, filename[1:]), 'r') as f:
                modifiedSentence = f.read()
            connectionSocket.send(("HTTP/1.1 200 OK\r\n\r\n" + modifiedSentence + "\r\n").encode())
            print("proxy-forward, Client, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))
        
        else:

            #Start connecting top webserver
            proxyclientSocket = socket(AF_INET, SOCK_STREAM)
            proxyclientSocket.connect((webserverName,webserverPort))
            
            #Send the filename to Web Server
            sentence = "GET " + filename + " HTTP/1.1"
            proxyclientSocket.send(sentence.encode())
            print("proxy-forward, Server, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))
            time.sleep(0.03)

            #Receive from Web Server and close the connection with web server
            modifiedSentence = proxyclientSocket.recv(2048).decode()
            proxyclientSocket.close()
            if not os.path.exists(os.path.join(cachePath, filename[1:])):
                with open(os.path.join(cachePath, filename[1:]), 'w') as f:
                    f.write(modifiedSentence[15:])

            connectionSocket.send(modifiedSentence.encode())
            print("proxy-forward, Client, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))
        return

    # Close client socket
    connectionSocket.close()

if __name__ == '__main__':
    # Prepare a sever socket
    proxyserverSocket = socket(AF_INET, SOCK_STREAM)

    proxyserverSocket.bind((proxyserverAddress,proxyserverPort))
    proxyserverSocket.listen(1)
    while True:
        connectionSocket, addr = proxyserverSocket.accept()
        thread = myThread(connectionSocket, proxyserverSocket)
        thread.start() #internal function of threading library
        threads.append(thread)
    for t in threads:
        t.join()

    # Close server socket
    serverSocket.close()

    # Terminate the program after sending the corresponding data
    sys.exit()