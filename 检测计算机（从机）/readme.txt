检测计算机，通信使用USART1， PA9接RX, PA10接TX。
功能：将上位机发来的数据转发回去，模拟实际系统中，对设备输出的检测。
接发报文格式：
	接收：轮询指令 A a 0x0d 0x0a  
	          数据重发指令 A f 0x0d 0x0a         
	          数据接收 A d 符号位 数据 0x0d 0x0a    例 Ad12550060x0d0x0a  收到数据25.5006
	           	     数据采用实际数据*10000后的整型传输，符号位为1数据为正，符号位为2数据为负
	发送：状态应答 0A 03 0x0d 0x0a
	          回传数据 0A 00 符号位 数据 0x0d 0x0a
  未接收到数据时，标志位为false，收到轮询指令，只进行状态应答。收到数据后，标志位置true，收到轮询指令，进行回传数据，并将标志位再次设为false。
USART1接收协议：设置16位寄存器USART_RX_STA，进行状态标记 
	bit15：为接收参数功能标志位（功能已禁用）
	bit14：为接收轮询指令标志位
	bit13：为接收数据指令标志位
	bit12：为接收广播时间标志位(功能暂未定义)
	bit11：为接收到地址符A标志位
	bit10：为接收到0X0A,即接收完成标志位
	bit9： 为接收到0X0D标志位
	bit8： 停机标志位（未使用）
	bit7： 主机接收到的数据CRC校验错误
	bit6~bit0：为接收计数
	接收完成后数据会被存在一个字节型数组USART_RX_BUF[] 中。 协议设计每次接收数据<=50个字节。否则拒绝接收。
											2021.2.18