import sys
import serial
import serial.tools.list_ports
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPainter,QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
from ui_demo_1 import Ui_Form
import pyqtgraph as pg
import numpy as np
import time
import os
import xlwt 
poll=0
TC_flag=-1
CC_flag=-1
MC_flag=-1
i = 0
x = [] # x轴的值
y = [] # y轴的值
TRANSPOND_FLAG=False
# CRC16
def calculateCRC(datalist): 
      if datalist:
        # 处理第1个字节数据 
        temp = calculateonebyte(datalist.pop(0), 0xFFFF) 
        # 循环处理其它字节数据 
        for data in datalist: 
            temp = calculateonebyte(data,temp) 
        return temp
 

def calculateonebyte(databyte, tempcrc): 

    # 把字节数据根CRC当前值的低8位相异或 
    low_byte = (databyte ^ tempcrc) & 0x00FF 
    # 当前CRC的高8位值不变 
    resultCRC = (tempcrc & 0xFF00) | low_byte 
 
    # 循环计算8位数据 
    for index in range(8): 
        # 若最低为1：CRC当前值跟生成多项式异或;为0继续 
        if resultCRC & 0x0001 == 1: 
            resultCRC >>= 1 
            resultCRC ^= 0xA001 # 0xA001是0x8005循环右移16位的值 
        else: 
            resultCRC >>= 1 
 
    return resultCRC 
def crc16_10(crc):
    if crc>0x60:
        return int(crc-0x60+9)
    else:
        return int(crc-0x30)

        

    #参数/数据格式化 
def dataformatting(data,len,flag):
    if flag:
        data=100000+data*1000
        return int(data)
    else:
        if data>2*(10**(len-1)):
            data=(0-(data-2*(10**(len-1))))/10000.0000
        else:
            data=(data-10**(len-1))/10000.0000
        return float(data)

