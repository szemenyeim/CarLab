import spidev
import struct


class CarControl(object):
    def __init__(self, bus=0, device=1):
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = 100000


    def setSpeed(self, speed):
        to_send = [0x00, 0x00, 0x00, 0x0A, 0x56]
        speed = float(speed)
        if speed < -1.0 or speed > 1.0:
            print("Speed must be between -1 and 1")
            return
        ba = bytearray(struct.pack("f", speed))
        for b in ba:
            to_send.append(b)
        to_send.append(0x00)
        self.spi.xfer(to_send)


    def start(self):
        to_send = [0x00, 0x00, 0x00, 0x0A, 0x47, 0x02, 0x00, 0x00, 0x00, 0x00]
        self.spi.xfer(to_send)


    def stop(self):
        to_send = [0x00, 0x00, 0x00, 0x0A, 0x53, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.spi.xfer(to_send)


    def steer(self, direction):
        to_send = [0x00, 0x00, 0x00, 0x0A, 0x73]
        direction = float(direction)
        if direction < -0.3 or direction > 0.3:
            print("Direction must be between -0.3 and 0.3")
            return
        ba = bytearray(struct.pack("f", direction))
        for b in ba:
            to_send.append(b)
        to_send.append(0x00)
        self.spi.xfer(to_send)
