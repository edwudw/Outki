import sys, socket, threading, subprocess, time, platform
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QPushButton, QApplication, QInputDialog, QSystemTrayIcon)
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QWindow
from PyQt5.QtCore import Qt, QEvent
class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)
        menu = QtWidgets.QMenu(parent)
        exitAction = menu.addAction("Exit")
        exitAction.triggered.connect(parent.close)
        self.setContextMenu(menu)

class ThreadingExample(object):
 
    def __init__(self):
    
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution
 
    def run(self):
        messageBox.append('Connected to Server!')
        while True:
            data = s.recv(2048)
            data2 = data.decode("utf-8")
            messageBox.append(data.decode("utf-8"))
            messageBox.moveCursor(QtGui.QTextCursor.End)
            print(platform.system())
            if ex.isActiveWindow() == False:
                print('ok cool')
                if platform.system() == "Linux":
                    subprocess.call("notify-send " + data2, shell=True)
                elif platform.system() == "win32" or platform.system() == "Darwin":
                    ex.tray_icon.showMessage('New Message', data2, QtGui.QIcon('Outki.ico'), 0)
            

class Example(QWidget, QWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
    def dialoga(self):
        text, ok = QInputDialog.getText(self, 'Username', 'Enter your username:')
        
        if ok:
            text = "/username" + text
            s.sendall(str.encode(text))
        else:
            print('error: NO USERNAME')
            sys.exit()
    def initUI(self):
        self.dialoga()
        self.sendamessage = QLabel('Send:')
        self.tray_icon = SystemTrayIcon(QtGui.QIcon('Outki.ico'), self)
        self.tray_icon.show()
        self.messageEdit = QLineEdit()
        global messageBox
        messageBox = QTextEdit()
        messageBox.setReadOnly(True)
        self.sendButton = QPushButton("Send")
        
        grid = QGridLayout()
        grid.setSpacing(1)
        
        grid.addWidget(messageBox, 1, 0, 2, 4)
        grid.addWidget(self.sendamessage, 3, 0, 4, 0)
        grid.addWidget(self.messageEdit, 3, 1, 4, 2)
        grid.addWidget(self.sendButton, 3, 3, 4, 3)
       
        self.setLayout(grid)
        self.sendButton.clicked.connect(self.send)
        self.messageEdit.returnPressed.connect(self.send)
        threade = ThreadingExample()
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Outki')
        self.setWindowIcon(QIcon('Outki.ico'))
        self.show()
    def send(self):
        tosend = self.messageEdit.text()
        self.messageEdit.clear()
        messageBox.moveCursor(QtGui.QTextCursor.End)
        messageBox.append('You: ' + tosend)
        s.sendall(str.encode(tosend))

        
if __name__ == '__main__':
    host = "localhost"
    port = 5558

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.connect((host,port))
    except socket.error as e:
        print (str(e))
        y = input('Press enter to close')
        sys.exit()
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
    
