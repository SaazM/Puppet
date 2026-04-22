from abc import abstractclassmethod
from re import L
import pyautogui

def clamp(minimum, maximum, v):
    return min(maximum, max(minimum, v))



# class ScreenControllerAction: 
#     def __init__(self, title):
#         self.title = title
    
#     @abstractclassmethod
#     def execute(self):
#         pass




class ScreenControllerPayload:
    def __init__(self, x, y, pressedL, pressedR, action, hands, present=True):
        self.x = x
        self.y = y
        self.pressedL = pressedL
        self.pressedR = pressedR
        self.action = action
        self.hands = hands
        self.present = present
        
        self.easeFactor = 0.4

    @staticmethod
    def createNull():
        return ScreenControllerPayload(None, None, None, None, None, None, present=None)

    def __str__(self):
        return f"ScreenControllerPayload({self.x}, {self.y}, {self.pressedL}, {self.pressedR}, {self.action}, {self.hands}, {self.present})"

    def setEaseFactor(self, factor):
        self.easeFactor = factor

    def getEaseFactor(self):
        # value belongs to (0,1), the higher the value the less intense gravity is
        return self.easeFactor

    def scale(self, x_scale, y_scale):
        if self.present:
            return ScreenControllerPayload(clamp(0,pyautogui.size()[0],  self.x * x_scale), clamp(0, pyautogui.size()[1], self.y * y_scale), self.pressedL, self.pressedR, self.action, self.hands,  self.present)
        return ScreenControllerPayload.createNull()