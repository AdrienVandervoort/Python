# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)

from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSlider, QSpinBox, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(786, 612)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(-1, 9, 241, 591))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(self.horizontalLayoutWidget)
        self.widget.setObjectName(u"widget")
        self.verticalLayoutWidget = QWidget(self.widget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 241, 591))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.horizontalSlider = QSlider(self.verticalLayoutWidget)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setValue(30)
        self.horizontalSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout.addWidget(self.horizontalSlider)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.groupBox = QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayoutWidget_2 = QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 9, 111, 161))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkBox_2 = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_2.setObjectName(u"checkBox_2")

        self.verticalLayout_2.addWidget(self.checkBox_2)

        self.checkBox_3 = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox_3.setObjectName(u"checkBox_3")

        self.verticalLayout_2.addWidget(self.checkBox_3)

        self.checkBox = QCheckBox(self.verticalLayoutWidget_2)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout_2.addWidget(self.checkBox)

        self.pushButton_3 = QPushButton(self.verticalLayoutWidget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.verticalLayout_2.addWidget(self.pushButton_3)

        self.verticalLayoutWidget_3 = QWidget(self.groupBox)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(110, 9, 131, 121))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.spinBox_2 = QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_2.setObjectName(u"spinBox_2")

        self.verticalLayout_3.addWidget(self.spinBox_2)

        self.spinBox_3 = QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox_3.setObjectName(u"spinBox_3")

        self.verticalLayout_3.addWidget(self.spinBox_3)

        self.spinBox = QSpinBox(self.verticalLayoutWidget_3)
        self.spinBox.setObjectName(u"spinBox")

        self.verticalLayout_3.addWidget(self.spinBox)


        self.verticalLayout.addWidget(self.groupBox)


        self.horizontalLayout.addWidget(self.widget)

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(249, 9, 551, 591))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_2 = QWidget(self.horizontalLayoutWidget_2)
        self.widget_2.setObjectName(u"widget_2")

        self.horizontalLayout_2.addWidget(self.widget_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Speed set point (RPM)", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"PID parameters", None))
        self.checkBox_2.setText(QCoreApplication.translate("MainWindow", u"Proportionelle", None))
        self.checkBox_3.setText(QCoreApplication.translate("MainWindow", u"Integrale", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"D\u00e9riv\u00e9e", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"Update", None))
    # retranslateUi

