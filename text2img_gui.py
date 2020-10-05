import os
import sys
sys.path.append("/usr/local/lib/python3.8/site-packages")
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

from collections import deque

import datetime, time, os, sys
import text2img

ui_path = "./mainwindow.ui"
form_class = uic.loadUiType(ui_path)[0]
        

#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.convertBtn.clicked.connect(self.convertBtnClicked)


    def getText(self):
        return self.inputText.toPlainText()


    def convertBtnClicked(self):
        file_name = text2img.text2img(self.getText())
        self.show_image(file_name)
        

    def show_image(self, img_path):
        img = QImage(img_path)
        s = QGraphicsScene()
        s.addPixmap(QPixmap.fromImage(img))
        self.graphicsView.setScene(s)
        self.graphicsView.show()


if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()