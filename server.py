from socket import *
from threading import Thread
from time import sleep
IP = '10.190.86.194'
Host,Port = 'localhost',8888 
def getJson():
    with open('h.json','r') as f:
        return f.read()
def handleConnection(newsocket,addr):

    # while True:
    information = newsocket.recv(1024)
    if len(information) > 0:
        print(str(information.decode('utf-8')))
        newsocket.sendall(getJson().encode('utf-8'))
    #print(len(information))
         # print(str(information.decode('utf-8')))
    else:
        print('client was closed')
    #sleep(10)
    print('done')
    newsocket.close()
def main():
    serSocket = socket(AF_INET,SOCK_STREAM)
    serSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    serSocket.bind((Host,Port))
    serSocket.listen(3)
    print('Serving HTTP on port %s ...' % Port)

    try:
        while True:
            newsocket,addr = serSocket.accept()
            print('--success connect---')
            client = Thread(target=handleConnection,args=(newsocket,addr))
            client.start()
    finally:
        serSocket.close()
if __name__ == '__main__':
    main()
    
from socket import *
from threading import Thread
from time import sleep
IP = '10.190.86.194'
Host,Port = 'localhost',8888 
def getJson():
    with open('h.json','r') as f:
        return f.read()
def handleConnection(newsocket,addr):

    # while True:
    information = newsocket.recv(1024)
    if len(information) > 0:
        print(str(information.decode('utf-8')))
        newsocket.sendall(getJson().encode('utf-8'))
    #print(len(information))
         # print(str(information.decode('utf-8')))
    else:
        print('client was closed')
    #sleep(10)
    print('done')
    newsocket.close()
def main():
    serSocket = socket(AF_INET,SOCK_STREAM)
    serSocket.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    serSocket.bind((Host,Port))
    serSocket.listen(3)
    print('Serving HTTP on port %s ...' % Port)

    try:
        while True:
            newsocket,addr = serSocket.accept()
            print('--success connect---')
            client = Thread(target=handleConnection,args=(newsocket,addr))
            client.start()
    finally:
        serSocket.close()
if __name__ == '__main__':
    main()
    
