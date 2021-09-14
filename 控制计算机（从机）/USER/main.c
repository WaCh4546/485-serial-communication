#include "sys.h"
#include "delay.h"
#include "usart.h"
#include "led.h"
#include "key.h"
#include "math.h"
#include "stdbool.h"
#include "string.h"
#include "stdlib.h"
u16 times=0;
int data[50],OUTPUT; 
float Out,R;
u8 Outstr[50]={0x30,0x42,0x30,0x30};
int Outstrsize;
int Flag1=0;
float arg[4]={0};//存放参数EPID

struct _pid{
    float SetSpeed;          
    float ActualSpeed;        
    float err;               
    float err_next;           
    float err_last;           
    float Kp,Ki,Kd;           
}pid;

void PID_init(){
    pid.SetSpeed=0.00;
    pid.ActualSpeed=0.00;
    pid.err=0.0000;
    pid.err_last=0.0000;
    pid.err_next=0.0000;
    pid.Kp=0.00;
    pid.Ki=0.00;
    pid.Kd=0.00;
}

unsigned short Crc(int LEN,u8 CRCBUFFER[],int j)
{

	int n,i;
	unsigned short tmp = 0xffff;
  
	 for (n = j; n < LEN; n++) {
        tmp = CRCBUFFER[n] ^ tmp;
        for (i = 0; i < 8; i++) {  
            if (tmp & 0x01) {
                tmp = tmp >> 1;
                tmp = tmp ^ 0xa001;
            }
            else {
                tmp = tmp >> 1;
            }
        }
    }
	 return (int)(tmp);
}

void DataConversion(int len,bool FLAG,int output)
{
	if(FLAG)
	{
	int i;
	for(i=0;i<len;i++)
	 {
		 if (USART_RX_BUF[i]>0x60)data[i]=USART_RX_BUF[i]-0x61+10;
		 else data[i]=USART_RX_BUF[i]-0x30;
	 }

 }
	else
	{
		int i,j,k,crc;
		int buf=output;
		int a[50];
		buf=abs(buf);
		for(i=0;buf>=1;i++)
		{
			a[i]=buf%10;
			buf=buf/10;
		}
		i+=1;
		Outstr[5]=i%10+0x30;
		if(i>=10)Outstr[4]=(int)(i/10)+0x30;
		else Outstr[4]=0x30;
		if(output<0)Outstr[6]=0x32;
		else Outstr[6]=0x31;
		for(j=i-2,k=7;j>=0;j--,k++)
		{
			Outstr[k]=a[j]+0x30;
		}
		crc=Crc(k,Outstr,6);
		if((int)(crc/(16*16*16))>9) Outstr[k]=(int)(crc/(16*16*16))-9+0x60;
		else Outstr[k]=(int)(crc/(16*16*16))+0x30;
		crc%=16*16*16;
		if((int)(crc/(16*16))>9) Outstr[k+1]=(int)(crc/(16*16))-9+0x60;
		else Outstr[k+1]=(int)(crc/(16*16))+0x30;
		crc%=16*16;
		if((int)(crc/(16))>9) Outstr[k+2]=(int)(crc/(16))-9+0x60;
		else Outstr[k+2]=(int)(crc/(16))+0x30;
		crc%=16;
		if(crc>9) Outstr[k+3]=crc-9+0x60;
		else Outstr[k+3]=crc+0x30;
		Outstr[k+4]=0x0d;
		Outstr[k+5]=0x0a;
		Outstrsize=k+6;
	}
}


float PID_realize(){
	  float incrementSpeed;
    pid.err=pid.SetSpeed-pid.ActualSpeed;
    incrementSpeed=pid.Kp*(pid.err-pid.err_next)+pid.Ki*pid.err+pid.Kd*(pid.err-2*pid.err_next+pid.err_last);
    pid.ActualSpeed+=incrementSpeed;
    pid.err_last=pid.err_next;
    pid.err_next=pid.err;
    return pid.ActualSpeed;
}

