# serial_protocol.py 修改部分
import struct
import serial

class SerialProtocol():
    HEAD = 0xAA
    TAIL = 0x55
    
    # 标签定义
    TAG_LASER_POINT = 0x01    # 激光点
    TAG_RECT_CENTER = 0x00    # 矩形中心点

    def __init__(self, port='/dev/ttyS0', baudrate=9600) -> None:
        """初始化串口连接"""
        self.ser = serial.Serial(port, baudrate)
    
    def build_packet(self, tag: int, x: int, y: int) -> bytes:
        """
        构建数据包: AA + 标签 + x低8位 + x高8位 + y低8位 + y高8位 + 55
        标签: 0x01=激光点, 0x00=矩形中心点
        """
        packet = bytearray()
        packet.append(self.HEAD)
        packet.append(tag)
        packet += bytes([x & 0xFF, (x >> 8) & 0xFF])
        packet += bytes([y & 0xFF, (y >> 8) & 0xFF])
        packet.append(self.TAIL)
        return bytes(packet)
    
    def send_laser_point(self, x: int, y: int) -> None:
        """发送激光点坐标"""
        packet = self.build_packet(self.TAG_LASER_POINT, x, y)
        self.ser.write(packet)
    
    def send_rect_center(self, x: int, y: int) -> None:
        """发送矩形中心点坐标"""
        packet = self.build_packet(self.TAG_RECT_CENTER, x, y)
        self.ser.write(packet)
    
    def close(self) -> None:
        """关闭串口连接"""
        if self.ser.is_open:
            self.ser.close()
    
    def __del__(self):
        """析构函数，确保串口被关闭"""
        self.close()