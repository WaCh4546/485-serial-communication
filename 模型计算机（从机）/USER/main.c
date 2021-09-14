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
int data[50],OUTPUT; //定义接收到的数据中小数点的位置
float Out,R;
u8 Outstr[50]={0x30,0x43,0x30,0x30};
int Outstrsize;
bool Flag1=false;
float arg[4]={0};//存放参数EPID

struct _modle{
    float InertiaTime ;          
    float ResultValueBack ;        
    float SampleTime ;               
    float PidOutput; 
		float SystemOutput;
}modle;

void modle_init(){
    modle.InertiaTime=3.0000;
    modle.ResultValueBack=0.00;
    modle.SampleTime=0.4000;
    modle.PidOutput=0.0000;
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
		int a[20];
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


float modle_realize(){
    modle.SystemOutput = (modle.InertiaTime * modle.ResultValueBack + modle.SampleTime * modle.PidOutput) / (modle.SampleTime + modle.InertiaTime);
	  modle.ResultValueBack = modle.SystemOutput;
    return modle.SystemOutput;
}

static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOC_CLK_ENABLE();
  __HAL_RCC_GPIOD_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);

  /*Configure GPIO pin : PC13 */
  GPIO_InitStruct.Pin = GPIO_PIN_13;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOC, &GPIO_InitStruct);
	
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
	modle_init();
	MX_GPIO_Init();

  while(1)
  {
    if(USART_RX_STA&0x0400) //FLAG为1 则启动循环接收命令
	    {
				HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
				times=1000;
		    len=USART_RX_STA&0x007F;//得到此次接收到的数据长度
				
				if(USART_RX_STA&0x8000) //设置参数
					{
					//modle_init();
					}
				else if(USART_RX_STA&0x4000) //轮询
					{
						if(Flag1)
						{
							
							HAL_UART_Transmit(&UART1_Handler,Outstr,Outstrsize,50);  //状态回复
				      while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1=false;
							
						}
						else{
						HAL_UART_Transmit(&UART1_Handler,"0C03\r\n",6,50);  //状态回复
				    while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET); 
							}
					}
				else if(USART_RX_STA&0x2000) //接收数据
				  {
						int ex=1;
						DataConversion(len,true,0);
						if(Crc(len-3,USART_RX_BUF,0)==data[len-1]+data[len-2]*16+data[len-3]*16*16)len=len-3;
						else if(Crc(len-4,USART_RX_BUF,0)==data[len-1]+data[len-2]*16+data[len-3]*16*16+data[len-4]*16*16*16)len=len-4;
						else{
							HAL_UART_Transmit(&UART1_Handler,"0C04\r\n",6,50);  //接受数据错误
				      while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1=false;
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
						modle.PidOutput=R;
						Out=modle_realize();
						OUTPUT=Out*10000;
						DataConversion(len,false,OUTPUT);
						Flag1=true;
					}
				else if(USART_RX_STA&0x0100){modle_init();Flag1=false;} //停机
				else if(USART_RX_STA&0x0080){Flag1=true;} //数据重发
				else   //时间同步
					{}				
	      USART_RX_STA=0;
	    }
			else
			{
				times--;
				HAL_Delay(1);
				if(times==0)HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_SET);
			}
			
   } 
}


			