class Pyqt5_Serial(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(Pyqt5_Serial, self).__init__()
        self.setupUi(self)
        self.init()
        self.setWindowTitle("监控计算机(主机)")
        #current_dir = os.path.abspath(os.path.dirname(__file__))
        self.setWindowIcon(QIcon('cartoon4.ico'))
        self.ser = serial.Serial()
        self.port_check()

        #设置背景
    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap('screen1.jpg')
        painter.drawPixmap(self.rect(),pixmap)


    def init(self):
        # 串口检测按钮
        self.s1__box_1.clicked.connect(self.port_check)

        # 串口信息显示
        self.s1__box_2.currentTextChanged.connect(self.port_imf)

        # 打开串口按钮
        self.open_button.clicked.connect(self.port_open)

        # 关闭串口按钮
        self.close_button.clicked.connect(self.port_close)

        # 发送参数
        self.PID_ENTER_button.clicked.connect(self.PID_data_send)
        # 取消发送参数
        self.PID_CANCEL_button.clicked.connect(self.PID_data_cancel)

        # 定时发送数据
        self.timer_send = QTimer()
        self.timer_send.timeout.connect(self.data_send)

        # 定时发送数据
        self.save_data = QTimer()
        self.save_data.timeout.connect(self.receive_data_save)

        # 定时器接收数据
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.data_receive)

        # 清除发送窗口
        self.DrawArea_button.clicked.connect(self.DrawArea_clear)

        # 暂停继续功能
        self.Pause_button.clicked.connect(self.Pause)
        self.Continue_button.clicked.connect(self.Continue)
        

        # 清除接收窗口
        self.s2__clear_button.clicked.connect(self.receive_data_clear)
        self.s2__save_button.clicked.connect(self.receive_data_save)
        #self.PID_ENTER_button.setEnabled(False)

        self.PID_ENTER_button.setEnabled(True)
        self.PID_CANCEL_button.setEnabled(False)
        self.Continue_button.setEnabled(False)
        self.Pause_button.setEnabled(False)


        
    # 串口检测
    def port_check(self):
        # 检测所有存在的串口，将信息存储在字典中
        self.Com_Dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.s1__box_2.clear()
        for port in port_list:
            self.Com_Dict["%s" % port[0]] = "%s" % port[1]
            self.s1__box_2.addItem(port[0])
        if len(self.Com_Dict) == 0:
            self.state_label.setText(" 无串口")

    # 串口信息
    def port_imf(self):
        # 显示选定的串口的详细信息
        imf_s = self.s1__box_2.currentText()
        if imf_s != "":
            self.state_label.setText(self.Com_Dict[self.s1__box_2.currentText()])

    # 打开串口
    def port_open(self):
        self.ser.port = self.s1__box_2.currentText()
        self.ser.baudrate = int(self.s1__box_3.currentText())
        self.ser.bytesize = int(self.s1__box_4.currentText())
        self.ser.stopbits = int(self.s1__box_6.currentText())
        self.ser.parity = self.s1__box_5.currentText()

        try:
            self.ser.open()
            if self.ser.isOpen():
                self.timer_send.start(100)
                self.save_data.start(360000)   #一个小时数据自动保存一次
        except:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！")
            return None

        # 打开串口接收定时器，周期为2ms
        self.timer.start(2)

        if self.ser.isOpen():
            self.open_button.setEnabled(False)
            self.close_button.setEnabled(True)
            self.formGroupBox.setTitle("串口设置（串口已开启）")

    # 关闭串口
    def port_close(self):
        self.PID_data_cancel()
        self.timer.stop()
        self.timer_send.stop()
        try:
            self.ser.close()
        except:
            pass
        self.open_button.setEnabled(True)
        self.close_button.setEnabled(False)
        self.PID_ENTER_button.setEnabled(True)
        self.PID_CANCEL_button.setEnabled(False) 
        
        # 接收数据和发送数据数目置零
        self.formGroupBox.setTitle("串口设置（串口已关闭）")
        self.label_TC_STATE.setText("<离线>")
        self.label_CC_STATE.setText("<离线>")
        self.label_MC_STATE.setText("<离线>")
        self.MoldingComputerReceive.setTitle('模型计算机')
        self.ControlComputerReceive.setTitle('控制计算机')

    #发送参数
    def PID_data_send(self):
        if self.ser.isOpen():
            if self.lineEdit_E.text() != '' and self.lineEdit_P.text() != '' and self.lineEdit_I.text() != '' and self.lineEdit_D.text() != ''  :
                self.timer_send.stop()
                # ascii发送
                global P,I,D,E
                P = dataformatting(float(self.lineEdit_P.text()),6,True)
                I = dataformatting(float(self.lineEdit_I.text()),6,True)
                D = dataformatting(float(self.lineEdit_D.text()),6,True)
                E = int(100000+float(self.lineEdit_E.text())*10)
                data1=str(E)+str(P)+str(I)+str(D)
                data=list(data1.encode('utf-8'))
                crc=calculateCRC(data)
                input_s = ('D'+'c'+data1+str(hex(crc))[2:] +'\r\n').encode('utf-8')
                #input_s = ('D'+'c'+data1 +'\r\n').encode('utf-8')
                num = self.ser.write(input_s)    
                #time.sleep(1)
                self.timer_send.start(100)
            else:
                QMessageBox.warning(self,'警告','请输入参数!',QMessageBox.Yes)
                
        else:
            pass
    #停止
    def PID_data_cancel(self):
        global TRANSPOND_FLAG
        self.PID_CANCEL_button.setEnabled(False)
        self.PID_ENTER_button.setEnabled(True)
        self.Continue_button.setEnabled(False)
        self.Pause_button.setEnabled(False)
        TRANSPOND_FLAG=False
        num = self.ser.write(('De\r\n').encode('utf-8'))
        self.MoldingComputerReceive.setTitle('模型计算机')
        self.ControlComputerReceive.setTitle('控制计算机')
        
        # 轮询发送数据
    def data_send(self):
        global poll,TC_flag,CC_flag,MC_flag
        if self.ser.isOpen():
            if poll%4==1:
                TC_flag-=1
                input_s = 'Aa'
                input_s = (input_s + '\r\n').encode('utf-8')
                num = self.ser.write(input_s)
            elif poll%4==2:
                CC_flag-=1
                input_s = 'Ba'
                input_s = (input_s + '\r\n').encode('utf-8')
                num = self.ser.write(input_s)
            elif poll%4==3:
                MC_flag-=1
                input_s = 'Ca'
                input_s = (input_s + '\r\n').encode('utf-8')
                num = self.ser.write(input_s)
            elif poll%100==0:
                poll=0
                input_s = 'Db'+str(time.strftime("%H:%M:%S", time.localtime()))
                input_s = (input_s + '\r\n').encode('utf-8')
                num = self.ser.write(input_s)
            off_line='<'+str(time.strftime("%H:%M:%S", time.localtime()))+'> : 设备离线!!!'
            if TC_flag==0:
                self.label_TC_STATE.setText("<离线>")
                self.TC__receive_text.insertPlainText(off_line)
                self.TC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                QMessageBox.critical(self, "警告", "检测计算机离线!")
                self.PID_ENTER_button.setEnabled(False)
                self.PID_CANCEL_button.setEnabled(False)
                TC_flag-=1
            if CC_flag==0:
                self.label_CC_STATE.setText("<离线>")
                self.ControlComputerReceive.setTitle('控制计算机')
                self.CC__receive_text.insertPlainText(off_line)
                self.CC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                QMessageBox.critical(self, "警告", "控制计算机离线!")
                self.PID_ENTER_button.setEnabled(False)
                self.PID_CANCEL_button.setEnabled(False)
                CC_flag-=1
            if MC_flag==0:
                self.label_MC_STATE.setText("<离线>")
                self.MoldingComputerReceive.setTitle('模型计算机')
                self.MC__receive_text.insertPlainText(off_line)
                self.MC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                QMessageBox.critical(self, "警告", "模型计算机离线!")
                self.PID_ENTER_button.setEnabled(False)
                self.PID_CANCEL_button.setEnabled(False)
                MC_flag-=1
            poll+=1
        else:
            pass

    # 接收数据
    def data_receive(self):
        global P,I,D,E,TC_flag,CC_flag,MC_flag,i,x,y,TRANSPOND_FLAG,MC_data,CC_data,TC_data,poll
        try:
            num = self.ser.inWaiting()
        except:
            self.port_close()
            return None
        if num >= 6:
            data = self.ser.read(num)
            num = len(data)
            if num>6:
                crc=calculateCRC(list(data[6:num-6])) #计算数据CRC
                crc1=crc16_10(int(data[-6]))*16*16*16+crc16_10(int(data[-5]))*16*16+crc16_10(int(data[-4]))*16+crc16_10(int(data[-3])) #提取原数据中附带的CRC
            if data[:2]==b'0A' and data[-2:]==b'\r\n':  #检测计算机
                if TC_flag<=0:
                    self.PID_ENTER_button.setEnabled(True)
                TC_flag=5
                self.label_TC_STATE.setText("<在线>")
                if data[2:4]==b'00':
                    if int(crc)==crc1:
                       #收到数据
                        data_pt='<'+str(time.strftime("%H:%M:%S", time.localtime()))+'> :'+str(dataformatting(int(data[6:6+int(data[4:6])]),num-12,False))  
                        self.TC__receive_text.insertPlainText(data_pt)
                        self.TC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                
                        # 获取到text光标
                        textCursor_TC = self.TC__receive_text.textCursor()
                        # 滚动到底部
                        textCursor_TC.movePosition(textCursor_TC.End)
                        # 设置光标到text中去
                        self.TC__receive_text.setTextCursor(textCursor_TC)
                        #转发
                        if TRANSPOND_FLAG:
                            TC_data = ('B'+'d'+str(int(data[6:6+int(data[4:6])]))).encode('utf-8')+data[-6:-2]+('\r\n').encode('utf-8')
                            tc_num = self.ser.write(TC_data)
                    else :
                        input_s = 'Af'
                        input_s = (input_s + '\r\n').encode('utf-8')
                        num = self.ser.write(input_s)
                        poll-=1
                    
            elif data[:2]==b'0B' and data[-2:]==b'\r\n':  #控制计算机
                if CC_flag<=0:
                    self.PID_ENTER_button.setEnabled(True)
                CC_flag=5
                self.label_CC_STATE.setText("<在线>")
                if data[2:4]==b'00':
                    if int(crc)==crc1:
                   #CC
                        data_pt='<'+str(time.strftime("%H:%M:%S", time.localtime()))+'> :'+str(dataformatting(int(data[6:6+int(data[4:6])]),num-12,False)) 
                        self.CC__receive_text.insertPlainText(data_pt)
                        self.CC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                
                        # 获取到text光标
                        textCursor_CC = self.CC__receive_text.textCursor()
                        # 滚动到底部
                        textCursor_CC.movePosition(textCursor_CC.End)
                        # 设置光标到text中去
                        self.CC__receive_text.setTextCursor(textCursor_CC)
                        #转发
                        CC_data = ('C'+'d'+str(int(data[6:6+int(data[4:6])]))).encode('utf-8')+data[-6:-2]+('\r\n').encode('utf-8') 
                        if TRANSPOND_FLAG:      
                            cc_num = self.ser.write(CC_data)
                    else:
                        input_s = 'Bf'
                        input_s = (input_s + '\r\n').encode('utf-8')
                        num = self.ser.write(input_s)
                        poll-=1

                 
                elif data[2:4]==b'01':
                    #参数设置成功
                    PID='控制计算机'+'<P='+str(float(self.lineEdit_P.text()))+';I='+str(float(self.lineEdit_I.text()))+';D='+str(float(self.lineEdit_D.text()))+'>'
                    self.ControlComputerReceive.setTitle(PID)
                    self.MoldingComputerReceive.setTitle('模型计算机<E='+str(float(self.lineEdit_E.text()))+'>')
                    self.PID_CANCEL_button.setEnabled(True)
                    #self.PID_ENTER_button.setEnabled(False)
                    self.Pause_button.setEnabled(True)
                    TRANSPOND_FLAG=True
                    
                elif data[2:4]==b'02':
                    #错误提示#
                    err_line='<'+str(time.strftime("%H:%M:%S", time.localtime()))+'>: 接收到的参数不正确！'
                    self.CC__receive_text.insertPlainText(err_line)
                    self.CC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                elif data[2:4]==b'04':
                    if TRANSPOND_FLAG:
                        tc_num = self.ser.write(TC_data)
                else:
                    pass
                    
                    

                    

            elif data[:2]==b'0C' and data[-2:]==b'\r\n':  #模型计算机
                  if MC_flag<=0:
                    self.PID_ENTER_button.setEnabled(True)
                  MC_flag=5
                  self.label_MC_STATE.setText("<在线>")
                  if data[2:4]==b'00':
                    if int(crc)==crc1:
                       #MC
                        data_pt='<'+str(time.strftime("%H:%M:%S", time.localtime()))+'> :'+str(dataformatting(int(data[6:6+int(data[4:6])]),num-12,False)) 
                        self.MC__receive_text.insertPlainText(data_pt)
                        self.MC__receive_text.insertPlainText((b'\r\n').decode('utf-8'))
                
                        # 获取到text光标
                        textCursor_MC = self.MC__receive_text.textCursor()
                        # 滚动到底部
                        textCursor_MC.movePosition(textCursor_MC.End)
                        # 设置光标到text中去
                        self.MC__receive_text.setTextCursor(textCursor_MC)
                        #转发
                        if TRANSPOND_FLAG:
                            MC_data = ('A'+'d'+str(int(data[6:6+int(data[4:6])]))).encode('utf-8')+data[-6:-2]+('\r\n').encode('utf-8')
                            mc_num = self.ser.write(MC_data)
                            #接收到的数据处理并显示到相应的文本框 并绘制图像
                            x.append(i)
                            i += 0.4
                            y.append(dataformatting(int(data[6:6+int(data[4:6])]),num-12,False))
                            self.curve.clear()
                            self.curve.setData(x,y)
                    else:
                        input_s = 'Cf'
                        input_s = (input_s + '\r\n').encode('utf-8')
                        num = self.ser.write(input_s)
                        poll-=1
                  elif data[2:4]==b'04':
                      if TRANSPOND_FLAG:
                        cc_num = self.ser.write(CC_data)
        else:
            pass


    # 清除显示
    def DrawArea_clear(self):
        global x,y,i
        self.curve.clear()
        x.clear()
        y.clear()
        i=0
        self.curve.setData(z=[],w=[])
    #数据接收区清除
    def receive_data_clear(self):
        self.TC__receive_text.setText("")
        self.CC__receive_text.setText("")
        self.MC__receive_text.setText("")
    #继续运行
    def Continue(self):
        global TRANSPOND_FLAG,CC_data
        TRANSPOND_FLAG=True
        self.Continue_button.setEnabled(False)
        self.Pause_button.setEnabled(True)
        cc_num = self.ser.write(CC_data)
    #暂停
    def Pause(self):
        global TRANSPOND_FLAG
        TRANSPOND_FLAG=False
        self.Continue_button.setEnabled(True)
        self.Pause_button.setEnabled(False)
    #数据保存
    def receive_data_save(self):
         global x,y
         try:
            workbook = xlwt.Workbook(encoding='utf-8')  
            booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True) 
            for i in range(len(x)):  
                booksheet.write(i,0,x[i])
                booksheet.write(i,1,y[i])
            dress=str(time.strftime('%Y-%m-%d %H.%M.%S', time.localtime()))+'.xls'
            workbook.save(dress)
            QMessageBox.about(self,"提示", "已保存！")
         except :
            QMessageBox.critical(self, "警告", "数据保存失败，请重试!")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = Pyqt5_Serial()
    myshow.show()
    sys.exit(app.exec_())