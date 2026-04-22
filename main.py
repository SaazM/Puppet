import asyncio
from multiprocessing import Event, Pipe
from multiprocessing.dummy import Process
from os import kill
import time

from utils.HandHandler import HandHandler
from utils.ScreenController import MouseController

import keyboard

if __name__ == "__main__":
    try:
        kill_event = Event()  # when this event is "set", the program will terminate
        # create the pipe
        conn1, conn2 = Pipe(False)
        # start the sender
        HandTracker_process = Process(
            target=HandHandler, args=(conn2, kill_event))
        HandTracker_process.start()
        # start the receiver
        MouseController_process = Process(
            target=MouseController, args=(conn1, kill_event))
        MouseController_process.start()

        # after the space key is pressed, the kill signal will be sent
        keyboard.wait('space')
        raise KeyboardInterrupt

    except KeyboardInterrupt:

        kill_event.set()
        HandTracker_process.join()
        MouseController_process.join()

    # wait for all processes to finish

# import rumps

# class AwesomeStatusBarApp(rumps.App):
#     @rumps.clicked("Preferences")
#     def prefs(self, _):
#         rumps.alert("jk! no preferences available!")


#     @rumps.clicked("Say hi")
#     def sayhi(self, _):
#         rumps.notification("Awesome title", "amazing subtitle", "hi!!1")

# if __name__ == "__main__":
#     AwesomeStatusBarApp("Puppet").run()