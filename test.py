from cmu_graphics import *
from types import SimpleNamespace
import pygame
from note import Note
def onAppStart(app):
    pygame.mixer.init()
    pygame.mixer.music.load("yo_phone_linging.mp3")

    app.width = 1400
    app.height = 600

    app.cellWidth = app.width/20
    app.cellHeight = app.height /12

    app.colWidth = app.width / 6

    app.gameStage = "play" #home, play, pause, scoreboard

    app.stepsPerSecond = 100
    app.scrollSpeed = .1

    app.colNotes = {1:[Note(1, "tap", 0)], 2:[], 3:[], 4:[], 5:[], 6:[]}

    


def redrawAll(app):
    if app.gameStage == "home":
        drawHomeScreen(app)
    if app.gameStage == "play":
        drawGameScreen(app)
        drawNotes(app)
    if app.gameStage == "testing":
        drawTesting(app)
        drawNotes(app)

def onStep(app):
    col = 1
    for note in app.colNotes[col]:
        note.move(10)

def drawHomeScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")
    drawLabel("Welcome to my term project!", app.width/2, 3*app.height/8, fill="white", size=50)
    drawLabel("Start", app.width/2, app.height/2 - 20, fill="white", size=30)


    drawLabel("About", app.width/2, app.height/2 + 20, fill="white", size=25)
    drawLabel("Settings", app.width/2, app.height/2 + 60, fill="white", size=25)

def drawGameScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")

    drawRect(0, 4*app.cellHeight, app.width, 8*app.cellHeight, fill="white")

    drawLine(0*app.cellWidth, 10.5*app.cellHeight, 20*app.cellWidth, 10.5*app.cellHeight)

    for i in range(6):
        drawLine(i*app.colWidth, 0, i*app.colWidth, app.height)



    #drawPolygon(7*app.cellWidth, 4*app.cellHeight, 0, app.height, app.width, app.height, 13*app.cellWidth, 4*app.cellHeight, fill=rgb(219,219,219))    
    
    drawLine(0, 4*app.cellHeight, app.width, 4*app.cellHeight, fill="black")

    # drawLine(7*app.cellWidth, 4*app.cellHeight, 0, app.height, fill="black")
    # drawLine(8*app.cellWidth, 4*app.cellHeight, 3.5*app.cellWidth, app.height, fill="black")
    # drawLine(9*app.cellWidth, 4*app.cellHeight, 7*app.cellWidth, app.height, fill="black")
    # drawLine(10*app.cellWidth, 4*app.cellHeight, 10*app.cellWidth, app.height, fill="black")
    # drawLine(11*app.cellWidth, 4*app.cellHeight, 13*app.cellWidth, app.height, fill="black")
    # drawLine(12*app.cellWidth, 4*app.cellHeight, 16.5*app.cellWidth, app.height, fill="black")
    # drawLine(13*app.cellWidth, 4*app.cellHeight, app.width, app.height, fill="black")

    #drawLine(1.5*app.cellWidth, 10.5*app.cellHeight, 18.5*app.cellWidth, 10.5*app.cellHeight)


def drawNotes(app):
    col = 1
    for note in app.colNotes[col]:
        drawRect(app.colWidth*(col-1), note.y, note.width, note.height, fill="green")
    pass

def newNote(app, col):
    pass


def drawTesting(app):
    pass


def onMouseMove(app, mouseX, mouseY):
    pass

def onKeyPress(app, key):
    if "p" in key:
        pygame.mixer.music.play()


    if app.gameStage == "play":
        if "s" in key:
            drawKeyPressed(app, 1)
        if "d" in key:
            drawKeyPressed(app, 2)
        if "f" in key:
            drawKeyPressed(app, 3)
        if "j" in key:
            drawKeyPressed(app, 4)
        if "k" in key:
            drawKeyPressed(app, 5)
        if "l" in key:
            drawKeyPressed(app, 6)

def drawKeyPressed(app, col):
    if col == 1:
        drawPolygon(0*app.cellWidth, 12*app.cellHeight, 1.5*app.cellWidth, 10.5*app.cellHeight,3*app.cellWidth, 10.5*app.cellHeight,3*app.cellWidth, 12*app.cellHeight, fill="cyan")

    

def main():
    print("blehh")
    runApp()

main()