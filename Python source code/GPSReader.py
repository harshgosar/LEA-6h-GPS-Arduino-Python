#########################################################################################################
#Author:          Harsh Gosar (harshgosar0@gmail.com)                                                   #
#Description:     To Read response from Arduino Serial port and display latitude and longitude on screen#
#Original Date:   12-MAY-2018                                                                           #
#Version:         1.0                                                                                   #
#########################################################################################################

import tkinter as tk
import tkinter.scrolledtext as tkscrolledtext
from tkinter import *
from tkinter import filedialog
import SerialPortHelperClass
import _thread

########### globals variable declaration #############################
serialPort = SerialPortHelperClass.SerialPort()

windowRoot = tk.Tk()  # create a Tk window
windowRoot.title("Arduino-Python GPS Reader - v1.0")
#######################################################################

########### set up the window size and position #######################
screen_width        =   windowRoot.winfo_screenwidth()
screen_height       =   windowRoot.winfo_screenheight()
window_width        =   screen_width / 2
window_height       =   screen_width / 3
window_position_x   =   screen_width / 2    -   window_width / 2
window_position_y   =   screen_height / 2   -   window_height / 2
windowRoot.geometry('%dx%d+%d+%d' % (window_width, window_height, window_position_x, window_position_y))
#######################################################################

########### scrolled text box used to display the serial data #########
frame       =   tk.Frame(windowRoot, bg='black')
frame.pack(side="bottom", fill='both', expand='no')

text_area   =   tkscrolledtext.ScrolledText(master=frame, wrap='word', width=180, height=10) #width=characters, height=lines
text_area.pack(side='bottom', fill='y', expand=True, padx=1, pady=1)
text_area.config(font="bold")

textbox     =   Entry(windowRoot, width=50)
textbox.place(x=100, y=128)
textbox.config(font="bold")

textbox2    =   Entry(windowRoot, width=50)
textbox2.place(x=100, y=168)
textbox2.config(font="bold")
#######################################################################

########### Latitude label ############################################
label_Latitude = Label(windowRoot, width=10, height=2, text="Latitude:")
label_Latitude.place(x=1, y=118)
label_Latitude.config(font="bold")
#######################################################################

########### Longitude label ###########################################
label_Longitude = Label(windowRoot, width=10, height=2, text="Longitude:")
label_Longitude.place(x=1, y=158)
label_Longitude.config(font="bold")
#######################################################################

########### COM Port label ############################################
label_comport = Label(windowRoot, width=10, height=2, text="COM Port:")
label_comport.place(x=10, y=26)
label_comport.config(font="bold")
#######################################################################

########### COM Port entry box ########################################
comport_edit = Entry(windowRoot, width=10)
comport_edit.place(x=100, y=36)
comport_edit.config(font="bold")
comport_edit.insert(END, "COM7")
#######################################################################

########### commands associated with button presses ###################
def OpenCommand():
    if button_openclose.cget("text") == 'Open COM port':
        comport = comport_edit.get()
        baudrate = baudrate_edit.get()
        text_area.insert(END, "Open")
        serialPort.Open(comport, baudrate)
        button_openclose.config(text='Close COM port')
        text_area.insert(END, "COM Port Opened\r\n")
    elif button_openclose.cget("text") == 'Close COM port':
        serialPort.Close()
        button_openclose.config(text='Open COM Port')
        text_area.insert(END, "COM Port Closed\r\n")
    else:
        text_area.insert(END, "An error occurred\r\n")
#######################################################################

########### COM Port open/close button ################################
button_openclose = Button(windowRoot, text="Open COM port", width=20, command=OpenCommand)
button_openclose.config(font="bold")
button_openclose.place(x=210, y=30)
#######################################################################

########### Clear text box data #######################################
def ClearDataCommand():
    textbox.delete(0, END)
    text_area.delete('1.0', END)
#######################################################################

########### Clear Rx Data button ######################################
button_cleardata = Button(windowRoot, text="Clear COM port data", width=20, command=ClearDataCommand)
button_cleardata.config(font="bold")
button_cleardata.place(x=210, y=72)
#######################################################################

########### Baud Rate label ###########################################
baudrate_label = Label(windowRoot, width=10, height=2, text="Baud Rate:")
baudrate_label.place(x=10, y=70)
baudrate_label.config(font="bold")
#######################################################################

########### Baud Rate entry box #######################################
baudrate_edit = Entry(windowRoot, width=10)
baudrate_edit.place(x=100, y=80)
baudrate_edit.config(font="bold")
baudrate_edit.insert(END, "9600")
#######################################################################

########### serial data callback function to read GPS data and calculate lat and long
def OnReceiveSerialData(message):
    str_message = message
    response = str_message.split(',')
    if len(response) > 4 and str_message.find("$GPRMC") == 0:
        textbox.delete(0, END)
        textbox2.delete(0, END)
        latdegreeConversion = ((float(response[3]) / 100.00) - (int(float(response[3]) / 100.00))) / 0.6 + int(
            float(response[3]) / 100.00)
        londegreeConversion = ((float(response[5]) / 100.00) - (int(float(response[5]) / 100.00))) / 0.6 + int(
            float(response[5]) / 100.00)
        textbox.insert(END, str(latdegreeConversion) + ' ' + response[4])
        textbox2.insert(END, str(londegreeConversion) + ' ' + response[6])
#######################################################################

########### Register the callback above with the serial port object ###
serialPort.RegisterReceiveCallback(OnReceiveSerialData)
#######################################################################

########### loop a loop function ######################################
def sdterm_main():
    windowRoot.after(200, sdterm_main)# run the main loop once each 200 ms
#######################################################################

########### The main loop #############################################
windowRoot.after(200, sdterm_main)
windowRoot.mainloop()
#######################################################################
