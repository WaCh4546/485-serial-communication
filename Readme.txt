 crc校验功能已添加
 

主机采用Python语言，使用vs2019软件编写；GUI使用pyqt5模块编写，其中：  
serial 的包直接搜索安装
serial.tools.list_ports的包搜索pyserial安装
pyqtgraph的包直接搜索安装 安装失败的话就挂vpn安装

从机使用三台STM32单片机，使用Keil5编写，若编译不通过则把文件目录所有中文改成英文
检测计算机和模型计算机使用STM32F103C8T6; 控制计算机使用STM32F103ZET6

python打包exe使用  pyinstaller 模块，vs2019里直接搜索安装
使用时，在.py文件夹下运行CMD 输入 pyinstaller -F -w text.py  可打包生成exe文件。 其中，-w是可执行文件运行时不带控制台