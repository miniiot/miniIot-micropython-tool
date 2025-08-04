# -*- coding: utf-8 -*-
from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout


class MainViewWindow(QMainWindow):

    def __init__(self):
        super().__init__()


    def initUI(self):

        self.setWindowTitle(self.tr("PressureCalibration"))
        self.setMinimumSize(700, 450)
        # self.setWindowIcon(QIcon(f'{os.getcwd()}\\logo.ico'))

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)
        self.layout = QHBoxLayout(self.widget)