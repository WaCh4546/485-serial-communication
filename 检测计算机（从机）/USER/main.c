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
int data[50],OUTPUT; //������յ���������С�����λ��
double Out,R;
u8 Outstr[20]={'0','A','0','0','0'};
bool Flag1=false;
int Outstrsize;
float arg[4]={0};//��Ų���EPID
void DataConversion(int len,bool FLAG,int output)
{
	if(FLAG)
	{
	int i;
	for(i=0;i<len;i++)
	 {
		 data[i]=USART_RX_BUF[i]-0x30;
	 }

 }
	else
	{
		int i,j,k;
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
		Outstr[k]=0x0d;
		Outstr[k+1]=0x0a;
	}
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
	int len;
	double E,P,I,D;
  HAL_Init();                    	 	//��ʼ��HAL��    
  Stm32_Clock_Init(RCC_PLL_MUL9);   	//����ʱ��,72M
	delay_init(72);               		//��ʼ����ʱ����
	uart_init(115200);					//��ʼ������
	LED_Init();							//��ʼ��LED	
	KEY_Init();							//��ʼ������
	HAL_Delay(200);
	MX_GPIO_Init();
  while(1)
  {
    if(USART_RX_STA&0x0400) //FLAGΪ1 ������ѭ����������
	    {
				HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, GPIO_PIN_RESET);
				times=1000;
		    len=USART_RX_STA&0x007F;//�õ��˴ν��յ������ݳ���
				len=len-4;
				if(USART_RX_STA&0x8000) //���ò���
					{
					if(len==24)
					{
						DataConversion(len,true,0);
						arg[0]=data[1]*100+data[2]*10+data[3]+data[4]*0.1+data[5]*0.01;
						arg[1]=data[7]*100+data[8]*10+data[9]+data[10]*0.1+data[11]*0.01;
						arg[2]=data[13]*100+data[14]*10+data[15]+data[16]*0.1+data[17]*0.01;
						arg[3]=data[19]*100+data[20]*10+data[21]+data[22]*0.1+data[23]*0.01;
						E=arg[0];P=arg[1];I=arg[2];D=arg[3];  //������ȡ 
						if (P||I||D)
						{
							HAL_UART_Transmit(&UART1_Handler,"0B01\r\n",6,50);   //�������óɹ�
							while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET); 
							Flag1=true;
							Out=E*(P/(I*D));
							OUTPUT=Out*10000;
							DataConversion(len,false,OUTPUT+1);
						}
						else
						{
							HAL_UART_Transmit(&UART1_Handler,"0B02\r\n",6,50);   //��������ʧ��
							while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1=false;							
						}
					}
					else
						{
							HAL_UART_Transmit(&UART1_Handler,"0B02\r\n",6,50);   //��������ʧ��
							while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
							Flag1=false;							
						}
					}
				else if(USART_RX_STA&0x4000) //��ѯ
					{
						if(Flag1)
						{
							
						HAL_UART_Transmit(&UART1_Handler,Outstr,Outstrsize,50);  //���ݷ���
				    while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET);
						Flag1=false;
							
						}
						else{
						HAL_UART_Transmit(&UART1_Handler,"0A03\r\n",6,50);  //״̬�ظ�
				    while(__HAL_UART_GET_FLAG(&UART1_Handler,UART_FLAG_TC)!=SET); 
							}
					}
				else if(USART_RX_STA&0x2000) //��������
				  {
						/*int ex=1;
						DataConversion(len,true,0);
						R=data[len-1];
						for(i=len-2;i>0;i--)
						{
							ex*=10;
							R+=data[i]*ex;
						}
						if(data[0]==2)R=0-R;
						R=R/10000;
						Out=(E-R)*P/(I*D);
						OUTPUT=Out*10000;
						DataConversion(len,false,OUTPUT);*/
						int i,j;
						Flag1=true;
						if (len>=10)
						{Outstr[4]=(int)(len/10);}
						Outstr[5]=(int)(len%10)+0x30;
						for(i=6,j=0;j<len+4;i++,j++)
						{
							Outstr[i]=USART_RX_BUF[j];
						}
						Outstr[i]=0x0d;
						Outstr[i+1]=0x0a;
						Outstrsize=i+2;
						
					}
				else if(USART_RX_STA&0x0100){Flag1=false;} //ͣ��
				else if(USART_RX_STA&0x0080){Flag1=true;} //�����ط�
				else   //ʱ��ͬ��
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


			
