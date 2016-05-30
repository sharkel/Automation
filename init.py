#!/usr/bin/python
#coding=utf-8
#-*- coding: utf-8 -*-

#TITLE  : 다다익선(多多益善)
#DATE   : 2016.02.26
#AUTHOR : KwangEun, An
#DESC   : Following by the MVC pattern, the CONTROLLER section code. Displays the actual status of current working and interact with the user.

#This program was developed under python3 program, 2.7 infact. The system has to be installed with 'python 2.7' not 'python 3.4'.
#And also requires the Python tkinter library to display a grapical user interface. If the program doesn't starts on linux type system, you need to install tkinter library(python-tk).

from Control import Screen
import Arduino
import Tkinter

def main():
    app = Screen(master=Tkinter.Tk())
    app.mainloop()

if __name__=="__main__":
    main()
