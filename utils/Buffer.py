class Buffer:
    def __init__(self, cap):
        self.cap = cap
        self.count = 0

    def inc(self):
        if self.count < self.cap:
            self.count += 1
    def dec(self):
        if self.count > 0:
            self.count -= 1
    def reset(self):
        self.count = 0

    def checkUp(self):
        return self.count == self.cap

    def checkDown(self):
        return self.count == 1