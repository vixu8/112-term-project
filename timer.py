import time

class Timer:
    def __init__(self, time):
        self.timeLeft = int(time)
        self.paused = True
    
    def pause(self):
        self.paused = True
    
    def unpause(self):
        self.paused = False
    
    def __repr__(self):
        return f"{self.timeLeft} left in timer, "+ ("un" if not (self.paused) else "" ) + "paused"
    
    def process(self):
        if not self.paused:
            self.timeLeft -= 1/60 #since im running 100 steps per second
    

