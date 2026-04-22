import rumps

class Controll():
    def __init__(self):
        self.activated = False
        self.rightHand = 0

# class Widget(rumps.App):
#     def __init__(self, killevent):
#         super(Widget, self).__init__(type(self).__name__, menu=['Activate', 'Left Hand', 'Clean Quit'], quit_button = None)
#         self.killevent = killevent


#     @rumps.clicked("Activate")
#     def onoff(self, sender):
#         sender.activated = not sender.activated

#     @rumps.clicked("Left Hand")
#     def left(self,Widget):
#         sender.rightHand = not sender.rightHand

#     @rumps.clicked('Clean Quit')
#     def clean_up_before_quit(self):
#         print("BRUHHh")
#         raise KeyboardInterrupt
#         rumps.quit_application()
