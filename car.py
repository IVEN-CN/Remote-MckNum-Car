"""在小车上接收体感遥控器（具有MPU6050）的指令，控制麦轮小车的运动
树莓派与驱动板的连接方式：(BCM编码方式)
    1. 5V -> 5V
    2. GND -> GND
    3. GPIO18 -> IN1
    4. GPIO23 -> IN2
    5. GPIO24 -> IN3
    6. GPIO17 -> IN4
    7. GPIO27 -> ENA
    8. GPIO22 -> ENB

要连接2个驱动板，第二个驱动板的连接方式：
    1. 5V -> 5V
    2. GND -> GND
    3. GPIO10 -> IN1
    4. GPIO9 -> IN2
    5. GPIO11 -> IN3
    6. GPIO5 -> IN4
    7. GPIO6 -> ENA
    8. GPIO13 -> ENB

其中哪些针脚控制哪几个电机：
    1. ENA -> 控制左边的2个电机
    2. ENB -> 控制右边的2个电机
    3. IN1 -> 控制左边的2个电机
    4. IN2 -> 控制左边的2个电机
    5. IN3 -> 控制右边的2个电机
    6. IN4 -> 控制右边的2个电机

"""
import RPi.GPIO as GPIO
import time
import bluetooth
import smbus

class Car:
    def __init__(self):
        # region 初始化蓝牙
        self.server_sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.port = 1
        self.server_sock.bind(("",self.port))   # 绑定端口
        self.server_sock.listen(1)  # 监听客户端的连接请求
        self.client_sock= self.server_sock.accept()[0] # 接收客户端的连接请求，返回客户端socket和地址
        # endregion

        # region 初始化引脚
        self.left_IN1 = 18
        self.left_IN2 = 23
        self.left_IN3 = 24
        self.left_IN4 = 17
        self.left_ENA = 27
        self.left_ENB = 22

        self.right_IN1 = 10
        self.right_IN2 = 9
        self.right_IN3 = 11
        self.right_IN4 = 5
        self.right_ENA = 6
        self.right_ENB = 13
        # endregion

        # region 初始化PWM
        GPIO.setmode(GPIO.BCM) # 以BCM编码格式
        GPIO.setwarnings(False)
        GPIO.setup(self.left_IN1,GPIO.OUT)
        GPIO.setup(self.left_IN2,GPIO.OUT)
        GPIO.setup(self.left_IN3,GPIO.OUT)
        GPIO.setup(self.left_IN4,GPIO.OUT)
        GPIO.setup(self.left_ENA,GPIO.OUT)
        GPIO.setup(self.left_ENB,GPIO.OUT)

        GPIO.setup(self.right_IN1,GPIO.OUT)
        GPIO.setup(self.right_IN2,GPIO.OUT)
        GPIO.setup(self.right_IN3,GPIO.OUT)
        GPIO.setup(self.right_IN4,GPIO.OUT)
        GPIO.setup(self.right_ENA,GPIO.OUT)
        GPIO.setup(self.right_ENB,GPIO.OUT)
        # endregion

