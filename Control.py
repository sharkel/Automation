#!/usr/bin/python
#coding=utf-8
#-*- coding: utf-8 -*-

#TITLE  : GUI controller using python3 tkinter module.
#DATE   : 2016.02.26
#AUTHOR : KwangEun, An
#DESC   : Following by the MVC pattern, the CONTROLLER section code. Displays the actual status of current working and interact with the user.

#This program was developed under python3 program, 2.7 infact. The system has to be installed with 'python 2.7' not 'python 3.4'.
#And also requires the Python tkinter library to display a grapical user interface. If the program doesn't starts on linux type system, you need to install tkinter library(python-tk).

#VER    : 0.0.2v
#AUTHOR : KwangEun An
import Tkinter
import os
#import pyaudio
#import wave
#import sys
#import cv2
#import PIL.Image
#import PIL.ImageTk

class Screen(Tkinter.Frame):
    
    #------Class Initilisation starts -----
    
    #Current Directory
    currentDirectory = os.path.dirname(os.path.realpath(__file__))+"/"
    
    #=======Edit here========
    
    #Audio/Alert file path
    #audioNumber = 1
    #audioFileDirectory = currentDirectory+"Audio/Alert_"
    
    #Image/opencv save location
    #imageFileDirectory = currentDirectory+"Image/Cam_"
    
    #Window/Window title
    windowTitle="다다익선(多多益善)"
    
    #Window/Monitor
    #Number of monitors
    numberOfMonitors = 6
    
    #Window/Monitor
    #Number of monitors in singleline
    monitorsInRow = 3
    
    #Window/Monitor font size
    fontSize = 24
    fontName = "couiser"
       
    #Window/Monitor size and color
    buttonSize = 2
    
    #Window/Monitor Colours
    #Colours are more expressible by using the HEX code. Check it out in here, http://cloford.com/resources/colours/500col.htm
    buttonBackgroundColour = "#cdc9c9"
    buttonBackgroundAlertColour = "#ff4500"
    buttonTextColour = "#000000"
    buttonTextAlertColour = "#ffffff"
    
    #=======Edit Stop========
    #DemoMode enabler
    demoMode = False
    
    #Audio/alert
    #audioFilePath = audioFileDirectory+str(audioNumber)+".wav"
    #audioClip = None
    #audioOn = 0
    #audioChunk = 1024
    
    #Window/Afterloop
    waitFor = 3000
    
    #Window/Button size and color
    buttonSizeWidth = buttonSize*4 #Horizontal paddings
    buttonSizeHeight = buttonSize*2 #Vertical paddings
    
    #Window/Screen maximumsizer
    masterHeight=int(buttonSizeWidth*60*3)
    masterWidth=int(buttonSizeWidth*120*3)
    
    #Window/Button Arrays
    Button=[0 for x in range(0, numberOfMonitors)]
    
    #Window/tkinter
    master = None
    #photo = None
    #------class Initilisation stops -----
    
    
    #Initilisation function of the Tkinter Module
    def __init__(self, master=None, demoMode=False):
        #create Window Structure
        self.master = master
        Tkinter.Frame.__init__(self, self.master)
        self.master.title(self.windowTitle)
        self.master.maxsize(self.masterWidth, self.masterHeight)
        self.pack()
        
        #creates monitors
        self.CreateMonitors(self.numberOfMonitors)
        self.Exit()
        
        #Demo / automatically disables the monitors which assume as controlers are not connected
        if(demoMode):
            self.demoMode=demoMode
            self.master.after(self.waitFor,self.Afterloop)
    
    #Runs any methos after the mainlooop starts
    def Afterloop(self):
        if(self.demoMode):
            for monitor in range(2,self.numberOfMonitors):
                self.ToogleMonitor(monitor) #Disable button
        self.master.update()
        
    #Disable or enables the monitor interaction
    def ToogleMonitor(self, monitorNumber, disable=1):
        if(disable):
            self.Button[monitorNumber].config(state="disabled")
        else:
            self.Button[monitorNumber].config(state="normal")
    
    #changes the colour of the button to alert   
    def AlertButton(self, monitorNumber, alert=1):
        monitorNumber = monitorNumber-1 #To use in nautral number
        
        if(alert):
            self.Button[monitorNumber].config(bg=self.buttonBackgroundAlertColour, fg=self.buttonTextAlertColour)
        else:
            self.Button[monitorNumber].config(bg=self.buttonBackgroundColour, fg=self.buttonTextColour)
            
    #creates the Monitors
    def CreateMonitors(self, numberOfMonitors):
        for monitor in range(0, self.numberOfMonitors):
            self.Button[monitor] = Tkinter.Button(self, command = lambda monitorId=monitor: self.SendMessage(monitorId))
            self.Button[monitor]["text"] = "모니터\n[%d]" % int(monitor+1)
            self.Button[monitor]["bg"] = self.buttonBackgroundColour
            self.Button[monitor]["fg"] = self.buttonTextColour
            self.Button[monitor]["width"] = self.buttonSizeWidth
            self.Button[monitor]["height"] = self.buttonSizeHeight
            self.Button[monitor]["font"] = "{"+str(self.fontName)+" "+str(self.fontSize)+" bold}"
            self.Button[monitor]["border"] = 5
            self.Button[monitor].grid(row=int(monitor/self.monitorsInRow), column=int(monitor%self.monitorsInRow))
     
    #Settings for image processings
    def PreInitialisation(self):
		
        
    #Checks connections from arduino
    def CheckConnection(self, monitorNumber):
        monitorNumber = int(monitorNumber-1) #To use in nautral number
        connection = True
        if (connection):
            return
        else:
            ToogleMonitor(monitorNumber)
     
    #Destory the current tkinter program
    def Exit(self):
        self.QUIT = Tkinter.Button(self, font="{"+str(self.fontName)+" "+str(self.fontSize)+" bold}", text="QUIT", fg="red", command=self.master.destroy, width=int(self.buttonSizeWidth*self.monitorsInRow), height=int(self.buttonSizeHeight/2))
        if(self.demoMode):
            self.Toogle = Tkinter.Button(self, font="{"+str(self.fontName)+" "+str(self.fontSize)+" bold}", text="Toogle", fg="Blue", command=lambda :self.Demo_ToogleSignal(), width=int(self.buttonSizeWidth), height=int(self.buttonSizeHeight/2))
            self.QUIT.grid(row=int(self.numberOfMonitors/self.monitorsInRow+1), column=1, columnspan=self.monitorsInRow)
            self.Toogle.grid(row=int(self.numberOfMonitors/self.monitorsInRow+1), column=0)
        else:
            self.QUIT.grid(row=int(self.numberOfMonitors/self.monitorsInRow+1), column=0, columnspan=self.monitorsInRow)
        
    #Callback Function
    def SendMessage(self, monitor,customResponse=None):
        if (monitor==999): #if the buttonId is '999', it means the button is not initialised well. 
            #Where errors to handle.
            print ("Errors in creating the Button, restart the hole program")
            return
            
        monitor = monitor+1 #To use in nautral number
        
        #Here you can replace to your custom function when it pressed.
        if(customResponse==None):
            print ("Monitor [%d] : Checked." % monitor) # In this example, you can see the changes on the terminal.
            self.DisplayImage(monitor)
            self.AlertButton(monitor,0)
        else:
            print ("Monitor [%d] : %s" % (monitor,customResponse)) # Otherwise, prints with custom Statements
    
    #Demonstration/Toogle Singal received
    def Demo_ToogleSignal(self):
        self.AlertButton(1)
        self.SendMessage(1, "System Halted")
        self.AlertButton(2)
        self.SendMessage(2, "System Halted")
    
    #displays the image
    def DisplayImage(self, monitorNumber, fileExtension=".gif"):
        #self.photo = ImageTk.PhotoImage(Image.open(imageFileDirectory+monitorNumber+".pgm"))
        self.photo = Tkinter.PhotoImage(file=self.imageFileDirectory+str(monitorNumber)+fileExtension)
        imagemul = 30
        self.imageScreen = Tkinter.Label(self,text="Screen", image=self.photo , width=int(self.buttonSizeWidth*self.monitorsInRow)*imagemul, height=self.buttonSizeHeight*self.monitorsInRow*2*imagemul)
        self.imageScreen.image = self.photo
        self.imageScreen.grid(row=int(self.numberOfMonitors/self.monitorsInRow+2), column=0, columnspan=self.monitorsInRow)
    
    #Audio/PyAudioplayer
    def AlertSound(self):
        wf = wave.open(self.audioFilePath, 'rb')

        p = pyaudio.PyAudio()

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback,
                        exception_on_underflow=True)

        stream.start_stream()

        #while stream.is_active():
            #time.sleep(0.1)

        stream.stop_stream()
        stream.close()
        wf.close()

        p.terminate()
