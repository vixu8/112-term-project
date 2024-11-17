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

    app.gameStage = "testing" #home, play, pause, scoreboard

    app.stepsPerSecond = 100
    app.scrollSpeed = .1

    app.colNotes = {1:[Note(1, "tap", 0)], 2:[], 3:[], 4:[], 5:[], 6:[]}
    
    app.keysPressed = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False}


    


def redrawAll(app):
    if app.gameStage == "home":
        drawHomeScreen(app)
    if app.gameStage == "play":
        drawGameScreen(app)
        drawNotes(app)
    if app.gameStage == "testing":
        drawGameScreen(app)
        drawNotes(app)
        drawPressedKeys(app)

def onStep(app):
    col = 1
    for note in app.colNotes[col]:
        note.move(10)
    print(app.keysPressed)

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
    if app.gameStage == "testing":
        if "s" in key:
            app.keysPressed[1] = True
        if "d" in key:
            app.keysPressed[2] = True
        if "f" in key:
            app.keysPressed[3] = True
        if "j" in key:
            app.keysPressed[4] = True
        if "k" in key:
            app.keysPressed[5] = True
        if "l" in key:
            app.keysPressed[6] = True

def onKeyRelease(app, key):
    if app.gameStage == "testing":
        if "s" in key:
            app.keysPressed[1] = False
        if "d" in key:
            app.keysPressed[2] = False
        if "f" in key:
            app.keysPressed[3] = False
        if "j" in key:
            app.keysPressed[4] = False
        if "k" in key:
            app.keysPressed[5] = False
        if "l" in key:
            app.keysPressed[6] = False

def drawPressedKeys(app):
    if app.keysPressed[1]:
        drawLabel("1", 2*app.cellWidth, 11*app.cellHeight)
    if app.keysPressed[2]:
        drawLabel("2", 6*app.cellWidth, 11*app.cellHeight)
    if app.keysPressed[3]:
        drawLabel("3", 8.5*app.cellWidth, 11*app.cellHeight)
    if app.keysPressed[4]:
        drawLabel("4", 11.5*app.cellWidth, 11*app.cellHeight)
    if app.keysPressed[5]:
        drawLabel("5", 14.5*app.cellWidth, 11*app.cellHeight)
    if app.keysPressed[6]:
        drawLabel("6", 18*app.cellWidth, 11*app.cellHeight)
    

def main():
    print("blehh")
    runApp()

main()