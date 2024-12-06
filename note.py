from types import SimpleNamespace

class Note:
    width = 1400
    height = 700

    noteWidth = width/8
    noteHeight = height/13

    boardSpecs = SimpleNamespace(
        boardH = height*12/13,

        cellWidth = width/20,
        cellHeight = height /13,

        colWidth = width / 8,
        horizonInitX = width/20*8.5,
        horizonColWidth = width/20*3/8,
        horizonY = 0*height /13,

        perfectH = height*11.25/13,

        travelTimeSec = 2

    )

    def __init__(self, col, type, time, up=False):
        self.col = col
        self.type = type
        self.time = time

        self.drawn = True

        self.up = up

    def __repr__(self):
        return f"Note, col {self.col}, at {self.time}, drawn is {self.drawn}"
        
    def getCoords(self, curTime):
        percent = (self.time - curTime)*100 / Note.boardSpecs.travelTimeSec
        if self.up:
            percent *= -1
        #returns a 8tuple with the 4 coords to draw the note, based on its percentage way down.
        #upper thing will be -.1*(100-percent) to the percent, lower will be +.1*(100-percent)
        delta = .025*(100-percent)
        return (*self.perspectivize(self.col-1, percent-delta), *self.perspectivize(self.col, percent-delta),
                *self.perspectivize(self.col, percent+delta), *self.perspectivize(self.col-1, percent+delta))

    def perspectivize(self, line, percent):
        #returns 2ple, with X and Y coords of that % on that line

        y = Note.boardSpecs.horizonY + (100-percent)/100 * (Note.boardSpecs.perfectH - Note.boardSpecs.horizonY)

        x = ((Note.boardSpecs.horizonInitX + line*Note.boardSpecs.horizonColWidth)
            -(100-percent)/100* ((Note.boardSpecs.horizonInitX + line*Note.boardSpecs.horizonColWidth -Note.boardSpecs.colWidth*line)*7.5/8))
        return (x, y)

    # def move(self, inc):

    #     self.percent -= inc

    #     if self.percent < 100 and self.percent >= -20:
    #         self.drawn = True
    #     else: self.drawn = False
    
    