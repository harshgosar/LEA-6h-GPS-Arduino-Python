#########################################################################################################
#Author:          Harsh Gosar (harshgosar0@gmail.com)                                                   #
#Description:     To Read response from Arduino Serial port and display latitude and longitude on screen#
#Original Date:   12-MAY-2018                                                                           #
#Version:         1.0                                                                                   #
#########################################################################################################

import serial
import sys
import _thread

class SerialPort:

    ## Constructor
    def __init__(self):
        self.comportName        =   ""
        self.baud               =   0
        self.timeout            =   None
        self.ReceiveCallback    =   None
        self.isopen             =   False
        self.receivedMessage    =   None
        self.serialport         =   serial.Serial()

    ## Destructor
    def __del__(self):
        try:
            if self.serialport.is_open():
                self.serialport.close()
        except:
            print("Destructor error closing COM port: ", sys.exc_info()[0] )

    ##  Callback function
    def RegisterReceiveCallback(self,aReceiveCallback):
        self.ReceiveCallback = aReceiveCallback
        try:
            _thread.start_new_thread(self.SerialReadlineThread, ())
        except:
            print("Error starting Read thread: ", sys.exc_info()[0])

    ## read serial port data and return to callback function
    def SerialReadlineThread(self):
        while True:
            try:
                if self.isopen:
                    self.receivedMessage = self.serialport.readline().decode("ascii", "ignore")
                    if self.receivedMessage != "":
                        self.ReceiveCallback(self.receivedMessage)
            except:
                print("Error reading COM port: ", sys.exc_info()[0])

    ## function to check if com port is open is not
    def IsOpen(self):
        return self.isopen

    ## function to Open com port
    def Open(self,portname,baudrate):
        if not self.isopen:
            # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N', stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = portname
            self.serialport.baudrate = baudrate
            try:
                self.serialport.open()
                self.isopen = True
            except:
                print("Error opening COM port: ", sys.exc_info()[0])

    ## function to close com port
    def Close(self):
        if self.isopen:
            try:
                self.serialport.close()
                self.isopen = False
            except:
                print("Close error closing COM port: ", sys.exc_info()[0])