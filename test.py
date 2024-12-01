from cmu_graphics import *
from types import SimpleNamespace
import simpleaudio as sa
from note import Note
import librosa
import numpy as np
import soundfile
import time
from timer import Timer


def onAppStart(app):
    app.audioFile = None
    app.play_object = None
    app.musicPlaying = False
    
    app.combo = 0
    app.maxCombo = 0
    app.score = 0
    app.multiplier = 1
    app.drawRating = ""

    #get sound ready
    selectSong(app, "accumula_town")

    app.width = 1400
    app.height = 700

    app.boardSpecs = SimpleNamespace(
        boardH = app.height*12/13,

        cellWidth = app.width/20,
        cellHeight = app.height /13,

        colWidth = app.width / 8,
        horizonInitX = app.width/20*8.5,
        horizonColWidth = app.width/20*3/8,
        horizonY = 0*app.height /13,

        perfectH = app.height*11.25/13
    )
    
    app.gameStage = "play" #home, play, pause, scoreboard

    app.stepsPerSecond = 60
    app.scrollSpeed = .02
    app.goodLim = 10
    app.greatLim = 5

    app.colNotes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    #testInit(app)
    
    app.keysPressed = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}

def selectSong(app, song):

    #create fade out audio thing
    try:
        wave_obj = sa.WaveObject.from_wave_file(song+"-fade.wav")
        print("fade audoi found")

        y, sr = librosa.load(song+"-fade.wav")
    except:
        print("making fade audio file")

        y, sr = librosa.load(song+".wav")

        #referenced stack overflow and chatgpt for this.
        # https://stackoverflow.com/questions/64894809/is-there-a-way-to-make-fade-out-by-librosa-or-another-on-python

        fade_length = 4*sr #4 second fade
        fade_end = y.shape[0]
        fade_start = len(y) - fade_length

        fade_curve = np.linspace(1, 0, fade_length)

        y[fade_start:fade_end] = y[fade_start:fade_end] * fade_curve 

        soundfile.write(song+"-fade.wav", y, samplerate=sr)

        wave_obj = sa.WaveObject.from_wave_file(song+"-fade.wav")

    app.play_object = wave_obj.play()
    app.play_object.pause()
    app.musicPlaying = False


    app.combo = 0
    app.maxCombo = 0
    app.score = 0
    app.multiplire = 1

def playMusic(app):
    app.play_object.resume()
    app.musicPlaying = True



def testInit(app):
    playMusic(app)

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
        drawPressedKeys(app)
        drawNotes(app)
        drawUI(app)
        
    if app.gameStage == "testing":
        drawGameScreen(app)
        drawPressedKeys(app)
        drawNotes(app)


def onStep(app):
    if app.gameStage == "play":
        if app.combo >= 30:
            app.multiplier = 4
        elif app.combo >= 10:
            app.multiplier = 2
        else: app.multiplier = 1

        for col in range(1, 9):
            for note in app.colNotes[col]:
                note.move(app.scrollSpeed * app.stepsPerSecond)
                # print(note)
                
                if note.percent < -30:
                    if app.combo > app.maxCombo:
                        app.maxCombo = app.combo
                    app.combo = 0
                    app.drawRating = "missed"
                    app.colNotes[col].pop(0)
    #print(app.keysPressed)

def drawHomeScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")
    drawLabel("Welcome to my term project!", app.width/2, 3*app.height/8, fill="white", size=50)
    drawLabel("Start", app.width/2, app.height/2 - 20, fill="white", size=30)


    drawLabel("About", app.width/2, app.height/2 + 20, fill="white", size=25)
    drawLabel("Settings", app.width/2, app.height/2 + 60, fill="white", size=25)

def drawGameScreen(app):
    drawImage('silly.png', 0, 0, width=app.width, height=app.height, visible=True, opacity=50)

    drawPolygon(app.boardSpecs.horizonInitX, 0,
                app.width-app.boardSpecs.horizonInitX, 0,
                app.width, app.boardSpecs.boardH,
                0, app.boardSpecs.boardH,
                fill="darkGray",
                opacity=75)

    drawRect(0, app.boardSpecs.boardH,
             app.width, app.height-app.boardSpecs.boardH,
             fill=gradient("darkGray", "gray", start="top"),
             opacity=75)
    
    drawLine(0, app.boardSpecs.boardH, app.width, app.boardSpecs.boardH)

    for i in range(9):
        drawLine(app.boardSpecs.horizonInitX + i*app.boardSpecs.horizonColWidth, app.boardSpecs.horizonY, i*app.boardSpecs.colWidth, app.boardSpecs.boardH)
        drawLine(i*app.boardSpecs.colWidth, app.boardSpecs.boardH, i*app.boardSpecs.colWidth, app.height)
        #drawLine(i*app.colWidth, 0, i*app.colWidth, app.height)
    

    # drawLine(*perspectivize(app, 0, app.goodLim), *perspectivize(app, 8, app.goodLim), lineWidth=5, fill="red")
    # drawLine(*perspectivize(app, 0, app.greatLim), *perspectivize(app, 8, app.greatLim), lineWidth=5, fill="yellow")
    # drawLine(*perspectivize(app, 0, -1*app.goodLim), *perspectivize(app, 8, -1*app.goodLim), lineWidth=5, fill="red")
    # drawLine(*perspectivize(app, 0, -1*app.greatLim), *perspectivize(app, 8, -1*app.greatLim), lineWidth=5, fill="yellow")

    drawLine(*perspectivize(app, 0, 0), *perspectivize(app, 8, 0), lineWidth=5, fill="green")

