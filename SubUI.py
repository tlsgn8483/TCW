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
    Control_Count = 0
    check_pcr_masking = False
    check_pcr_reagent = False
    check_extraction_reagent = False

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        plrn_path, bcd_path = self.DB.display_path()
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("TCW")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        self.resize(770, 800)
        self.tabWidget = QtWidgets.QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(97, -20, 680, 825))
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
        self.toolButton_load.setGeometry(QtCore.QRect(233, 100, 30, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_load.setFont(font)
        self.toolButton_load.setStyleSheet("")
        self.toolButton_load.setObjectName("toolButton_load")

        self.toolButton_load_txt = QtWidgets.QToolButton(self.Tab_1)
        self.toolButton_load_txt.setGeometry(QtCore.QRect(265, 100, 30, 22))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_load_txt.setFont(font)
        self.toolButton_load_txt.setStyleSheet("")
        self.toolButton_load_txt.setObjectName("toolButton_load_txt")

        self.tabWidget_bcd = QtWidgets.QTabWidget(self.Tab_1)
        self.tabWidget_bcd.setGeometry(QtCore.QRect(70, 170, 530, 560))
        self.tabWidget_bcd.setObjectName("tabWidget_bcd")
        self.Tab_bcd_1 = QtWidgets.QWidget()
        self.Tab_bcd_1.setObjectName("Tab_bcd_1")
        self.Tab_bcd_2 = QtWidgets.QWidget()
        self.Tab_bcd_2.setObjectName("Tab_bcd_2")
        self.tabWidget_bcd.tabBar().hide()

        self.tableWidget_smp_select = QtWidgets.QTableWidget(self.Tab_bcd_2)
        self.tableWidget_smp_select.setGeometry(QtCore.QRect(-1, -1, 528, 560))
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
        self.pushButton_confirm.setGeometry(QtCore.QRect(490, 136, 71, 28))
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.pushButton_confirm.setEnabled(False)

        self.pushButton_cancel = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_cancel.setGeometry(QtCore.QRect(490, 136, 71, 28))
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.pushButton_cancel.setVisible(False)

        self.tableWidget_smp = QtWidgets.QTableWidget(self.Tab_bcd_1)
        self.tableWidget_smp.setGeometry(QtCore.QRect(-1, -1, 528, 560))
        self.tableWidget_smp.setObjectName("tableWidget_smp")
        self.tableWidget_smp.setColumnCount(2)
        self.tableWidget_smp.setRowCount(0)
        self.tableWidget_smp.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)
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
        self.label_smp_bcd.setGeometry(QtCore.QRect(310, 100, 71, 21))
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
        self.pushButton_smp_info_1 = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_smp_info_1.setGeometry(QtCore.QRect(-1, 60, 325, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_smp_info_1.setFont(font)
        self.pushButton_smp_info_1.setStyleSheet("border-style: outset;\n"
                                                 "background-color: rgb(225, 225, 225);\n"
                                                 "border-width: 0px;")
        self.pushButton_smp_info_1.setObjectName("pushButton_smp_info_1")
        self.pushButton_protocol_info_1 = QtWidgets.QPushButton(self.Tab_1)
        self.pushButton_protocol_info_1.setGeometry(QtCore.QRect(324, 60, 360, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.pushButton_protocol_info_1.setFont(font)
        self.pushButton_protocol_info_1.setStyleSheet("border-style: outset;\n"
                                                      "background-color: rgb(225, 225, 225);\n"
                                                      "color: rgb(150, 150, 150);\n"
                                                      "border-width: 0px;")
        self.pushButton_protocol_info_1.setObjectName("pushButton_protocol_info_1")
        self.lineEdit_smp_bcd.raise_()
        self.toolButton_load.raise_()
        self.toolButton_load_txt.raise_()
        self.tableWidget_smp.raise_()
        self.label_smp_count.raise_()
        self.lineEdit_smp_count.raise_()
        self.label_smp_bcd.raise_()
        self.pushButton_next_1.raise_()
        self.pushButton_smp_info_1.raise_()
        self.pushButton_protocol_info_1.raise_()
        self.tabWidget.addTab(self.Tab_1, "")
        self.tabWidget_bcd.addTab(self.Tab_bcd_1, "")
        self.tabWidget_bcd.addTab(self.Tab_bcd_2, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_protocol = QtWidgets.QLabel(self.tab_2)
        self.label_protocol.setGeometry(QtCore.QRect(30, 120, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_protocol.setFont(font)
        self.label_protocol.setObjectName("label_protocol")
        self.pushButton_prev_1 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_prev_1.setGeometry(QtCore.QRect(20, 750, 93, 28))
        self.pushButton_prev_1.setObjectName("pushButton_prev_1")
        self.listWidget_protocol = QtWidgets.QListWidget(self.tab_2)
        self.listWidget_protocol.setGeometry(QtCore.QRect(110, 120, 470, 110))
        self.listWidget_protocol.setObjectName("listWidget_protocol")
        self.listWidget_protocol.setEnabled(False)
        self.pushButton_run = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_run.setGeometry(QtCore.QRect(530, 750, 93, 28))
        self.pushButton_run.setObjectName("pushButton_run")
        self.pushButton_run.setEnabled(False)

        self.pushButton_hidden = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_hidden.setGeometry(QtCore.QRect(245, 408, 15, 15))
        self.pushButton_hidden.setObjectName("pushButton_hidden")
        self.pushButton_hidden.setStyleSheet("border-style: outset;\n"
                                             "border-width: 1px;\n"
                                             "border-color: black;")
        self.label_tube_type = QtWidgets.QLabel(self.tab_2)
        self.label_tube_type.setGeometry(QtCore.QRect(40, 260, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_tube_type.setFont(font)
        self.label_tube_type.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_tube_type.setObjectName("label_tube_type")
        self.radioButton_tube_1 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_tube_1.setGeometry(QtCore.QRect(260, 260, 110, 20))
        self.radioButton_tube_1.setObjectName("radioButton_tube_1")
        self.buttonGroup_2 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_2.setObjectName("buttonGroup_2")
        self.buttonGroup_2.addButton(self.radioButton_tube_1)
        self.radioButton_tube_2 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_tube_2.setGeometry(QtCore.QRect(390, 260, 110, 20))
        self.radioButton_tube_2.setObjectName("radioButton_tube_2")
        self.buttonGroup_2.addButton(self.radioButton_tube_2)
        self.label_cap_type = QtWidgets.QLabel(self.tab_2)
        self.label_cap_type.setGeometry(QtCore.QRect(40, 300, 200, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_cap_type.setFont(font)
        self.label_cap_type.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_cap_type.setObjectName("label_cap_type")
        self.radioButton_cap_1 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_cap_1.setGeometry(QtCore.QRect(260, 300, 110, 20))
        self.radioButton_cap_1.setObjectName("radioButton_cap_1")
        self.buttonGroup_3 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_3.setObjectName("buttonGroup_3")
        self.buttonGroup_3.addButton(self.radioButton_cap_1)
        self.radioButton_cap_2 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_cap_2.setGeometry(QtCore.QRect(390, 300, 110, 20))
        self.radioButton_cap_2.setObjectName("radioButton_cap_2")
        self.buttonGroup_3.addButton(self.radioButton_cap_2)
        self.lineEdit_pcr_bcd = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_pcr_bcd.setGeometry(QtCore.QRect(260, 406, 250, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_pcr_bcd.setFont(font)
        self.lineEdit_pcr_bcd.setStyleSheet("")
        self.lineEdit_pcr_bcd.setObjectName("lineEdit_pcr_bcd")

        self.lineEdit_Extraction_bcd = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_Extraction_bcd.setGeometry(QtCore.QRect(260, 506, 250, 20))
        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_Extraction_bcd.setFont(font)
        self.lineEdit_Extraction_bcd.setStyleSheet("")
        self.lineEdit_Extraction_bcd.setObjectName("lineEdit_Extraction_bcd")

        self.label_pcr_bcd = QtWidgets.QLabel(self.tab_2)
        self.label_pcr_bcd.setGeometry(QtCore.QRect(40, 400, 200, 30))

        self.label_extraction_bcd = QtWidgets.QLabel(self.tab_2)
        self.label_extraction_bcd.setGeometry(QtCore.QRect(40, 500, 200, 30))

        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_pcr_bcd.setFont(font)
        self.label_pcr_bcd.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_pcr_bcd.setObjectName("label_pcr_bcd")

        self.label_extraction_bcd.setFont(font)
        self.label_extraction_bcd.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_extraction_bcd.setObjectName("label_extraction_bcd")
        self.label_testcount = QtWidgets.QLabel(self.tab_2)
        self.label_testcount.setGeometry(QtCore.QRect(40, 434, 200, 30))
        # self.label_extractioncount = QtWidgets.QLabel(self.tab_2)
        # self.label_extractioncount.setGeometry(QtCore.QRect(40, 534, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_testcount.setFont(font)
        self.label_testcount.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_testcount.setObjectName("label_testcount")

        # self.label_extractioncount.setFont(font)
        # self.label_extractioncount.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        # self.label_extractioncount.setObjectName("label_extractioncount")

        self.label_PCR_plate = QtWidgets.QLabel(self.tab_2)
        self.label_PCR_plate.setGeometry(QtCore.QRect(40, 600, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_PCR_plate.setFont(font)
        self.label_PCR_plate.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_PCR_plate.setObjectName("label_PCR_plate")
        self.lineEdit_PCR_plate = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_PCR_plate.setGeometry(QtCore.QRect(260, 606, 250, 20))

        font = QtGui.QFont()
        font.setKerning(True)
        self.lineEdit_PCR_plate.setFont(font)
        self.lineEdit_PCR_plate.setStyleSheet("")
        self.lineEdit_PCR_plate.setObjectName("lineEdit_PCR_plate")

        self.label_DWP = QtWidgets.QLabel(self.tab_2)
        self.label_DWP.setGeometry(QtCore.QRect(40, 634, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_DWP.setFont(font)
        self.label_DWP.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_DWP.setObjectName("label_DWP")
        self.lineEdit_DWP = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_DWP.setGeometry(QtCore.QRect(260, 640, 250, 20))
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
        self.textBrowser_testcount.setGeometry(QtCore.QRect(260, 440, 50, 20))

        # self.textBrowser_extractioncount = QtWidgets.QTextBrowser(self.tab_2)
        # self.textBrowser_extractioncount.setGeometry(QtCore.QRect(260, 540, 50, 20))

        self.textBrowser_testcount.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_testcount.setObjectName("textBrowser_testcount")

        # self.textBrowser_extractioncount.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.textBrowser_extractioncount.setObjectName("textBrowser_extractioncount")

        self.pushButton_smp_info_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_smp_info_2.setGeometry(QtCore.QRect(-1, 60, 325, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        self.pushButton_smp_info_2.setFont(font)
        self.pushButton_smp_info_2.setStyleSheet("border-style: outset;\n"
                                                 "background-color: rgb(225, 225, 225);\n"
                                                 "color : rgb(150, 150, 150);\n"
                                                 "border-width: 0px;")
        self.pushButton_smp_info_2.setObjectName("pushButton_smp_info_2")
        self.pushButton_protocol_info_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_protocol_info_2.setGeometry(QtCore.QRect(324, 60, 360, 29))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_protocol_info_2.setFont(font)
        self.pushButton_protocol_info_2.setStyleSheet("border-style: outset;\n"
                                                      "background-color: rgb(225, 225, 225);\n"
                                                      "border-width: 0px;")
        self.pushButton_protocol_info_2.setObjectName("pushButton_protocol_info_2")

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
        # self.label_extractioncount.raise_()
        self.textBrowser_testcount.raise_()
        # self.textBrowser_extractioncount.raise_()
        self.pushButton_smp_info_2.raise_()
        self.pushButton_protocol_info_2.raise_()
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_ctrl_seq = QtWidgets.QLabel(self.tab_3)
        self.label_ctrl_seq.setGeometry(QtCore.QRect(50, 110, 180, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ctrl_seq.setFont(font)
        self.label_ctrl_seq.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_ctrl_seq.setObjectName("label_ctrl_seq")

        self.label_plrn_path = QtWidgets.QLabel(self.tab_3)
        self.label_plrn_path.setGeometry(QtCore.QRect(50, 185, 180, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_plrn_path.setFont(font)
        self.label_plrn_path.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_plrn_path.setObjectName("label_plrn_path")
        self.textBrowser_plrn_path = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_plrn_path.setGeometry(QtCore.QRect(250, 185, 320, 50))
        self.textBrowser_plrn_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path.setObjectName("textBrowser_plrn_path")
        self.textBrowser_plrn_path.setText(plrn_path[0][0])
        self.toolButton_plrn_path = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_plrn_path.setGeometry(QtCore.QRect(580, 185, 30, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_plrn_path.setFont(font)
        self.toolButton_plrn_path.setObjectName("toolButton_plrn_path")

        self.label_add_path_2 = QtWidgets.QLabel(self.tab_3)
        self.label_add_path_2.setGeometry(QtCore.QRect(140, 270, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(75)
        self.label_add_path_2.setFont(font)
        self.label_add_path_2.setObjectName("label_add_path_2")
        self.add_path_2 = QtWidgets.QCheckBox(self.tab_3)
        self.add_path_2.setGeometry(QtCore.QRect(220, 265, 20, 31))

        if plrn_path[0][1] != "":
            self.add_path_2.setChecked(True)
        self.textBrowser_plrn_path_2 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_plrn_path_2.setGeometry(QtCore.QRect(250, 255, 320, 50))
        self.textBrowser_plrn_path_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_2.setObjectName("textBrowser_plrn_path_2")
        self.textBrowser_plrn_path_2.setText(plrn_path[0][1])
        self.textBrowser_plrn_path_2.setEnabled(False)
        self.toolButton_plrn_path_2 = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_plrn_path_2.setGeometry(QtCore.QRect(580, 255, 30, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_plrn_path_2.setFont(font)
        self.toolButton_plrn_path_2.setText("...")
        self.toolButton_plrn_path_2.setObjectName("toolButton_plrn_path_2")
        self.toolButton_plrn_path_2.setEnabled(False)
        if self.add_path_2.isChecked() == True:
            self.textBrowser_plrn_path_2.setEnabled(True)
            self.toolButton_plrn_path_2.setEnabled(True)

        self.label_add_path_3 = QtWidgets.QLabel(self.tab_3)
        self.label_add_path_3.setGeometry(QtCore.QRect(140, 340, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(75)
        self.label_add_path_3.setFont(font)
        self.label_add_path_3.setObjectName("label_add_path_3")
        self.add_path_3 = QtWidgets.QCheckBox(self.tab_3)
        self.add_path_3.setGeometry(QtCore.QRect(220, 335, 20, 31))
        if plrn_path[0][2] != "":
            self.add_path_3.setChecked(True)
        self.textBrowser_plrn_path_3 = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_plrn_path_3.setGeometry(QtCore.QRect(250, 325, 320, 50))
        self.textBrowser_plrn_path_3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_plrn_path_3.setObjectName("textBrowser_plrn_path_3")
        self.textBrowser_plrn_path_3.setText(plrn_path[0][2])
        self.textBrowser_plrn_path_3.setEnabled(False)
        self.toolButton_plrn_path_3 = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_plrn_path_3.setGeometry(QtCore.QRect(580, 325, 30, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_plrn_path_3.setFont(font)
        self.toolButton_plrn_path_3.setText("...")
        self.toolButton_plrn_path_3.setObjectName("toolButton_plrn_path_3")
        self.toolButton_plrn_path_3.setEnabled(False)
        if self.add_path_3.isChecked() == True:
            self.textBrowser_plrn_path_3.setEnabled(True)
            self.toolButton_plrn_path_3.setEnabled(True)

        self.label_worklist_path = QtWidgets.QLabel(self.tab_3)
        self.label_worklist_path.setGeometry(QtCore.QRect(50, 435, 180, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_worklist_path.setFont(font)
        self.label_worklist_path.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignTrailing | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_worklist_path.setObjectName("label_worklist_path")
        self.textBrowser_worklist_path = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_worklist_path.setGeometry(QtCore.QRect(250, 435, 320, 50))
        self.textBrowser_worklist_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_worklist_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_worklist_path.setObjectName("textBrowser_worklist_path")
        self.textBrowser_worklist_path.setText(bcd_path[0][0])
        self.toolButton_worklist_path = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_worklist_path.setGeometry(QtCore.QRect(580, 435, 31, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_worklist_path.setFont(font)
        self.toolButton_worklist_path.setStyleSheet("")
        self.toolButton_worklist_path.setObjectName("toolButton_worklist_path")

        self.label_inst_path = QtWidgets.QLabel(self.tab_3)
        self.label_inst_path.setGeometry(QtCore.QRect(50, 505, 180, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_inst_path.setFont(font)
        self.label_inst_path.setObjectName("label_inst_path")
        self.textBrowser_inst_path = QtWidgets.QTextBrowser(self.tab_3)
        self.textBrowser_inst_path.setGeometry(QtCore.QRect(250, 505, 320, 50))
        self.textBrowser_inst_path.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_inst_path.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.textBrowser_inst_path.setObjectName("textBrowser_inst_path")
        self.textBrowser_inst_path.setText(bcd_path[0][1])
        self.toolButton_inst_path = QtWidgets.QToolButton(self.tab_3)
        self.toolButton_inst_path.setGeometry(QtCore.QRect(580, 505, 31, 23))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolButton_inst_path.setFont(font)
        self.toolButton_inst_path.setStyleSheet("")
        self.toolButton_inst_path.setObjectName("toolButton_inst_path")

        self.label_use_barcode = QtWidgets.QLabel(self.tab_3)
        self.label_use_barcode.setGeometry(QtCore.QRect(40, 635, 200, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_use_barcode.setFont(font)
        self.label_use_barcode.setObjectName("label_use_barcode")

        self.radioButton_use_bcd_1 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_1.setGeometry(QtCore.QRect(260, 635, 140, 16))
        self.radioButton_use_bcd_1.setObjectName("radioButton_use_bcd_1")
        self.radioButton_use_bcd_1.setChecked(True)
        self.radioButton_use_bcd_2 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_2.setGeometry(QtCore.QRect(410, 635, 140, 16))
        self.radioButton_use_bcd_2.setObjectName("radioButton_use_bcd_2")
        self.radioButton_use_bcd_3 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_3.setGeometry(QtCore.QRect(260, 675, 140, 16))
        self.radioButton_use_bcd_3.setObjectName("radioButton_use_bcd_2")
        self.radioButton_use_bcd_4 = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_use_bcd_4.setGeometry(QtCore.QRect(410, 675, 140, 16))
        self.radioButton_use_bcd_4.setObjectName("radioButton_use_bcd_2")

        self.buttonGroup_5 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_5.setObjectName("buttonGroup_5")
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_1)
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_2)
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_3)
        self.buttonGroup_5.addButton(self.radioButton_use_bcd_4)

        self.radioButton_ncpc = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_ncpc.setGeometry(QtCore.QRect(260, 110, 108, 19))
        self.radioButton_ncpc.setObjectName("radioButton_ncpc")
        self.radioButton_ncpc.setChecked(True)
        self.buttonGroup_4 = QtWidgets.QButtonGroup(self)
        self.buttonGroup_4.setObjectName("buttonGroup_4")
        self.buttonGroup_4.addButton(self.radioButton_ncpc)
        self.radioButton_pcnc = QtWidgets.QRadioButton(self.tab_3)
        self.radioButton_pcnc.setGeometry(QtCore.QRect(400, 110, 108, 19))
        self.radioButton_pcnc.setObjectName("radioButton_pcnc")
        self.buttonGroup_4.addButton(self.radioButton_pcnc)
        self.tabWidget.addTab(self.tab_3, "")
        self.label_worklist = QtWidgets.QLabel(self)
        self.label_worklist.setGeometry(QtCore.QRect(100, -7, 685, 71))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_worklist.setFont(font)
        self.label_worklist.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.label_worklist.setObjectName("label_worklist")

        self.widget_bar = QtWidgets.QWidget(self)
        self.widget_bar.setGeometry(QtCore.QRect(0, 0, 100, 820))
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
                                           "border-color: rgb(15, 123, 255);")
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
                                             "border-color: rgb(15, 123, 255);")
        self.pushButton_Option.setObjectName("pushButton_Option")
        self.line_1 = QtWidgets.QFrame(self)
        self.line_1.setGeometry(QtCore.QRect(100, 59, 685, 8))
        self.line_1.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_1.setLineWidth(1)
        self.line_1.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_1.setObjectName("line_1")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(100, 90, 685, 8))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.line_2.setLineWidth(1)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line_2.setObjectName("line_2")
        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.center_line = QtWidgets.QFrame(self)
        self.center_line.setGeometry(QtCore.QRect(400, 64, 60, 30))
        self.center_line.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.center_line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.center_line.setObjectName("center_line")

        self.label_topbar = QtWidgets.QLabel(self.tab_3)
        self.label_topbar.setGeometry(QtCore.QRect(0, 60, 670, 30))
        self.label_topbar.setStyleSheet("background-color: rgb(225, 225, 225);")
        self.label_topbar.setText("")
        self.label_topbar.setObjectName("label_topbar")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "TCW"))
        self.toolButton_load.setText(_translate("MainWindow", "csv"))
        self.toolButton_load_txt.setText(_translate("MainWindow", "txt"))
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
        # self.label_extractioncount.setText(_translate("MainWindow", "Extraction Count"))
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
        self.pushButton_Home.setText(_translate("MainWindow", "Home"))
        self.pushButton_Option.setText(_translate("MainWindow", "Option"))
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
        self.tableWidget_smp.setColumnWidth(0, 249)
        self.tableWidget_smp.setColumnWidth(1, 249)

        # 버튼
        self.pushButton_next_1.clicked.connect(self.page_2)
        self.pushButton_prev_1.clicked.connect(self.page_1)
        self.pushButton_Option.clicked.connect(self.page_option)
        self.pushButton_Home.clicked.connect(self.page_home)
        self.pushButton_smp_ok.clicked.connect(self.Count_smp)
        self.lineEdit_smp_count.returnPressed.connect(self.Count_smp)
        self.toolButton_load.clicked.connect(self.Load_csv)
        self.toolButton_load_txt.clicked.connect(self.Load_Barcode_txt)
        self.lineEdit_smp_bcd.returnPressed.connect(self.BCD_smp)
        self.buttonGroup_1.buttonClicked.connect(self.Select_bcd)
        self.buttonGroup_1.buttonClicked.connect(self.Sel_List)
        self.buttonGroup_2.buttonClicked.connect(self.Select_plate)
        self.buttonGroup_3.buttonClicked.connect(self.Select_cap)
        self.buttonGroup_4.buttonClicked.connect(self.Select_ctrl)
        self.buttonGroup_5.buttonClicked.connect(self.Select_use_bcd)
        self.toolButton_plrn_path.clicked.connect(lambda: self.plrn_path(1))  # 기본 plrn 경로
        self.pushButton_run.clicked.connect(self.Run)

        self.lineEdit_pcr_bcd.returnPressed.connect(self.display_test_count)
        self.lineEdit_pcr_bcd.returnPressed.connect(self.PCR_Bcd_Check)
        self.lineEdit_pcr_bcd.returnPressed.connect(self.check_test_count)
        self.pushButton_hidden.clicked.connect(self.Hidden)

        # self.lineEdit_Extraction_bcd.returnPressed.connect(self.display_Extraction_count)
        self.lineEdit_Extraction_bcd.returnPressed.connect(self.check_Extraction_count)

        self.add_path_2.clicked.connect(lambda: self.enable_path(2))  # add path 체크
        self.add_path_3.clicked.connect(lambda: self.enable_path(3))
        self.toolButton_plrn_path_2.clicked.connect(lambda: self.plrn_path(2))  # 추가 plrn 경로 2
        self.toolButton_plrn_path_3.clicked.connect(lambda: self.plrn_path(3))  # 추가 plrn 경로 3

        self.toolButton_worklist_path.clicked.connect(lambda: self.plrn_path(4))  # Worklist 바코드 파일 경로
        self.toolButton_inst_path.clicked.connect(lambda: self.plrn_path(5))  # instrument 바코드 파일 경로

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
        self.toolButton_load_txt.setEnabled(False)
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
        self.toolButton_load_txt.setEnabled(True)
        self.pushButton_cancel.setVisible(False)
        self.pushButton_next_1.setEnabled(False)
        self.pushButton_confirm.setVisible(True)
        self.radioButton_bcd_1.setEnabled(True)
        self.radioButton_bcd_2.setEnabled(True)
        self.lineEdit_smp_bcd.setEnabled(False)

    # plrn path 추가
    def enable_path(self, i):
        if i == 2:
            if self.add_path_2.isChecked():
                self.textBrowser_plrn_path_2.setEnabled(True)
                self.toolButton_plrn_path_2.setEnabled(True)
            elif not self.add_path_2.isChecked():
                self.textBrowser_plrn_path_2.setEnabled(False)
                self.toolButton_plrn_path_2.setEnabled(False)
                self.textBrowser_plrn_path_2.setText("")
                self.DB.set_dir("", 2)
        elif i == 3:
            if self.add_path_3.isChecked():
                self.textBrowser_plrn_path_3.setEnabled(True)
                self.toolButton_plrn_path_3.setEnabled(True)
            elif not self.add_path_3.isChecked():
                self.textBrowser_plrn_path_3.setEnabled(False)
                self.toolButton_plrn_path_3.setEnabled(False)
                self.textBrowser_plrn_path_3.setText("")
                self.DB.set_dir("", 3)

    # Hidden 바코드
    def Hidden(self):
        try:
            QtWidgets.QMessageBox.information(self, "System", "Hidden Barcode!")
            self.lineEdit_pcr_bcd.setText("Hidden Barcode")
            self.textBrowser_testcount.setText("100")
            self.lineEdit_Extraction_bcd.setText("Hidden Barcode")

            self.check_pcr_masking = True
            self.check_pcr_reagent = True
            self.check_extraction_reagent = True

            self.check_run()

        except Exception as err:
            print(err)
            print("Hidden 에러")


    # 기본 setting값 설정
    def update_setting(self):
        protocol_name, plate_type, cap_type, ctrl_seq, use_bcd, protocol_list = self.DB.load_setting()
        for i in range(len(protocol_list)):
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
        try:
            if self.check_pcr_masking:
                test_count = self.textBrowser_testcount.toPlainText()
                smp_count = self.tableWidget_smp_select.rowCount()

                if int(test_count) < smp_count:  # 시약 잔량 < 샘플 수
                    QtWidgets.QMessageBox.information(self, "System",
                                                      "The remaining amount of PCR reagent is insufficient.\nPlease replace PCR reagent.")
                    self.check_pcr_reagent = False

                elif int(test_count) >= smp_count:  # 시약 잔량 >= 샘플 수
                    self.check_pcr_reagent = True

                self.check_run()

            else:
                return False

        except Exception as err:
            print(err)
            print("check_test_count 에러")

    # Extraction 시약 바코드 확인
    def check_Extraction_count(self):
        try:
            Extraction_test = self.lineEdit_Extraction_bcd.text()
            if Extraction_test != "":  # 시약 바코드 입력하면
                self.check_extraction_reagent = True

            elif Extraction_test == "":  # 시약 바코드 입력 안하면
                self.check_extraction_reagent = False

            self.check_run()
        # test_count = self.textBrowser_extractioncount.toPlainText()
        # smp_count = self.tableWidget_smp_select.rowCount()
        # pcr_test = self.lineEdit_pcr_bcd.text()
        # if int(test_count) < smp_count:
        #     QtWidgets.QMessageBox.information(self, "System",
        #                                       "The remaining amount of Extraction reagent is insufficient.\nPlease replace Extraction reagent.")
        #     self.pushButton_run.setEnabled(False)
        # elif pcr_test == "":
        #     self.pushButton_run.setEnabled(False)
        # else:
        #     self.pushButton_run.setEnabled(True)
        # check_extraction_cnt = self.DB.Sel_Extraction_Use(self.lineEdit_Extraction_bcd.text())
        # if check_extraction_cnt == '0':
        #     QtWidgets.QMessageBox.information(self, "System", "already Use Extraction Reagent Barcode Number 10 times")
        #     self.lineEdit_Extraction_bcd.setText("")
        #     self.pushButton_run.setEnabled(False)
        #     self.textBrowser_extractioncount.setText("")

        except Exception as err:
            print(err)
            print("check_Extraction_count 에러")

    # run 버튼 활성화 여부
    def check_run(self):
        try:
            if self.check_pcr_masking:  # PCR 시약 masking이 올바르면
                if self.check_pcr_reagent and self.check_extraction_reagent:  # PCR 바코드, Extraction 올바르면
                    self.pushButton_run.setEnabled(True)

                else:
                    self.pushButton_run.setEnabled(False)
            else:
                self.pushButton_run.setEnabled(False)

        except Exception as err:
            print(err)
            print("check_run 에러")

    # 프로토콜 이름 , Protocol Masking
    def PCR_Bcd_Check(self):
        try:
            temp = self.lineEdit_pcr_bcd.text()
            temp = temp.replace('(', '').replace(')', '')
            temp3 = 0
            PCR_Count = self.DB.Sel_PCR_cnt(temp)  # PCR 시약 사용횟수 확인
            if PCR_Count == '0':
                QtWidgets.QMessageBox.information(self, "System", "already Use PCR Reagent Barcode Number")
                self.lineEdit_pcr_bcd.setText("")
                self.textBrowser_testcount.setText("")
                self.check_pcr_masking = False
                return False

            Protocol_Name = self.listWidget_protocol.currentItem().text()
            temp2 = self.DB.Sel_Protocol_Num(Protocol_Name)  # Protocol Masking 정보 불러옴
            Protocol_check = temp2[0][0]

            if Protocol_check != None and self.lineEdit_pcr_bcd.text() != "":  # Masking 정보가 None이 아니고 lineEdit가 빈칸이 아니면
                temp3 = temp.find(Protocol_check)
            elif Protocol_check == None:  # Masking 정보가 None이면
                temp3 = -1

            if temp3 != -1 and self.lineEdit_pcr_bcd.text() != "":  # 올바른 PCR 바코드 입력하면
                # temp = temp[:34] + Protocol_check + temp[34:]
                self.lineEdit_pcr_bcd.setText(temp)
                if len(temp) > 50:  # 바코드 2번 이상 찍는 경우
                    self.lineEdit_pcr_bcd.setText("")
                    self.textBrowser_testcount.setText("")
                    QtWidgets.QMessageBox.information(self, "System",
                                                      "PCR Reagent Barcode over length")
                    self.check_pcr_masking = False
                    return False
                else:
                    self.check_pcr_masking = True
                    return True

            elif temp3 == -1 or PCR_Count == -1:
                self.lineEdit_pcr_bcd.setText("")
                self.pushButton_run.setEnabled(False)
                self.textBrowser_testcount.setText("")
                QtWidgets.QMessageBox.information(self, "System", "PCR Reagent Barcode Not Matched with Protocol Name")
                self.check_pcr_masking = False
                return False

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
            if i == 1:  # 기본 plrn 경로
                self.textBrowser_plrn_path.setText(dir_path)
                self.DB.set_dir(dir_path, 1)
            elif i == 2:  # 추가 plrn 경로 2
                if self.textBrowser_plrn_path.toPlainText() == str(
                        dir_path) or self.textBrowser_plrn_path_3.toPlainText() == str(dir_path):  # 이미 지정된 경로이면
                    QtWidgets.QMessageBox.information(self, "System",
                                                      "This path is already specified. Please change the path.")
                else:
                    self.textBrowser_plrn_path_2.setText(dir_path)
                    self.DB.set_dir(dir_path, 2)
            elif i == 3:  # 추가 plrn 경로 3
                if self.textBrowser_plrn_path.toPlainText() == str(
                        dir_path) or self.textBrowser_plrn_path_2.toPlainText() == str(dir_path):  # 이미 지정된 경로이면
                    QtWidgets.QMessageBox.information(self, "System",
                                                      "This path is already specified. Please change the path.")
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

        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', f'{self.DB.open_dir_csv()}',
                                                      'csv File(*.csv);; csv File(*.csv)')
        if fname[0]:
            self.path_csv = fname[0]
            self.csv_signal = 1
            temp_1 = fname[0].split("/")
            self.worklist_name = temp_1[-1].replace(".csv", "")

            del temp_1[-1]
            self.dir_csv = "/".join(temp_1)
            self.DB.save_dir_csv(self.dir_csv)  # 최근에 load한 경로 저장

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

    # 설명 : 바코드 load txt 버튼 Visible 기능
    # 생성일자 : 2022/03/16
    # 이름 : 이신후
    def Visible_txt_Button(self):
        try:
            Protocol_Name = self.DB.Sel_Bcd()
            Protocol_Name = Protocol_Name[0][0].rsplit('\\', 3)
            Protocol_Name = Protocol_Name[2]
            Protocol_Name = Protocol_Name.upper().find("PCRSETUP")
            if Protocol_Name != -1:
                self.toolButton_load_txt.setVisible(True)
            else:
                self.toolButton_load_txt.setVisible(False)

        except Exception as err:
            print(err)
            print("Visible_txt_Button 에러")

    # 설명 : 기존에 생성되었던 바코드 txt 파일을 읽어옴.
    # 생성일자 : 2022/03/17
    # 이름 : 이신후
    def Load_Barcode_txt(self):
        try:
            # File_Dir = self.DB.Sel_Bcd()

            column = 0
            pre_sel_bcd = self.DB.Previous_Sel_Bcd()
            pre_sel_bcd_temp = pre_sel_bcd.rsplit('/', 1)
            pre_sel_bcd = pre_sel_bcd_temp[0]

            # 현재 비교할 텍스트 파일
            bcd_list = []

            file_name = QtWidgets.QFileDialog.getOpenFileName(self, "파일 열기 . . .", pre_sel_bcd, "text File (*.txt)")

            File_Dir = file_name[0].rsplit('/', 3)
            if File_Dir[1] == "PCR":
                column = 3
            elif File_Dir[1] == "SampleRack":
                column = 2

            file = open(file_name[0], "r", encoding="utf8")
            lines = file.readlines()  # list 형태로 읽어옴
            lines.pop(0)
            cnt = 0

            for line in lines:
                if not line:
                    break

                temp = lines[cnt].split()

                Control_Check = temp[column]
                if Control_Check[:1] == "R":
                    continue
                bcd_list.append(str(temp[column]))

                cnt += 1

            file.close()
            self.tableWidget_smp.setRowCount(len(bcd_list))

            for i in range(0, len(bcd_list)):
                self.tableWidget_smp.setItem(i, 0, QtWidgets.QTableWidgetItem(bcd_list[i]))
                self.tableWidget_smp.setItem(i, 1, QtWidgets.QTableWidgetItem(str(i + 1)))

            for i in range(0, len(bcd_list)):
                if self.tableWidget_smp.item(i, 0).text() != self.tableWidget_smp.item(i, 1).text():
                    self.tableWidget_smp.item(i, 0).setBackground(QtGui.QColor(255, 208, 208))
                    self.tableWidget_smp.item(i, 1).setBackground(QtGui.QColor(255, 208, 208))

        except Exception as err:
            print(err)
            print("Visible_txt_Button 에러")

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
                # plrn 생성에 필요한 데이터 저장
                self.id_plrn = self.DB.Input_plrn_data(date, Protocol_Name, rowCount, self.plate_type,
                                                       self.cap_type,
                                                       self.ctrl_seq, pcr_bcd, self.selection_bcd,
                                                       self.lineEdit_PCR_plate.text(), self.lineEdit_DWP.text(),
                                                       Extraction_bcd)
                # 샘플 데이터 저장
                self.DB.Input_sample_data(smp_bcd, self.id_plrn)
                # PCR 시약 데이터 저장
                self.DB.Use_PCR(pcr_bcd, rowCount)
                # Item 설정값 저장
                self.DB.save_Temp(Protocol_Name, self.plate_type, self.cap_type, self.ctrl_seq, self.use_bcd)
                # Control Count 저장
                self.DB.set_control_count(Ui_MainWindow.Control_Count)
                # flag 확인 후 plrn 만들어주는 경우인지 확인
                plrn_flag = self.DB.get_plrn_flag()
                if plrn_flag == 1:  # plrn 생성
                    self.DB.make_plrn(self.id_plrn, Ui_MainWindow.Control_Count)
                    self.DB.delete_bcd()
                # 바코드 파일 생성
                if self.tableWidget_smp.item(0, 0) is not None:
                    for j in range(rowCount):
                        worklist_bcd.append(self.tableWidget_smp.item(j, 0).text())
                self.DB.Create_barcode(self.id_plrn, worklist_bcd, self.path_csv, self.worklist_name,
                                       self.csv_signal)
                # 샘플 데이터 삭제
                # self.DB.delete_bcd()  ########
                self.textBrowser_testcount.setText(str(count))

            elif self.listWidget_protocol.currentItem() == None or self.lineEdit_pcr_bcd.text() == "":
                QtWidgets.QMessageBox.information(self, "System", "Please enter all protocol information.")
                self.pushButton_run.setEnabled(False)
            self.check_pcr_masking = False
            self.check_pcr_reagent = False
            self.check_extraction_reagent = False
            self.signal_close = 1
            self.close()
            temp = self.DB.Sel_Bcd()
            file = temp[0][0]
            # os.remove(file)

        except Exception as err:
            print(err)

    # 초기 바코드 리스트 불러오기
    def Bcd_list(self):
        try:
            Ui_MainWindow.Control_Count = 0
            self.bcd_list = []
            self.temp_bcd_list = []
            temp = self.DB.Sel_Bcd()
            is_path = temp[0][0].rsplit('\\', 3)

            Previous_Barcode = is_path[2].upper().find("PCRSETUP")

            column = 0
            if is_path[1] == "PCR":
                column = 3
            elif is_path[1] == "SampleRack":
                column = 2
            file = open(temp[0][0], "r", encoding="utf8")
            # 현재 비교할 텍스트 파일
            lines = file.readlines()  # list 형태로 읽어옴
            lines.pop(0)
            cnt = 0
            self.Visible_txt_Button()

            for line in lines:
                if not line:
                    break

                temp3 = lines[cnt].split()

                Control_Check = temp3[column]
                if Control_Check[:1] == "R":
                    Ui_MainWindow.Control_Count += 1
                    continue
                self.bcd_list.append(str(temp3[column]))

                # self.tableWidget_smp.setRowHeight(cnt, 60)
                cnt += 1
            file.close()
            self.tableWidget_smp.setRowCount(len(self.bcd_list))

            for i in range(0, len(self.bcd_list)):
                self.tableWidget_smp.setItem(i, 0, QtWidgets.QTableWidgetItem(""))
                self.tableWidget_smp.setItem(i, 1, QtWidgets.QTableWidgetItem(self.bcd_list[i]))

            for i in range(0, len(self.bcd_list)):
                if self.tableWidget_smp.item(i, 0).text() != self.tableWidget_smp.item(i, 1).text():
                    self.tableWidget_smp.item(i, 0).setBackground(QtGui.QColor(255, 208, 208))
                    self.tableWidget_smp.item(i, 1).setBackground(QtGui.QColor(255, 208, 208))

            if Previous_Barcode != -1 and is_path[1] == "PCR":
                self.Previous_Load_Barcode()


        except Exception as err:
            print(err)
            print("Bcd_list 기능에러")

    # 설명 : 이전에 생성했던 바코드 txt 파일을 읽어옴.
    # 생성일자 : 2022/03/17
    # 이름 : 이신후
    def Previous_Load_Barcode(self):
        try:
            Previous_Barcode = self.DB.Previous_Sel_Bcd()

            # 현재 비교할 텍스트 파일
            bcd_list = []

            File_Dir = Previous_Barcode.rsplit('\\', 3)
            if File_Dir[1] == "PCR":
                column = 3
            elif File_Dir[1] == "SampleRack":
                column = 2

            file = open(Previous_Barcode, "r", encoding="utf8")
            lines = file.readlines()  # list 형태로 읽어옴
            lines.pop(0)
            cnt = 0

            for line in lines:
                if not line:
                    break

                temp = lines[cnt].split()

                Control_Check = temp[column]
                if Control_Check[:1] == "R":
                    continue
                bcd_list.append(str(temp[column]))

                cnt += 1

            file.close()
            self.tableWidget_smp.setRowCount(len(bcd_list))

            for i in range(0, len(bcd_list)):
                self.tableWidget_smp.setItem(i, 0, QtWidgets.QTableWidgetItem(bcd_list[i]))
                self.tableWidget_smp.setItem(i, 1, QtWidgets.QTableWidgetItem(str(i + 1)))

            for i in range(0, len(bcd_list)):
                if self.tableWidget_smp.item(i, 0).text() != self.tableWidget_smp.item(i, 1).text():
                    self.tableWidget_smp.item(i, 0).setBackground(QtGui.QColor(255, 208, 208))
                    self.tableWidget_smp.item(i, 1).setBackground(QtGui.QColor(255, 208, 208))

        except Exception as err:
            print(err)
            print("Previous_Load_Barcode 에러")

    # 바코드 갱신기능
    def Reload(self):
        try:
            bcd_list = []
            temp_bcd_list = []
            if self.lineEdit_smp_count.text() == "":
                QtWidgets.QMessageBox.information(self, "System", "Please Insert Sample Count.")
            Sample_Count = int(self.lineEdit_smp_count.text())

            temp = self.DB.Sel_Bcd()
            is_path = temp[0][0].rsplit('\\', 3)
            column = 0
            if is_path[1] == "PCR":
                column = 3
            elif is_path[1] == "SampleRack":
                column = 2

            file = open(temp[0][0], "r", encoding="utf8")
            # 현재 비교할 텍스트 파일
            lines = file.readlines()  # list 형태로 읽어옴
            lines.pop(0)
            cnt = 0

            for line in lines:
                if not line:
                    break

                temp3 = lines[cnt].split()

                Control_Check = temp3[column]
                if Control_Check[:1] == "R":
                    continue
                bcd_list.append(str(temp3[column]))

                # self.tableWidget_smp.setRowHeight(cnt, 60)
                cnt += 1

            file.close()
            self.tableWidget_smp.setRowCount(Sample_Count)

            # Ok, 버튼누를 때, text에 있는 숫자개수만큼의 행을 만들고, 행만큼 바코드정보를 넣어준다.
            for i in range(0, Sample_Count):
                if i >= len(bcd_list):
                    self.tableWidget_smp.setItem(i, 1, QtWidgets.QTableWidgetItem(""))
                else:
                    self.tableWidget_smp.setItem(i, 1, QtWidgets.QTableWidgetItem(bcd_list[i]))

            for i in range(0, Sample_Count):
                if self.tableWidget_smp.item(i, 0).text() != self.tableWidget_smp.item(i, 1).text():
                    self.tableWidget_smp.item(i, 0).setBackground(QtGui.QColor(255, 208, 208))
                    self.tableWidget_smp.item(i, 1).setBackground(QtGui.QColor(255, 208, 208))
        except Exception as err:
            print(err)
            print("Reload 기능에러")

    def closeEvent(self, event):
        try:
            if self.signal_close == 0:
                reply = QtWidgets.QMessageBox.question(self, "System",
                                                       "Are you sure to quit?",
                                                       QtWidgets.QMessageBox.StandardButton.Yes |
                                                       QtWidgets.QMessageBox.StandardButton.No,
                                                       QtWidgets.QMessageBox.StandardButton.No)

                if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                    event.accept()
                else:
                    event.ignore()
        except Exception as err:
            print(err)
