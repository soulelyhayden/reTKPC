import mttkinter as tk
import threading
import time
import numpy as np
import ChainMaker
import TwitterScrubber

# lots of variable setup happens here
window = tk.mtTkinter.Tk()
window.title("ReThink Participatory Communication")

bufferSize = (1 * window.winfo_screenwidth()) / 100 + (1 * window.winfo_screenheight()) / 100
fWidth = window.winfo_screenwidth()
fHeight = window.winfo_screenheight()

frame = tk.mtTkinter.Frame(window, width=fWidth, height=fHeight)
canvas = tk.mtTkinter.Canvas(frame, width=fWidth, height=fHeight, background='#EEEEEE')
canvas.pack()
frame.pack()

colour1, colour12, colour2, colour22, txtColour= '#0F8B8D', '#143642', '#B7314A', '#8B1E3F', '#FFFFFF'
bsFont = "Helvetica", (fWidth + fHeight) / 35
qtnNmb = 0
paused = False
m = 0

tNum = 0
timeChange = 0
timeChange2 = 0

originalTxt, newTxt = "These are your original Tweets.", "This is what happens to your words."

leftText = canvas.create_text(fWidth / 2, fHeight / 4, font=bsFont, text=originalTxt, width=fWidth / 2 - bufferSize * 4, fill=txtColour)
rightText = canvas.create_text(fWidth / 4, fHeight / 4, font=bsFont, text=newTxt, width=fWidth / 2 - bufferSize * 4, fill=txtColour)

leftRec = canvas.create_rectangle(bufferSize, bufferSize, fWidth / 2 - bufferSize, fHeight - bufferSize, fill=colour1, outline=colour12, width=bufferSize/3)
rightRec = canvas.create_rectangle(fWidth / 2 + bufferSize, bufferSize, fWidth - bufferSize, fHeight - bufferSize, fill=colour2, outline=colour22, width=bufferSize/3)


# gui stuff, alignment, etc
def configure(size):
    global fWidth, fHeight, leftText, rightText, leftRec, rightRec, bsFont, bufferSize
    canvas.delete("all")
    fWidth, fHeight = size.width, size.height

    bufferSize = (1 * fWidth) / 100 + (1 * fHeight) / 100
    bsFont = "Helvetica", (fWidth + fHeight) / 35

    leftRec = canvas.create_rectangle(bufferSize, bufferSize, fWidth / 2 - bufferSize, fHeight - bufferSize,
                                      fill=colour1, outline=colour12, width=bufferSize/3)
    rightRec = canvas.create_rectangle(fWidth / 2 + bufferSize, bufferSize, fWidth - bufferSize, fHeight - bufferSize,
                                       fill=colour2, outline=colour22, width=bufferSize/3)

    leftText = canvas.create_text(fWidth / 4, fHeight / 2, font=bsFont, text=originalTxt, width=fWidth / 2 - bufferSize * 4,
                                  fill=txtColour)
    rightText = canvas.create_text(fWidth / 2 + fWidth / 4, fHeight / 2, font=bsFont, text=newTxt, width=fWidth / 2 - bufferSize * 4,
                                   fill=txtColour)


# this takes care of updating the text when it needs to be and the little animation that happens
class textThread(object):

    def __init__(self, interval=0.1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def updateText(self, lblItem, newStr):
        global leftText, rightText, bufferSize, bsFont, fHeight,fWidth, newTxt, originalTxt, txtColour
        chain = list(newStr)
        for i in range(np.random.randint(3, 10)):
            np.random.shuffle(chain)
            txt = ''.join(chain)
            cConfig(lblItem, txt)
            time.sleep(float(np.random.uniform(0.01, 0.15, 1)))

        txt = newStr
        cConfig(lblItem, txt)
        return txt

    def tweetUpdate(self):
        global newTxt, length, paused, tNum, originalTxt, timeChange, timeChange2, length2
        length = len(newTxt)
        length2 = len(originalTxt)

        if len(ChainMaker.tweets) > tNum:
            timeChange2 = 0
            length2 = len(ChainMaker.tweets[tNum])
            originalTxt = self.updateText(leftText, ChainMaker.tweets[tNum])
            tNum += 1

        if ChainMaker.started is True:
            timeChange += 0.7
            timeChange2 += 0.7

        if timeChange > length + 1:
            newChain = ChainMaker.generateChain()
            length = len(newChain)
            timeChange = 0
            newTxt = self.updateText(rightText, newChain)

        if timeChange2 > length2 + 1:
            nT = np.random.choice(ChainMaker.tweets)

            while nT == "":
                nT = np.random.choice(ChainMaker.tweets)

            originalTxt = self.updateText(leftText, nT)
            length2 = len(nT)
            timeChange2 = 0

    def run(self):
        while True:
            self.tweetUpdate()

            time.sleep(self.interval)


# canvas configuration on text update
def cConfig(lblItem, txt):
    canvas.itemconfigure(lblItem, text=txt)
    canvas.update()


# initialize twitter scrubber as a thread through a function in the main class
def init_stream():
    TwitterScrubber.setup()


# most of the setup stuff happens here, lots of threading
if __name__ == '__main__':
    canvas.bind("<Configure>", configure)
    txtThread = textThread()

    tw = threading.Thread(target=init_stream)
    tw.setDaemon(True)
    tw.start()

    canvas.itemconfigure(rightText, text=newTxt)

    window.mainloop()