def drawUI(app):
    drawLabel(f"SCORE: {app.score}", app.boardSpecs.cellWidth*16, 2*app.boardSpecs.cellHeight, size=20, bold=True)
    drawLabel(f"COMBO: {app.combo}", app.boardSpecs.cellWidth*16, app.boardSpecs.cellHeight, size=30, bold=True)

    if app.drawRating == "perfect":
        drawLabel("PERFECT!", app.boardSpecs.cellWidth*10, 2*app.boardSpecs.cellHeight, size=40, fill=rgb(20,247,249))
    elif app.drawRating == "great":
        drawLabel("Great", app.boardSpecs.cellWidth*10, 2*app.boardSpecs.cellHeight, size=40, fill=rgb(34, 207, 43))
    elif app.drawRating == "good":
        drawLabel("good", app.boardSpecs.cellWidth*10, 2*app.boardSpecs.cellHeight, size=40, fill=rgb(128, 243, 134))
    elif app.drawRating == "missed":
        drawLabel("miss", app.boardSpecs.cellWidth*10, 2*app.boardSpecs.cellHeight, size=40, fill=rgb(105, 10, 10))

def perspectivize(app, line, percent):
    #returns 2ple, with X and Y coords of that % on that line
    y = app.boardSpecs.horizonY + (100-percent)/100 * (app.boardSpecs.perfectH - app.boardSpecs.horizonY)
    x = ((app.boardSpecs.horizonInitX + line*app.boardSpecs.horizonColWidth)
        -(100-percent)/100* ((app.boardSpecs.horizonInitX + line*app.boardSpecs.horizonColWidth -app.boardSpecs.colWidth*line)*10.25/11))
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

                drawPolygon(*note.getCoords(), fill=gradient('yellow', 'orange'), opacity=80)
                # drawRect(app.boardSpecs.colWidth*(col-1), note.y-note.noteHeight/2, note.noteWidth, note.noteHeight, fill="green")
                # drawLine(app.boardSpecs.colWidth*(col-1), note.y, app.boardSpecs.colWidth*col,note.y, fill="black", lineWidth = 5)
    pass

def newNote(app, col, percent):
    app.colNotes[col].append(Note(col, "tap", percent))
    pass

def noteHit(app, col):
    note = app.colNotes[col][0]
    if note.percent < 1 and note.percent > -1:
        app.combo += 1
        app.score += 200 * app.multiplier

        app.drawRating = "perfect"
    elif note.percent < app.greatLim and note.percent > -1*app.greatLim:
        app.combo += 1
        app.score += 100 * app.multiplier

        app.drawRating = "great"
    elif note.percent < app.goodLim and note.percent > -1*app.goodLim:
        app.combo += 1
        app.score += 50 * app.multiplier
        app.drawRating = "good"
    else: 
        if app.combo > app.maxCombo:
            app.maxCombo = app.combo
        app.combo = 0
        app.drawRating = "missed"

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
    if app.gameStage == "play":
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
    if app.gameStage == "play":
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
            drawPolygon(  app.boardSpecs.colWidth*(col-1), app.boardSpecs.boardH,
                        app.boardSpecs.colWidth*(col), app.boardSpecs.boardH,
                        app.boardSpecs.horizonInitX+app.boardSpecs.horizonColWidth*(col), app.boardSpecs.horizonY,
                        app.boardSpecs.horizonInitX+app.boardSpecs.horizonColWidth*(col-1), app.boardSpecs.horizonY,
                        fill=gradient('lightSteelBlue','white',start='bottom'),
                        opacity=50
            )
            drawRect(app.boardSpecs.colWidth*(col-1), app.boardSpecs.boardH,
             app.boardSpecs.colWidth, app.height-app.boardSpecs.boardH,
             fill=gradient("gray", "steelBlue", start="top"),
             opacity=75)

def main():
    print("blehh")
    runApp()

main()