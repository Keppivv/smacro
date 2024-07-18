import threading
import time
import tkinter as tk
from tkinter import ttk
import mousekey
import pyautogui
import keyboard
class Normal:

    def doMouseMove(self, x, y):
        mousekey.natural_mouse_movement(x=int(x), y=int(y))
    def doMouseClick(self, isRight, delay):
        if isRight:
            mousekey.MouseKey().right_mouse_down()
            time.sleep(float(delay)/1000)
            mousekey.MouseKey().right_mouse_up()
        else:
            mousekey.MouseKey().left_mouse_down()
            time.sleep(float(delay) / 1000)
            mousekey.MouseKey().left_mouse_up()
    def doKeyPress(self, key, holdDuration):
        keyboard.press_and_release(str(key), True, False)
        time.sleep(float(holdDuration)/1000)
        keyboard.press_and_release(str(key), False, True)
    def doDelay(self, delay):
        time.sleep(float(delay)/1000)
    def startMacro(self):
        self.currentLoops = 0
        if self.infiboxValue == 1:
            self.maxLoops = 200
        else:
            getLoops = self.loopInput.get()
            if not str(getLoops).isnumeric():
                getLoops = 1
            self.maxLoops = int(getLoops)
        self.running = True
        self.startMacroButton.configure(state="disabled")
        self.stopMacroButton.configure(state="enabled")
        thread = threading.Thread(target=self.playMacro)
        thread.start()
    def playMacro(self):
        while self.running and self.currentLoops < self.maxLoops:
            for i in self.actionList:
                actionType, x, y, key, delay = None, None, None, None, None
                for e in self.actionList[i]:
                    if str(e).startswith("X="):
                        x = str(e).removeprefix("X=")
                    elif str(e).startswith("Y="):
                        y = str(e).removeprefix("Y=")
                    elif str(e).startswith("Type="):
                        actionType = str(e).removeprefix("Type=")
                    elif str(e).startswith("Key="):
                        key = str(e).removeprefix("Key=")
                    elif str(e).startswith("Delay="):
                        delay = str(e).removeprefix("Delay=")
                if actionType == "Left Click":
                    if x == "None":
                        x = int(pyautogui.position().x)
                    if y == "None":
                        y = int(pyautogui.position().y)
                    shouldMove = False
                    if int(x) > pyautogui.position().x + 1 or int(x) < pyautogui.position().x - 1:
                        shouldMove = True
                    if int(y) > pyautogui.position().y + 1 or int(y) < pyautogui.position().y - 1:
                        shouldMove = True
                    if shouldMove:
                        self.doMouseMove(int(x), int(y))
                    self.doMouseClick(False, delay)
                if actionType == "Right Click":
                    if x == "None":
                        x = pyautogui.position().x
                    if y == "None":
                        y = pyautogui.position().y
                    shouldMove = False
                    if int(x) > pyautogui.position().x+1 or int(x) < pyautogui.position().x-1:
                        shouldMove = True
                    if int(y) > pyautogui.position().y + 1 or int(y) < pyautogui.position().y - 1:
                        shouldMove = True
                    if shouldMove:
                        self.doMouseMove(int(x), int(y))
                    self.doMouseClick(True, delay)
                if actionType == "Key Press":
                    self.doKeyPress(key, delay)
                if actionType == "Delay":
                    self.doDelay(delay)
            if self.infiboxValue == 0:
                self.currentLoops += 1
        self.running = False
        self.startMacroButton.configure(state="enabled")
        self.stopMacroButton.configure(state="disabled")
    def removeActions(self):
        for i in self.scrollable_frame.winfo_children():
            i.destroy()
            self.removeActionsButton.configure(state="normal")
            self.addActionButton.configure(state="normal")
            self.actionList = {}
    def stopRun(self):
        self.running = False
    def addAction(self):
        self.addActionButton.configure(state="disabled")
        self.removeActionsButton.configure(state="disabled")
        def removeThisAction():
            localFrame.destroy()
            self.addActionButton.configure(state="normal")
            self.removeActionsButton.configure(state="normal")
        def validateAction():
            a_type, x, y, key, delay = "Delay", "None", "None", "None", 500
            if len(localType.get()) >= 1:
                a_type = localType.get()
            if len(localXPosInput.get()) >= 1:
                x = localXPosInput.get()
            if len(localYPosInput.get()) >= 1:
                y = localYPosInput.get()
            if len(localKeyInput.get()) >= 1:
                key = localKeyInput.get()
            if len(localDelayInput.get()) >= 1:
                delay = localDelayInput.get()
            localCommand = {f"Type={a_type}", f"X={x}", f"Y={y}", f"Key={key}", f"Delay={delay}",
                            f"index:{len(self.actionList)}"}
            localValidateButton.destroy()
            self.actionList[len(self.actionList)] = localCommand
            self.addActionButton.configure(state="normal")
            self.removeActionsButton.configure(state="normal")
            localRemoveButton.destroy()
            localType.configure(state="disabled")
            localXPosInput.configure(state="disabled")
            localYPosInput.configure(state="disabled")
            localKeyInput.configure(state="disabled")
            localDelayInput.configure(state="disabled")


        localIndex = len(self.scrollable_frame.children)

        localFrame = tk.Frame(self.scrollable_frame)
        localType = ttk.Combobox(localFrame, values=("Left Click", "Right Click", "Key Press", "Delay"), width=10)
        localType.grid(row=0, column=0, padx=3)

        localXPosLabel = tk.Label(localFrame, text="x:", width=1)
        localXPosLabel.grid(row=0, column=1)
        localXPosInput = tk.Entry(localFrame, width=4)
        localXPosInput.grid(row=0, column=2)

        localYPosLabel = tk.Label(localFrame, text="y:", width=1)
        localYPosLabel.grid(row=0, column=3)
        localYPosInput = tk.Entry(localFrame, width=4)
        localYPosInput.grid(row=0, column=4)

        localKeyLabel = tk.Label(localFrame, text="key:", width=3)
        localKeyLabel.grid(row=0, column=5)
        localKeyInput = tk.Entry(localFrame, width=2)
        localKeyInput.grid(row=0, column=6)

        localDelayLabel = tk.Label(localFrame, text="delay:", width=5)
        localDelayLabel.grid(row=0, column=7)
        localDelayInput = tk.Entry(localFrame, width=6)
        localDelayInput.grid(row=0, column=8)


        localValidateButton = tk.Button(localFrame, text="✔", bg="light green", width=2, height=1,
                                        command=validateAction)
        localValidateButton.grid(row=0, column=9, padx=10)
        localRemoveButton = tk.Button(localFrame, text="X", bg="red", width=2, height=1, command=removeThisAction)
        localRemoveButton.grid(row=0, column=10, padx=0)
        localFrame.pack(fill="x", pady=5)
    def hotkeyPress(self):
        if self.running == True:
            self.running = False
        else:
            self.startMacro()
    def Start(self):
        self.top_button_frame = ttk.Frame(self.root)
        self.top_button_frame.pack(side="top", fill="x")

        # Add buttons to the button frame
        self.addActionButton = ttk.Button(self.top_button_frame, text="Add Action", command=self.addAction)
        self.addActionButton.pack(side="left", padx=5, pady=5)
        self.removeActionsButton = ttk.Button(self.top_button_frame, text="Remove All Actions",
                                              command=self.removeActions)
        self.removeActionsButton.pack(side="left", padx=5, pady=5)

        self.canvas_frame = ttk.Frame(self.root)
        self.canvas_frame.pack(side="top", fill="both", expand=True)

        # Create a canvas and a vertical scrollbar
        self.canvas = tk.Canvas(self.canvas_frame)
        self.scrollbar = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)),
                                                                                "units"))

        # Configure the canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.configure(scrollregion=(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height()))

        # Create a window in the canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the canvas and scrollbar into the canvas frame
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        def infiBox():
            if self.infiboxValue == 0:
                self.infiboxValue = 1
            else:
                self.infiboxValue = 0
        self.downFrame = tk.Frame(self.root)
        self.downFrame.pack(side="bottom", fill="x")
        self.loopLabel = tk.Label(self.downFrame, text="Loops:", width=5)
        self.loopLabel.pack(side="left", pady=10, padx=5)
        self.loopInput = tk.Entry(self.downFrame, width=7)
        self.loopInput.insert(1, "1")
        self.loopInput.pack(side="left", padx=5, pady=10)
        self.infiniteBox = tk.Checkbutton(self.downFrame, width=12, text="infinite Loops", command=infiBox)
        self.infiniteBox.pack(side="left", padx=20, pady=10)

        # Create a frame for the buttons
        self.down_button_frame = ttk.Frame(self.root)
        self.down_button_frame.pack(side="bottom", fill="x")

        # Add buttons to the button frame
        self.saveMacroButton = ttk.Button(self.down_button_frame, text="Save Macro")
        self.saveMacroButton.pack(side="left", padx=5, pady=5)
        self.stopMacroButton = ttk.Button(self.down_button_frame, text="Stop (F6)", state="disabled")
        self.stopMacroButton.pack(side="right", padx=5, pady=5)
        self.startMacroButton = ttk.Button(self.down_button_frame, text="Play (F6)", command=self.startMacro)
        self.startMacroButton.pack(side="right", padx=5, pady=5)

    def titleUpdater(self):
        FPS = 0.01
        while True:
            self.root.title(f"X:{int(pyautogui.position().x)} Y:{int(pyautogui.position().y)}")
            time.sleep(FPS)

    def __init__(self):
        self.actionList = {}
        self.running = False
        self.infiboxValue = 0
        self.currentLoops = 0
        self.maxLoops = 1
        keyboard.add_hotkey("F6", self.hotkeyPress, suppress=True)
        self.root = tk.Tk()
        self.root.title("---")
        self.root.geometry("420x380+15+15")
        self.root.attributes("-topmost", True)
        self.root.attributes("-toolwindow", True)
        self.root.after(500, self.Start)
        thready = threading.Thread(target=self.titleUpdater)
        thready.start()
        self.root.mainloop()

Normal()
