from cmu_graphics import *
from types import SimpleNamespace
import simpleaudio as sa
from note import Note
import librosa
import numpy as np

def onAppStart(app):
    song = "yo_phone_linging"
    audioFile = song+".wav"
    y, sr = librosa.load(audioFile)
    print("loaded")
    beatFile = song+".txt"
    '''
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
    '''

    #print(str(beats))

    wave_obj = sa.WaveObject.from_wave_file(audioFile)
    app.play_object = wave_obj.play()
    app.play_object.pause()
    app.musicPlaying = False

    app.width = 1400
    app.height = 700

    print("pre")
    app.boardSpecs = SimpleNamespace(
        boardH = app.height*12/13,

        cellWidth = app.width/20,
        cellHeight = app.height /13,

        colWidth = app.width / 8,
        horizonInitX = app.width/20*8.5,
        horizonColWidth = app.width/20*3/8,
        horizonY = app.height /13*4,

        perfectH = app.height*11.25/13
    )

    print("outta here")
    
    app.gameStage = "testing" #home, play, pause, scoreboard

    app.stepsPerSecond = 100
    app.scrollSpeed = .02

    app.colNotes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    testInit(app)
    
    app.keysPressed = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}

def testInit(app):
    # newNote(app, 1, 120)
    newNote(app, 2, 120)
    newNote(app, 3, 150)

    newNote(app, 4, 200)
    newNote(app, 5, 250)
    newNote(app, 6, 300)
    


def redrawAll(app):
    if app.gameStage == "home":
        drawHomeScreen(app)
    if app.gameStage == "play":
        drawGameScreen(app)
        drawNotes(app)
    if app.gameStage == "testing":
        drawGameScreen(app)
        drawPressedKeys(app)
        drawNotes(app)


def onStep(app):
    
    for col in range(1, 9):
        for note in app.colNotes[col]:
            note.move(app.scrollSpeed * app.stepsPerSecond)
            print(note)
            
            if note.percent < -30:
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

    drawRect(0, 4*app.boardSpecs.cellHeight, app.width, 8*app.boardSpecs.cellHeight, fill="white")

    drawLine(0*app.boardSpecs.cellWidth, 10.5*app.boardSpecs.cellHeight, 20*app.boardSpecs.cellWidth, 10.5*app.boardSpecs.cellHeight)

    

    for i in range(9):
        drawLine(app.boardSpecs.horizonInitX + i*app.boardSpecs.horizonColWidth, app.boardSpecs.horizonY, i*app.boardSpecs.colWidth, app.boardSpecs.boardH)
        #drawLine(i*app.colWidth, 0, i*app.colWidth, app.height)
    

    drawLine(*perspectivize(app, 0, 10), *perspectivize(app, 8, 10), lineWidth=5, fill="red")
    drawLine(*perspectivize(app, 0, 3), *perspectivize(app, 8, 3), lineWidth=5, fill="yellow")
    drawLine(*perspectivize(app, 0, -10), *perspectivize(app, 8, -10), lineWidth=5, fill="red")
    drawLine(*perspectivize(app, 0, -3), *perspectivize(app, 8, -3), lineWidth=5, fill="yellow")

    drawLine(*perspectivize(app, 0, 0), *perspectivize(app, 8, 0), lineWidth=5, fill="green")


def perspectivize(app, line, percent):
    #returns 2ple, with X and Y coords of that % on that line
    y = app.boardSpecs.horizonY + (100-percent)/100 * (app.boardSpecs.perfectH - app.boardSpecs.horizonY)
    x = ((app.boardSpecs.horizonInitX + line*app.boardSpecs.horizonColWidth)
        -(100-percent)/100* ((app.boardSpecs.horizonInitX + line*app.boardSpecs.horizonColWidth -app.boardSpecs.colWidth*line)*7.25/8))
    return (x, y)

def drawTesting(app):
    pass




#stuff w notes
def drawNotes(app):
    for col in range(1, 9):
        for note in app.colNotes[col]:
            if note.drawn == True:
                # print("doijfadfjaodsf")
                coords = note.getCoords()
                # print(coords)
                # drawCircle(coords[0], coords[1], 5, fill="green")
                # drawCircle(coords[2], coords[3], 5, fill="green")
                # drawCircle(coords[4], coords[5], 5, fill="green")
                # drawCircle(coords[6], coords[7], 5, fill="green")

                drawPolygon(*note.getCoords(), fill="cyan")
                # drawRect(app.boardSpecs.colWidth*(col-1), note.y-note.noteHeight/2, note.noteWidth, note.noteHeight, fill="green")
                # drawLine(app.boardSpecs.colWidth*(col-1), note.y, app.boardSpecs.colWidth*col,note.y, fill="black", lineWidth = 5)
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
            drawLabel(f"{col}", 20+app.boardSpecs.colWidth*(col-1), 11*app.boardSpecs.cellHeight)

def main():
    print("blehh")
    runApp()

main()