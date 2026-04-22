


import collections
from math import atan2, hypot
import math


class KinematicsTracker:
    def __init__(self, x,y):
        buflen = 5
        self.position_buffer = collections.deque(maxlen=buflen)
        self.velocity_buffer = collections.deque(maxlen=buflen)
        for i in range(buflen):
            self.position_buffer.append((x,y,0))

    def update(self, x,y, dt):
        self.position_buffer.append((x,y,dt))
        a_x, a_y, _ = self.position_buffer[-2]
        b_x, b_y, b_dt = self.position_buffer[-1]

        x_vel = (b_x - a_x) / b_dt
        y_vel = (b_y - a_y) / b_dt

        self.velocity_buffer.append((x_vel,y_vel))
        
    def getVelocity(self):
        return self.velocity_buffer[-1]

    @staticmethod
    def polarize(x_val, y_val):
        theta = atan2(y_val,x_val) * (180.0 / math.pi)
        mag = hypot(x_val, y_val)
        return theta, mag

    def getVelocityPolar(self):
        x_vel, y_vel = self.getVelocity()
        return KinematicsTracker.polarize(x_vel, y_vel)

    def getAvgVelocity(self):
        x_vel = 0
        y_vel = 0
        for x,y in self.velocity_buffer:
            x_vel += x
            y_vel += y
        
        x_vel /= len(self.velocity_buffer)
        y_vel /= len(self.velocity_buffer)
    
        return x_vel, y_vel

    def getAvgVelocityPolar(self):
        x_vel, y_vel = self.getAvgVelocity()
        return KinematicsTracker.polarize(x_vel, y_vel)


