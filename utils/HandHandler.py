from multiprocessing.connection import _ConnectionBase
from os import kill
import cv2
from utils.Hand import Hand
from utils.ScreenController import ScreenControllerPayload
from time import sleep
from utils.Buffer import Buffer
import numpy as np
import time
import pickle
import os
import math
import mediapipe as mp


BUFFER = {
    'move': Buffer(4),
    'clicked': Buffer(10),
    'pointer': Buffer(6),
    'openKeyboard': Buffer(4),
    'closeKeyboard': Buffer(4),   
}

MP_HANDS = mp.solutions.hands


def Keyboard(detector, img):
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if lmList:
            min = 1
            minId = 0
            for id, lmHand in enumerate(lmList):
                if lmHand[9][2] < min:
    
                    min = lmHand[9][2]
                    minId = id

            x = lmList[minId][9][0]
            y = lmList[minId][9][1]

            l, _, _ = detector.findDistance(8, 7, img, 0, draw=False)
            l2, _, _ = detector.findDistance(16, 13, img, 0, draw=False)

            # when clicked
            if l < l2/6.5:
                pressed = True
    
            else:
                pressed = False
            return True, (x, y, pressed, lmList[minId][0][0], len(lmList))

        else:
            return False, ()

def dist_to_point(wrist, other):
    return math.sqrt((wrist.x - other.x) ** 2 + (wrist.y - other.y) ** 2 + (wrist.z - other.z) ** 2)

def process_landmarks(landmarks):
    if landmarks.multi_hand_world_landmarks:
        hand_landmarks = landmarks.multi_hand_world_landmarks[0]
        wrist_coord = hand_landmarks.landmark[MP_HANDS.HandLandmark.WRIST]  # Index of 0
        other_coords = hand_landmarks.landmark[MP_HANDS.HandLandmark.THUMB_CMC:]  # Index of 1 and onwards
        delta_landmarks = [dist_to_point(wrist_coord, coord) for coord in other_coords]
        return delta_landmarks
    else:
        return None

def find_direction(landmarks):
    if landmarks[8][0] < landmarks[20][0]:
        return 'r'
    else:
        return 'l'

commands = {
    'direction': None, 
    'openKeyboard': False, 
    'closeKeyboard': False, 
    'move': False, 
    'clicked': False, 
    'pointer': False,
    'pointerPoint': None,
}

def Gesture(frame, model, clusters):
    global commands
    with MP_HANDS.Hands(max_num_hands=2, min_detection_confidence=0.01, model_complexity=1,
                        static_image_mode=True) as hands:
        results = hands.process(frame)
        new_landmarks = process_landmarks(results)

        moveBuffer = BUFFER['move']
        pointerBuffer = BUFFER['pointer']
        clickedBuffer = BUFFER['clicked']

        openKeyboardBuffer = BUFFER['openKeyboard']
        closeKeyboardBuffer = BUFFER['closeKeyboard'] 

        if new_landmarks is not None:
            hand_landmarks = results.multi_hand_world_landmarks[0]
            hand_landmarks_list = [(landmark.x, landmark.y, landmark.z) for landmark in hand_landmarks.landmark]
            direc = find_direction(hand_landmarks_list)
            commands["direction"] = direc

            newer_landmarks = np.expand_dims(new_landmarks, axis=0).reshape(1, -1).tolist()
            corrected_landmarks = np.array(newer_landmarks).astype('float32')
            out = model.predict(corrected_landmarks)[0]
            dist = np.linalg.norm(clusters[out] - corrected_landmarks)

            movePressed = True if out == 1 else False
            clickedPressed = True if out == 0 else False
            pointerPressed = True if out == 2 else False

            openKeyboardPressed = True if movePressed and len(results.multi_hand_landmarks) == 2 else False
            closeKeyboardPressed = True if clickedPressed and len(results.multi_hand_landmarks) == 2 else False

            commands['pointerPoint'] = hand_landmarks_list[0]

            if closeKeyboardPressed:
                closeKeyboardBuffer.inc()
                if closeKeyboardBuffer.checkUp():
                    commands['closeKeyboard'] = True
            else:
                closeKeyboardBuffer.dec()
                if closeKeyboardBuffer.checkDown():
                    commands['closeKeyboard'] = False

            if openKeyboardPressed:
                openKeyboardBuffer.inc()
                if openKeyboardBuffer.checkUp():
                    commands['openKeyboard'] = True
            else:
                openKeyboardBuffer.dec()
                if openKeyboardBuffer.checkDown():
                    commands['openKeyboard'] = False


            if movePressed and not openKeyboardPressed:
                moveBuffer.inc()
                if moveBuffer.checkUp():
                    commands['move'] = True
            else:
                moveBuffer.dec()
                if moveBuffer.checkDown():
                    commands['move'] = False



            if clickedPressed and not closeKeyboardPressed:
                clickedBuffer.inc()
                if clickedBuffer.checkUp():
                    commands['clicked'] = True
            else:
                clickedBuffer.dec()
                if clickedBuffer.checkDown():
                    commands['clicked'] = False


            if pointerPressed:
                pointerBuffer.inc()
                if pointerBuffer.checkUp():
                    commands['pointer'] = True
            else:
                pointerBuffer.dec()
                if pointerBuffer.checkDown():
                    commands['pointer'] = False
            
        else:
            closeKeyboardBuffer.dec()
            if closeKeyboardBuffer.checkDown():
                commands['closeKeyboard'] = False

            openKeyboardBuffer.dec()
            if openKeyboardBuffer.checkDown():
                commands['openKeyboard'] = False

            moveBuffer.dec()
            if moveBuffer.checkDown():
                commands['move'] = False

            clickedBuffer.dec()
            if clickedBuffer.checkDown():
                commands['clicked'] = False

            pointerBuffer.dec()
            if pointerBuffer.checkDown():
                commands['pointer'] = False

    return commands

