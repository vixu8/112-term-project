class Note:
    def __init__(self, col, type, timestamp):
        self.col = col
        self.type = type
        self.timeUntil = timestamp
    
    def giveCoordByPercent(startX, startY, endX, endY, percent):
        lengthX = (endX-startX)
        lengthY = (endY - startY)

        return (startX + lengthX*percent, startY + lengthY*percent)

    