from cmu_graphics import *
from types import SimpleNamespace
import simpleaudio as sa
from note import Note
import librosa
import numpy as np
import soundfile
import time
from button import Button


'''
ACTION ITEMS:
instead of it all as a list, try going with that prev idea of splitting it by line, 
    with each line having percents from 0 to 100
so that u can load a line at a time/1 whole section at a time instead of indiv.
also figure out how to read that.



'''


def onAppStart(app):
    app.song = "accumula_town"


    app.audioFile = None
    app.play_object = None
    app.musicPlaying = False
    
    app.combo = 0
    app.maxCombo = 0
    app.score = 0
    app.multiplier = 1
    app.drawRating = ""

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
    
    app.gameStage = "home" #home, play, create, select, score
#====general game vars====
    app.stepsPerSecond = 50
    app.travelTimeSec = 2
    app.goodLim = .1* app.travelTimeSec
    app.greatLim = .05*app.travelTimeSec

    app.startTime = time.time()
    app.songLength = 0
    app.currentDelTime = 0
    app.endTime = 0

#====create map vars====
    
    app.writeFile = None
    app.recording = False
#==== play game vars===
    app.notesLoaded = 0
    app.endReached = False
    app.playing = False

    app.buttonsHome ={
        Button(app.width/2, app.height/2 - 20, 200, 50, "Start Play", "green", "lightGreen", 30): startPlay,
        Button(app.width/2, app.height/2 + 40, 200, 50, "Start Create", "blue", "lightBlue", 30): startCreate,
        Button(app.width/2, app.height/2 + 100, 200, 50, "Select Song", "gray", "lightGray", 30): startSelect
    }

    app.songList = [
        "this_fffire",
        "accumula_town",
        "apple_cider",
        "12_51",
        "clip"
    ]

    app.buttonsSelect = {
        Button(app.width/2, app.height/2 - 80, 250, 50, app.songList[0], "blue", "lightBlue", 30): 0,
        Button(app.width/2, app.height/2 - 20, 250, 50, app.songList[1], "blue", "lightBlue", 30): 1,
        Button(app.width/2, app.height/2 + 40, 250, 50, app.songList[2], "blue", "lightBlue", 30): 2,
        Button(app.width/2, app.height/2 + 100, 250, 50, app.songList[3], "blue", "lightBlue", 30): 3,
        Button(app.width/2, app.height/2 + 160, 250, 50, app.songList[4], "blue", "lightBlue", 30): 4,

        Button(50, 50, 50, 50, "<", "gray", "lightGray", 50): returnHome
    }

    app.buttonReturn = {
        Button(50, 50, 50, 50, "<", "gray", "lightGray", 50): returnHome
    }

    app.colNotes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    
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


    app.songLength = librosa.get_duration(y=y, sr=sr)

    app.play_object = wave_obj.play()
    app.play_object.pause()
    app.musicPlaying = False


#=================play functions==================
def clearNotes(app):
    app.colNotes = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}
    app.keysPressed = {1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}


def startPlay(app):
    clearNotes(app)
    selectSong(app, app.song)
    print("play mode")
    if loadMapFile(app, app.song) == False:
        return
    
    time.sleep(2)

    app.currentDelTime = 0

    app.combo = 0
    app.maxCombo = 0
    app.score = 0
    app.multiplier= 1

    app.endReached = False
    app.playing = True
    playMusic(app)
    app.startTime = time.time()
    app.endTime = app.startTime + app.songLength

    app.gameStage = "play"


def loadMapFile(app, song):
    try:
        app.mapFile = open(song+"-map.txt", "r")
        return True
    except:
        return False
        print("no map foud :(")

#=================create functions==================
def startCreate(app):
    selectSong(app, app.song)
    prepareCreate(app, app.song)
    app.recording = True
    playMusic(app)
    app.gameStage = "create"
    app.startTime = time.time()
    app.endTime = app.startTime + app.songLength

    print("create mode")

def prepareCreate(app, song):
    app.writeFile = open(song+"-map.txt", "w")


#=================select functions==================
def startSelect(app):
    app.gameStage = "select"
    print("select mode)")

def changeSongTo(app, index):
    app.song = app.songList[index]

def returnHome(app):
    app.ended = False
    app.recording = False
    app.gameStage = "home"

