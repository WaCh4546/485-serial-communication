
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'demo_1.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDoubleValidator,QIcon
import pyqtgraph as pg
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(950, 478)
        #串口设置组
        self.formGroupBox = QtWidgets.QGroupBox(Form) #创建表单组合框
        self.formGroupBox.setGeometry(QtCore.QRect(20, 20, 167, 301)) # 从20，20 开始画一个167，301的框
        self.formGroupBox.setObjectName("formGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.formGroupBox) #在组合框里创建一个表单布局
        self.formLayout.setContentsMargins(10, 10, 10, 10) #设置左上右下的边距
        self.formLayout.setSpacing(10) #设置各个控件上下边距
        self.formLayout.setObjectName("formLayout")
        self.s1__lb_1 = QtWidgets.QLabel(self.formGroupBox) 
        self.s1__lb_1.setObjectName("s1__lb_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.s1__lb_1)
        self.s1__box_1 = QtWidgets.QPushButton(self.formGroupBox)  # 串口检测按钮
        self.s1__box_1.setAutoRepeatInterval(100)
        self.s1__box_1.setDefault(True)
        self.s1__box_1.setObjectName("s1__box_1")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.s1__box_1)
        self.s1__lb_2 = QtWidgets.QLabel(self.formGroupBox) #串口信息显示
        self.s1__lb_2.setObjectName("s1__lb_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.s1__lb_2)
        self.s1__box_2 = QtWidgets.QComboBox(self.formGroupBox) #串口下拉菜单
        self.s1__box_2.setObjectName("s1__box_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.s1__box_2)
        self.s1__lb_3 = QtWidgets.QLabel(self.formGroupBox)  #波特率文本显示
        self.s1__lb_3.setObjectName("s1__lb_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.s1__lb_3)
        self.s1__box_3 = QtWidgets.QComboBox(self.formGroupBox)   #波特率下拉菜单
        self.s1__box_3.setObjectName("s1__box_3")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.s1__box_3.addItem("")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.s1__box_3) #s1__box_3设置在第四行
        self.s1__lb_4 = QtWidgets.QLabel(self.formGroupBox) #数据位文本
        self.s1__lb_4.setObjectName("s1__lb_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.s1__lb_4)
        self.s1__box_4 = QtWidgets.QComboBox(self.formGroupBox) #数据位下拉菜单
        self.s1__box_4.setObjectName("s1__box_4")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.s1__box_4.addItem("")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.s1__box_4)
        self.s1__lb_5 = QtWidgets.QLabel(self.formGroupBox)#校验位文本
        self.s1__lb_5.setObjectName("s1__lb_5") 
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.s1__lb_5)
        self.s1__box_5 = QtWidgets.QComboBox(self.formGroupBox) #校验位下拉菜单
        self.s1__box_5.setObjectName("s1__box_5")
        self.s1__box_5.addItem("")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.s1__box_5)
        self.open_button = QtWidgets.QPushButton(self.formGroupBox) #打开串口按钮
        self.open_button.setObjectName("open_button")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.open_button)
        self.close_button = QtWidgets.QPushButton(self.formGroupBox) #关闭串口按钮
        self.close_button.setObjectName("close_button")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.close_button)
        self.s1__lb_6 = QtWidgets.QLabel(self.formGroupBox)
        self.s1__lb_6.setObjectName("s1__lb_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.s1__lb_6)
        self.s1__box_6 = QtWidgets.QComboBox(self.formGroupBox)
        self.s1__box_6.setObjectName("s1__box_6")
        self.s1__box_6.addItem("")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.s1__box_6)
        self.state_label = QtWidgets.QLabel(self.formGroupBox)
        self.state_label.setText("")
        self.state_label.setTextFormat(QtCore.Qt.AutoText)
        self.state_label.setScaledContents(True)
        self.state_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.state_label.setObjectName("state_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.state_label)

        #参数设置区
        self.formGroupBox2 = QtWidgets.QGroupBox(Form) #创建表单组合框
        self.formGroupBox2.setGeometry(QtCore.QRect(210, 240, 171, 221))
        self.formGroupBox2.setObjectName("formGroupBox2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formGroupBox2) #创建表单布局
        self.formLayout_3.setContentsMargins(10, 10, 10, 10)
        self.formLayout_3.setSpacing(10)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_E = QtWidgets.QLabel(self.formGroupBox2)
        self.label_E.setObjectName("label_E")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_E) #激励
        self.lineEdit_E = QtWidgets.QLineEdit(self.formGroupBox2)
        self.lineEdit_E.setObjectName("lineEdit_E")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_E)#激励文本行
        self.label_P = QtWidgets.QLabel(self.formGroupBox2)
        self.label_P.setObjectName("label_P")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_P) #比例
        self.label_I = QtWidgets.QLabel(self.formGroupBox2)
        self.label_I.setObjectName("label_I")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_I) #积分
        self.lineEdit_P = QtWidgets.QLineEdit(self.formGroupBox2)
        self.lineEdit_P.setObjectName("lineEdit_P")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_P) #比例文本行
        self.lineEdit_I = QtWidgets.QLineEdit(self.formGroupBox2)
        self.lineEdit_I.setObjectName("lineEdit_I")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_I)#积分文本行
        self.label_D = QtWidgets.QLabel(self.formGroupBox2)
        self.label_D.setObjectName("label_D")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_D) #微分
        self.lineEdit_D = QtWidgets.QLineEdit(self.formGroupBox2)
        self.lineEdit_D.setObjectName("lineEdit_D")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_D)#微分文本行
        self.PID_ENTER_button = QtWidgets.QPushButton(self.formGroupBox2) #确认
        self.PID_ENTER_button.setObjectName("PID_ENTER_button")
        self.formLayout_3.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.PID_ENTER_button)
        self.PID_CANCEL_button = QtWidgets.QPushButton(self.formGroupBox2) #取消
        self.PID_CANCEL_button.setObjectName("PID_CANCEL_button")
        self.formLayout_3.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.PID_CANCEL_button)
        self.doubleValidator_e = QDoubleValidator(self)
        self.doubleValidator_pid = QDoubleValidator(self)
        self.doubleValidator_e.setRange(0,9999)
        self.doubleValidator_pid.setRange(0,99)
        self.doubleValidator_e.setNotation(QDoubleValidator.StandardNotation)  #标准表示法
        self.doubleValidator_pid.setNotation(QDoubleValidator.StandardNotation)  #标准表示法
        self.doubleValidator_e.setDecimals(1)
        self.doubleValidator_pid.setDecimals(3)
        self.lineEdit_E.setValidator(self.doubleValidator_e)
        self.lineEdit_P.setValidator(self.doubleValidator_pid)
        self.lineEdit_I.setValidator(self.doubleValidator_pid)
        self.lineEdit_D.setValidator(self.doubleValidator_pid)
       
       #数据接收区
          #检测计算机接受区
        self.verticalGroupBox = QtWidgets.QGroupBox(Form) #创建垂直组合框  接受区
        self.verticalGroupBox.setGeometry(QtCore.QRect(210, 20, 201, 201))
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalGroupBox) #创建垂直布局
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TC__receive_text = QtWidgets.QTextBrowser(self.verticalGroupBox) #创建文本浏览框
        self.TC__receive_text.setObjectName("TC__receive_text")
        self.verticalLayout.addWidget(self.TC__receive_text)

          #控制计算机接受区
        self.ControlComputerReceive = QtWidgets.QGroupBox(Form) #创建垂直组合框  接受区
        self.ControlComputerReceive.setGeometry(QtCore.QRect(430, 20, 201, 201))
        self.ControlComputerReceive.setObjectName("ControlComputerReceive")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.ControlComputerReceive) #创建垂直布局
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.CC__receive_text = QtWidgets.QTextBrowser(self.ControlComputerReceive) #创建文本浏览框
        self.CC__receive_text.setObjectName("CC__receive_text")
        self.verticalLayout.addWidget(self.CC__receive_text)

          #模型计算机接受区
        self.MoldingComputerReceive = QtWidgets.QGroupBox(Form) #创建垂直组合框  接受区
        self.MoldingComputerReceive.setGeometry(QtCore.QRect(650, 20, 201, 201))
        self.MoldingComputerReceive.setObjectName("MoldingComputerReceive")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.MoldingComputerReceive) #创建垂直布局
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.MC__receive_text = QtWidgets.QTextBrowser(self.MoldingComputerReceive) #创建文本浏览框
        self.MC__receive_text.setObjectName("MC__receive_text")
        self.verticalLayout.addWidget(self.MC__receive_text)

          #接收区清除和保存
        self.s2__clear_button = QtWidgets.QPushButton(Form)   #接收区清除按钮
        self.s2__clear_button.setGeometry(QtCore.QRect(870, 40, 61, 31))
        self.s2__clear_button.setObjectName("s2__clear_button")
        self.s2__save_button = QtWidgets.QPushButton(Form)   #接收区保存按钮
        self.s2__save_button.setGeometry(QtCore.QRect(870, 100, 61, 31))
        self.s2__save_button.setObjectName("self.s2__save_button")
       

        #从机状态区
        self.formGroupBox1 = QtWidgets.QGroupBox(Form) #创建表单组合框
        self.formGroupBox1.setGeometry(QtCore.QRect(20, 340, 171, 121))
        self.formGroupBox1.setObjectName("formGroupBox1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formGroupBox1) #创建表单布局
        self.formLayout_2.setContentsMargins(15, 15, 15, 15)
        self.formLayout_2.setSpacing(20)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_TC = QtWidgets.QLabel(self.formGroupBox1)
        self.label_TC.setObjectName("label_TC")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_TC) #已接收标签
        self.label_CC = QtWidgets.QLabel(self.formGroupBox1)
        self.label_CC.setObjectName("label_CC")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_CC) #已发送标签
        self.label_MC = QtWidgets.QLabel(self.formGroupBox1)
        self.label_MC.setObjectName("label_MC")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_MC) #已发送标签
        self.label_TC_STATE = QtWidgets.QLabel(self.formGroupBox1)
        self.label_TC_STATE.setObjectName("label_TC_STATE")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.label_TC_STATE) #已接收文本行
        self.label_CC_STATE = QtWidgets.QLabel(self.formGroupBox1)
        self.label_CC_STATE.setObjectName("label_CC_STATE")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.label_CC_STATE) #已接收文本行
        self.label_MC_STATE = QtWidgets.QLabel(self.formGroupBox1)
        self.label_MC_STATE.setObjectName("label_MC_STATE")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.label_MC_STATE) #已接收文本行
        
        

        #绘图区
        self.DrawPoints = QtWidgets.QGroupBox(Form) #创建表单组合框
        self.DrawPoints.setGeometry(QtCore.QRect(430, 240, 421, 221))
        self.DrawPoints.setObjectName("DrawPoints")
        self.DrawArea = QtWidgets.QVBoxLayout(self.DrawPoints) #创建垂直布局
        self.DrawArea.setObjectName("DrawArea")
        self.DrawPoints.setContentsMargins(15, 15, 15, 15)
        self.plot = pg.PlotWidget(enableAutoRange=True)   #创建绘图控件
        self.DrawArea.addWidget(self.plot)   #添加至垂直布局
        self.curve = self.plot.plot()
        self.DrawArea_button = QtWidgets.QPushButton(Form) #清除按钮
        self.DrawArea_button.setGeometry(QtCore.QRect(870, 260, 61, 31))
        self.DrawArea_button.setObjectName("DrawArea_button")
        self.Continue_button = QtWidgets.QPushButton(Form) #继续按钮
        self.Continue_button.setGeometry(QtCore.QRect(870, 360, 61, 31))
        self.Continue_button.setObjectName("Continue_button")  
        self.Pause_button = QtWidgets.QPushButton(Form) #暂停按钮
        self.Pause_button.setGeometry(QtCore.QRect(870, 420, 61, 31))
        self.Pause_button.setObjectName("Pause_button")  

        #控件的应用
        self.verticalGroupBox.raise_()
        self.ControlComputerReceive.raise_()
        self.ControlComputerReceive.raise_()
        self.MoldingComputerReceive.raise_()
        self.formGroupBox.raise_()
        self.DrawArea_button.raise_()
        self.Pause_button.raise_()
        self.Continue_button.raise_()
        self.formGroupBox.raise_()
        self.s2__clear_button.raise_()
        self.s2__save_button.raise_()
        self.PID_ENTER_button.raise_()
        

        #设置控件标签内容
        self.retranslateUi(Form)


        QtCore.QMetaObject.connectSlotsByName(Form) #根据objectName和signal自动绑定slot

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.formGroupBox.setTitle(_translate("Form", "串口设置"))
        self.DrawPoints.setTitle(_translate("Form", "实时图像"))
        self.s1__lb_1.setText(_translate("Form", "串口检测："))
        self.s1__box_1.setText(_translate("Form", "检测串口"))
        self.s1__lb_2.setText(_translate("Form", "串口选择："))
        self.s1__lb_3.setText(_translate("Form", "波特率："))
        self.s1__box_3.setItemText(0, _translate("Form", "115200"))
        self.s1__box_3.setItemText(1, _translate("Form", "2400"))
        self.s1__box_3.setItemText(2, _translate("Form", "4800"))
        self.s1__box_3.setItemText(3, _translate("Form", "9600"))
        self.s1__box_3.setItemText(4, _translate("Form", "14400"))
        self.s1__box_3.setItemText(5, _translate("Form", "19200"))
        self.s1__box_3.setItemText(6, _translate("Form", "38400"))
        self.s1__box_3.setItemText(7, _translate("Form", "57600"))
        self.s1__box_3.setItemText(8, _translate("Form", "76800"))
        self.s1__box_3.setItemText(9, _translate("Form", "12800"))
        self.s1__box_3.setItemText(10, _translate("Form", "230400"))
        self.s1__box_3.setItemText(11, _translate("Form", "460800"))
        self.s1__lb_4.setText(_translate("Form", "数据位："))
        self.s1__box_4.setItemText(0, _translate("Form", "8"))
        self.s1__box_4.setItemText(1, _translate("Form", "7"))
        self.s1__box_4.setItemText(2, _translate("Form", "6"))
        self.s1__box_4.setItemText(3, _translate("Form", "5"))
        self.s1__lb_5.setText(_translate("Form", "校验位："))
        self.s1__box_5.setItemText(0, _translate("Form", "N"))
        self.open_button.setText(_translate("Form", "打开串口"))
        self.close_button.setText(_translate("Form", "关闭串口"))
        self.s1__lb_6.setText(_translate("Form", "停止位："))
        self.s1__box_6.setItemText(0, _translate("Form", "1"))
        self.verticalGroupBox.setTitle(_translate("Form", "检测计算机"))
        self.MoldingComputerReceive.setTitle(_translate("Form", "模型计算机"))
        self.ControlComputerReceive.setTitle(_translate("Form", "控制计算机"))
        self.DrawArea_button.setText(_translate("Form", "清除"))
        self.Pause_button.setText(_translate("Form", "暂停"))
        self.Continue_button.setText(_translate("Form", "继续"))
        self.formGroupBox1.setTitle(_translate("Form", "从机状态"))
        self.formGroupBox2.setTitle(_translate("Form", "从机参数设置"))
        self.label_TC.setText(_translate("Form", "检测计算机："))
        self.label_CC.setText(_translate("Form", "控制计算机："))
        self.label_MC.setText(_translate("Form", "模型计算机："))
        self.label_TC_STATE.setText(_translate("Form", "<离线>"))
        self.label_CC_STATE.setText(_translate("Form", "<离线>"))
        self.label_MC_STATE.setText(_translate("Form", "<离线>"))
        self.label_E.setText(_translate("Form", "激励(E)："))
        self.label_P.setText(_translate("Form", "比例(P)："))
        self.label_I.setText(_translate("Form", "积分(I)："))
        self.label_D.setText(_translate("Form", "微分(D)："))
        self.PID_ENTER_button.setText(_translate("Form", "运行"))
        self.PID_CANCEL_button.setText(_translate("Form", "停止"))
        self.s2__clear_button.setText(_translate("Form", "清除"))
        self.s2__save_button.setText(_translate("Form", "保存"))


        