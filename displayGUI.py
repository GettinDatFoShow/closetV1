#START CODE
#Author: Robert Morris

__author__ = 'Robert Morris'
'''This file contains the tkinter code for the creation of the GUI
interface of the closetV1 storage system.'''

from tkinter import *
import time
from guts import * # import classes for the guts of the system

# GLOBAL Variables

LARGE_FONT = ("Verdana", 11, 'bold italic') # Bottom Button fonts
QUIT_FONT = ("Verdana", 11, 'bold italic') # quit button font
BB_COLOR = "#4682b4" #(70, 130, 180) # Bottom Button Colors = steel blue
TB_FG_COLOR = "#000000" # Tray Button fore ground color = black
TB_BG_COLOR = "#a0522d" #(160, 82, 45) # Tray Button back ground color = sienna
BOT_COLOR = TB_FG_COLOR # Bottom window Color = sienna

class Closet:

    def __init__(self, master=None, start=False):
        self.setUpVariables(start=start) # call to system variable setup function
        self.frame = Frame(master) # initialize app frame
        self.topWindow = Frame(master, bg=TB_BG_COLOR) # initialize inner top 2 tray buttons host frame with color
        self.midWindow = Frame(master, bg=TB_BG_COLOR) # initialize inner bottom 2 tray buttons host frame with color
        self.botWindow = Frame(master, bg=BOT_COLOR) # initialize bottom frame to hose user input buttons with color
        self.createTrays() # call to tray button creation function
        self.createButtons() # call to user input button creation function
        self.topWindow.pack(expand=1, side='top', fill='both') # finalize top window
        self.midWindow.pack(expand=1, fill='both' )# finalize middle window
        self.botWindow.pack(side='bottom', fill='x') # finalize bottome window
        self.frame.pack() # finalize app window

    def setUpVariables(self, start=False):
        """
        Function sets the system Atributes
        :return: None
        """

        self.sender = InfoSender('/dev/ttyACM0', 9600) # initialize serial class connection to arduino
        self.cam = TrayCam() #initializes camera class
        self.cam.camLightOff() # sets camera flash off
        self.sender.sendInfo("close\n") # serial command to initialize the door to close on startup
        self.start = start # variable for system startup tray picture loader commmand
        self.imageArchive = "/home/pi/pyCode/closetV1/Images/" #location for picture storage
        self.ledNumber = LEDCounter(1) #seven seg display class initialization
        self.open = 0 # open/close boolean door variable
        self.rotating = 0 # table rotating boolean variable
        if self.start == True: # check for tray picture load apon startup
            self.startUp()
            self.AllImageUpdater()
        else:
            self.AllImageUpdater()

    def createTrays(self):
        """
        function sets up storage trays, creates tkinter buttons for trays and pictures and configures them
        :return: None
        """

        self.tray1 = Button(self.topWindow, text="Tray 1",
                            bg=TB_FG_COLOR, fg='white', command=self.buttonPress1)
        self.tray2 = Button(self.topWindow, text="Tray 2",
                            bg=TB_FG_COLOR, fg='white', command=self.buttonPress2)
        self.tray3 = Button(self.midWindow, text="Tray 3",
                            bg=TB_FG_COLOR, fg='white', command=self.buttonPress3)
        self.tray4 = Button(self.midWindow, text="Tray 4",
                            bg=TB_FG_COLOR, fg='white', command=self.buttonPress4)
        self.trayConfig() # calls pictures configure function
        # place buttons inside master window
        self.tray1.pack(side='left', expand=1, fill='both')
        self.tray2.pack(side='right', expand=1, fill='both')
        self.tray3.pack(side='left', expand=1, fill='both')
        self.tray4.pack(side='right', expand=1, fill='both')

    def createButtons(self):
        """
        function sets up system/user control buttons for bottom window in gui and configures them
        :return: None
        """
        self.exitProgButton = quitButton(self.botWindow)

        self.reload = Button(self.botWindow, text=" "*10+ "Reload" + " " *10 ,
                             bg=BB_COLOR, fg='black', font=LARGE_FONT, command=self.RELOADALL)

        self.door = Button(self.botWindow, text=" "*8 + "Open/Close" + " "*8,
                           bg=BB_COLOR, fg='black', font=LARGE_FONT, command=self.OPENCLOSE)

        self.turnl = Button(self.botWindow, text=" "*10+ "Turn L" + " "*10,
                            bg=BB_COLOR, fg='black', font=LARGE_FONT, command=self.TURNL)

        self.turnr = Button(self.botWindow, text=" "*10 + "Turn R" + " "*10,
                            bg=BB_COLOR, fg='black', font=LARGE_FONT, command=self.TURNR)

        self.table = Button(self.botWindow, text=" "*7+ "Adjust Table" + " "*7,
                            bg=BB_COLOR, fg='black', font=LARGE_FONT, command=self.CALIBRATE)
        # place buttons inside master window
        self.door.pack(padx=5, side='left', expand=1)
        self.reload.pack(padx=5,  side='left', expand=1)
        self.turnr.pack(padx=5, side='left', expand=1)
        self.table.pack(padx=5, side='right', expand=1)
        self.turnl.pack(padx=5, side='right', expand=1)
        self.tray3.pack(side='left', expand=1, fill='both')
        self.tray4.pack(side='right', expand=1, fill='both')

    def AllImageUpdater(self):
        """
        class settor/mutator and image initialization function
        :return: None
        """
        self.tray_one_image = TrayImage(self.imageArchive, "tray1", "jpg")
        self.tray_two_image = TrayImage(self.imageArchive, "tray2", "jpg")
        self.tray_three_image = TrayImage(self.imageArchive, "tray3", "jpg")
        self.tray_four_image = TrayImage(self.imageArchive, "tray4", "jpg")

    def trayConfig(self):
        """
        function that configures previously set up tray buttons with images
        :return: None
        """
        self.tray1.config(image=self.tray_one_image.image)
        self.tray2.config(image=self.tray_two_image.image)
        self.tray3.config(image=self.tray_three_image.image)
        self.tray4.config(image=self.tray_four_image.image)

    def CALIBRATE(self):
        """
        function that sends commands via serial to the Arduino to
        start or stop the table motor for adjument based on boolean rotate variable.
        Event trigger based on user/Adjust Table button
        :return: None
        """
        if self.rotating == 0:
            time.sleep(.5)
            self.sender.sendInfo('rotate\n') # sends serial command to Arduino to start rotation
            self.rotating = 1 # sets boolean variable to true
        else:
            time.sleep(.5)
            self.sender.sendInfo('x\n') # sends random event serial command to Arduino to stop rotation
            self.rotating = 0 # sets boolean variable to false

    def RELOADALL(self):
        """
        function that allows user to reset all of the tray button pictures with current pictures
        upon event from user/reload button
        :return: None
        """
        self.startUp()
        self.open = 0 # reset open variable to false
        self.AllImageUpdater() #call to tray image update function
        self.trayConfig()# call to tray button configure function

    def OPENCLOSE(self):
        """
        :return: None
        function that sends commands via serial to the Arduino to
        open or close door based on boolean open. Triggered based on event from user/door button
        """
        if self.open == 0: # if door closed
            time.sleep(.5)
            self.sender.sendInfo('open\n') # open command string sent over serial to Arduino
            self.open = 1 # boolean open variable set to true
        else:
            time.sleep(.5) # if door open
            self.sender.sendInfo('close\n') # close command string sent over serial to Arduino
            self.open = 0 # boolean close variable set to false

    def TURNR(self):
        """
        function send a command string over serial to Arduino to turn
        table right one tray. Triggered by event from user/Turn R button
        :return: None
        """
        time.sleep(.5)
        self.sender.sendInfo("turnR\n") # command string sent over serial to Ardunio

    def TURNL(self):
        """
        function send a command string over serial to Arduino to turn
        table left one tray. Triggered by event from user/Turn L button
        :return: None
        """
        time.sleep(.5)
        self.sender.sendInfo("turnL\n") # command string sent over serial to Ardunio

    def startUp(self):
        """
        fucntion that loads loads each tray with a new image.
        :return: None
        """
        trayList = [] # create a list for tray strings
        for i in range(4): # for loop to populate list with 4 tray strings
            trayList.append("tray"+str(i+1))
        time.sleep(2)
        self.sender.sendInfo("open\n") # command sent to Arduino over serial to open door
        time.sleep(2)

        for i in range(4): # loop through each tray to take a picture
            self.ledNumber.updateLED(i+1) # updating the SSDisplay number for user
            time.sleep(2)
            self.cam.captureImage(location=self.imageArchive, name=trayList[i], type=".jpg") # capture/store image with type and name
            time.sleep(.5)
            if i != 3: # skip last turn on 4th tray
                self.sender.sendInfo("turnL\n") # command sent to Arduino over serial to turn table one tray to left

        self.ledNumber.updateLED(1) # reset SSDisplay to 1st tray
        self.sender.sendInfo("close\n") # command sent to Arduino over serial to close door
        time.sleep(2)

        for i in range(3): # return the tray to the first tray
            self.sender.sendInfo("turnR\n") # command sent to Arduino over serial to turn table one tray to right
            time.sleep(1)
        self.open = 0 # gaurentee boolean door variable is false

    def buttonPress1(self):
        """
        function that upon user/first tray 1 event, turns table to tray and opens door.
        waits for user to take item out of tray or insert item
        :return: None
        """
        self.ledNumber.updateLED(1) # updates SSdipslay for user
        self.sender.sendInfo("openwait\n") # command sent to Arduino over serial to open the door and wait for detection or timeout
        #print("Tray1 Selected")
        command = self.reciever(self.sender.serial) # call to master serial buffer to wait for and recieve command from Arduino
        #print(command)

        if command == '1': # if detection
            time.sleep(1)
            self.cam.captureImage(location=self.imageArchive, name="tray1", type=".jpg") # capture new picture
            time.sleep(.5)
            self.tray_one_image.updateImage() # update tray image with new image
            self.tray1.config(image=self.tray_one_image.image) # configure tray button with new image
        self.sender.sendInfo("close\n") # command sent to Arduino over serial to close door
        self.open = 0 # gaurentee boolean door variable is false

    def buttonPress2(self):
        """
        function that upon user/first tray 2 event, turns table to tray and opens door.
        waits for user to take item out of tray or insert item
        :return: None
        """
        self.ledNumber.updateLED(2) # updates SSdipslay for user
        self.sender.sendInfo("turnL\n")
        time.sleep(2)
        print("Tray2 Selected")
        self.sender.sendInfo("openwait\n") # command sent to Arduino over serial to open the door and wait for detection or timeout
        command = self.reciever(self.sender.serial)  # call to master serial buffer to wait for and recieve command from Arduino
        #print(command)

        if True or (command == '1' or command == "0"): # if detection
            time.sleep(1)
            self.cam.captureImage(location=self.imageArchive, name="tray2", type=".jpg") # capture new picture
            time.sleep(.5)
            self.tray_two_image.updateImage() # update tray image with new image
            self.tray2.config(image=self.tray_two_image.image)  # configure tray button with new image
        self.sender.sendInfo("close\n")  # command sent to Arduino over serial to close door
        time.sleep(2)
        self.sender.sendInfo("turnR\n")
        self.open = 0 # gaurentee boolean door variable is false

    def buttonPress3(self):
        """
        function that upon user/first tray 3 event, turns table to tray and opens door.
        waits for user to take item out of tray or insert item
        :return: None
        """
        self.ledNumber.updateLED(3) # updates SSdipslay for user
        for i in range(2):
            self.sender.sendInfo("turnL\n")
            time.sleep(1.5)
        print("Tray3 Selected")
        self.sender.sendInfo("openwait\n") # command sent to Arduino over serial to open the door and wait for detection or timeout
        command = self.reciever(self.sender.serial)  # call to master serial buffer to wait for and recieve command from Arduino
        #print(command)

        if True or (command == '1' or command == '0'): # if detection
            time.sleep(1)
            self.cam.captureImage(location=self.imageArchive, name="tray3", type=".jpg") # capture new picture
            time.sleep(.5)
            self.tray_three_image.updateImage() # update tray image with new image
            self.tray3.config(image=self.tray_three_image.image)  # configure tray button with new image
        self.sender.sendInfo("close\n")  # command sent to Arduino over serial to close door
        time.sleep(2)

        for i in range(2):
            self.sender.sendInfo("turnR\n")
            time.sleep(1.5)
        self.open = 0 # gaurentee boolean door variable is false

    def buttonPress4(self):
        """
        function that upon user/first tray 4 event, turns table to tray and opens door.
        waits for user to take item out of tray or insert item
        :return: None
        """
        self.ledNumber.updateLED(4) # updates SSdipslay for user
        self.sender.sendInfo("turnR\n")
        time.sleep(2)
        print("Tray4 Selected")
        self.sender.sendInfo("openwait\n") # command sent to Arduino over serial to open the door and wait for detection or timeout
        command = self.reciever(self.sender.serial)  # call to master serial buffer to wait for and recieve command from Arduino
        #print(command)

        if True or (command == '0' or command == '0'): # if detection
            time.sleep(2)
            self.cam.captureImage(location=self.imageArchive, name="tray4", type=".jpg") # capture new picture
            time.sleep(.5)
            self.tray_four_image.updateImage() # update tray image with new image
            self.tray4.config(image=self.tray_four_image.image)  # configure tray button with new image
        self.sender.sendInfo("close\n")  # command sent to Arduino over serial to close door
        time.sleep(2)
        self.sender.sendInfo("turnL\n")
        self.open = 0 # gaurentee boolean door variable is false

    def reciever(self, port):
        """
        function that listens to the serial for bytes of information from the Arduino,
        then converts the information upon detection of new line character to string.
        :param port: Arduino serial port for buffer listener
        :return: string command from Arduino via serial
        """
        while True:
            info = port.readline().decode('utf-8') # read buffer until bytes are detected, then convert
                                                    #those bytes to a string utf-8 format until new line char detected
            if info: # there is a string
                #print("<<<<"+info+">>>>")
                return info

class quitButton:
    """
    Quit Button object, Terminates program upon even from user/Exit Program button
    """
    def __init__(self, master):
        self.quitButton = Button(master, text=" "*7+"Exit Program"+" "*7,
                                 bg=BB_COLOR, fg='black', font=QUIT_FONT, command=quit)
        self.quitButton.pack(padx=5, side='right', expand=1)

def main():
    """
        main program function
        :return: None
    """
    window = Tk() # Tk Object intialization of main app frame
    w, h = window.winfo_screenwidth(), window.winfo_screenheight() # get info on monitor display width and height
    window.overrideredirect(1) # get rid top system window bar with minimize, maximize, and x button
    window.geometry("%dx%d+0+0" % (w,h)) # set man window frame to info of width and height previously gathered
    #window.title("Closet v.1") #set system window bar title
    app = Closet(master=window, start=False) #initialize and create app/program object frame
    window.mainloop() # run program main loop

main() #start program call

#END CODE
