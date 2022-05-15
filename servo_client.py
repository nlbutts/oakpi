import zmq
import data_pb2
import time
from enum import Enum

class State(Enum):
    PITCH_UP = 1,
    ROTATE_CCW = 2,
    PITCH_DOWN = 3,
    ROTATE_CW = 4,
    STOP = 5,


class StateMachine():
    @property
    def rotate(self):
        return self.rotate

    def rotate(self, value):
        self.rotate = value

    def pitch(self):
        return self.pitch

    def pitch(self, value):
        self.pitch = value

    def __init__(self, rotate_start = 0.5, pitch_start = 0.5, step = 0.01):
        self.state = State.PITCH_UP
        self.rotate = rotate_start
        self.pitch = pitch_start
        self.step = step

    def process(self):
        if self.state == State.PITCH_UP:
            self.pitch += self.step
            if self.pitch > 0.9:
                self.state = State.PITCH_DOWN
        elif self.state == State.PITCH_DOWN:
            self.pitch -= self.step
            if self.pitch < 0.3:
                self.state = State.ROTATE_CCW
                time.sleep(1)
        if self.state == State.ROTATE_CCW:
            self.rotate += self.step
            if self.rotate > 0.9:
                self.state = State.ROTATE_CW
                time.sleep(1)
        elif self.state == State.ROTATE_CW:
            self.rotate -= self.step
            if self.rotate < 0.30:
                self.state = State.STOP
        elif self.state == State.STOP:
            # Do nothing
            self.state = State.STOP

context = zmq.Context()
#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://oakpi:5555")

def sendcmd(rotate, pitch, socket):
    print(f'Sending command rotate: {rotate} pitch: {pitch}')
    pb = data_pb2.servo_cmd()
    pb.rotate = rotate
    pb.pitch = pitch
    message = pb.SerializeToString()
    socket.send(message)
    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {message}")

state = StateMachine()
rotate = 0.5
pitch = 0.5
while True:
    sendcmd(state.rotate, state.pitch, socket)
    state.process()
    time.sleep(0.1)



