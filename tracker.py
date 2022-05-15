#!/usr/bin/env python3

import numpy as np
import zmq
import data_pb2

class Tracker():

    _step = 0

    def get_rotate(self):
        return self._rotate

    def set_rotate(self, value):
        if value > 1:
            value = 1
        elif value < 0:
            value = 0
        self._rotate = value

    rotate = property(get_rotate, set_rotate)

    def get_pitch(self):
        return self._pitch

    def set_pitch(self, value):
        if value > 1:
            value = 1
        elif value < 0:
            value = 0
        self._pitch = value

    pitch = property(get_pitch, set_pitch)

    def __init__(self, rotate_start = 0.5, pitch_start = 0.6, step = 0.001):
        self._rotate = rotate_start
        self._pitch = pitch_start
        self._step = step

        self.context = zmq.Context()
        #  Socket to talk to server
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://oakpi:5555")
        self.sendcmd()

    def sendcmd(self):
        pb = data_pb2.servo_cmd()
        pb.rotate = self.rotate
        pb.pitch = self.pitch
        print(pb)
        message = pb.SerializeToString()
        self.socket.send(message)
        #  Get the reply.
        message = self.socket.recv()
        #print(f"Received reply {message}")

    def ccw(self):
        self.rotate += self._step
        #print(f'rotating ccw {self._rotate}')

    def cw(self):
        self.rotate -= self._step
        #print(f'rotating cw {self._rotate}')

    def pitch_up(self):
        self.pitch += self._step

    def pitch_down(self):
        self.pitch -= self._step

    def update_tracker(self, x1, x2, y1, y2, spartial_info):
        center_x = (x2 + x1) // 2
        center_y = (y2 + y1) // 2
        #print(f'Center_x: {center_x} {x1} - {x2} - {spartial_info.z}')
        #print(f'Center_y: {center_y} {y1} - {y2} - {spartial_info.z}')
        if center_x > (150 + 20):
            self.cw()
        elif center_x < (150 - 20):
            self.ccw()
        # if center_y > (150 + 20):
        #     self.pitch_down()
        # elif center_y < (150 - 20):
        #     self.pitch_up()

        self.sendcmd()