
import cv2
import mediapipe as mp
import math


class Hand:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.05, minTrackCon=0.5):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        # def init(self, mode=False, maxHands=2,modelC=1, detectionCon=0.5, trackCon=0.5):
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1,
                                        self.detectionCon, self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

        self.averagez = []
        self.nomHands = 0

    def findHands(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        self.lmList = []
        if self.results.multi_hand_landmarks:

            for handNo in range(len(self.results.multi_hand_landmarks)):
                xList = []
                yList = []
                zList = []
                lmListCurr = []
                myHand = self.results.multi_hand_landmarks[handNo]
                for id, lm in enumerate(myHand.landmark):
                    xList.append(lm.x)
                    yList.append(lm.y)
                    zList.append(lm.z)
                    lmListCurr.append([lm.x, lm.y, lm.z])
                self.averagez.append(sum(zList)/len(zList))
                self.lmList.append(lmListCurr)

        return self.lmList

    def findStandD(self, id, draw=True):
        zList = []
        for el in self.lmList[id]:
            zList.append(el[2])

        if (1 == 9):
            return True
        return False

    def findDistance(self, p1, p2, img, id, draw=True):


        if self.results.multi_hand_landmarks:

            x1, y1 = self.lmList[id][p1][0], self.lmList[id][p1][1]
            x2, y2 = self.lmList[id][p2][0], self.lmList[id][p2][1]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            length = math.hypot(x2 - x1, y2 - y1)
            return length, img, [x1, y1, x2, y2, cx, cy]

    def handType(self):

        if self.results.multi_hand_landmarks:
            if self.lmList[17][0] < self.lmList[5][0]:
                return "Right"
            else:
                return "Left"

    # def direction(self):
    #     if self.results.multi_hand_landmarks:
    #         if self.lmlist[8][0] < self.lmlist[20][0]:
    #             return "Right"
    #         else:
    #             return "Left"


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bboxInfo = detector.findPosition(img)
        print(detector.handType())

        cv2.imshow("Image", img)

if __name__ == "__main__":
    main()