int main(void)
{
	int i,len;
  HAL_Init();                    	 	//初始化HAL库    
  Stm32_Clock_Init(RCC_PLL_MUL9);   	//设置时钟,72M
	delay_init(72);               		//初始化延时函数
	uart_init(115200);					//初始化串口
	LED_Init();							//初始化LED	
	KEY_Init();							//初始化按键
	HAL_Delay(200);
	PID_init();
	
  while(1)
  {
    if(USART_RX_STA&0x0400) //FLAG为1 则启动循环接收命令
	    {
		    len=USART_RX_STA&0x007F;//得到此次接收到的数据长度
				LED0=0;
				times=1000;
				if(USART_RX_STA&0x8000) //设置参数
					{
					unsigned short tmp;
					int crc;
					//PID_init();
					tmp=Crc(24,USART_RX_BUF,0);
					DataConversion(len,true,0);
					arg[0]=data[1]*1000+data[2]*100+data[3]*10+data[4]+data[5]*0.1;
					arg[1]=data[7]*10+data[8]+data[9]*0.1+data[10]*0.01+data[11]*0.001;
					arg[2]=data[13]*10+data[14]+data[15]*0.1+data[16]*0.01+data[17]*0.001;
					arg[3]=data[19]*10+data[20]+data[21]*0.1+data[22]*0.01+data[23]*0.001;
					pid.SetSpeed=arg[0];pid.Kp=arg[1];pid.Ki=arg[2];pid.Kd=arg[3];  //参数提取 
					if(len==27)crc=data[26]+data[25]*16+data[24]*16*16;
					else if(len==28)crc=data[27]+data[26]*16+data[25]*16*16+data[24]*16*16*16;// crc校验码提取
					if (tmp==crc)
					{
						HAL_UART_Transmit(&UART1_Handler,"0B01\r\n",6,50);   //参数设置成功
						while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET); 
						Flag1=true;
						Out=PID_realize();
						OUTPUT=Out*10000;
						DataConversion(len,false,OUTPUT);
						LED1=0;
						}
						else
						{
							HAL_UART_Transmit(&UART1_Handler,"0B02\r\n",6,50);   //参数设置失败
							while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1=false;
							LED1=1;
						}
				
					}
				else if(USART_RX_STA&0x4000) //轮询
					{
						if(Flag1!=0)
						{
							
							HAL_UART_Transmit(&UART1_Handler,Outstr,Outstrsize,50);  //状态回复
				      while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1-=1;
							
						}
						else{
						HAL_UART_Transmit(&UART1_Handler,"0B03\r\n",6,50);  //状态回复
				    while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET); 
							}
					}
				else if(USART_RX_STA&0x2000) //接收数据
				  {
						int ex=1;
						DataConversion(len,true,0);
						if(Crc(len-3,USART_RX_BUF,0)==data[len-1]+data[len-2]*16+data[len-3]*16*16)len=len-3;  //适用于CRC校验码为3位
						else if(Crc(len-4,USART_RX_BUF,0)==data[len-1]+data[len-2]*16+data[len-3]*16*16+data[len-4]*16*16*16)len=len-4; //适用于CRC校验码为4位
						else{
							HAL_UART_Transmit(&UART1_Handler,"0B04\r\n",6,50);  //接受数据错误
				      while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1=3;
							USART_RX_STA=0;
							continue;
						}
						R=data[len-1];
						for(i=len-2;i>0;i--)
						{
							ex*=10;
							R+=data[i]*ex;
						}
						if(data[0]==2)R=0-R;
						R=R/10000;
						pid.ActualSpeed=R;
						Out=PID_realize();
						OUTPUT=Out*10000;
						DataConversion(len,false,OUTPUT);
						Flag1=3;
					}
				else if(USART_RX_STA&0x0100){PID_init();LED1=1;Flag1=0;} //停机
				else if(USART_RX_STA&0x0080){Flag1=3;} //数据重发
				else   //时间同步
					{}				
	      USART_RX_STA=0;
	    }
			else
			{
				times--;
				HAL_Delay(1);
				if(times==0)LED0=1;
			}
			
   } 
}


			
