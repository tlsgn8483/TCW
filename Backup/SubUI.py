from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog
import pandas as pd
import pic_1_rc
import sys
import os
import datetime
import csv
from WorkList_db import WorkList_db_class
from cryptography.fernet import Fernet


class Singleton(type):  # Type을 상속받음
    __instances = {}  # 클래스의 인스턴스를 저장할 속성

    def __call__(cls, *args, **kwargs):  # 클래스로 인스턴스를 만들 때 호출되는 메서드
        if cls not in cls.__instances:  # 클래스로 인스턴스를 생성하지 않았는지 확인
            cls.__instances[cls] = super().__call__(*args, **kwargs)  # 생성하지 않았으면 인스턴스를 생성하여 해당 클래스 사전에 저장
        return cls.__instances[cls]  # 클래스로 인스턴스를 생성했으면 인스턴스 반환


class Ui_MainWindow(QDialog):
    plate_type = "Plate"
    cap_type = "Cap"
    ctrl_seq = "NC, PC"
    selection_bcd = ""
    smp_count_1 = 0
    smp_count_2 = 0
    path_csv = ""
    csv_signal = 0
    dir_csv = ""
    temp_src = ""
    use_bcd = "PCR Plate and DWP"
    worklist_name = ""
    Sel_Signal = 0
    bcd_list = []
    temp_bcd_list = []
    DB = WorkList_db_class()
    signal_close = 0

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        plrn_path, bcd_path = self.DB.display_path()
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowFlags.WindowStaysOnTopHint)
        self.setWindowTitle("TCW")
        # self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(770, 800)
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(97, -24, 680, 825))
        self.tabWidget.setObjectName("tabWidget")
        self.Tab_1 = QtWidgets.QWidget()
        self.Tab_1.setObjectName("Tab_1")
        self.lineEdit_smp_bcd = QtWidgets.QLineEdit(self.Tab_1)
        self.lineEdit_smp_bcd.setGeometry(QtCore.QRect(370, 100, 251, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_smp_bcd.setFont(font)
        self.lineEdit_smp_bcd.setStyleSheet("")
        self.lineEdit_smp_bcd.setObjectName("lineEdit_smp_bcd")
        self.lineEdit_smp_bcd.setEnabled(False)
        self.toolButton_load = QtWidgets.QToolButton(self.Tab_1)
        self.toolButton_load.setGeometry(QtCore.QRect(233, 100, 28, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_load.setFont(font)
        self.toolButton_load.setStyleSheet("")
        self.toolButton_load.setObjectName("toolButton_load")
        self.pushButton_temp = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_temp.setGeometry(QtCore.QRect(191, 101, 0, 0))

        self.tabWidget_bcd = QtWidgets.QTabWidget(self.Tab_1)
        self.tabWidget_bcd.setGeometry(QtCore.QRect(70, 170, 511, 561))
        self.tabWidget_bcd.setObjectName("tabWidget_bcd")
        self.Tab_bcd_1 = QtWidgets.QWidget()
        self.Tab_bcd_1.setObjectName("Tab_bcd_1")
        self.Tab_bcd_2 = QtWidgets.QWidget()
        self.Tab_bcd_2.setObjectName("Tab_bcd_2")
        self.tabWidget_bcd.tabBar().hide()

        self.tableWidget_smp_select = QtWidgets.QTableWidget(self.Tab_bcd_2)
        self.tableWidget_smp_select.setGeometry(QtCore.QRect(0, 0, 511, 561))
        self.tableWidget_smp_select.setObjectName("tableWidget_smp_select")
        self.tableWidget_smp_select.setColumnCount(1)
        self.tableWidget_smp_select.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_smp_select.setHorizontalHeaderItem(0, item)
        self.tableWidget_smp_select.horizontalHeader().setStretchLastSection(True)

        self.radioButton_bcd_1 = QtWidgets.QRadioButton(self.Tab_1)
        self.radioButton_bcd_1.setGeometry(QtCore.QRect(70, 140, 120, 25))
        self.radioButton_bcd_1.setObjectName("radioButton_bcd_1")
        self.buttonGroup_1 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_1.setObjectName("buttonGroup_2")
        self.buttonGroup_1.addButton(self.radioButton_bcd_1)
        self.radioButton_bcd_2 = QtWidgets.QRadioButton(self.Tab_1)
        self.radioButton_bcd_2.setGeometry(QtCore.QRect(190, 140, 135, 25))
        self.radioButton_bcd_2.setObjectName("radioButton_bcd_2")
        self.buttonGroup_1.addButton(self.radioButton_bcd_2)

        self.pushButton_confirm = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_confirm.setGeometry(QtCore.QRect(490, 136, 71, 28))  # 490, 136, 71, 28
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.pushButton_confirm.setEnabled(False)

        self.pushButton_cancel = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_cancel.setGeometry(QtCore.QRect(490, 136, 71, 28))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_cancel.setVisible(False)

        self.tableWidget_smp = QtWidgets.QTableWidget(self.Tab_bcd_1)
        self.tableWidget_smp.setGeometry(QtCore.QRect(0, 0, 511, 561))
        self.tableWidget_smp.setObjectName("tableWidget_smp")
        self.tableWidget_smp.setColumnCount(2)
        self.tableWidget_smp.setRowCount(0)
        # self.tableWidget_smp.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_smp.setEditTriggers(QtWidgets.QAbstractItemView.EditTriggers.NoEditTriggers)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_smp.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.tableWidget_smp.setHorizontalHeaderItem(1, item)

        self.pushButton_smp_ok = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_smp_ok.setGeometry(QtCore.QRect(191, 101, 40, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.pushButton_smp_ok.setFont(font)
        self.pushButton_smp_ok.setStyleSheet("background-color: rgb(77, 154, 231);\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "border-width: 0px;")
        self.pushButton_smp_ok.setObjectName("pushButton_smp_ok")

        self.label_smp_count = QtWidgets.QLabel(self.Tab_1)
        self.label_smp_count.setGeometry(QtCore.QRect(29, 100, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_smp_count.setFont(font)
        self.label_smp_count.setObjectName("label_smp_count")
        self.lineEdit_smp_count = QtWidgets.QLineEdit(self.Tab_1)
        self.lineEdit_smp_count.setGeometry(QtCore.QRect(138, 101, 50, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_smp_count.setFont(font)
        self.lineEdit_smp_count.setStyleSheet("")
        self.lineEdit_smp_count.setObjectName("lineEdit_smp_count")
        self.label_smp_bcd = QtWidgets.QLabel(self.Tab_1)
        self.label_smp_bcd.setGeometry(QtCore.QRect(300, 100, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_smp_bcd.setFont(font)
        self.label_smp_bcd.setObjectName("label_smp_bcd")
        self.pushButton_next_1 = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_next_1.setGeometry(QtCore.QRect(530, 750, 93, 28))
        self.pushButton_next_1.setObjectName("pushButton_next_1")
        self.pushButton_next_1.setEnabled(False)
        self.pushButton_arrow_1 = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_arrow_1.setGeometry(QtCore.QRect(315, 60, 16, 31))
        self.pushButton_arrow_1.setStyleSheet("image: url(:/newPrefix/pic_1.png);\n"
                                              "border-style: outset;\n"
                                              "border-width: 0px;\n"
                                              "border-color: black;\n"
                                              "padding: 1px;\n"
                                              "border-radius: 15px;\n"
                                              "")
        self.pushButton_arrow_1.setText("")
        self.pushButton_arrow_1.setObjectName("pushButton_arrow_1")
        self.pushButton_smp_info_1 = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_smp_info_1.setGeometry(QtCore.QRect(-1, 60, 325, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_smp_info_1.setFont(font)
        self.pushButton_smp_info_1.setStyleSheet("border-style: outset;\n"
                                                 "background-color: rgb(225, 225, 225);\n"
                                                 "border-width: 0px;\n"
                                                 "\n"
                                                 "\n"
                                                 "")
        self.pushButton_smp_info_1.setObjectName("pushButton_smp_info_1")
        self.pushButton_protocol_info_1 = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_protocol_info_1.setGeometry(QtCore.QRect(324, 60, 360, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.pushButton_protocol_info_1.setFont(font)
        self.pushButton_protocol_info_1.setStyleSheet("border-style: outset;\n"
                                                      "background-color: rgb(225, 225, 225);\n"
                                                      "border-width: 0px;\n"
                                                      "\n"
                                                      "\n"
                                                      "")
        self.pushButton_protocol_info_1.setObjectName("pushButton_protocol_info_1")
        self.line_5 = QtWidgets.QFrame(self.Tab_1)
        self.line_5.setGeometry(QtCore.QRect(0, 85, 685, 8))
        # self.line_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_5.setLineWidth(1)
        # self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setObjectName("line_5")
        self.lineEdit_smp_bcd.raise_()
        self.toolButton_load.raise_()
        self.tableWidget_smp.raise_()
        self.label_smp_count.raise_()
        self.lineEdit_smp_count.raise_()
        self.label_smp_bcd.raise_()
        self.pushButton_next_1.raise_()
        self.pushButton_smp_info_1.raise_()
        self.pushButton_protocol_info_1.raise_()
        self.line_5.raise_()
        self.pushButton_arrow_1.raise_()
        self.tabWidget.addTab(self.Tab_1, "")
        self.tabWidget_bcd.addTab(self.Tab_bcd_1, "")
        self.tabWidget_bcd.addTab(self.Tab_bcd_2, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_protocol = QtWidgets.QLabel(self.tab_2)
        self.label_protocol.setGeometry(QtCore.QRect(30, 120, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_protocol.setFont(font)
        self.label_protocol.setObjectName("label_protocol")
        self.pushButton_prev_1 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_prev_1.setGeometry(QtCore.QRect(30, 750, 93, 28))
        self.pushButton_prev_1.setObjectName("pushButton_prev_1")
        self.listWidget_protocol = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_protocol.setGeometry(QtCore.QRect(110, 120, 370, 100))
        self.listWidget_protocol.setObjectName("listWidget_protocol")
        self.listWidget_protocol.setEnabled(False)
        self.pushButton_run = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_run.setGeometry(QtCore.QRect(530, 750, 93, 28))
        self.pushButton_run.setObjectName("pushButton_run")
        self.pushButton_run.setEnabled(False)

        self.pushButton_hidden = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_hidden.setGeometry(QtCore.QRect(0, 420, 15, 15))
        self.pushButton_hidden.setObjectName("pushButton_hidden")
        self.pushButton_hidden.setStyleSheet("border-style: outset;\n"
                                             "border-width: 0px;\n"
                                             "border-color: black;\n"
                                             "")
        self.label_tube_type = QtWidgets.QLabel(self.tab_2)
        self.label_tube_type.setGeometry(QtCore.QRect(30, 260, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_tube_type.setFont(font)
        self.label_tube_type.setObjectName("label_tube_type")
        self.radioButton_tube_1 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_tube_1.setGeometry(QtCore.QRect(220, 260, 108, 19))
        self.radioButton_tube_1.setObjectName("radioButton_tube_1")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_tube_1)
        self.radioButton_tube_2 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_tube_2.setGeometry(QtCore.QRect(370, 260, 108, 19))
        self.radioButton_tube_2.setObjectName("radioButton_tube_2")
        self.buttonGroup_2.addButton(self.radioButton_tube_2)
        self.label_cap_type = QtWidgets.QLabel(self.tab_2)
        self.label_cap_type.setGeometry(QtCore.QRect(30, 320, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_cap_type.setFont(font)
        self.label_cap_type.setObjectName("label_cap_type")
        self.radioButton_cap_1 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_cap_1.setGeometry(QtCore.QRect(220, 320, 108, 19))
        self.radioButton_cap_1.setObjectName("radioButton_cap_1")
        self.buttonGroup_3 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_3.setObjectName("buttonGroup_3")
        self.buttonGroup_3.addButton(self.radioButton_cap_1)
        self.radioButton_cap_2 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_cap_2.setGeometry(QtCore.QRect(370, 320, 108, 19))
        self.radioButton_cap_2.setObjectName("radioButton_cap_2")
        self.buttonGroup_3.addButton(self.radioButton_cap_2)
        self.lineEdit_pcr_bcd = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_pcr_bcd.setGeometry(QtCore.QRect(210, 418, 400, 20))

        self.lineEdit_Extraction_bcd = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_Extraction_bcd.setGeometry(QtCore.QRect(210, 496, 400, 20))

        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_pcr_bcd.setFont(font)
        self.lineEdit_pcr_bcd.setStyleSheet("")
        self.lineEdit_pcr_bcd.setObjectName("lineEdit_pcr_bcd")

        self.lineEdit_Extraction_bcd.setFont(font)
        self.lineEdit_Extraction_bcd.setStyleSheet("")
        self.lineEdit_Extraction_bcd.setObjectName("lineEdit_Extraction_bcd")

        self.label_pcr_bcd = QtWidgets.QLabel(self.tab_2)
        self.label_pcr_bcd.setGeometry(QtCore.QRect(30, 412, 191, 31))


        self.label_extraction_bcd = QtWidgets.QLabel(self.tab_2)
        self.label_extraction_bcd.setGeometry(QtCore.QRect(30, 490, 191, 31))

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_pcr_bcd.setFont(font)
        self.label_pcr_bcd.setObjectName("label_pcr_bcd")

        self.label_extraction_bcd.setFont(font)
        self.label_extraction_bcd.setObjectName("label_extraction_bcd")
        self.label_testcount = QtWidgets.QLabel(self.tab_2)
        self.label_testcount.setGeometry(QtCore.QRect(30, 435, 91, 31))

        self.label_extractioncount = QtWidgets.QLabel(self.tab_2)
        self.label_extractioncount.setGeometry(QtCore.QRect(30, 512, 191, 31))

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_testcount.setFont(font)
        self.label_testcount.setObjectName("label_testcount")

        self.label_extractioncount.setFont(font)
        self.label_extractioncount.setObjectName("label_extractioncount")

        self.label_PCR_plate = QtWidgets.QLabel(self.tab_2)
        self.label_PCR_plate.setGeometry(QtCore.QRect(30, 560, 180, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_PCR_plate.setFont(font)
        self.label_PCR_plate.setObjectName("label_PCR_plate")
        self.lineEdit_PCR_plate = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_PCR_plate.setGeometry(QtCore.QRect(210, 566, 251, 20))



        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_PCR_plate.setFont(font)
        self.lineEdit_PCR_plate.setStyleSheet("")
        self.lineEdit_PCR_plate.setObjectName("lineEdit_PCR_plate")


        self.label_DWP = QtWidgets.QLabel(self.tab_2)
        self.label_DWP.setGeometry(QtCore.QRect(30, 596, 120, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DWP.setFont(font)
        self.label_DWP.setObjectName("label_DWP")
        self.lineEdit_DWP = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_DWP.setGeometry(QtCore.QRect(210, 602, 251, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_DWP.setFont(font)
        self.lineEdit_DWP.setStyleSheet("")
        self.lineEdit_DWP.setObjectName("lineEdit_DWP")

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_testcount = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_testcount.setGeometry(QtCore.QRect(210, 445, 51, 20))

        self.textBrowser_extractioncount = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_extractioncount.setGeometry(QtCore.QRect(210, 520, 51, 20))

        # self.textBrowser_testcount.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_testcount.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_testcount.setObjectName("textBrowser_testcount")

        self.textBrowser_extractioncount.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_extractioncount.setObjectName("textBrowser_extractioncount")

        self.pushButton_smp_info_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_smp_info_2.setGeometry(QtCore.QRect(-1, 60, 325, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.pushButton_smp_info_2.setFont(font)
        self.pushButton_smp_info_2.setStyleSheet("border-style: outset;\n"
                                                 "background-color: rgb(225, 225, 225);\n"
                                                 "border-width: 0px;\n"
                                                 "\n"
                                                 "\n"
                                                 "")
        self.pushButton_smp_info_2.setObjectName("pushButton_smp_info_2")
        self.pushButton_arrow_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_arrow_2.setGeometry(QtCore.QRect(315, 60, 16, 31))
        self.pushButton_arrow_2.setStyleSheet("image: url(:/newPrefix/pic_1.png);\n"
                                              "border-style: outset;\n"
                                              "border-width: 0px;\n"
                                              "border-color: black;\n"
                                              "padding: 1px;\n"
                                              "border-radius: 15px;\n"
                                              "")
        self.pushButton_arrow_2.setText("")
        self.pushButton_arrow_2.setObjectName("pushButton_arrow_2")
        self.pushButton_protocol_info_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_protocol_info_2.setGeometry(QtCore.QRect(324, 60, 360, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_protocol_info_2.setFont(font)
        self.pushButton_protocol_info_2.setStyleSheet("border-style: outset;\n"
                                                      "background-color: rgb(225, 225, 225);\n"
                                                      "border-width: 0px;\n"
                                                      "\n"
                                                      "\n"
                                                      "")
        self.pushButton_protocol_info_2.setObjectName("pushButton_protocol_info_2")
        self.line_6 = QtWidgets.QFrame(self.tab_2)
        self.line_6.setGeometry(QtCore.QRect(0, 85, 685, 8))
        # self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_6.setLineWidth(1)
        # self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_6.setObjectName("line_6")
        self.pushButton_prev_1.raise_()
        self.label_protocol.raise_()
        self.listWidget_protocol.raise_()
        self.pushButton_run.raise_()
        self.pushButton_hidden.raise_()
        self.label_tube_type.raise_()
        self.radioButton_tube_1.raise_()
        self.radioButton_tube_2.raise_()
        self.label_cap_type.raise_()
        self.radioButton_cap_1.raise_()
        self.radioButton_cap_2.raise_()
        self.lineEdit_pcr_bcd.raise_()
        self.lineEdit_Extraction_bcd.raise_()
        self.label_pcr_bcd.raise_()
        self.label_extraction_bcd.raise_()
        self.label_testcount.raise_()
        self.label_extractioncount.raise_()
        self.textBrowser_testcount.raise_()
        self.textBrowser_extractioncount.raise_()
        self.pushButton_smp_info_2.raise_()
        self.pushButton_protocol_info_2.raise_()
        self.line_6.raise_()
        self.pushButton_arrow_2.raise_()
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_ctrl_seq = QtWidgets.QLabel(self.tab_3)
        self.label_ctrl_seq.setGeometry(QtCore.QRect(30, 90, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ctrl_seq.setFont(font)
        self.label_ctrl_seq.setObjectName("label_ctrl_seq")

        self.label_plrn_path = QtWidgets.QLabel(self.tab_3)
        self.label_plrn_path.setGeometry(QtCore.QRect(30, 150, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_plrn_path.setFont(font)
        self.label_plrn_path.setObjectName("label_plrn_path")
        self.textBrowser_plrn_path = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_plrn_path.setGeometry(QtCore.QRect(230, 150, 320, 40))
        # self.textBrowser_plrn_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.textBrowser_plrn_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path.setObjectName("textBrowser_plrn_path")
        self.textBrowser_plrn_path.setText(plrn_path[0][0])
        self.toolButton_plrn_path = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_plrn_path.setGeometry(QtCore.QRect(554, 149, 28, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_plrn_path.setFont(font)
        self.toolButton_plrn_path.setStyleSheet("")
        self.toolButton_plrn_path.setObjectName("toolButton_plrn_path")

        self.label_add_path_2 = QtWidgets.QLabel(self.tab_3)
        self.label_add_path_2.setGeometry(QtCore.QRect(65, 209, 150, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(75)
        self.label_add_path_2.setFont(font)
        self.label_add_path_2.setObjectName("add_path_2")
        self.add_path_2 = QtWidgets.QCheckBox(self.tab_3)
        self.add_path_2.setGeometry(QtCore.QRect(135, 205, 30, 30))

        if plrn_path[0][1] != "":
            self.add_path_2.setChecked(True)
        self.textBrowser_plrn_path_2 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_plrn_path_2.setGeometry(QtCore.QRect(230, 200, 320, 40))
        # self.textBrowser_plrn_path_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.textBrowser_plrn_path_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_2.setObjectName("textBrowser_plrn_path_2")
        self.textBrowser_plrn_path_2.setText(plrn_path[0][1])
        self.textBrowser_plrn_path_2.setEnabled(False)
        self.toolButton_plrn_path_2 = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_plrn_path_2.setGeometry(QtCore.QRect(554, 199, 28, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_plrn_path_2.setFont(font)
        self.toolButton_plrn_path_2.setText("...")
        self.toolButton_plrn_path_2.setStyleSheet("")
        self.toolButton_plrn_path_2.setObjectName("toolButton_plrn_path_2")
        self.toolButton_plrn_path_2.setEnabled(False)
        if self.add_path_2.isChecked() == True:
            self.textBrowser_plrn_path_2.setEnabled(True)
            self.toolButton_plrn_path_2.setEnabled(True)

        self.label_add_path_3 = QtWidgets.QLabel(self.tab_3)
        self.label_add_path_3.setGeometry(QtCore.QRect(65, 259, 150, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(75)
        self.label_add_path_3.setFont(font)
        self.label_add_path_3.setObjectName("add_path_3")
        self.add_path_3 = QtWidgets.QCheckBox(self.tab_3)
        self.add_path_3.setGeometry(QtCore.QRect(135, 255, 30, 30))
        if plrn_path[0][2] != "":
            self.add_path_3.setChecked(True)
        self.textBrowser_plrn_path_3 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_plrn_path_3.setGeometry(QtCore.QRect(230, 250, 320, 40))
        # self.textBrowser_plrn_path_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.textBrowser_plrn_path_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_3.setObjectName("textBrowser_plrn_path_3")
        self.textBrowser_plrn_path_3.setText(plrn_path[0][2])
        self.textBrowser_plrn_path_3.setEnabled(False)
        self.toolButton_plrn_path_3 = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_plrn_path_3.setGeometry(QtCore.QRect(554, 249, 28, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_plrn_path_3.setFont(font)
        self.toolButton_plrn_path_3.setText("...")
        self.toolButton_plrn_path_3.setStyleSheet("")
        self.toolButton_plrn_path_3.setObjectName("toolButton_plrn_path_3")
        self.toolButton_plrn_path_3.setEnabled(False)
        if self.add_path_3.isChecked() == True:
            self.textBrowser_plrn_path_3.setEnabled(True)
            self.toolButton_plrn_path_3.setEnabled(True)

        self.label_worklist_path = QtWidgets.QLabel(self.tab_3)
        self.label_worklist_path.setGeometry(QtCore.QRect(30, 350, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_worklist_path.setFont(font)
        self.label_worklist_path.setObjectName("label_worklist_path")
        self.textBrowser_worklist_path = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_worklist_path.setGeometry(QtCore.QRect(230, 350, 320, 40))
        # self.textBrowser_worklist_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_worklist_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.textBrowser_worklist_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_worklist_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_worklist_path.setObjectName("textBrowser_worklist_path")
        self.textBrowser_worklist_path.setText(bcd_path[0][0])
        self.toolButton_worklist_path = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_worklist_path.setGeometry(QtCore.QRect(554, 349, 28, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_worklist_path.setFont(font)
        self.toolButton_worklist_path.setStyleSheet("")
        self.toolButton_worklist_path.setObjectName("toolButton_worklist_path")

        self.label_inst_path = QtWidgets.QLabel(self.tab_3)
        self.label_inst_path.setGeometry(QtCore.QRect(30, 410, 220, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_inst_path.setFont(font)
        self.label_inst_path.setObjectName("label_inst_path")
        self.textBrowser_inst_path = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_inst_path.setGeometry(QtCore.QRect(230, 410, 320, 40))
        # self.textBrowser_inst_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_inst_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.textBrowser_inst_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textBrowser_inst_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_inst_path.setObjectName("textBrowser_inst_path")
        self.textBrowser_inst_path.setText(bcd_path[0][1])
        self.toolButton_inst_path = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_inst_path.setGeometry(QtCore.QRect(554, 409, 28, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_inst_path.setFont(font)
        self.toolButton_inst_path.setStyleSheet("")
        self.toolButton_inst_path.setObjectName("toolButton_inst_path")

        self.label_use_barcode = QtWidgets.QLabel(self.tab_3)
        self.label_use_barcode.setGeometry(QtCore.QRect(30, 580, 300, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_use_barcode.setFont(font)
        self.label_use_barcode.setObjectName("label_use_barcode")

        self.radioButton_use_bcd_1 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_1.setGeometry(QtCore.QRect(270, 582, 100, 19))
        self.radioButton_use_bcd_1.setObjectName("radioButton_use_bcd_1")
        self.radioButton_use_bcd_1.setChecked(True)
        self.radioButton_use_bcd_2 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_2.setGeometry(QtCore.QRect(270, 620, 100, 19))
        self.radioButton_use_bcd_2.setObjectName("radioButton_use_bcd_2")
        self.radioButton_use_bcd_3 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_3.setGeometry(QtCore.QRect(430, 620, 100, 19))
        self.radioButton_use_bcd_3.setObjectName("radioButton_use_bcd_2")
        self.radioButton_use_bcd_4 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_4.setGeometry(QtCore.QRect(430, 582, 200, 19))
        self.radioButton_use_bcd_4.setObjectName("radioButton_use_bcd_2")

        self.buttonGroup_5 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_5.setObjectName("buttonGroup_5")
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_1)
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_2)
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_3)
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_4)

        self.radioButton_ncpc = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_ncpc.setGeometry(QtCore.QRect(250, 92, 108, 19))
        self.radioButton_ncpc.setObjectName("radioButton_ncpc")
        self.radioButton_ncpc.setChecked(True)
        self.buttonGroup_4 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_4.setObjectName("buttonGroup_4")
        self.buttonGroup_4.addButton(self.radioButton_ncpc)
        self.radioButton_pcnc = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_pcnc.setGeometry(QtCore.QRect(400, 92, 108, 19))
        self.radioButton_pcnc.setObjectName("radioButton_pcnc")
        self.buttonGroup_4.addButton(self.radioButton_pcnc)
        self.tabWidget.addTab(self.tab_3, "")
        self.label_worklist = QtWidgets.QLabel(self.Tab_1)
        self.label_worklist.setGeometry(QtCore.QRect(0, -7, 685, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_worklist.setFont(font)
        self.label_worklist.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.label_worklist.setObjectName("label_worklist")

        self.label_worklist_2 = QtWidgets.QLabel(self.tab_2)
        self.label_worklist_2.setGeometry(QtCore.QRect(0, -7, 685, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_worklist_2.setFont(font)
        self.label_worklist_2.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.label_worklist_2.setObjectName("label_worklist_2")

        self.label_worklist_3 = QtWidgets.QLabel(self.tab_3)
        self.label_worklist_3.setGeometry(QtCore.QRect(0, -7, 685, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_worklist_3.setFont(font)
        self.label_worklist_3.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.label_worklist_3.setObjectName("label_worklist_3")

        self.widget_bar = QtWidgets.QWidget(self)
        self.widget_bar.setGeometry(QtCore.QRect(0, 0, 100, 800))
        self.widget_bar.setStyleSheet("background-color: rgb(3, 56, 125);")
        self.widget_bar.setObjectName("widget_bar")
        self.pushButton_Home = QtWidgets.QPushButton(self.widget_bar)
        self.pushButton_Home.setGeometry(QtCore.QRect(0, 100, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Home.setFont(font)
        self.pushButton_Home.setStyleSheet("background-color: rgb(0, 40, 93);\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border-width: 0px;\n"
                                           "border-color: rgb(15, 123, 255);\n"
                                           "")
        self.pushButton_Home.setObjectName("pushButton_Home")
        self.pushButton_Option = QtWidgets.QPushButton(self.widget_bar)
        self.pushButton_Option.setGeometry(QtCore.QRect(0, 141, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_Option.setFont(font)
        self.pushButton_Option.setStyleSheet("background-color: rgb(0, 40, 93);\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "border-width: 0px;\n"
                                             "border-color: rgb(15, 123, 255);\n"
                                             "")
        self.pushButton_Option.setObjectName("pushButton_Option")
        self.line_1 = QtWidgets.QFrame(self.Tab_1)
        self.line_1.setGeometry(QtCore.QRect(0, 59, 685, 8))
        # self.line_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_1.setLineWidth(1)
        # self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_1.setObjectName("line_1")
        self.line_2 = QtWidgets.QFrame(self.tab_2)
        self.line_2.setGeometry(QtCore.QRect(0, 59, 685, 8))
        # self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_2.setLineWidth(1)
        # self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.tab_3)
        self.line_3.setGeometry(QtCore.QRect(0, 59, 685, 8))
        # self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_3.setLineWidth(1)
        # self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_3.setObjectName("line_3")
        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        # self.setWindowIcon(QtGui.QIcon('C:\WorkList\icon_TCW.png')) # 아이콘
        # self.setWindowIcon(QtGui.QIcon('icon_TCW.png'))
        self.setWindowTitle(_translate("MainWindow", "TCW"))
        self.toolButton_load.setText(_translate("MainWindow", "..."))
        self.toolButton_plrn_path.setText(_translate("MainWindow", "..."))
        self.toolButton_worklist_path.setText(_translate("MainWindow", "..."))
        self.toolButton_inst_path.setText(_translate("MainWindow", "..."))
        item = self.tableWidget_smp.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "WorkList Barcode"))
        item_2 = self.tableWidget_smp.horizontalHeaderItem(1)
        item_2.setText(_translate("MainWindow", "Instrument Barcode"))
        item_4 = self.tableWidget_smp_select.horizontalHeaderItem(0)
        item_4.setText(_translate("MainWindow", "Barcode"))

        self.label_smp_count.setText(_translate("MainWindow", "Sample Count"))
        self.label_smp_bcd.setText(_translate("MainWindow", "Barcode"))
        self.pushButton_next_1.setText(_translate("MainWindow", "Next"))
        self.pushButton_prev_1.setText(_translate("MainWindow", "Prev"))
        self.pushButton_smp_info_1.setText(_translate("MainWindow", "Sample Information"))
        self.pushButton_protocol_info_1.setText(_translate("MainWindow", "Protocol Information"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Tab_1), _translate("MainWindow", "Tab_1"))
        self.label_protocol.setText(_translate("MainWindow", "Protocol"))
        self.pushButton_run.setText(_translate("MainWindow", "Make"))
        self.pushButton_hidden.setText(_translate("MainWindow", ""))
        self.label_tube_type.setText(_translate("MainWindow", "Tube/Plate Type"))
        self.radioButton_bcd_1.setText(_translate("MainWindow", "WorkList Barcode"))
        self.radioButton_bcd_2.setText(_translate("MainWindow", "Instrument Barcode"))
        self.radioButton_tube_1.setText(_translate("MainWindow", "Plate"))
        self.radioButton_tube_2.setText(_translate("MainWindow", "8 - Strip Tube"))
        self.label_cap_type.setText(_translate("MainWindow", "Cap Type"))
        self.radioButton_cap_1.setText(_translate("MainWindow", "Cap"))
        self.radioButton_cap_2.setText(_translate("MainWindow", "Film"))
        self.label_pcr_bcd.setText(_translate("MainWindow", "PCR Reagent Barcode"))
        self.label_extraction_bcd.setText(_translate("MainWindow", "Extraction Reagent Barcode"))

        self.label_testcount.setText(_translate("MainWindow", "Test Count"))
        self.label_extractioncount.setText(_translate("MainWindow", "Extraction Count"))
        self.label_PCR_plate.setText(_translate("MainWindow", "PCR Plate Barcode"))
        self.label_DWP.setText(_translate("MainWindow", "DWP Barcode"))
        self.textBrowser_testcount.setHtml(_translate("MainWindow",
                                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                      "p, li { white-space: pre-wrap; }\n"
                                                      "</style></head><body style=\" font-family:\'Gulim\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                                                      "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton_smp_info_2.setText(_translate("MainWindow", "Sample Information"))
        self.pushButton_protocol_info_2.setText(_translate("MainWindow", "Protocol Information"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab_2"))
        self.label_ctrl_seq.setText(_translate("MainWindow", "PCR Control sequence"))
        self.label_use_barcode.setText(_translate("MainWindow", "PCR Plate / DWP Barcode"))
        self.label_plrn_path.setText(_translate("MainWindow", "plrn File path"))
        self.label_worklist_path.setText(_translate("MainWindow", "WorkList File path"))
        self.label_inst_path.setText(_translate("MainWindow", "Instrument Barcode path"))
        self.label_add_path_2.setText(_translate("MainWindow", "add path"))
        self.label_add_path_3.setText(_translate("MainWindow", "add path"))
        self.radioButton_ncpc.setText(_translate("MainWindow", "NC, PC"))
        self.radioButton_pcnc.setText(_translate("MainWindow", "PC, NC"))
        self.radioButton_use_bcd_1.setText(_translate("MainWindow", "Not used"))
        self.radioButton_use_bcd_2.setText(_translate("MainWindow", "PCR Plate"))
        self.radioButton_use_bcd_3.setText(_translate("MainWindow", "DWP"))
        self.radioButton_use_bcd_4.setText(_translate("MainWindow", "PCR Plate and DWP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Tab_3"))
        self.label_worklist.setText(_translate("MainWindow", " Seegene WorkList"))
        self.label_worklist_2.setText(_translate("MainWindow", " Seegene WorkList"))
        self.label_worklist_3.setText(_translate("MainWindow", " Seegene WorkList"))
        self.pushButton_Home.setText(_translate("MainWindow", "Home"))
        self.pushButton_Option.setText(_translate("MainWindow", "Option"))
        # self.pushButton_copy.setText(_translate("MainWindow", "Copy(All)"))
        # self.pushButton_reload.setText(_translate("MainWindow", "Reload"))
        self.pushButton_smp_ok.setText(_translate("MainWindow", "OK"))
        self.pushButton_confirm.setText(_translate("MainWindow", "Confirm"))
        self.pushButton_cancel.setText(_translate("MainWindow", "Cancel"))



        # Instrument Barcode Setting, Style Sheet
        self.Bcd_list()
        self.tableWidget_smp.resizeColumnsToContents()
        self.tableWidget_smp.resizeRowsToContents()
        self.tableWidget_smp.setStyleSheet("color: black;"
                                           "font: 15px;"
                                           "padding: 1px;"
                                           "header: 10px;"
                                           )
        self.tableWidget_smp.setColumnWidth(0, 240)
        self.tableWidget_smp.setColumnWidth(1, 240)

        # 버튼
        self.pushButton_next_1.clicked.connect(self.page_2)
        self.pushButton_prev_1.clicked.connect(self.page_1)
        self.pushButton_Option.clicked.connect(self.page_option)
        self.pushButton_Home.clicked.connect(self.page_home)
        self.pushButton_smp_ok.clicked.connect(self.Count_smp)
        self.lineEdit_smp_count.returnPressed.connect(self.Count_smp)
        self.toolButton_load.clicked.connect(self.Load_csv)
        self.lineEdit_smp_bcd.returnPressed.connect(self.BCD_smp)
        self.buttonGroup_1.buttonClicked.connect(self.Select_bcd)
        self.buttonGroup_1.buttonClicked.connect(self.Sel_List)
        self.buttonGroup_2.buttonClicked.connect(self.Select_plate)
        self.buttonGroup_3.buttonClicked.connect(self.Select_cap)
        self.buttonGroup_4.buttonClicked.connect(self.Select_ctrl)
        self.buttonGroup_5.buttonClicked.connect(self.Select_use_bcd)
        self.toolButton_plrn_path.clicked.connect(lambda: self.plrn_path(1)) # 기본 plrn 경로
        self.pushButton_run.clicked.connect(self.Run)

        self.lineEdit_pcr_bcd.returnPressed.connect(self.display_test_count)
        self.lineEdit_pcr_bcd.returnPressed.connect(self.check_test_count)
        self.lineEdit_pcr_bcd.returnPressed.connect(self.PCR_Bcd_Check)
        self.pushButton_hidden.clicked.connect(self.Hidden)

        self.lineEdit_Extraction_bcd.returnPressed.connect(self.display_Extraction_count)
        self.lineEdit_Extraction_bcd.returnPressed.connect(self.check_Extraction_count)

        self.add_path_2.clicked.connect(lambda: self.enable_path(2))  # add path 체크
        self.add_path_3.clicked.connect(lambda: self.enable_path(3))
        self.toolButton_plrn_path_2.clicked.connect(lambda: self.plrn_path(2)) # 추가 plrn 경로 2
        self.toolButton_plrn_path_3.clicked.connect(lambda: self.plrn_path(3)) # 추가 plrn 경로 3

        self.toolButton_worklist_path.clicked.connect(lambda: self.plrn_path(4)) # Worklist 바코드 파일 경로
        self.toolButton_inst_path.clicked.connect(lambda: self.plrn_path(5)) # instrument 바코드 파일 경로

        self.pushButton_confirm.clicked.connect(self.Confirm)
        self.pushButton_cancel.clicked.connect(self.Cancel)

        self.lineEdit_PCR_plate.returnPressed.connect(self.focus_DWP)

        self.update_setting()

    # PCR Plate 바코드 스캔시 DWP 바코드로 포커스 이동
    def focus_DWP(self):
        self.lineEdit_DWP.setFocus()

    # 해당 바코드 선택시 배경화면 변경하는 기능
    def Sel_List(self):
        try:
            if self.radioButton_bcd_1.isChecked() == True:
                self.Sel_Signal = 0
            elif self.radioButton_bcd_2.isChecked() == True:
                self.Sel_Signal = 1

            if self.Sel_Signal == 0:
                for i in range(self.tableWidget_smp.rowCount()):
                    self.tableWidget_smp.item(i, 0).setBackground(QtGui.QColor(183, 229, 191))
                    self.tableWidget_smp.item(i, 1).setBackground(QtGui.QColor(255, 255, 255))
            elif self.Sel_Signal == 1:
                for i in range(self.tableWidget_smp.rowCount()):
                    self.tableWidget_smp.item(i, 0).setBackground(QtGui.QColor(255, 255, 255))
                    self.tableWidget_smp.item(i, 1).setBackground(QtGui.QColor(183, 229, 191))
        except Exception as err:
            print(err)

    # confirm 버튼
    def Confirm(self):
        self.tabWidget_bcd.setCurrentIndex(1)
        self.pushButton_smp_ok.setEnabled(False)
        self.lineEdit_smp_count.setEnabled(False)
        self.toolButton_load.setEnabled(False)
        self.pushButton_cancel.setVisible(True)
        self.pushButton_next_1.setEnabled(True)
        self.pushButton_confirm.setVisible(False)
        self.radioButton_bcd_1.setEnabled(False)
        self.radioButton_bcd_2.setEnabled(False)
        self.lineEdit_smp_bcd.setEnabled(True)
        self.lineEdit_smp_bcd.setFocus()
        try:
            self.tableWidget_smp_select.setRowCount(self.tableWidget_smp.rowCount())

            if self.Sel_Signal == 0:
                for i in range(self.tableWidget_smp_select.rowCount()):
                    self.tableWidget_smp_select.setItem(i, 0, QtWidgets.QTableWidgetItem(
                        self.tableWidget_smp.item(i, 0).text()))
            elif self.Sel_Signal == 1:
                for i in range(self.tableWidget_smp_select.rowCount()):
                    self.tableWidget_smp_select.setItem(i, 0, QtWidgets.QTableWidgetItem(
                        self.tableWidget_smp.item(i, 1).text()))
        except Exception as err:
            print(err)
        self.smp_count_1 = self.tableWidget_smp.rowCount()
        self.smp_count_2 = self.tableWidget_smp.rowCount()

    # cancel 버튼
    def Cancel(self):
        self.tabWidget_bcd.setCurrentIndex(0)
        self.pushButton_smp_ok.setEnabled(True)
        self.lineEdit_smp_count.setEnabled(True)
        self.toolButton_load.setEnabled(True)
        self.pushButton_cancel.setVisible(False)
        self.pushButton_next_1.setEnabled(False)
        self.pushButton_confirm.setVisible(True)
        self.radioButton_bcd_1.setEnabled(True)
        self.radioButton_bcd_2.setEnabled(True)
        self.lineEdit_smp_bcd.setEnabled(False)

    # plrn path 추가
    def enable_path(self, i):
        if i == 2:
            if self.add_path_2.isChecked() == True:
                self.textBrowser_plrn_path_2.setEnabled(True)
                self.toolButton_plrn_path_2.setEnabled(True)
            elif self.add_path_2.isChecked() == False:
                self.textBrowser_plrn_path_2.setEnabled(False)
                self.toolButton_plrn_path_2.setEnabled(False)
                self.textBrowser_plrn_path_2.setText("")
                self.DB.set_dir("", 2)
        elif i == 3:
            if self.add_path_3.isChecked() == True:
                self.textBrowser_plrn_path_3.setEnabled(True)
                self.toolButton_plrn_path_3.setEnabled(True)
            elif self.add_path_3.isChecked() == False:
                self.textBrowser_plrn_path_3.setEnabled(False)
                self.toolButton_plrn_path_3.setEnabled(False)
                self.textBrowser_plrn_path_3.setText("")
                self.DB.set_dir("", 3)

    # Hidden 바코드
    def Hidden(self):
        QtWidgets.QMessageBox.information(self, "System", "Hidden Barcode!")
        self.lineEdit_pcr_bcd.setText("Hidden Barcode")
        self.textBrowser_testcount.setText("100")

        self.lineEdit_Extraction_bcd.setText("Hidden Barcode")
        self.textBrowser_extractioncount.setText("96")

        self.check_test_count()
        self.check_Extraction_count()

    # 기본 setting값 설정
    def update_setting(self):
        protocol_name, plate_type, cap_type, ctrl_seq, use_bcd protocol_list = self.DB.load_setting()
        for i in range(len(protocol_list)):,
            self.listWidget_protocol.addItem(protocol_list[i][0])
            if protocol_name == self.listWidget_protocol.item(i).text():
                self.listWidget_protocol.setCurrentItem(self.listWidget_protocol.item(i))

        if plate_type == self.radioButton_tube_1.text():
            self.radioButton_tube_1.setChecked(True)
        else:
            self.radioButton_tube_2.setChecked(True)
            self.radioButton_cap_2.setEnabled(False)

        if cap_type == self.radioButton_cap_1.text():
            self.radioButton_cap_1.setChecked(True)
        else:
            self.radioButton_cap_2.setChecked(True)

        if ctrl_seq == self.radioButton_ncpc.text():
            self.radioButton_ncpc.setChecked(True)
        else:
            self.radioButton_pcnc.setChecked(True)

        if use_bcd == self.radioButton_use_bcd_1.text():
            self.radioButton_use_bcd_1.setChecked(True)
            self.lineEdit_PCR_plate.setEnabled(False)
            self.lineEdit_DWP.setEnabled(False)
        elif use_bcd == self.radioButton_use_bcd_2.text():
            self.radioButton_use_bcd_2.setChecked(True)
            self.lineEdit_PCR_plate.setEnabled(True)
            self.lineEdit_DWP.setEnabled(False)
        elif use_bcd == self.radioButton_use_bcd_3.text():
            self.radioButton_use_bcd_3.setChecked(True)
            self.lineEdit_PCR_plate.setEnabled(False)
            self.lineEdit_DWP.setEnabled(True)
        else:
            self.radioButton_use_bcd_4.setChecked(True)
            self.lineEdit_PCR_plate.setEnabled(True)
            self.lineEdit_DWP.setEnabled(True)

    def page_1(self):
        self.tabWidget.setCurrentIndex(0)

    def page_2(self):
        self.tabWidget.setCurrentIndex(1)

    def page_option(self):
        self.tabWidget.setCurrentIndex(2)

    def page_home(self):
        self.tabWidget.setCurrentIndex(0)

    def encrypt(self, raw):
        temp = 10
        ret = ''
        for char in raw:
            ret += chr(ord(char) + temp)
        return ret

    def decrypt(self, raw):
        ret = ''
        temp = 10
        for char in raw:
            ret += chr(ord(char) - temp)
        return ret

    # PCR 시약 잔량 표시
    def display_test_count(self):
        try:
            pcr_bcd = self.lineEdit_pcr_bcd.text()
            test_cnt = "100"
            test_cnt = self.encrypt(test_cnt)

            pcr_cnt = "5"
            pcr_cnt = self.encrypt(pcr_cnt)

            test_count = self.DB.PCR_test_count(pcr_bcd, test_cnt, pcr_cnt)
            self.textBrowser_testcount.setText(test_count)
        except Exception as err:
            print(err)

    # Extraction 시약 잔량 표시
    def display_Extraction_count(self):
        try:
            Extraction_bcd = self.lineEdit_Extraction_bcd.text()
            extraction_cnt = "96"
            extraction_cnt = self.encrypt(extraction_cnt)

            pcr_cnt = "10"
            pcr_cnt = self.encrypt(pcr_cnt)

            extraction_cnt = self.DB.PCR_Extraction_count(Extraction_bcd, extraction_cnt, pcr_cnt)
            self.textBrowser_extractioncount.setText(extraction_cnt)
        except Exception as err:
            print(err)

    # PCR 시약 잔량과 샘플수 비교
    def check_test_count(self):
        test_count = self.textBrowser_testcount.toPlainText()
        smp_count = self.tableWidget_smp_select.rowCount()
        Extraction_test = self.lineEdit_Extraction_bcd.text()
        if int(test_count) < smp_count:
            QtWidgets.QMessageBox.information(self, "System",
                                              "The remaining amount of PCR reagent is insufficient.\nPlease replace PCR reagent.")
            self.pushButton_run.setEnabled(False)
        elif Extraction_test == "":
            self.pushButton_run.setEnabled(False)
        else:
            self.pushButton_run.setEnabled(True)

    # Extraction 시약 잔량과 샘플수 비교
    def check_Extraction_count(self):
        test_count = self.textBrowser_extractioncount.toPlainText()
        smp_count = self.tableWidget_smp_select.rowCount()
        pcr_test = self.lineEdit_pcr_bcd.text()

        self.lineEdit_pcr_bcd.setPlaceholderText("please Write Barcode")
        self.lineEdit_Extraction_bcd.setPlaceholderText("please Write Barcode")
        if int(test_count) < smp_count:
            QtWidgets.QMessageBox.information(self, "System",
                                              "The remaining amount of Extraction reagent is insufficient.\nPlease replace Extraction reagent.")
            self.pushButton_run.setEnabled(False)
        elif pcr_test == "":
            self.pushButton_run.setEnabled(False)
        else:
            self.pushButton_run.setEnabled(True)


        check_extraction_cnt = self.DB.Sel_Extraction_Use(self.lineEdit_Extraction_bcd.text())
        if check_extraction_cnt == '0':
            QtWidgets.QMessageBox.information(self, "System", "already Use Extraction Reagent Barcode Number 10 times")
            self.lineEdit_Extraction_bcd.setText("")
            self.pushButton_run.setEnabled(False)
            self.textBrowser_extractioncount.setText("")
    # 프로토콜 이름 , Protocol Masking
    def PCR_Bcd_Check(self):
        try:
            temp = self.lineEdit_pcr_bcd.text()
            temp = temp.replace('(', '').replace(')', '')
            temp3 = 0
            PCR_Count = self.DB.Sel_PCR_cnt(temp)
            if PCR_Count == '0':
                QtWidgets.QMessageBox.information(self, "System", "already Use PCR Reagent Barcode Number")
                self.lineEdit_pcr_bcd.setText("")
                self.pushButton_run.setEnabled(False)
                self.textBrowser_testcount.setText("")

            Protocol_Name = self.listWidget_protocol.currentItem().text()

            temp2 = self.DB.Sel_Protocol_Num(Protocol_Name)
            Protocol_check = temp2[0][0]

            if Protocol_check != None and self.lineEdit_pcr_bcd.text() != "":
                temp3 = temp.find(Protocol_check)
            elif Protocol_check == None:
                temp3 = -1

            if temp3 != -1 and self.lineEdit_pcr_bcd.text() != "":
                # temp = temp[:34] + Protocol_check + temp[34:]
                self.lineEdit_pcr_bcd.setText(temp)
                if len(temp) > 50: # 바코드 2번 이상 찍는 경우
                    self.lineEdit_pcr_bcd.setText("")
                    self.pushButton_run.setEnabled(False)
                    self.textBrowser_testcount.setText("")
                    QtWidgets.QMessageBox.information(self, "System",
                                                      "PCR Reagent Barcord over length")

            elif temp3 == -1:
                self.lineEdit_pcr_bcd.setText("")
                self.pushButton_run.setEnabled(False)
                self.textBrowser_testcount.setText("")
                QtWidgets.QMessageBox.information(self, "System", "PCR Reagent Barcord Not Matched with Protocol Name")

        except Exception as err:
            print(err)

    # 라디오버튼 Type(Barcode, Plate, Cap, Control)
    def Select_bcd(self):
        try:
            if self.radioButton_bcd_2.isChecked() == True:
                self.selection_bcd = self.buttonGroup_1.checkedButton().text()
                self.pushButton_confirm.setEnabled(True)
            elif self.tableWidget_smp.item(0, 0).text() != "":
                self.selection_bcd = self.buttonGroup_1.checkedButton().text()
                self.pushButton_confirm.setEnabled(True)
        except:
            self.pushButton_confirm.setEnabled(False)
            self.selection_bcd = self.buttonGroup_1.checkedButton().text()
            QtWidgets.QMessageBox.information(self, "System", "Please enter the count of samples.")

    def Select_plate(self):
        if self.buttonGroup_2.checkedButton().text() == "8 - Strip Tube":
            self.radioButton_cap_2.setEnabled(False)
            self.radioButton_cap_1.setChecked(True)
            self.cap_type = "Cap"
        else:
            self.radioButton_cap_2.setEnabled(True)
        self.plate_type = self.buttonGroup_2.checkedButton().text()

    def Select_cap(self):
        self.cap_type = self.buttonGroup_3.checkedButton().text()

    def Select_ctrl(self):
        self.ctrl_seq = self.buttonGroup_4.checkedButton().text()

    def Select_use_bcd(self):
        self.use_bcd = self.buttonGroup_5.checkedButton().text()
        if self.use_bcd == "Not used":
            self.lineEdit_PCR_plate.setEnabled(False)
            self.lineEdit_DWP.setEnabled(False)
        elif self.use_bcd == "PCR Plate":
            self.lineEdit_PCR_plate.setEnabled(True)
            self.lineEdit_DWP.setEnabled(False)
        elif self.use_bcd == "DWP":
            self.lineEdit_PCR_plate.setEnabled(False)
            self.lineEdit_DWP.setEnabled(True)
        else:
            self.lineEdit_PCR_plate.setEnabled(True)
            self.lineEdit_DWP.setEnabled(True)

    # plrn / WorkList / Inst barcode 파일 경로 설정
    def plrn_path(self, i):
        dir_path = QtWidgets.QFileDialog.getExistingDirectory()
        if dir_path != "":
            if i == 1: # 기본 plrn 경로
                self.textBrowser_plrn_path.setText(dir_path)
                self.DB.set_dir(dir_path, 1)
            elif i == 2: # 추가 plrn 경로 2
                if self.textBrowser_plrn_path.toPlainText() == str(dir_path) or self.textBrowser_plrn_path_3.toPlainText() == str(dir_path): # 이미 지정된 경로이면
                    QtWidgets.QMessageBox.information(self, "System", "This path is already specified. Please change the path.")
                else:
                    self.textBrowser_plrn_path_2.setText(dir_path)
                    self.DB.set_dir(dir_path, 2)
            elif i == 3: # 추가 plrn 경로 3
                if self.textBrowser_plrn_path.toPlainText() == str(dir_path) or self.textBrowser_plrn_path_2.toPlainText() == str(dir_path): # 이미 지정된 경로이면
                    QtWidgets.QMessageBox.information(self, "System", "This path is already specified. Please change the path.")
                else:
                    self.textBrowser_plrn_path_3.setText(dir_path)
                    self.DB.set_dir(dir_path, 3)
            elif i == 4:  # WorkList 파일
                self.textBrowser_worklist_path.setText(dir_path)
                self.DB.set_dir(dir_path, 4)
            elif i == 5:  # Inst 바코드 파일
                self.textBrowser_inst_path.setText(dir_path)
                self.DB.set_dir(dir_path, 5)

    # 샘플 개수 OK
    def Count_smp(self):
        count = self.lineEdit_smp_count.text()
        self.csv_signal = 0
        try:
            if int(count) < 1:
                QtWidgets.QMessageBox.information(self, "System", "Please enter a number of 1 or more.")
                self.lineEdit_smp_count.setText("")
            elif 0 < int(count) < 95:
                self.tableWidget_smp.setRowCount(int(count))
                for i in range(int(count)):
                    self.tableWidget_smp.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
            elif 94 < int(count):
                QtWidgets.QMessageBox.information(self, "System", "The maximum number of samples is 94.")
                self.lineEdit_smp_count.setText("")
        except:
            QtWidgets.QMessageBox.information(self, "System", "Please enter a number.")
            self.lineEdit_smp_count.setText("")
        self.Reload()
        if self.radioButton_bcd_1.isChecked() == True or self.radioButton_bcd_2.isChecked() == True:
            self.Sel_List()
            self.pushButton_confirm.setEnabled(True)


    # Load WorkList
    def Load_csv(self):
        csv_header = []
        temp_1 = []
        csv_item = []
        temp = 0
        load_check = 0

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', f'{self.DB.open_dir_csv()}', 'csv File(*.csv);; csv File(*.csv)')
        if fname[0]:
            self.path_csv = fname[0]
            self.csv_signal = 1
            temp_1 = fname[0].split("/")
            self.worklist_name = temp_1[-1].replace(".csv", "")

            del temp_1[-1]
            self.dir_csv = "/".join(temp_1)
            self.DB.save_dir_csv(self.dir_csv) # 최근에 load한 경로 저장

            csv_file = pd.read_csv(fname[0], encoding='utf-8')
            rdr = csv.reader(csv_file)
            for line in rdr:
                csv_header.append(line)

            load_item = csv_file[csv_header[4]]
            item_val = load_item.values.tolist()

            for i in range(len(item_val)):
                if item_val[i][0] != True:
                    # self.path_csv = ""
                    self.csv_signal = 0
                    QtWidgets.QMessageBox.information(self, "System", "WorkList Csv File Not Corrected")
                    return

            sel_txt = self.DB.Sel_Bcd()
            sel_txt = sel_txt[0][0]
            load_check = sel_txt.find(csv_header[4][0])
            if load_check == -1:
                # self.path_csv = ""
                self.csv_signal = 0
                QtWidgets.QMessageBox.information(self, "System", "WorkList Csv File Not Corrected")
                return

            load_headitem = self.DB.Sel_Protocol()

            for i in range(len(load_headitem)):
                if csv_header[4][0] == load_headitem[i][0]:
                    temp = 1

            if temp == 0:
                QtWidgets.QMessageBox.information(self, "System",
                                                      "Selected protocol does not exist in the database.")
                return

            load_bcd = csv_file['Barcode']
            bcd_val = load_bcd.values.tolist()
            self.tableWidget_smp.setRowCount(len(bcd_val))
            self.lineEdit_smp_count.setText(str(len(bcd_val)))
            for i in range(len(bcd_val)):
                self.tableWidget_smp.setItem(i, 0, QtWidgets.QTableWidgetItem(str(bcd_val[i])))
            self.temp_bcd_list = bcd_val
        else:
            QtWidgets.QMessageBox.information(self, "System", "No file selected.")
        self.Reload()

        if self.radioButton_bcd_1.isChecked() == True or self.radioButton_bcd_2.isChecked() == True:
            self.Sel_List()
            self.pushButton_confirm.setEnabled(True)


    # 샘플 바코드 입력
    def BCD_smp(self):
        if self.smp_count_1 > 0:
            bcd = self.lineEdit_smp_bcd.text()
            self.tableWidget_smp_select.setItem(self.smp_count_2 - self.smp_count_1, 0, QtWidgets.QTableWidgetItem(bcd))
            self.smp_count_1 -= 1
            self.lineEdit_smp_bcd.setText("")
        else:
            self.lineEdit_smp_bcd.setText("")

        if self.radioButton_bcd_1.isChecked() == True or self.radioButton_bcd_2.isChecked() == True:
            self.Sel_List()

    # Run 버튼(DB에 정보 입력, plrn 생성)
    def Run(self):
        try:
            test_count = self.textBrowser_testcount.toPlainText()
            smp_count = self.tableWidget_smp_select.rowCount()
            count = int(test_count) - smp_count
            if self.listWidget_protocol.currentItem() != None and self.lineEdit_pcr_bcd.text() != "" and count >= 0:
                QtWidgets.QMessageBox.information(self, "System", "Please close the door and click 'Run'.")
                smp_bcd = []
                worklist_bcd = []
                date = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
                Protocol_Name = self.listWidget_protocol.currentItem().text()
                rowCount = self.tableWidget_smp_select.rowCount()
                pcr_bcd = self.lineEdit_pcr_bcd.text()
                Extraction_bcd = self.lineEdit_Extraction_bcd.text()
                for i in range(rowCount):
                    smp_bcd.append(self.tableWidget_smp_select.item(i, 0).text())
                id_plrn = self.DB.Input_plrn_data(date, Protocol_Name, rowCount, self.plate_type, self.cap_type,
                                                  self.ctrl_seq, pcr_bcd, self.selection_bcd,
                                                  self.lineEdit_PCR_plate.text(), self.lineEdit_DWP.text(), self.lineEdit_Extraction_bcd.text())
                self.DB.Input_sample_data(smp_bcd, id_plrn)
                self.DB.Use_PCR(pcr_bcd, rowCount)
                self.DB.Use_Extraction_Reagent(Extraction_bcd, rowCount)
                self.DB.make_plrn(id_plrn)
                self.DB.save_Temp(Protocol_Name, self.plate_type, self.cap_type, self.ctrl_seq, self.use_bcd)
                if self.tableWidget_smp.item(0, 0) is not None:
                    for j in range(rowCount):
                        worklist_bcd.append(self.tableWidget_smp.item(j, 0).text())
                self.DB.Create_barcode(id_plrn, worklist_bcd, self.path_csv, self.worklist_name, self.csv_signal)
                self.DB.delete_bcd()
                self.textBrowser_testcount.setText(str(count))

            elif self.listWidget_protocol.currentItem() == None or self.lineEdit_pcr_bcd.text() == "":
                QtWidgets.QMessageBox.information(self, "System", "Please enter all protocol information.")
                self.pushButton_run.setEnabled(False)
            self.signal_close = 1
            self.close()
            temp = self.DB.Sel_Bcd()
            file = temp[0][0]
            os.remove(file)
        except Exception as err:
            print(err)

    # 초기 바코드 리스트 불러오기
    def Bcd_list(self):
        self.bcd_list = []
        self.temp_bcd_list = []

        temp = self.DB.Sel_Bcd()
        file = open(temp[0][0], "r", encoding="utf8")
        # 현재 비교할 텍스트 파일
        lines = file.readlines()  # list 형태로 읽어옴
        lines.pop(0)
        cnt = 0
        count = []
        background = []

        self.tableWidget_smp.setRowCount(len(lines))

        for i in range(len(lines)):
            self.bcd_list.append("")

        for line in lines:
            if not line:
                break

            temp3 = lines[cnt].split()

            if temp3[2] == self.bcd_list[cnt]:
                count.append("O")

            elif temp3[2] != self.bcd_list[cnt]:
                count.append("X")
                background.append(cnt)

            self.tableWidget_smp.setItem(cnt, 1, QtWidgets.QTableWidgetItem(str(temp3[2])))
            self.tableWidget_smp.setRowHeight(cnt, 60)
            cnt += 1
        file.close()
        for i in range(len(background)):
            self.tableWidget_smp.item(background[i], 1).setBackground(QtGui.QColor(255, 208, 208))

    # 바코드 갱신기능
    def Reload(self):
        temp = self.DB.Sel_Bcd()
        file = open(temp[0][0], "r", encoding="utf8")  # 현재 비교할 텍스트 파일
        lines = file.readlines()  # list 형태로 읽어옴
        lines.pop(0)  # Header는 제외 (CODE)
        cnt = 0
        check = 0
        count = []
        background = []
        self.temp_bcd_list = []
        try:
            if len(lines) > int(self.lineEdit_smp_count.text()):  # Sample Count 수보다 텍스트파일 Barcode가 많을 경우
                self.tableWidget_smp.setRowCount(int(self.lineEdit_smp_count.text()))
            else:
                self.tableWidget_smp.setRowCount(len(lines))  # 같거나 작을경우는 텍스트파일 Barcode 기준으로 행 세팅

            if len(lines) == int(self.lineEdit_smp_count.text()):  # 같거나 작거나 많거나 Sampler Count에 적힌 수만큼 임시 바코드리트에 넣어줌
                for i in range(0, int(self.lineEdit_smp_count.text())):
                    self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())
            elif len(lines) < int(self.lineEdit_smp_count.text()):
                for i in range(len(lines)):
                    self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())
                QtWidgets.QMessageBox.information(self, "System", "Too Much Samples Count Please confirm Sample.")
            elif len(lines) > int(self.lineEdit_smp_count.text()):
                for i in range(0, int(self.lineEdit_smp_count.text())):
                    self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())
        except Exception as err:
            print(err)

        try:
            for line in lines:  # 텍스트파일 라인수만큼 반복
                if not line:  # 라인이 없을경우 반복문 break
                    break

                temp3 = lines[cnt].split()  # 한 줄을 쪼갬

                if temp3[2] == self.temp_bcd_list[cnt]:  # 한 라인의 Code와 임시 바코드와 비교

                    # print("{0}번째 해당 줄이 같습니다.".format(cnt))
                    # print(temp3[2])
                    count.append("O")  # Check List

                elif temp3[2] != self.temp_bcd_list[cnt]:
                    # print("{0}번째 해당 줄이 다릅니다.".format(2))
                    # print("1번 리스트 : " + temp3[2])
                    # print("2번 리스트 : " + Ui_MainWindow.temp_bcd_list[cnt])
                    count.append("X")
                    background.append(cnt)  # 현재 행에 대한 BackGround List
                # 첫번째 컬럼 text를 임시 바코드리스트에 있는 값으로 세팅
                # 두번째 컬럼은 텍스트파일의 값으로 세팅(cnt를 통해서 각 행에 대한 값으로 세팅)
                self.tableWidget_smp.setItem(cnt, 0, QtWidgets.QTableWidgetItem(str(self.temp_bcd_list[cnt])))
                self.tableWidget_smp.setItem(cnt, 1, QtWidgets.QTableWidgetItem(str(temp3[2])))

                cnt += 1
                if cnt >= int(self.lineEdit_smp_count.text()):
                    break

            # 텍스트파일의 라인수보다 샘플카운트가 크거나 같다면 임시바코드리스트에 라인수만큼 넣어줌.
            if len(lines) <= int(self.lineEdit_smp_count.text()):
                for i in range(len(lines)):
                    self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())
            # 텍스트파일의 라인수가 샘플카운트가 작아도 임시바코드리스트에 라인수만큼 넣어줌.
            # elif len(lines) > int(self.lineEdit_smp_count.text()):
            #     for i in range(len(self.temp_bcd_list)):
            #         self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())

            # 비교했을때 다른경우에만 Background에 넣어주었고, Background 리스트 수만큼 Backgroun Color 세팅
            for i in range(len(background)):
                self.tableWidget_smp.item(background[i], 0).setBackground(QtGui.QColor(255, 208, 208))
                self.tableWidget_smp.item(background[i], 1).setBackground(QtGui.QColor(255, 208, 208))
        except Exception as err:
            print(err)

        try:
            if len(lines) > int(self.lineEdit_smp_count.text()):
                cnt = 0
                for line in lines:
                    temp3 = lines[cnt].split()
                    if temp3[2] == self.temp_bcd_list[cnt]:
                        # print("{0}번째 해당 줄이 같습니다.".format(cnt))
                        # print(temp3[2])
                        count.append("O")

                    elif temp3[2] != self.temp_bcd_list[cnt]:
                        # print("{0}번째 해당 줄이 다릅니다.".format(2))
                        # print("1번 리스트 : " + temp3[2])
                        # print("2번 리스트 : " + Ui_MainWindow.temp_bcd_list[cnt])
                        count.append("X")
                        background.append(cnt)

                    self.tableWidget_smp.setItem(cnt, 0,
                                                 QtWidgets.QTableWidgetItem(str(self.temp_bcd_list[cnt])))
                    self.tableWidget_smp.setItem(cnt, 1, QtWidgets.QTableWidgetItem(str(temp3[2])))

                    cnt += 1

                    if cnt >= int(self.lineEdit_smp_count.text()):
                        break
                if len(lines) <= int(self.lineEdit_smp_count.text()):
                    for i in range(len(lines)):
                        self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())

                elif len(lines) > int(self.lineEdit_smp_count.text()):
                    for i in range(int(self.lineEdit_smp_count.text())):
                        self.temp_bcd_list.append((self.tableWidget_smp.item(i, 0)).text())

                for i in range(len(background)):
                    self.tableWidget_smp.item(background[i], 0).setBackground(QtGui.QColor(255, 208, 208))
                    self.tableWidget_smp.item(background[i], 1).setBackground(QtGui.QColor(255, 208, 208))
        except Exception as err:
            print(err)

        if len(background) == 0:
            check = 1

        if check == 1:
            # self.pushButton_next_1.setEnabled(True)
            pass
        else:
            self.pushButton_next_1.setEnabled(False)
        file.close()

    def closeEvent(self, event):
        try:
            if self.signal_close == 0:
                reply = QtWidgets.QMessageBox.question(self, "System",
                                                   "Are you sure to quit?", QtWidgets.QMessageBox.StandardButtons.Yes |
                                                   QtWidgets.QMessageBox.StandardButtons.No, QtWidgets.QMessageBox.StandardButtons.No)

                if reply == QtWidgets.QMessageBox.StandardButtons.Yes:
                    event.accept()
                else:
                    event.ignore()
        except Exception as err:
            print(err)