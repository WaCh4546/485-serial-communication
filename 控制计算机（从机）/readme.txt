控制计算机，通信使用USART1， PA9接RX, PA10接TX。
功能：将上位机发来的反馈量输入PID模型进行计算得到新的控制量，并对输出进行回传。
接发报文格式：
	接收：轮询指令 B a 0x0d 0x0a
	          数据重发指令 B f 0x0d 0x0a           
	          数据接收 B d 符号位 数据 0x0d 0x0a    例 Bd1255006 crc 0x0d0x0a  收到数据25.5006
	           	     数据采用实际数据*10000后的整型传输，符号位为1数据为正，符号位为2数据为负
	          参数接收 D c 符号位 激励数据 符号位 Kp的数据 符号位 Ki的数据 符号位 Kd的数据 0x0d 0x0a
		     数据采用固定格式，每个数据加上符号位共6位，其中激励数据为实际值*10取整，其他数据为                                     实际值*1000取整，即激励取值范围为0-9999.9，PID数据取值范围为0-99.999
	          时间同步 D b 0x0d 0x0a
	          停机指令 D e 0x0d 0x0a  停机，停止接收数据，并清空数据缓存。
	发送：状态应答 0B 03 0x0d 0x0a
	          回传数据 0B 00 符号位 数据 0x0d 0x0a
	          CRC校验错误 0B 04 0x0d 0x0a
	          参数设置正确 0B 01 0x0d 0x0a
	          参数设置错误 0B 02 0x0d 0x0a
  未收到参数设置时，标志位为false, 收到参数后 ，标志位置true，收到轮询指令，进行回传数据，并将标志位再次设为false。未接收到数据时，标志位为false，收到轮询指令，只进行状态应答。  收到数据后，标志位置true，收到轮询指令，进行回传数据，并将标志位再次设为false。
USART1接收协议：设置16位寄存器USART_RX_STA，进行状态标记 
	bit15：为接收参数功能标志位
	bit14：为接收轮询指令标志位
	bit13：为接收数据指令标志位
	bit12：为接收广播时间标志位(功能暂未定义)
	bit11：为接收到地址符B标志位
	bit10：为接收到0X0A,即接收完成标志位
	bit9： 为接收到0X0D标志位
	bit8： 为停机标记位
	bit7： 主机接收到的数据CRC校验错误
	bit6~bit0：为接收计数
	接收完成后数据会被存在一个字节型数组USART_RX_BUF[] 中。 协议设计每次接收数据<=50个字节。否则拒绝接收。

PID控制器采用增量式进行计算
    incrementSpeed=pid.Kp*(pid.err-pid.err_next)+pid.Ki*pid.err+pid.Kd*(pid.err-2*pid.err_next+pid.err_last);
    pid.ActualSpeed+=incrementSpeed;

incrementSpeed ：本次计算得出的增量
pid.ActualSpeed：本次输出+上一次的输出pid.ActualSpeed+本次增量incrementSpeed 
pid.Kp，pid.Ki，pid.Kd：PID参数
pid.err ：本次误差量 =设定值pid.SetSpeed-上一次实际输出pid.ActualSpeed
pid.err_next：前一次误差量
pid.err_last：上前一次误差量
											2021.2.18