from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt

class Ui_MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.WindowFlags.WindowStaysOnTopHint)
        # self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.setGeometry(0, 0, 1920, 1080)
        self.setWindowOpacity(0.7)
