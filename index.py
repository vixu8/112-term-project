from cmu_graphics import *
from types import SimpleNamespace

def onAppStart(app):
    app.width = 1400
    app.height = 600

    app.cellWidth = app.width/20
    app.cellHeight = app.height /12

    app.gameStage = "play" #home, play, pause, scoreboard

    app.stepsPerSecond = 100
    app.scrollSpeed = .1

    app = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}


def redrawAll(app):
    if app.gameStage == "home":
        drawHomeScreen(app)
    if app.gameStage == "play":
        drawGameScreen(app)
    if app.gameStage == "testing":
        drawTesting(app)


def drawHomeScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")
    drawLabel("Welcome to my term project!", app.width/2, 3*app.height/8, fill="white", size=50)
    drawLabel("Start", app.width/2, app.height/2 - 20, fill="white", size=30)


    drawLabel("About", app.width/2, app.height/2 + 20, fill="white", size=25)
    drawLabel("Settings", app.width/2, app.height/2 + 60, fill="white", size=25)

def drawGameScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")

    drawPolygon(7*app.cellWidth, 4*app.cellHeight, 0, app.height, app.width, app.height, 13*app.cellWidth, 4*app.cellHeight, fill=rgb(219,219,219))    
    
    drawLine(0, 4*app.cellHeight, app.width, 4*app.cellHeight, fill="black")

    drawLine(7*app.cellWidth, 4*app.cellHeight, 0, app.height, fill="black")
    drawLine(8*app.cellWidth, 4*app.cellHeight, 3.5*app.cellWidth, app.height, fill="black")
    drawLine(9*app.cellWidth, 4*app.cellHeight, 7*app.cellWidth, app.height, fill="black")
    drawLine(10*app.cellWidth, 4*app.cellHeight, 10*app.cellWidth, app.height, fill="black")
    drawLine(11*app.cellWidth, 4*app.cellHeight, 13*app.cellWidth, app.height, fill="black")
    drawLine(12*app.cellWidth, 4*app.cellHeight, 16.5*app.cellWidth, app.height, fill="black")
    drawLine(13*app.cellWidth, 4*app.cellHeight, app.width, app.height, fill="black")

    drawLine(1.5*app.cellWidth, 10.5*app.cellHeight, 18.5*app.cellWidth, 10.5*app.cellHeight)


def drawNotes(app):
    pass

def newNote(app, col):
    pass


def drawTesting(app):
    pass


def onMouseMove(app, mouseX, mouseY):
    pass


def main():
    print("blehh")
    runApp()

main()