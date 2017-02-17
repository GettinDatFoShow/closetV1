#START CODE
#Author Robert Morris

__author__ = 'Robert Morris'
import serial
from PIL import Image, ImageTk
import time
import RPi.GPIO as gpio
import picamera
gpio.setwarnings(False)
gpio.cleanup()
gpio.setmode(gpio.BCM)

class InfoSender:
    """
    creates master/slave serial communication object
    :param: connection: slave device location on serial
    :param: baud: default baud rate for communication with Arduino (Arduino must be same baud)
    """
    def __init__(self, connection, baud):
        self.connection = connection # updates com serial variable with location of slave device
        self.baud = baud # updates default baud rate for serial byte transfer variable
        self.serial = serial.Serial(self.connection, self.baud) # call to python serial module to create serial object

    def sendInfo(self, info):
        """
        function to allow the conversion and sending of information (string commands) in a python 3
        formate over the serial connection to the Arduino.
        :param: info: string
        :return: None
        """
        self.serial.write(bytes(info, 'utf-8')) # converts string to bytes in utf-8 format and sends over serial

class TrayImage():
    """
    Tray Image Object, creates a stores an Image for tkinter buffer
    """
    def __init__(self, location, name, imageType):
        self.location = location # image location variable
        self.imageType = "." + imageType # image time variable
        self.name = name # image name variable
        self.image = self.getImage(self.location, self.name, self.imageType) # call to function to update object with first image

    def getImage(self, location, name, imageType):
        """
        function to get or update an image from a file location
        :return: tkinter image
        """
        imageSize = 570, 500 # image size bounds
        location = location + name + imageType # full image file name+pathway
        load = Image.open(location) # read image into buffer
        load.thumbnail(imageSize, Image.ANTIALIAS) # create tumbnail image for tkinter processing
        image = ImageTk.PhotoImage(load) # create tkinter usable photo from thumbnail
        return image  # return tkinter image

    def updateImage(self):
        """
        funtion to mutate current object image with new image.
        :reference: self.getImage()
        :return: None
        """
        self.image = self.getImage(self.location, self.name, self.imageType)

class LEDCounter:
    """
    Seven Segment LED Dispaly Object
    """
    def __init__(self, num):

        top, ltop, rtop, mid, lbot, rbot, bot, single,= 21, 20, 16, 12, 6, 13, 26, 19 # gpio pin numbers
        self.pinList = [top, ltop, rtop, mid, lbot, rbot, bot, single] #gpio pin list
        self.setUpPins() # call to gpio pin setup function
        self.one = [rtop, rbot] # pin list for LEDs that form the visual number 1
        self.two = [top, rtop, mid, lbot, bot] # pin list for LEDs that form the visual number 2
        self.three = [top, rtop, mid, rbot, bot] # pin list for LEDs that form the visual number 3
        self.four = [ltop, rtop, mid, rbot] # pin list for LEDs that form the visual number 4
        self.single = single # single dot on bottom of display (UNUSED)
        self.current = self.updateLED(num) # call to display update function with integer param to update

    def updateLED(self, num):
        """
        function that updates the LED display to the number provided
        :param: integer
        :return: None
        """
        self.displayOff() # call to function turn off any currently display number

        if num == 1:
            self.oneOn() # call to fucntion for Display of number 1

        elif num == 2:
            self.twoOn() # call to fucntion for Display of number 2

        elif num == 3:
            self.threeOn() # call to fucntion for Display of number 3

        elif num == 4:
            self.fourOn() # call to fucntion for Display of number

        else:
            self.singleOn() # call to fucntion for Display of single bottom led dot (if shown means error)

    def setUpPins(self):
        """
        function to setup up gpio led pins as output channels
        :return: None
        """
        for i in self.pinList:
            gpio.setup(i, gpio.OUT) # setup each pin in list to output pin

    def displayOff(self):
        """
        function that gaurentees LED display is off
        :return: None
        """
        self.oneOff() # call to fucntion for one off
        self.twoOff() # call to fucntion for two off
        self.threeOff()# call to fucntion for three off
        self.fourOff() # call to fucntion for four off
        self.singleOff() # call to fucntion for single dot led off

    def oneOn(self):
        """
        function that turns on display LEDs in shape 1
        :return: None
        """
        for i in self.one:
            gpio.output(i, True)

    def twoOn(self):
        """
        function that turns on display LEDs in shape 2
        :return: None
        """
        for i in self.two:
            gpio.output(i, True)

    def threeOn(self):
        """
        function that turns on display LEDs in shape 3
        :return: None
        """
        for i in self.three:
            gpio.output(i, True)

    def fourOn(self):
        """
        function that turns on display LEDs in shape 4
        :return: None
        """
        for i in self.four:
            gpio.output(i, True)

    def oneOff(self):
        """
        function that turns OFF display LEDs
        :return: None
        """
        for i in self.one:
            gpio.output(i, False)

    def twoOff(self):
        """
        function that turns OFF display LEDs
        :return: None
        """
        for i in self.two:
            gpio.output(i, False)

    def threeOff(self):
        """
        function that turns OFF display LEDs
        :return: None
        """
        for i in self.three:
            gpio.output(i, False)

    def fourOff(self):
        """
        function that turns OFF display LEDs
        :return: None
        """
        for i in self.four:
            gpio.output(i, False)

    def singleOn(self):
        """
        function that turns ON display LED for bottom dot
        :return: None
        """
        gpio.output(self.single, True)

    def singleOff(self):
        """
        function that turns OFF display LED
        :return: None
        """
        gpio.output(self.single, False)

class TrayCam:
    """
        System camera class
    """
    def __init__(self):
        self.cam = picamera.PiCamera() # initializes a Raspberry Pi camera from the Pi camera module
        camL1, camL2 = 2, 3 # set up pin numbers for camera led lights for camera flash
        self.camList = [camL1, camL2] # led list
        self.setUpPins() # Call to gpio setup function

    def captureImage(self, location, name, type):
        """
        fucntion that captures and stores and image using the camera and the led flash
        :param location: the directory in which to store the images
        :param name: what to name to label the image file
        :param type: the image file time (i.e. .jpeg)
        :return: None
        """
        self.camLightOn() #turn flash on
        time.sleep(.25)
        self.cam.capture(location+name+type) # call to camera image capture function
        time.sleep(.25)
        self.camLightOff() # flash off

    def setUpPins(self):
        """
        function that sets up the led pins for use as flash
        :return: None
        """
        for i in self.camList:
            gpio.setup(i, gpio.OUT) # sets the led pin to output

    def camLightOn(self):
        """
        function that turns the LED lights to on.
        :return: None
        """
        for i in self.camList:
            gpio.output(i, True) # sets the LED pin output to HIGH

    def camLightOff(self):
        """
        function that turns the LED lights to off.
        :return: None
        """
        for i in self.camList:
            gpio.output(i, False) # sets the LED pin output to LOW

#END CODE
