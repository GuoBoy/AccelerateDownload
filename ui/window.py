# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(525, 414)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.show_history_btn = QtWidgets.QPushButton(self.widget_2)
        self.show_history_btn.setObjectName("show_history_btn")
        self.gridLayout_4.addWidget(self.show_history_btn, 5, 2, 1, 1)
        self.modify_server_btn = QtWidgets.QPushButton(self.widget_2)
        self.modify_server_btn.setObjectName("modify_server_btn")
        self.gridLayout_4.addWidget(self.modify_server_btn, 1, 2, 1, 1)
        self.whether_open = QtWidgets.QCheckBox(self.widget_2)
        self.whether_open.setObjectName("whether_open")
        self.gridLayout_4.addWidget(self.whether_open, 5, 0, 1, 2)
        self.save_path_btn = QtWidgets.QPushButton(self.widget_2)
        self.save_path_btn.setObjectName("save_path_btn")
        self.gridLayout_4.addWidget(self.save_path_btn, 3, 2, 1, 1)
        self.save_path_input = QtWidgets.QLineEdit(self.widget_2)
        self.save_path_input.setObjectName("save_path_input")
        self.gridLayout_4.addWidget(self.save_path_input, 3, 0, 1, 1)
        self.download_btn = QtWidgets.QPushButton(self.widget_2)
        self.download_btn.setObjectName("download_btn")
        self.gridLayout_4.addWidget(self.download_btn, 2, 2, 1, 1)
        self.download_url_input = QtWidgets.QLineEdit(self.widget_2)
        self.download_url_input.setObjectName("download_url_input")
        self.gridLayout_4.addWidget(self.download_url_input, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.widget_2)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout_4.addWidget(self.comboBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.widget_2, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.log_area = QtWidgets.QTextBrowser(self.groupBox)
        self.log_area.setObjectName("log_area")
        self.gridLayout_2.addWidget(self.log_area, 0, 0, 1, 1)
        self.progress_bar = QtWidgets.QProgressBar(self.groupBox)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout_2.addWidget(self.progress_bar, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)

        self.retranslateUi(Form)
        self.download_btn.clicked.connect(Form.on_download) # type: ignore
        self.save_path_btn.clicked.connect(Form.on_path) # type: ignore
        self.whether_open.stateChanged['int'].connect(Form.to_openpath) # type: ignore
        self.show_history_btn.clicked.connect(Form.show_history) # type: ignore
        self.modify_server_btn.clicked.connect(Form.show_server_manager) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "文件加速下载"))
        self.show_history_btn.setText(_translate("Form", "查看下载历史"))
        self.modify_server_btn.setText(_translate("Form", "管理服务器"))
        self.whether_open.setText(_translate("Form", "下载完成打开文件"))
        self.save_path_btn.setText(_translate("Form", "保存位置"))
        self.save_path_input.setPlaceholderText(_translate("Form", "默认当前路径"))
        self.download_btn.setText(_translate("Form", "下载"))
        self.download_url_input.setPlaceholderText(_translate("Form", "输入下载地址"))
        self.comboBox.setPlaceholderText(_translate("Form", "服务器地址"))
        self.groupBox.setTitle(_translate("Form", "logs"))
