from socket import *
import threading
import sys
import random

class MultithreadingTCPServer:
    def __init__(self, name, port):
        self.serverName = name
        self.serverPort = port
        self.ans = []
        self.client_list = []

    def start(self):
        try:
            #self.creat_ans()
            with socket(AF_INET, SOCK_STREAM) as serverSocket:
                print('Bind server socket to', self.serverName, ':', self.serverPort)
                serverSocket.bind((self.serverName, self.serverPort))
                serverSocket.listen(1)
                print('Multithreading server binding success')
                self.ans = random.sample('0123456789', 4)
                print(self.ans)
                print('Creat quetion')
                while True:
                    clientSocket, address = serverSocket.accept()
                    thread = threading.Thread(target = self.__handleClient, args = (clientSocket,))
                    thread.start()
        except:
            pass
        finally:
            print('Server shutdown.')
            
    def __handleClient(self, clientSocket):
        clientName, clientPort = clientSocket.getpeername()
        print('Connecting to', clientName, clientPort)
        try:
            #Enter name
            sign = '[系統]Enter your Name:'
            clientSocket.send(sign.encode())
            message = clientSocket.recv(1024)
            name = message.decode()
            sign = '[' + name + ']' + name
            clientSocket.send(sign.encode())
            sign = '[系統]Start guessing~~~'
            clientSocket.send(sign.encode())
            self.client_list.append(clientSocket)
            while True:
                message = clientSocket.recv(1024)
                if len(message) is 0 or message.decode() == 'exit':
                    break
                sentence = message.decode()
                print(sentence)
                #capitalizedSentence = sentence.upper()
                correct, capitalizedSentence = self.check_ans(sentence) 
                capitalizedSentence = '[' + name + '] guess '  + sentence + ': ' + capitalizedSentence
                for client in self.client_list:
                        client.send(capitalizedSentence.encode())
                if correct:
                    for client in self.client_list:
                        sign = '[系統]' + name + ' bingo!!!\n[系統]Change puzzle' 
                        client.send(sign.encode())
                    self.creat_ans()
                    print(self.ans)
                    
        except:
            clientSocket.close()
        finally:
            print('Disconnecting to', clientName, ':', clientPort)
        
    def creat_ans(self):
        self.ans = random.sample('0123456789', 4)
        
    def check_ans(self, guess):
        a = 0
        b = 0
        correct = False
        for i in range(len(guess)):
            for k in range(len(self.ans)):
                if guess[i] == self.ans[k]:
                    if i == k:
                        a = a + 1
                    else:
                        b = b + 1
        if a==4:
            correct = True
        tmp = str(a) + 'A' + str(b) + 'B'
        return correct, tmp
        
        
if len(sys.argv) < 3:
    serverName = '127.0.0.1'
    serverPort = 12000
else:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])

server = MultithreadingTCPServer(serverName, serverPort)
server.start()

