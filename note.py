class Note:
    screenHeight = 600
    width = 1400/8
    height = 700/13

    def __init__(self, col, type, percent):
        self.col = col
        self.type = type
        self.percent = percent
        self.y = Note.screenHeight-(Note.screenHeight*(self.percent/100))
        #self.y = something  based on time until
        self.x = 0

        if self.percent < 100:
            self.drawn = True
        else: self.drawn = False

    def __repr__(self):
        return f"Note, col {self.col}, at {self.percent}%"
        
    def giveCoordByPercent(startX, startY, endX, endY, percent):
        lengthX = (endX-startX)
        lengthY = (endY - startY)

        return (startX + lengthX*percent, startY + lengthY*percent)

    def move(self, px):
        self.y += px
        self.percent = (-1*(self.y -Note.screenHeight)/Note.screenHeight)*100
        if self.percent < 100 and self.percent > -20:
            self.drawn = True
        else: self.drawn = False
    