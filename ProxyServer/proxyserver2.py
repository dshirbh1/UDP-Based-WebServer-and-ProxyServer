# Import socket module
from socket import *
from PyPDF2 import PdfReader
# In order to terminate the program
import sys
import os
# Import thread module, datetime for timestamp
import threading
import datetime
import time

webserverName = "192.168.1.103"
webserverPort = 5002
proxyserverPort = 5003
proxyserverAddress = "192.168.1.103"
time_diff = 120.0
time_noted = datetime.datetime.now()
started = False
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
    global started
    global time_noted
    global time_diff
    message = connectionSocket.recv(2048).decode()
    filename = message.split()[1]

    if started == True and (datetime.datetime.now() - time_noted).total_seconds() >= time_diff:
        if os.path.exists(os.path.join(cachePath, filename[1:])):
            os.remove(os.path.join(cachePath, filename[1:]))
            started = False

    if os.path.exists(os.path.join(cachePath, filename[1:])):
        if filename[1:].endswith(".html"):
            with open(os.path.join(cachePath, filename[1:]), 'r') as f:
                modifiedSentence = f.read()
            connectionSocket.send(("HTTP/1.1 200 OK\r\n\r\n" + modifiedSentence + "\r\n").encode())
            print("proxy-cache, Client, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))

        elif filename[1:].endswith("pdf"):
            reader = PdfReader(filename[1:], 'rb')
            number_of_pages = len(reader.pages) ##len(reader.pages)
                
            current_page = 0
            whole_text = ""
            while current_page < number_of_pages:
                # getting a specific page from the pdf file
                page = reader.pages[current_page]
                    
                # extracting text from page
                outputdata = page.extract_text()
                whole_text = whole_text + outputdata
                current_page += 1
            # Send one HTTP header line into socket with data
            connectionSocket.send(("HTTP/1.1 200 OK\r\n\r\n" + whole_text + "\r\n").encode())
            print("proxy-cache, Client, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))
            
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
            if "404 Not Found" not in modifiedSentence:
                with open(os.path.join(cachePath, filename[1:]), 'w') as f:
                    f.write(modifiedSentence[15:])
                    time_noted = datetime.datetime.now()
                    started = True

        connectionSocket.send(modifiedSentence.encode())
        print("proxy-forward, Client, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))

    # Close client socket
    connectionSocket.close()

if __name__ == '__main__':
    # Prepare a sever socket
    proxyserverSocket = socket(AF_INET, SOCK_STREAM)
    proxyserverSocket.bind((proxyserverAddress,proxyserverPort))
    proxyserverSocket.listen(1)

    #Handling catche files from previous run
    for item in os.listdir(cachePath):
        if not item.endswith(".py"):
            os.remove(os.path.join(cachePath, item))

    while True:
        try:
            connectionSocket, addr = proxyserverSocket.accept()
            thread = myThread(connectionSocket, proxyserverSocket)
            thread.start() #internal function of threading library
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