
from ctypes import pointer
import math
from syslog import LOG_LOCAL2
import time
import pyautogui
from multiprocessing.connection import _ConnectionBase
import scripts.macApi
from utils.ScreenControllerPayload import ScreenControllerPayload
from utils.KinematicsTracker import KinematicsTracker
import numpy as np
from utils.Buffer import Buffer
lastPayload= None

# we are hacking this.... this is not a good idea for a final product:) 
def toggleKeyboard():
    pos = pyautogui.position()
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(0,pyautogui.size()[1])
    time.sleep(0.2)
    pyautogui.moveTo(pos[0], pos[1])
    # print("Click")
    # pyautogui.moveTo(pos[0], pos[1])

pointerState = False
pointerBufferDown = Buffer(5) 


def togglePointer():
    pyautogui.press("l")

    
def handleAction(action):
    global pointerState
    if action:
        keys = list(action.keys())
        the_action = keys[0]
        global pointerErrorBuff
        if the_action == "keyboard":
            print("keyboard")
            toggleKeyboard()
        elif "move" in keys:
            if "right" in keys:
                pyautogui.press("right")
            elif "left" in keys:
                pyautogui.press("left")
            elif pointerState:
                togglePointer()
                pointerState = False
        elif the_action == "pointer" and not pointerState:
            pointerState = True
            togglePointer()
    else:
        if pointerState:
            togglePointer()
            pointerState = False

    # print(pointerState)
SwipeErrorBuffer = 0

def Overscan(origin, point, overscan):
    t_x = origin[0] - point[0]
    t_y = origin[1] - point[1]

    h = math.hypot(t_x, t_y) * overscan
    theta = math.atan2(t_y, t_x)

    p = (h * math.cos(theta), h * math.sin(theta))
    return (p[0] + origin[0], p[1] + origin[1])
    
def MouseController(connection: _ConnectionBase, kill_event):
    print('MouseController: Runn ing', flush=True)
    payload: ScreenControllerPayload = connection.recv()
    while not payload.x:
        payload: ScreenControllerPayload = connection.recv()
          # this statement is blocking
    
    payload = payload.scale(pyautogui.size()[0], pyautogui.size()[1])
    scripts.macApi.toggle_keyboard()
    handTracker = KinematicsTracker(payload.x, payload.y)
    lastPointer = False
    seconds = time.time()
    while True:
        lastPayload = payload
        if connection.poll():  # checks if there is a message that must be recieved
            payload: ScreenControllerPayload = connection.recv()  # this statement is blocking
            if payload is None:  # None is our break case. Send it from ScreenController to kill the MouseController
                print("PAYLOAD WAS NONE... BREAKING", flush=True)
                break
            # payload is [0,1], we need to scale it up to the size of the display
            # print(payloadppppppppppphelllll.[])
            #TODO: Fix overscan by transforming GUI to the center
            OVERSCAN = 0
            
            payload = payload.scale((pyautogui.size()[0]), (pyautogui.size()[1]))
            if payload.x:
                new_cursor = Overscan((pyautogui.size()[0]/2, pyautogui.size()[1]/2), (payload.x, payload.y), -1.3)
                payload.x = new_cursor[0]
                payload.y = new_cursor[1]
            

            if payload.x and payload.hands == 1:
                handTracker.update(payload.x, payload.y, time.time()-seconds)
                seconds = time.time()
                xvel, yvel = handTracker.getAvgVelocity()
                global SwipeErrorBuffer
                if abs(xvel) > 450 and SwipeErrorBuffer > 7 and abs(yvel) < 100:
                    # print(abs(xvel), abs(yvel))
                    SwipeErrorBuffer = 0
                    print("SWIPED " + ( "right" if np.sign(xvel) > 0 else "left"))
                    if np.sign(xvel) > 0:
                        if payload.action is not None:
                            payload.action["left"] = True
                        else:
                            payload.action = {"left": True}
                    else:
                        if payload.action is not None:
                            payload.action["right"] = True
                        else:
                            payload.action = {"right": True}
                else: 
                    SwipeErrorBuffer += 1
                    print("...")
                print(payload)
            
        # print(f'>receiver got {str(mouse)}', flush=True)
        # print("PAYLOAD" payload)
        if payload.present:
            # adding physics to the mouse???
            if payload.pressedR and not lastPayload.pressedR:
                pyautogui.mouseDown(button="right")
            elif not payload.pressedR and lastPayload.pressedR:
                pyautogui.mouseUp(button="right")
            if payload.pressedL and not lastPayload.pressedL:
                pyautogui.mouseDown(button="left")
            elif not payload.pressedL and lastPayload.pressedL:
                pyautogui.mouseUp(button="left")
            # print(f"ACTION:     {payload.action}")
            handleAction(payload.action)

            dx = payload.x - pyautogui.position()[0]
            dy = payload.y - pyautogui.position()[1]

            new_x = pyautogui.position()[0] + dx * payload.getEaseFactor()
            new_y = pyautogui.position()[1] + dy * payload.getEaseFactor()

            pyautogui.moveTo(new_x, new_y, _pause=False)

            time.sleep(0.04)

        else:
            handleAction(None)
        if kill_event.is_set():
            # scripts.macApi.toggle_keyboard()
            break
    # all done
    print('Receiver: Done', flush=True)
