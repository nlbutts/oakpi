from numpy import maximum
from board import SCL, SDA
import busio
import time
import argparse
import data_pb2

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685
import zmq

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-f', '--freq', type=int, default=500,
                    help='The frequency to use')

args = parser.parse_args()

# Set the PWM frequency to 60hz.
pca.frequency = args.freq

# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://0.0.0.0:5555")

while True:
  message = socket.recv()
  pb = data_pb2.servo_cmd()
  pb.ParseFromString(message)
  if pb.frequency:
    print('Frequency is present')
    pca.frequency = pb.frequency
  print(pb)
  socket.send(b'OK')
  rotate = max(min(pb.rotate, 0.8), 0.2)
  pitch = max(min(pb.pitch, 0.8), 0.2)
  value1 = int(rotate * 65535)
  value2 = int(pitch * 65535)
  print(f'Capped rotate: {rotate}/{value1}  Capped pitch: {pitch}/{value2}')
  pca.channels[0].duty_cycle = value1
  pca.channels[1].duty_cycle = value2
  pca.channels[15].duty_cycle = value2
