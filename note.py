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
        horizonY = height /13,

        perfectH = height*11.25/13
    )

    def __init__(self, col, type, percent):
        self.col = col
        self.type = type
        self.percent = percent

        if self.percent < 100:
            self.drawn = True
        else: self.drawn = False

    def __repr__(self):
        return f"Note, col {self.col}, at {self.percent}%, drawn is {self.drawn}"
        
    def getCoords(self):
        #returns a 8tuple with the 4 coords to draw the note, based on its percentage way down.
        #upper thing will be -.1*(100-percent) to the percent, lower will be +.1*(100-percent)
        delta = .05*(100-self.percent)
        return (*self.perspectivize(self.col-1, self.percent-delta), *self.perspectivize(self.col, self.percent-delta),
                *self.perspectivize(self.col, self.percent+delta), *self.perspectivize(self.col-1, self.percent+delta))

    def perspectivize(self, line, percent):
        #returns 2ple, with X and Y coords of that % on that line

        y = Note.boardSpecs.horizonY + (100-percent)/100 * (Note.boardSpecs.perfectH - Note.boardSpecs.horizonY)

        x = ((Note.boardSpecs.horizonInitX + line*Note.boardSpecs.horizonColWidth)
            -(100-percent)/100* ((Note.boardSpecs.horizonInitX + line*Note.boardSpecs.horizonColWidth -Note.boardSpecs.colWidth*line)*7.25/8))
        return (x, y)


        # y = Note.boardSpecs.horizonY + percent/100 * (Note.boardSpecs.perfectH - Note.boardSpecs.horizonY)
        # if line == 4:
        #     return (0, y)
        # else:
        #     x = (Note.boardSpecs.horizonInitX + line*Note.boardSpecs.horizonColWidth)- (100-percent)/100* ((Note.boardSpecs.horizonInitX + line*Note.boardSpecs.horizonColWidth -Note.boardSpecs.colWidth*line)*7.25/8)

        # return (x, y)

    def move(self, inc):

        self.percent -= inc

        if self.percent < 100 and self.percent >= -20:
            self.drawn = True
        else: self.drawn = False
    
    