#=============================
def playMusic(app):
    app.play_object.resume()
    app.musicPlaying = True

def stopMusic(app):
    app.play_object.pause()
    app.musicPlaying = False




def loadNotes(app):
    while app.notesLoaded < 30 and app.endReached == False:
        line = app.mapFile.readline()
        if line == "end":
            app.endReached = True
        else:
            newNote(app, int(line[0]), float(line[2:]))
            app.notesLoaded+=1

def redrawAll(app):
    if app.gameStage == "home":
        drawHomeScreen(app)
    
    if app.gameStage == "create":
        drawGameScreen(app)
        drawPressedKeys(app)
        drawNotes(app)
        if app.recording == False:
            for button in app.buttonReturn:
                drawButton(app, button)

    if app.gameStage == "play":
        drawGameScreen(app)
        drawPressedKeys(app)
        drawNotes(app)
        drawUI(app)

    if app.gameStage == "select":
        drawSelectScreen(app)

    if app.gameStage == "score":
        drawScoreScreen(app)

def onStep(app):
    if app.gameStage == "create":
        app.currentDelTime = time.time() - app.startTime
        if time.time() + .15 >= app.endTime and app.recording == True:
            print("STOP!!!!")
            app.writeFile.write("end")
            stopMusic(app)

            app.recording = False

            print("stoped writing")
            app.writeFile.close()
            return
        if app.recording == True:
            for col in range(1, 9):
                for note in app.colNotes[col]:
                    if app.currentDelTime-note.time > app.travelTimeSec:
                        app.colNotes[col].pop(0)

    if app.gameStage == "play":
        print(app.currentDelTime)
        print(time.time(), "current")
        print(app.endTime, "lim")
        print(app.songLength, "length")
        print(app.startTime, "started at")
        app.currentDelTime = time.time() - app.startTime
        if time.time() + .2 >= app.endTime:
            stopMusic(app)
            print("STOP!!!!")

            app.playing = False
            app.gameStage = "score"
            if app.combo > app.maxCombo:
                app.maxCombo = app.combo
            return
        loadNotes(app)
        if app.playing == True:
            
            if app.combo >= 30:
                app.multiplier = 4
            elif app.combo >= 10:
                app.multiplier = 2
            else: app.multiplier = 1

            if app.playing == True:

                for col in range(1, 9):
                    for note in app.colNotes[col]:
                        if note.time - app.currentDelTime <= 1:
                            note.drawn = True
                        # print(note)
                        
                        if note.time - app.currentDelTime < -.3:
                            if app.combo > app.maxCombo:
                                app.maxCombo = app.combo
                            app.combo = 0
                            app.drawRating = "missed"
                            app.notesLoaded -= 1
                            app.colNotes[col].pop(0)
        
            
    #print(app.keysPressed)



def drawHomeScreen(app):
    drawRect(0,0,app.width, app.height, fill="gray")
    drawLabel("Welcome to my term project!", app.width/2, 3*app.height/8, fill="white", size=50)
    for button in app.buttonsHome:
        drawButton(app, button)
    drawLabel(f"Selected song: {app.song}", app.width/2, 7*app.height/8, fill="white", size = 40)

