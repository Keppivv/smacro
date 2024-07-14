import threading
import time
import mousekey
import keyboard
import ctypes
import tkinter as tk

# Globals
playing = False
timeBetweenLoops = 500  # 0.5 Seconds (500ms) by default
rightClickTypeList = ["rightclick", "rclick"]
leftClickTypeList = ["leftclick", "click", "lclick", "normalclick"]
middleClickTypeList = ["mclick", "middleclick", "scrollclick", "scrollwheelclick", "wheelclick"]
delayTypeList = ["sleep", "duration", "delay"]
keyTypeList = ["press", "presskey"]
isInf = False
FPS = 30
# Functions
def StartClicked():
    global playing
    playing = True
    startBtn.config(state="disabled")
    stopBtn.config(state="normal")
    grabText = macroField.get(1.0, tk.END).splitlines()
    grabText = [line for line in grabText if line.strip()]
    print("Starting Thread")
    thread = threading.Thread(target=startPlaying, args=(grabText,))
    thread.start()

def infBox():
    global isInf
    isInf = not isInf
def hotkeyClick():
    global playing
    if playing:
        playing = False
    else:
        StartClicked()
def startPlaying(inText):
    global playing
    global timeBetweenLoops
    global isInf
    total_loops = int(loopCount_Input.get())
    timeBetweenLoops = int(tbl_Input.get())
    cLoops = 0
    while playing and cLoops < total_loops:
        for textIn in inText:
            command = parseCommand(textIn)
            execCommand(command=command)
        time.sleep(float(float(timeBetweenLoops) / float(1000)))
        if not isInf:
            cLoops += 1
    print("Killing Thread")
    playing = False
    startBtn.config(state="normal")
    stopBtn.config(state="disabled")


def StopClicking():
    global playing
    playing = False
    startBtn.config(state="normal")
    stopBtn.config(state="disabled")


def execCommand(command):
    typa = command[0].lower()
    x = command[1]
    y = command[2]
    delay = float(command[3] / 1000)
    key = command[4]
    if typa in leftClickTypeList:
        mousekey.MouseKey().move_to(x=x, y=y)
        mousekey.left_click_xy_natural(x=x, y=y, print_coords=False, delay=delay)
    elif typa in rightClickTypeList:
        mousekey.MouseKey().move_to(x=x, y=y)
        mousekey.right_click_xy_natural(x=x, y=y, print_coords=False, delay=delay)
    elif typa in middleClickTypeList:
        mousekey.MouseKey().move_to(x=x, y=y)
        mousekey.middle_click_xy_natural(x=x, y=y, print_coords=False, delay=delay)
    elif str(typa) in delayTypeList:
        time.sleep(delay)
    elif str(typa) in keyTypeList:
        mousekey.MouseKey().press_key(keycode=key, delay=delay)

def nameChange():
    while True:
        x, y = mousekey.MouseKey().get_cursor_position()
        titleString = "x:" + str(x) + " y:" + str(y)
        root.title(titleString)
        time.sleep(float(1/FPS))

def parseCommand(command):
    commandType = None
    duration = 5  # 5ms Default
    key = None
    locationX, locationY = mousekey.MouseKey().get_cursor_position()
    for part in command.rsplit(" "):
        if commandType is None:
            if part.lower() in leftClickTypeList:
                commandType = part.lower()
            if part.lower() in delayTypeList:
                commandType = part.lower()
            if part.lower() in keyTypeList:
                commandType = part.lower()
        if str(part).rfind("x=", 0, 2) == 0:
            locationX = str(part).removeprefix("x=")
        if str(part).rfind("y=", 0, 2) == 0:
            locationY = str(part).removeprefix("y=")
        if str(part).rfind("duration=", 0, 9) == 0:
            duration = str(part).removeprefix("duration=")
        if str(part).rfind("delay=", 0, 6) == 0:
            duration = str(part).removeprefix("delay=")
        if str(part).rfind("key=", 0, 4) == 0:
            key = str(part).removeprefix("key=")

    return [str(commandType), int(locationX), int(locationY), float(duration), str(key)]


root = tk.Tk()
root.title("WR >> M")
root.geometry("285x275+15+15")
root.attributes("-topmost", True)
root.attributes("-toolwindow", True)

macroField = tk.Text(root, width=35, height=8, wrap="none")
macroField.grid(column=1, columnspan=2, row=0, pady=5)

tbl_Label = tk.Label(root, text="Time Between Loops (ms)", height=1)
tbl_Label.grid(column=1, row=1, pady=5)
tbl_Input = tk.Entry(root, width=10)
tbl_Input.grid(column=2, row=1, pady=5)
tbl_Input.insert(0, "1")

loopCount_Label = tk.Label(root, text="Loop Count")
loopCount_Label.grid(column=1, row=2, pady=5)
loopCount_Input = tk.Entry(root, width=10)
loopCount_Input.grid(column=2, row=2, pady=5)
loopCount_Input.insert(0, "1")
loop_InfBox = tk.Checkbutton(root, text="Infinite Loop", command=infBox)
loop_InfBox.grid(column=2, row=3, pady=5)

startBtn = tk.Button(root, text="Start (F6)", width=7, height=1, command=StartClicked)
startBtn.grid(column=1, row=4, pady=5)
stopBtn = tk.Button(root, text="Stop (F6)", width=7, height=1, state="disabled", command=StopClicking)
stopBtn.grid(column=2, row=4, pady=5)

label_LoopTime = tk.Label(root, text="Loop Delay:")
label_LoopCount = tk.Label(root, text="Loops:")

keyboard.add_hotkey("F6", hotkeyClick, suppress=True)

thready = threading.Thread(target=nameChange)
thready.start()

root.mainloop()
