from cmu_graphics import *
from types import SimpleNamespace
from note import Note
from pydub import AudioSegment
from pydub.playback import play

def onAppStart(app):
    app.song = AudioSegment.from_mp3("assets\Your_Phone_Ringing_-_Funny_Asian-650683.mp3")


    app.width = 1400
    app.height = 650

    app.cellWidth = app.width/20
    app.cellHeight = app.height /13

    app.gameStage = "play" #home, play, pause, scoreboard

    app.stepsPerSecond = 100

    app.bpm = 120 #bpm of the song
    app.bps = app.bpm/60    

    app.secondsToCross = 2 #seconds for note to make it from horizon to cyan line
    app.ticks = 100 #this number of 'ticks' to go from top of screen to cyan line
    app.stepsPerTick = app.stepsPerSecond*app.secondsToCross / app.ticks
    #app.timeOneHundred = app.stepsPerSecond * app.secondsToCross

    app.keysPressed = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False}

    app.notes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}


def redrawAll(app):
    if app.gameStage == "home":
        drawHomeScreen(app)
    if app.gameStage == "play":
        drawGameScreen(app)
    if app.gameStage == "testing":
        drawTesting(app)
    drawPressedKeys(app)


def drawHomeScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")
    drawLabel("Welcome to my term project!", app.width/2, 3*app.height/8, fill="white", size=50)
    drawLabel("Start", app.width/2, app.height/2 - 20, fill="white", size=30)


    drawLabel("About", app.width/2, app.height/2 + 20, fill="white", size=25)
    drawLabel("Settings", app.width/2, app.height/2 + 60, fill="white", size=25)

def drawGameScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")

    drawPolygon(7*app.cellWidth, 4*app.cellHeight, 0, 12*app.cellHeight, app.width, 12*app.cellHeight, 13*app.cellWidth, 4*app.cellHeight, fill=rgb(219,219,219))    
    
    drawLine(0, 4*app.cellHeight, app.width, 4*app.cellHeight, fill="black")

    drawLine(7*app.cellWidth, 4*app.cellHeight, 0, 12*app.cellHeight, fill="black")
    drawLine(8*app.cellWidth, 4*app.cellHeight, 3.5*app.cellWidth, 12*app.cellHeight, fill="black")
    drawLine(9*app.cellWidth, 4*app.cellHeight, 7*app.cellWidth, 12*app.cellHeight, fill="black")
    drawLine(10*app.cellWidth, 4*app.cellHeight, 10*app.cellWidth, 12*app.cellHeight, fill="black")
    drawLine(11*app.cellWidth, 4*app.cellHeight, 13*app.cellWidth, 12*app.cellHeight, fill="black")
    drawLine(12*app.cellWidth, 4*app.cellHeight, 16.5*app.cellWidth, 12*app.cellHeight, fill="black")
    drawLine(13*app.cellWidth, 4*app.cellHeight, app.width, 12*app.cellHeight, fill="black")

    drawLine(1.5*app.cellWidth, 10*app.cellHeight, 18.5*app.cellWidth, 10*app.cellHeight)
    drawLine(1.5*app.cellWidth, 11*app.cellHeight, 18.5*app.cellWidth, 11*app.cellHeight, fill="cyan")


def drawNotes(app):
    pass

def drawTesting(app):
    pass

def onStep(app):
    for col in app.notes:
        for note in app.notes[col]:
            note.increment

def onMouseMove(app, mouseX, mouseY):
    pass

def onKeyPress(app, key):
    if "p" in key:
        play(app.song)
    if app.gameStage == "play":
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
    if app.gameStage == "play":
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