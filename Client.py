from socket import *
from PyQt5 import QtWidgets, QtCore
import threading
import sys
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit, QFrame
from PyQt5 import QtGui


class Input(QtWidgets.QWidget):

    def __init__(self, parent = None):

        super().__init__(parent)
        self.temp = ""
        self.serverName = '127.0.0.1'
        self.serverPort = 12000
        self.input_text = ''
        self.connect = True
        self.log = ''
        self.name_list = []
        
        self.layout = QtWidgets.QFormLayout()
        
        '''
        self.btn2 = QtWidgets.QPushButton('Connect')
        self.btn2.clicked.connect(self.connect)
        self.layout.addRow(self.btn2)
        '''
        '''
        self.log_text = QtWidgets.QLabel("")
        #self.log_text.setBaseSize
        self.log_text.setBaseSize(350, 600)
        self.log_text.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        setReadOnly(True)
        '''
        self.log_text = QtWidgets.QTextBrowser()
        self.log_text.setGeometry(QtCore.QRect(40, 20, 450, 300))
        self.layout.addRow(self.log_text)
        
        self.input = QtWidgets.QLineEdit()
        
        self.btn1 = QtWidgets.QPushButton("輸入")
        self.btn1.setAutoDefault(False)

        self.btn1.clicked.connect(self.get_input)
        
        self.Label1 = QtWidgets.QLabel("Input")
        self.layout.addRow(self.Label1, self.input)
        self.layout.addRow(self.btn1)
        
        self.setLayout(self.layout)
        self.setWindowTitle("Practice")
        self.setGeometry(150, 150, 500, 800)
        
        thread_tcp = threading.Thread(target = self.MultithreadingTCPClient)
        thread_tcp.start()
        
    def MultithreadingTCPClient(self):
        try:
            with socket(AF_INET, SOCK_STREAM) as clientSocket:
                print('Connect to server', self.serverName, ':', self.serverPort)
                clientSocket.connect((self.serverName, self.serverPort))
                clientAddress, clientPort = clientSocket.getsockname()
                print('Client', clientAddress, ':', clientPort)
                print('Connecting to server', self.serverName, ':', self.serverPort)
                thread = threading.Thread(target = self.__listening, args = (clientSocket,))
                thread.start()
                while self.connect:
                    while self.input_text:
                        clientSocket.send(self.input_text.encode())
                        if self.input_text == 'exit':
                            self.connect = False
                            break
                        self.input_text = ''
        except:
            pass
        finally:
            print('Connection shutdown')
            
    def get_input(self):
        self.input_text = self.input.text()
        self.input.clear()
    
    def __listening(self, clientSocket):
        color = {
                    0: QtGui.QColor(255, 36, 0),
                    1: QtGui.QColor(13, 51, 255),
                    2: QtGui.QColor(22, 152, 43),
                    3: QtGui.QColor(255, 165, 0),
                    4: QtGui.QColor(255, 255, 0),
                    5: QtGui.QColor(255, 0, 255)
                }
        try:
            while True:
                message = clientSocket.recv(1024)
                if len(message) is 0:
                    break
                sentence = message.decode()
                name = sentence[1:sentence.find(']')]
                if name not in self.name_list:
                    self.name_list.append(name)
                self.log_text.setTextColor(color[self.name_list.index(name)])
                self.log_text.append(sentence)
                self.log_text.verticalScrollBar().setValue(self.log_text.verticalScrollBar().maximum()+1)
                print(sentence)
        except:
            pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    example = Input()
    example.show()
    app.exec_()


if __name__ == '__main__':
    main()