# 这段程序可将图标gen.ico转换成icon.py文件里的base64数据
import base64
import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow

from Robot_Ui import Ui_MainWindow

open_icon = open("fb.ico", "rb")
b64str = base64.b64encode(open_icon.read())
open_icon.close()
write_data = "img = '%s'" % b64str
f = open("icon.py", "w+")
f.write(write_data)
f.close()


class MyUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super(MyUi, self).setupUi(MainWindow)


# ...省略部分
import base64
from icon import img
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()

    # 将import进来的icon.py里的数据转换成临时文件tmp.ico，作为图标
    tmp = open("tmp.ico", "wb+")
    tmp.write(base64.b64decode(img))
    tmp.close()
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("tmp.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)
    os.remove("tmp.ico")  # 删掉临时文件

    ui = MyUi()
    ui.setupUi(MainWindow)
    MainWindow.show()
