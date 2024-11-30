from cmu_graphics import *
from types import SimpleNamespace
import simpleaudio as sa
from note import Note
import librosa
import numpy as np

def onAppStart(app):
    

    #print(str(beats))
    app.audioFile = None

    selectSong(app, "yo_phone_linging")

    wave_obj = sa.WaveObject.from_wave_file(app.audioFile)
    app.play_object = wave_obj.play()
    app.play_object.pause()
    app.musicPlaying = False

    app.width = 1400
    app.height = 700
    app.boardH = 600

    app.cellWidth = app.width/20
    app.cellHeight = (app.height) /13

    app.colWidth = app.width / 8

    app.gameStage = "testing" #home, play, pause, scoreboard

    app.stepsPerSecond = 100
    app.scrollSpeed = .1

    app.colNotes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    testInit(app)
    
    app.keysPressed = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}

def selectSong(app, song):
    app.audioFile = song+".wav"
    y, sr = librosa.load(app.audioFile)
    print("loaded")
    beatFile = song+".txt"

    #beat audio thing
    try:
        f = open(beatFile, 'r')
        print("file found")
        beats = f.read()
        f.close()
    except:
        print("making new file")
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        f = open(beatFile, 'w')
        f.write(str(beat_times))
        beats = beat_times
        f.close()

def testInit(app):
    newNote(app, 1, 200)
    newNote(app, 2, 300)
    newNote(app, 3, 500)
    newNote(app, 1, 500)

    # newNote(app, 4, 200)
    # newNote(app, 5, 300)
    # newNote(app, 6, 300)
    


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
    
    for col in range(1, 9):
        for note in app.colNotes[col]:
            note.move(10)
            
            if note.percent < -50:
                print("missed")
                app.colNotes[col].pop(0)
    #print(app.keysPressed)

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

    for i in range(8):
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

    drawLine(0, app.boardH-.1*app.boardH, app.width, app.boardH-.1*app.boardH, lineWidth = 3, fill="red")
    drawLine(0, app.boardH-.03*app.boardH, app.width, app.boardH-.03*app.boardH, lineWidth = 3, fill="yellow")
    drawLine(0, app.boardH+.03*app.boardH, app.width, app.boardH+.03*app.boardH, lineWidth = 3, fill="yellow")
    drawLine(0, app.boardH+.1*app.boardH, app.width, app.boardH+.1*app.boardH, lineWidth = 3, fill="red")


def drawTesting(app):
    pass




#stuff w notes
def drawNotes(app):
    for col in range(1, 9):
        for note in app.colNotes[col]:
            if note.drawn == True:
                print(note)
                drawRect(app.colWidth*(col-1), note.y-note.height/2, note.width, note.height, fill="green")
                drawLine(app.colWidth*(col-1), note.y, app.colWidth*col,note.y, fill="black", lineWidth = 5)
    pass

def newNote(app, col, percent):
    app.colNotes[col].append(Note(col, "tap", percent))
    pass

def noteHit(app, col):
    note = app.colNotes[col][0]
    if note.percent < 1 and note.percent > -1:
        print("perfect")
    elif note.percent < 3 and note.percent > -3:
        print("great")
    elif note.percent < 10 and note.percent > -10:
        print("good")
    else: 
        print("bad")
    app.colNotes[col].pop(0)
    #add points



#input
def onMouseMove(app, mouseX, mouseY):
    pass


def onKeyPress(app, key):

    if "t" in key:
        #control music playing
        if app.musicPlaying == False:
            app.play_object.resume()
            app.musicPlaying = True
        else:
            app.play_object.pause()
            app.musicPlaying = False

    #pressing keys
    if app.gameStage == "testing":
        if "a" in key:
            processTap(app, 1)
        if "s" in key:
            processTap(app, 2)
        if "d" in key:
            processTap(app, 3)
        if "f" in key:
            processTap(app, 4)
        if "j" in key:
            processTap(app, 5)
        if "k" in key:
            processTap(app, 6)
        if "l" in key:
            processTap(app, 7)
        if ";" in key:
            processTap(app, 8)

def processTap(app, col):
    app.keysPressed[col] = True
    if len(app.colNotes[col]) != 0 and app.colNotes[col][0].drawn == True:
        noteHit(app, col)

def onKeyRelease(app, key):
    if app.gameStage == "testing":
        if "a" in key:
            app.keysPressed[1] = False
        if "s" in key:
            app.keysPressed[2] = False
        if "d" in key:
            app.keysPressed[3] = False
        if "f" in key:
            app.keysPressed[4] = False
        if "j" in key:
            app.keysPressed[5] = False
        if "k" in key:
            app.keysPressed[6] = False
        if "l" in key:
            app.keysPressed[7] = False
        if ";" in key:
            app.keysPressed[8] = False

        if "q" in key:
            newNote(app, 1, 100)
        if "w" in key:
            newNote(app, 2, 100)
        if "e" in key:
            newNote(app, 3, 100)
        if "r" in key:
            newNote(app, 4, 100)
        if "u" in key:
            newNote(app, 5, 100)
        if "i" in key:
            newNote(app, 6, 100)
        if "o" in key:
            newNote(app, 7, 100)
        if "p" in key:
            newNote(app, 8, 100)

def drawPressedKeys(app):
    for col in range(1, 9):
        if app.keysPressed[col]:
            drawLabel(f"{col}", 20+app.colWidth*(col-1), 11*app.cellHeight)

def main():
    print("blehh")
    runApp()

main()