# Form implementation generated from reading ui file 'd:\source\projects\PyQtMvvm\qt-mvvm\app\pages\UI\MainPage.ui'
#
# Created by: PyQt6 UI code generator 6.4.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 62, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.entryUserName = QtWidgets.QLineEdit(Form)
        self.entryUserName.setObjectName("entryUserName")
        self.gridLayout.addWidget(self.entryUserName, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.entryEmail = QtWidgets.QLineEdit(Form)
        self.entryEmail.setObjectName("entryEmail")
        self.gridLayout.addWidget(self.entryEmail, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelUserName = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelUserName.setFont(font)
        self.labelUserName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelUserName.setObjectName("labelUserName")
        self.verticalLayout.addWidget(self.labelUserName)
        self.labelEmail = QtWidgets.QLabel(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.labelEmail.setFont(font)
        self.labelEmail.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.labelEmail.setObjectName("labelEmail")
        self.verticalLayout.addWidget(self.labelEmail)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonSend = QtWidgets.QPushButton(Form)
        self.buttonSend.setObjectName("buttonSend")
        self.verticalLayout_2.addWidget(self.buttonSend)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(84, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 62, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 2, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Username"))
        self.label_2.setText(_translate("Form", "Email"))
        self.labelUserName.setText(_translate("Form", "TextLabel"))
        self.labelEmail.setText(_translate("Form", "TextLabel"))
        self.buttonSend.setText(_translate("Form", "PushButton"))
