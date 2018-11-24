
import pgWidgets
import schulzeBeat
from collections import deque

'''
This file is the main GUI file for the playground interaction.
The UI effects will be implemented first and then, connected to the calculated matrix.
'''


from tkinter import *

def init(data):
    data.inPlayList = []
    data.margin = 50
    data.mouseMotion = (-1, -1)
    data.mouseSelection = (-1, -1)
    data.mouseSelectionHist = deque(maxlen = 1)
    data.doubleClickSelection = (-1,-1)
    data.mouseHeldPosition = (-1, -1)
    data.playerNode = []
    data.playerNodeSep = data.height//len(data.playerList)
    data.sittingPlayerLoc = {}
    loadSittingPlayers(data)
    data.operationButton = []
    data.buttonNum = 4
    data.buttonWidth = 160
    data.buttonSep = (data.width - 4 * data.margin)//data.buttonNum + 30
    loadOperationButton(data)
    data.playground = None

def loadOperationButton(data):
    horizontalAlign = (2 * data.height - 3 * data.margin)//2 
    button1 = pgWidgets.ShowConnectionButton("Show One-Way Path", data.margin + data.buttonWidth//2, horizontalAlign, data.buttonWidth)
    data.operationButton.append(button1)
    button2 = pgWidgets.ShowConnectionButton("Show Two-Way Path", data.margin + data.buttonWidth//2 + data.buttonSep, horizontalAlign, data.buttonWidth)
    data.operationButton.append(button2)
    button3 = pgWidgets.SmithSetFinderButton("Show Smith Set", data.margin + data.buttonWidth//2 + data.buttonSep * 2, horizontalAlign, data.buttonWidth)
    data.operationButton.append(button3)
    button4 = pgWidgets.BeatDemoButton("Beat Path Demo", data.margin + data.buttonWidth//2 + data.buttonSep * 3, horizontalAlign, data.buttonWidth)
    data.operationButton.append(button4)
    button5 = pgWidgets.HintButton("Hint", data.margin//2 + 5, data.margin//2 + 5, 40, 40)
    data.operationButton.append(button5)

def loadSittingPlayers(data):
    heightOffset = 1.5 * data.margin
    verticalAlign = ((data.width - 3 * data.margin) + data.width)//2
    for i in range(len(data.playerList)):
        player = pgWidgets.PlayerNode(data.playerList[i], verticalAlign, heightOffset + i * data.playerNodeSep)
        data.playerNode.append(player)
        data.sittingPlayerLoc[player.playerName] = (player.cx, player.cy)

def mousePressed(event, data):
    data.mouseSelection = (event.x, event.y)

def mouseDoublePressed(event, data):
    data.doubleClickSelection = (event.x, event.y)

def mouseHeld(event, data):
    data.mouseHeldPosition = (event.x, event.y)

def mouseHeldReleased(event, data):
    pass

def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def drawPlaygroundBG(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "black")

def drawPlaygroundField(canvas, data):
    mouseX, mouseY = data.mouseMotion
    vertexNW, vertexSE = (data.margin, data.margin), (data.width - 3 * data.margin, data.height - 3 * data.margin)
    data.playground = pgWidgets.Playground(vertexNW,vertexSE)
    data.playground.draw(canvas, mouseX, mouseY, 20)

def drawPlayerNode(canvas, data):
    mouseX, mouseY = data.mouseMotion
    mousePressedX, mousePressedY = data.mouseSelection
    mouseDoublePressedX, mouseDoublePressedY = data.doubleClickSelection
    mouseHeldX, mouseHeldY = data.mouseHeldPosition
    for node in data.playerNode:
        node.ifSingleClicked(canvas, data.playground, mousePressedX, mousePressedY, data.inPlayList, data.mouseSelectionHist)
        node.ifDoubleClicked(canvas, data.playground, mouseDoublePressedX, mouseDoublePressedY, data.sittingPlayerLoc, data.inPlayList)
        node.ifDragged(canvas, data.playground, mouseHeldX, mouseHeldY)
        if not node.isInSmith:
            node.draw(canvas, mouseX, mouseY)
        else:
            node.draw(canvas, mouseX, mouseY, outline = "gold")

def drawOperationButton(canvas, data):
    mouseX, mouseY = data.mouseMotion
    mousePressedX, mousePressedY = data.mouseSelection
    for button in data.operationButton:
        if type(button) == pgWidgets.SmithSetFinderButton:
            button.ifClicked(canvas, mousePressedX, mousePressedY, data.mouseSelectionHist, data.positiveBeatScoreList, data.playerNode, data.inPlayList, data.playground, data.matrix) 
        elif type(button) == pgWidgets.BeatDemoButton:
            button.ifClicked(canvas, mousePressedX, mousePressedY, data.mouseSelectionHist, data.positiveBeatScoreList, data.playerNode, data.inPlayList, data.playground, data.matrix) 
        else:
            button.ifClicked(canvas, mousePressedX, mousePressedY, data.mouseSelectionHist, data.beatScoreList, data.playerNode, data.inPlayList, data.playground, data.matrix)
        button.draw(canvas, mouseX, mouseY, data.playground)


def redrawAll(canvas, data):
    drawPlaygroundBG(canvas, data)
    drawPlaygroundField(canvas, data)
    drawPlayerNode(canvas, data)
    drawOperationButton(canvas, data)

def mouseTracker(event, data):
    data.mouseMotion = (event.x, event.y)

def run(width, height, matrix, playerList):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseDoublePressedWrapper(event, canvas, data):
        mouseDoublePressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseHeldWrapper(event, canvas, data):
        mouseHeld(event, data)
        redrawAllWrapper(canvas, data)
    
    def mouseHeldReleasedWrapper(event, canvas, data):
        mouseHeldReleased(event, data)
        redrawAllWrapper(canvas, data)

    def mouseTrackerWrapper(event, data):
        mouseTracker(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    data.playerList = playerList
    data.matrix = matrix
    data.beatScoreList = schulzeBeat.PathIdentifier().pathIdentifier(data.matrix, data.playerList)
    data.positiveBeatScoreList = schulzeBeat.PositiveBeatFinder().positiveBeatFinder(data.matrix, data.playerList)
    root = Tk()
    root.title("Magic Desicion Maker Box")
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event:
                            mouseTrackerWrapper(event, data))  
    root.bind("<Double-Button-1>", lambda event:
                            mouseDoublePressedWrapper(event, canvas, data))
    root.bind("<B1-Motion>", lambda event:
                            mouseHeldWrapper(event, canvas, data))
    root.bind("<ButtonRelease-1>", lambda event:
                            mouseHeldReleasedWrapper(event, canvas, data))                        
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")



matrix = [  [ 4,  1,  2,  3 ],
            ['A','C','A','C'],
            ['B','B','D','A'],
            ['C','D','B','B'],
            ['D','A','C','D']]

playerList = ['A','B','C','D']

run(1200, 800, matrix, playerList)
