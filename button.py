class Button:
    def __init__(self, centerX, centerY, totalW, totalH, text, color1, color2, textSize):
        self.centerX = centerX
        self.centerY = centerY
        self.totalW = totalW
        self.totalH = totalH
        self.text = text
        self.colorUnselected = color1
        self.colorSelected = color2
        self.selected = False
        self.textSize = textSize
    

    def isOnButton(self, mouseX, mouseY):
        #updates if the mouse i son button
        if self.centerX-(self.totalW/2) <= mouseX <= self.centerX+(self.totalW/2) and self.centerY-(self.totalH/2) <= mouseY <= self.centerY+(self.totalH/2):
            self.selected = True
            return True
        else:
            self.selected = False
            return False
        #return true or false

    def __repr__(self):
        return f"{self.text} button at {self.centerX}, {self.centerY}"

    def __hash__(self):
        return hash(str(self))