def keyboardDouble(data, timeLast, last_x, last_y):
    if math.sqrt((data[0]-last_x)**2+(data[1]-last_y)**2)<0.5:
        if time.time()-timeLast > 10:
            return data[2]

        else:
            return False
    else:
        return data[2]

    

def HandHandler(connection: _ConnectionBase, kill_event):
    print('HandHandler: Running', flush=True)
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = Hand(detectionCon=0.8)
    model = pickle.load(open('model/model.pkl', 'rb'))
    clusters = model.cluster_centers_

    last_x = 0
    last_y = 0
    timeLast = time.time()

    keyboardToggle = False
    clickerToggle = False
    
    while True:
        payload = ScreenControllerPayload.createNull()
        
        success, orig_image = cap.read()
        img = cv2.flip(orig_image, 1)

        ret, data = Keyboard(detector, img)
        commands  = Gesture(orig_image, model, clusters)

        if commands['openKeyboard'] and not keyboardToggle:
            payload.action = {'keyboard': True}
            keyboardToggle = True
        
        if commands['closeKeyboard'] and keyboardToggle:
            payload.action = {'keyboard': False}
            keyboardToggle = False

        
        if commands['pointer']:
            payload.action = {"pointer": True}
            payload.setEaseFactor(0.35)

        if commands['move']:
            payload.action = {"move": True}
            payload.setEaseFactor(0.35)
        
        if ret:
            payload.x = data[0]
            payload.y = data[1]
            payload.hands = data[4]
            payload.present = True
        else:
            payload.hands = 0
            payload.present = False

        if keyboardToggle:
            if ret:
                keyboardPress = keyboardDouble(data, timeLast, last_x, last_y)
                if keyboardPress:
                    last_x = data[0]
                    last_y = data[1]
                    timeLast = time.time()
                payload.pressedR = data[2]
            else:
                payload.pressedR = False
            payload.pressedL = False
            
            
        else:
            
            if commands['clicked'] and not clickerToggle:
                clickerToggle = True

            if commands['move'] and clickerToggle:
                clickerToggle = False
            
            if clickerToggle:
                if commands['direction'] == 'r':
                    payload.pressedR = True
                elif commands['direction'] == 'l':
                    payload.pressedL = True

                payload.y += 0.01

        # print(payload)
        # print(commands)
        # print()
        connection.send(payload)

        
        cv2.waitKey(60)
        if kill_event.is_set():
            # kill process :
            break

    cap.release()

