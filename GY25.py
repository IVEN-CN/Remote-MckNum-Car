"""GY25陀螺仪读取角度测试文件，并且显示在OLED上"""
import serial
import struct
import os
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
from PIL import ImageFont

class GY25:
    def __init__(self, port='/dev/ttyS5', baudrate=115200):
        self.ser = serial.Serial(port, baudrate)

    def read_angle(self):
        while True:
            data = self.ser.read(8)  # 读取8个字节的数据
            if len(data) == 8 and data[0] == 0xAA:  # 检查数据包的头部
                yaw, pitch, roll = struct.unpack('<hhh', data[1:7])  # 解析数据包，<hhh表示3个16位整数
                # 分别对应yaw、pitch、roll，数据类型为小端字节序，即低位在前，高位在后
                return yaw / 100.0, pitch / 100.0, roll / 100.0  # 返回角度信息

class OLED():
    def __init__(self, port, add) -> None:
        self.port = port
        self.address = add
        # 创建一个I2C接口的实例
        serial = i2c(port=self.port, address=self.address)
        self.device = ssd1306(serial)
        self.font = ImageFont.load_default()
    def write_text(self, text):
        with canvas(self.device) as draw:
            draw.text((0, 0), text, font=self.font, fill="white")

if __name__ == '__main__':
    gy25 = GY25()
    oled = OLED(3, 0x3C)
    while True:
        yaw, pitch, roll = gy25.read_angle()
        os.system('clear')
        print('偏航角:', yaw, '\n俯仰角:', pitch, '\n滚动角:', roll)
        # 在画布上绘制文本
        oled.write_text('偏航角: %s\n俯仰角: %s\n滚动角: %s' % (yaw, pitch, roll))
