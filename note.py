class Note:
    width = 50
    height = 20

    def __init__(self, col, type, timestamp):
        self.col = col
        self.type = type
        self.timeUntil = timestamp
        self.y = 50
        #self.y = something  based on time until
        self.x = 0
        
    def giveCoordByPercent(startX, startY, endX, endY, percent):
        lengthX = (endX-startX)
        lengthY = (endY - startY)

        return (startX + lengthX*percent, startY + lengthY*percent)

    def move(self, px):
        self.y += px
    