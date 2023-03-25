# Import socket module
from socket import *
# In order to terminate the program
import sys
# Import thread module, datetime for timestamp
import threading
import datetime
import time

webserverName = "192.168.1.103"
webserverPort = 5002
proxyserverPort = 5003
proxyserverAddress = "192.168.1.103"

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
    message = connectionSocket.recv(2048).decode()
    filename = message.split()[1]

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

    connectionSocket.send(modifiedSentence.encode())
    print("proxy-forward, Client, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))

    # Close client socket
    connectionSocket.close()

if __name__ == '__main__':
    # Prepare a sever socket
    proxyserverSocket = socket(AF_INET, SOCK_STREAM)

    proxyserverSocket.bind((proxyserverAddress,proxyserverPort))
    proxyserverSocket.listen(1)
    while True:
        try:
            connectionSocket, addr = proxyserverSocket.accept()
            thread = myThread(connectionSocket, proxyserverSocket)
            thread.start()
            threads.append(thread)
        except KeyboardInterrupt:
            #Shutting down the threads before ending
            for t in threads:
                t.join()
            break

    # Close server socket
    proxyserverSocket.close()
    # Terminate the program after sending the corresponding data
    sys.exit()