def drawButton(app, button):
    if button.selected:
        drawRect(button.centerX - button.totalW/2, button.centerY - button.totalH/2, button.totalW, button.totalH, fill=button.colorSelected, border="black")
    else: 
        drawRect(button.centerX - button.totalW/2, button.centerY - button.totalH/2, button.totalW, button.totalH, fill=button.colorUnselected, border="black")

    drawLabel(button.text, button.centerX, button.centerY, size = button.textSize, fill="white")
    
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
    
    drawLine(*perspectivize(app, 0, 0), *perspectivize(app, 8, 0), lineWidth=5, fill="green")

    drawLabel("A", .5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel("S", 1.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel("D", 2.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel("F", 3.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel("J", 4.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel("K", 5.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel("L", 6.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)
    drawLabel(";", 7.5*app.boardSpecs.colWidth, app.height*12.5/13, size=30, bold=True, fill="red", opacity=100)


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

def drawSelectScreen(app):
    drawRect(0, 0, app.width, app.height, fill="lightBlue")
    for button in app.buttonsSelect:
        drawButton(app, button)


def drawScoreScreen(app):
    drawRect(0,0,app.width, app.height, fill="pink")
    drawLabel("song complete!", app.width/2, 3*app.height/8, size=80)
    drawLabel(f"score: {app.score}", app.width/2, 6*app.height/8, size=30)
    drawLabel(f"max combo: {app.maxCombo}", app.width/2, 7*app.height/8, size=30)

    for button in app.buttonReturn:
        drawButton(app, button)



#stuff w notes
def drawNotes(app):
    for col in range(1, 9):
        for note in app.colNotes[col]:
            if note.drawn == True:
                # print("doijfadfjaodsf")
                #                 # print(coords)
                # drawCircle(coords[0], coords[1], 5, fill="green")
                # drawCircle(coords[2], coords[3], 5, fill="green")
                # drawCircle(coords[4], coords[5], 5, fill="green")
                # drawCircle(coords[6], coords[7], 5, fill="green")

                drawPolygon(*note.getCoords(app.currentDelTime), fill=gradient('yellow', 'orange'), opacity=80)
                # drawRect(app.boardSpecs.colWidth*(col-1), note.y-note.noteHeight/2, note.noteWidth, note.noteHeight, fill="green")
                # drawLine(app.boardSpecs.colWidth*(col-1), note.y, app.boardSpecs.colWidth*col,note.y, fill="black", lineWidth = 5)
    pass

def newNote(app, col, time, up=False):
    app.colNotes[col].append(Note(col, "tap", time, up))
    pass

def noteHit(app, col):
    note = app.colNotes[col][0]
    if note.time-app.currentDelTime <= .01 and note.time-app.currentDelTime >= -.01:
        app.combo += 1
        app.score += 200 * app.multiplier

        app.drawRating = "perfect"
    elif note.time-app.currentDelTime < app.greatLim and note.time-app.currentDelTime > -1*app.greatLim:
        app.combo += 1
        app.score += 100 * app.multiplier

        app.drawRating = "great"
    elif note.time-app.currentDelTime < app.goodLim and note.time-app.currentDelTime > -1*app.goodLim:
        app.combo += 1
        app.score += 50 * app.multiplier
        app.drawRating = "good"
    else: 
        if app.combo > app.maxCombo:
            app.maxCombo = app.combo
        app.combo = 0
        app.drawRating = "missed"

    app.colNotes[col].pop(0)
    app.notesLoaded -= 1
    #add points


#input
def onMouseMove(app, mouseX, mouseY):
    if app.gameStage == "home":
        for button in app.buttonsHome:
            button.isOnButton(mouseX, mouseY)
    
    if app.gameStage == "select":
        for button in app.buttonsSelect:
            button.isOnButton(mouseX, mouseY)
    
    if app.gameStage == "create" or app.gameStage == "score":
        for button in app.buttonReturn:
            button.isOnButton(mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    if app.gameStage == "home":
        for button in app.buttonsHome:
            if button.selected:
                app.buttonsHome[button](app)
    
    if app.gameStage == "select":
        for button in app.buttonsSelect:
            if button.selected:
                if type(app.buttonsSelect[button]) is int:
                    changeSongTo(app, app.buttonsSelect[button])
                    button.selected = False
                    returnHome(app)
                else:
                    button.selected = False
                    returnHome(app)

    if app.gameStage == "score" or (app.gameStage == "create" and app.recording == False):
        for button in app.buttonReturn:
            if button.selected:
                button.selected = False
                returnHome(app)

def makeNote(app, col):
    newNote(app, col, app.currentDelTime, True)
    print(f"new note: {col} {app.currentDelTime}")
    app.writeFile.write(f"{col} {app.currentDelTime}\n")

def onKeyPress(app, key):
    if app.gameStage == "create" or app.gameStage == "play":
        if "y" in key:
            print("fdoijfaoids")
            stopMusic(app)

    if app.gameStage == "create":
        


        if app.recording == True:
            if "a" in key:
                makeNote(app, 1)
            if "s" in key:
                makeNote(app, 2)
            if "d" in key:
                makeNote(app, 3)
            if "f" in key:
                makeNote(app, 4)
            if "j" in key:
                makeNote(app, 5)
            if "k" in key:
                makeNote(app, 6)
            if "l" in key:
                makeNote(app, 7)
            if ";" in key:
                makeNote(app, 8)

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
    if app.gameStage == "play" or app.gameStage == "create":
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