# Import socket module
from socket import *
from PyPDF2 import PdfReader
# In order to terminate the program
import sys
# Import thread module
import threading
import datetime

class myThread (threading.Thread):
   def __init__(self, connectionSocket):
      threading.Thread.__init__(self)
      self.socket = connectionSocket

   def run(self):
      # Get lock to synchronize threads
      threadLock.acquire()
      sendFile(self.socket)
      # Free lock to release next thread
      threadLock.release()

threadLock = threading.Lock()
threads = list()
# thread function
def sendFile(connectionSocket):
    try:
        message = connectionSocket.recv(2048).decode()
        filename = message.split()[1]
            
        if filename.endswith("pdf"):
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
            print("server-response, 200 OK, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))
            
        elif filename.endswith("html"):
            f = open(filename[1:])
            outputdata = f.read()

            # Send one HTTP header line into socket
            connectionSocket.send(("HTTP/1.1 200 OK\r\n\r\n" + outputdata + "\r\n").encode())
            print("server-response, 200 OK, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))

    except IOError:
        # Send response message for file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n File not found \r\n".encode())
        print("server-response, 404 Not Found, " + str(threading.get_ident()) + ", " +  str(datetime.datetime.now()))

    # Close client socket
    connectionSocket.close()

if __name__ == '__main__':
    # Prepare a sever socket
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverPort = 5002
    serverAddress = "192.168.1.103"
    serverSocket.bind((serverAddress,serverPort))
    serverSocket.listen(1)
    while True:
        try:
            # Establish the connection
            connectionSocket, addr = serverSocket.accept()
            thread = myThread(connectionSocket)
            thread.start()
            threads.append(thread)
        except KeyboardInterrupt:
            #Shutting down the threads before ending
            for t in threads:
                t.join()
            break

    # Close server socket
    serverSocket.close()
    # Terminate the program after sending the corresponding data
    sys.exit()