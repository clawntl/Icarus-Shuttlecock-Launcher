enableKeybinds = True #Set the this to False to disable keybindings

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, Menu, PhotoImage, simpledialog
from tkinter import messagebox as box
from random import randint,randrange

#Allow a file to be found relatively
def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class Application(tk.Frame):
    def __init__(self, master=None,keybinds=None):
        super().__init__(master)
        self.master = master
        self.keybinds = keybinds
        #Set the title
        master.title("Shuttlecock Launcher Programme Creator")
        #Set the resolution and minimum resolution
        master.geometry("1000x567+490+240")
        master.minsize(1000,567)
        #Set the leave protocol
        master.protocol("WM_DELETE_WINDOW", self.exitWithoutSaving)

        #Set the icon
        img = PhotoImage(file=resource_path("icon.gif"))
        master.tk.call("wm", "iconphoto", master._w, img)

        #Setup keybindings (if enabled)
        if keybinds == True:
            master.bind("<Control-n>", lambda event: self.newProgram())
            master.bind("<Control-o>", lambda event: self.openProgram())
            master.bind("<Control-s>", lambda event: self.saveProgram())
            master.bind("<Control-S>", lambda event: self.saveAs())
            master.bind("<Control-q>", lambda event: self.exitWithoutSaving())

            master.bind("<Return>", lambda event: self.addNewShot())
            master.bind("<Insert>", lambda event: self.editShot())
            master.bind("<Delete>", lambda event: self.removeShot())
            master.bind("<Control-c>", lambda event: self.copyShot())
            master.bind("<Control-v>", lambda event: self.pasteShot())

        #Setup Variables
        self.shotNumber = 0
        self.shotNumberString = tk.StringVar()
        self.shotNumberString.set(f"Number of shots: {self.shotNumber}")
        self.saveas = True

        #Setup the grid
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")

        #Create the widgets
        self.createWidgets()

    def createWidgets(self):
        #Create menubar
        menubar = Menu(self.master,tearoff=0)
        self.master.config(menu=menubar)

        #Create menus
        fileMenu = Menu(menubar,tearoff=0)
        editMenu = Menu(menubar,tearoff=0)
        helpMenu = Menu(menubar,tearoff=0)

        #Add commands (depends on if keybinds are enabled)
        if self.keybinds == True:
            fileMenu.add_command(label="New               Ctrl+N", command=self.newProgram)
            fileMenu.add_command(label="Open             Ctrl+O", command=self.openProgram)
            fileMenu.add_command(label="Save               Ctrl+S", command=self.saveProgram)
            fileMenu.add_command(label="Save As...       Ctrl+Shift+S", command=self.saveAs)
            fileMenu.add_separator()
            fileMenu.add_command(label="Exit                 Ctrl+Q", command=self.exitWithoutSaving)

            editMenu.add_command(label="Add                Enter", command=self.addNewShot)
            editMenu.add_command(label="Edit                 Insert", command=self.editShot)
            editMenu.add_command(label="Delete             Del", command=self.removeShot)
            editMenu.add_separator()
            editMenu.add_command(label="Copy Shot(s)   Ctrl+C", command=self.copyShot)
            editMenu.add_command(label="Paste Shot(s)   Ctrl+V", command=self.addNewShot)

        else:
            fileMenu.add_command(label="New", command=self.newProgram)
            fileMenu.add_command(label="Open", command=self.openProgram)
            fileMenu.add_command(label="Save", command=self.saveProgram)
            fileMenu.add_command(label="Save As...", command=self.saveAs)
            fileMenu.add_separator()
            fileMenu.add_command(label="Exit", command=self.exitWithoutSaving)

            editMenu.add_command(label="Add", command=self.addNewShot)
            editMenu.add_command(label="Edit", command=self.editShot)
            editMenu.add_command(label="Delete", command=self.removeShot)
            editMenu.add_separator()
            editMenu.add_command(label="Copy Shot(s)", command=self.copyShot)
            editMenu.add_command(label="Paste Shot(s)", command=self.addNewShot)
        helpMenu.add_command(label="About", command=self.about)

        #Add the menus to the menubar as cascades
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Edit", menu=editMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)

        #Scales and checkbuttons (launch parameters)
        self.shotNumberLabel = tk.Label(self,textvariable=self.shotNumberString,font=(None, 12))
        self.shotNumberLabel.grid(row=0,column=0,padx=(20,5),pady=(10,5), sticky="nsew")

        self.speed = tk.Scale(self, from_=10, to=50, orient=tk.HORIZONTAL,length=200,font=(None, 10))
        self.speed["label"] = "Speed:"
        self.speed.set(10)
        self.speed.grid(row=1,column=0,padx=(40,20),pady=(10,5), sticky="nsew")

        self.direction = tk.Scale(self, from_=-60, to=60, orient=tk.HORIZONTAL,length=200,font=(None, 10),resolution=10)
        self.direction["label"] = "Direction:"
        self.direction.set(0)
        self.direction.grid(row=2,column=0,padx=(40,20),pady=5, sticky="nsew")

        self.pitch = tk.Scale(self, from_=0, to=80, orient=tk.HORIZONTAL,length=200,font=(None, 10),resolution=10)
        self.pitch["label"] = "Pitch:"
        self.pitch.set(0)
        self.pitch.grid(row=3,column=0,padx=(40,20),pady=5, sticky="nsew")

        self.delay = tk.Scale(self, from_=0, to=15, orient=tk.HORIZONTAL,command=self.updateMaxBuzzerLedDelay,length=200,font=(None, 10))
        self.delay["label"] = "Shot Delay:"
        self.delay.set(2)
        self.delay.grid(row=4,column=0,padx=(40,20),pady=5, sticky="nsew")

        self.buzzerState = tk.IntVar()
        self.buzzer = tk.Checkbutton(self, text="Buzzer",variable=self.buzzerState,font=(None, 12))
        self.buzzer.grid(row=5,column=0,padx=(40,20),pady=5, sticky="nsew")

        self.ledState = tk.IntVar()
        self.led = tk.Checkbutton(self, text="LED",variable=self.ledState,font=(None, 12))
        self.led.grid(row=6,column=0,padx=(40,20),pady=5, sticky="nsew")

        self.LED_BUZZER_delay = tk.Scale(self, from_=0, to=self.delay.get(), orient=tk.HORIZONTAL,length=400,font=(None, 10))
        self.LED_BUZZER_delay["label"] = "LED/Buzzer Delay:"
        self.LED_BUZZER_delay.set(0)
        self.LED_BUZZER_delay.grid(row=7,column=0,padx=(40,20),pady=5, sticky="nsew")

        #Buttons
        self.add = tk.Button(self, text="Add",command=self.addNewShot, height = 1, width = 5)
        self.add.grid(row=8,column=2,padx=0,pady=(10,20), sticky="nsew")

        self.edit = tk.Button(self, text="Edit",command=self.editShot, height = 1, width = 5)
        self.edit.grid(row=8,column=4,padx=0,pady=(10,20), sticky="nsew")

        self.delete = tk.Button(self, text="Delete",command=self.removeShot, height = 1, width = 5)
        self.delete.grid(row=8,column=6,padx=0,pady=(10,20), sticky="nsew")

        self.random = tk.Button(self, text="Random",command=self.randomShots, height = 1, width = 5)
        self.random.grid(row=8,column=8,padx=0,pady=(10,20), sticky="nsew")

        self.save = tk.Button(self, text="Save",command=self.saveProgram, height = 1, width = 5)
        self.save.grid(row=8,column=10,padx=0,pady=(10,20), sticky="nsew")

        self.exit = tk.Button(self, text="Exit",command=self.exitWithoutSaving,height = 1, width = 5)
        self.exit.grid(row=8,column=12,padx=0,pady=(10,20), sticky="nsew")

        #Setup the treeview and scrollbar
        style = ttk.Style(self)
        style.configure("Treeview", rowheight=29)
        self.shots = ttk.Treeview(self,height=15)
        self.scrollbar = ttk.Scrollbar(orient="vertical",command=self.shots.yview)
        self.scrollbar.grid(row=0,column=14,padx=(0,20),pady=(20,66),sticky="nsew")
        self.shots.configure(yscrollcommand=self.scrollbar.set)

        self.shots["columns"] = ("Speed", "Direction","Pitch","Delay","Buzzer","LED","Buzzer/LED Delay")
        self.shots.column("#0", width=0,minwidth=0,stretch=False)
        self.shots.column("Speed", width=50,minwidth=50, anchor="center",stretch=True)
        self.shots.column("Direction", width=60,minwidth=60, anchor="center",stretch=True)
        self.shots.column("Pitch", width=50,minwidth=50, anchor="center",stretch=True)
        self.shots.column("Delay", width=50,minwidth=50, anchor="center",stretch=True)
        self.shots.column("Buzzer", width=50,minwidth=50, anchor="center",stretch=True)
        self.shots.column("LED", width=50,minwidth=50, anchor="center",stretch=True)
        self.shots.column("Buzzer/LED Delay", width=100,minwidth=100, anchor="center",stretch=True)
        self.shots.heading("Speed", text="Speed",anchor="center")
        self.shots.heading("Direction", text="Direction",anchor="center")
        self.shots.heading("Pitch", text="Pitch",anchor="center")
        self.shots.heading("Delay", text="Delay",anchor="center")
        self.shots.heading("Buzzer", text="Buzzer",anchor="center")
        self.shots.heading("LED", text="LED",anchor="center")
        self.shots.heading("Buzzer/LED Delay", text="Buzzer/LED Delay",anchor="center")
        self.shots.grid(row=0,column=1,rowspan=8,padx=(10,0),pady=(20,10),columnspan=13, sticky="nsew")
        self.shots.tag_configure("T", font=(None, 12))

        #Configure the columns and rows
        for x in range(14):
            self.columnconfigure(x, weight=1)
        for y in range(7):
            self.rowconfigure(y, weight=1)

        #Prevent treeview columns from being adjusted
        def disableEvent(event):
            if self.shots.identify_region(event.x, event.y) == "separator":
                return "break"

        self.shots.bind("<Button-1>", disableEvent)
        self.shots.bind("<Motion>", disableEvent)

    #Check if the user wants to leave without saving
    def exitWithoutSaving(self):
        if self.saveas == True and  self.shots.get_children() != ():
            checkLeave = box.askyesnocancel("Exit", "Do you want to exit without saving?")
            if  checkLeave == True:
                self.master.destroy()
            elif checkLeave == False:
                self.saveProgram()
        else:
            self.master.destroy()

    #Update the limit for the LED/Buzzer Delay
    def updateMaxBuzzerLedDelay(self,value):
        self.LED_BUZZER_delay.configure(to=value)

    #Add a shot to the treeview
    def addNewShot(self):
        if self.shotNumber <= 29:
            values = (f"{self.speed.get()}",f"{self.direction.get()}",f"{self.pitch.get()}",
                      f"{self.delay.get()}",f"{['Off','On'][self.buzzerState.get()]}",
                      f"{['Off','On'][self.ledState.get()]}",f"{self.LED_BUZZER_delay.get()}")

            self.shots.insert("","end",values=values,tags="T")
            self.shotNumber += 1
            self.shotNumberString.set(f"Number of shots: {self.shotNumber}")
        else:
            box.showwarning("Shot Limit Reached","The shot limit of 30 has been reached.")

    #Update the selected shot(s) with the current settings
    def editShot(self):
        selected_items = self.shots.selection()
        values = (f"{self.speed.get()}",f"{self.direction.get()}",f"{self.pitch.get()}",
                  f"{self.delay.get()}",f"{['Off','On'][self.buzzerState.get()]}",
                  f"{['Off','On'][self.ledState.get()]}",f"{self.LED_BUZZER_delay.get()}")
        self.shots.item(selected_items[0],values = values)

    #Remove a shot from the treeview
    def removeShot(self):
        selected_items = self.shots.selection()
        for selected_item in selected_items:
            self.shots.delete(selected_item)
        self.shotNumber -= len(selected_items)
        self.shotNumberString.set(f"Number of shots: {self.shotNumber}")

    #Add selected shots to the clipboard
    def copyShot(self):
        self.clipboard = self.shots.selection()

    #Add clipboard shots to the treeview
    def pasteShot(self):
        #Store the parameters so they can be retained
        previousSettings = [self.speed.get(),self.direction.get(),self.pitch.get(),
                           self.delay.get(),self.buzzerState.get(),self.ledState.get(),
                           self.LED_BUZZER_delay.get()]
        #Add shots from clipboard
        for item in self.clipboard:
            vals = self.shots.item(f"{item}")["values"]
            self.speed.set(vals[0])
            self.direction.set(vals[1])
            self.pitch.set(vals[2])
            self.delay.set(vals[3])
            if vals[4] == "Off":
                self.buzzerState.set(0)
            elif vals[4] == "On":
                self.buzzerState.set(1)
            if vals[5] == "Off":
                self.ledState.set(0)
            elif vals[5] == "On":
                self.ledState.set(1)
            self.LED_BUZZER_delay.set(vals[6])
            self.addNewShot()
        #Reset back to the original parameters
        self.speed.set(previousSettings[0])
        self.direction.set(previousSettings[1])
        self.pitch.set(previousSettings[2])
        self.delay.set(previousSettings[3])
        self.buzzerState.set(previousSettings[4])
        self.ledState.set(previousSettings[5])
        self.LED_BUZZER_delay.set(previousSettings[6])

    #Generate random shots
    def randomShots(self):
        num = simpledialog.askinteger("Random Shots", "Number of Shots:",parent=self.master,minvalue=1, maxvalue=(30-self.shotNumber))
        maxSpeed = self.speed.get()
        maxPitch = self.pitch.get()
        if maxPitch == 0:
            pitch = 0
        else:
            pitch = randrange(0,maxPitch,10)
        for i in range(0,num):
            self.speed.set(randint(10,maxSpeed))
            self.direction.set(randrange(-60,60,10))
            self.pitch.set(pitch)
            self.delay.set(randint(0,15))
            self.updateMaxBuzzerLedDelay(self.delay.get())
            self.buzzerState.set(randint(0,1))
            self.ledState.set(randint(0,1))
            self.LED_BUZZER_delay.set(randint(0,self.delay.get()))
            self.addNewShot()

    #Clear the treeview
    def clearProgram(self):
        self.shots.delete(*self.shots.get_children())
        self.shotNumber = 0
        self.shotNumberString.set(f"Number of shots: {self.shotNumber}")

    #Create a new program
    def newProgram(self):
        self.checkSaved("Open")
        self.clearProgram()
        self.saveas = True

    #Open a program
    def openProgram(self):
        self.checkSaved("Open")
        self.saveas = False
        self.filename =  filedialog.askopenfilename(initialdir = "/",title = "Open",filetypes = (("txt files","*.txt"),("all files","*.*")),defaultextension="*.txt*")
        file = open(self.filename,"r")
        self.clearProgram()
        lines=file.readlines()
        for i in range(0,len(lines),7):
            line = lines[i:i+7]
            self.speed.set(int(line[0]))
            self.direction.set(int(line[1]))
            self.pitch.set(int(line[2]))
            self.delay.set(int(line[3]))
            self.buzzerState.set(int(line[4]))
            self.ledState.set(int(line[5]))
            self.LED_BUZZER_delay.set(int(line[6].rstrip("\x00")))
            self.addNewShot()

    #Check if the program has been saved
    def checkSaved(self,boxtitle):
        if self.saveas == True and  self.shots.get_children() != ():
            checkSave = box.askyesnocancel(boxtitle, "Do you want to save the current file?")
            if checkSave == True:
                self.saveProgram()

    #Check if a file has already been saved or not
    def saveProgram(self):
        if self.shots.get_children() != ():
            if self.saveas == True:
                self.saveAs()
            else:
                self.saveNormal()
        else:
            box.showwarning("File Empty","The programme must have at least 1 shot.")

    #Save the program
    def saveNormal(self):
        self.shotsData = []
        for i in self.shots.get_children():
            shots = self.shots.item(f"{i}")["values"]
            for shot in shots:
                if shot == "Off":
                    shot = 0
                elif shot == "On":
                    shot = 1
                self.shotsData.append(shot)
        file = open(self.filename,"w")
        counter = 0
        for data in self.shotsData:
            file.write(str(data))
            if counter == len(self.shotsData)-1:
                file.write("\0")
            else:
                file.write("\n")
            counter += 1
        file.close()
        self.saveas = False

    #Save the program as
    def saveAs(self):
        self.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Save as...",filetypes = (("txt files","*.txt"),("all files","*.*")),defaultextension="*.txt*")
        self.saveNormal()

    #About window
    def about(self):
        aboutInfo = tk.Toplevel(self)
        aboutInfo.wm_title("About")
        img = PhotoImage(file=resource_path("icon.gif"))
        aboutInfo.tk.call("wm", "iconphoto", aboutInfo._w, img)
        aboutInfo.geometry("300x100+810+470")
        aboutInfo.resizable(0, 0)
        aboutTitle = tk.Label(aboutInfo, text="Shuttlecock Laucher Programme Creator",anchor="center")
        aboutCreator = tk.Label(aboutInfo, text="by Nathan Law",anchor="center")
        aboutTitle.pack(side="top",pady=10)
        aboutCreator.pack(side="top",pady=10)

def main():
    root = tk.Tk()
    app = Application(master=root,keybinds=enableKeybinds)
    app.mainloop()

if __name__ == "__main__":
    main()
