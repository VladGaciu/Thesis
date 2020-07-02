import pandas as pd
import numpy as np
from numpy.linalg import inv
from scipy import stats

from tkinter import Frame, BOTTOM, LEFT, RIGHT, Label, Entry
from tkinter import *

class GUI:
    def __init__(self, master):
        self.master = master
        master.title("Laser Calibration")

        self.widthFrame = Frame(master)
        self.widthFrame.pack(side = TOP)
        
        self.wavelengthWidthFrame = Frame(master)
        self.wavelengthWidthFrame.pack(side = TOP)
        
        self.widthSpecWidthFrame = Frame(master)
        self.widthSpecWidthFrame.pack(side = TOP)
        
        self.positionFrame = Frame(master)
        self.positionFrame.pack(side = TOP)
        
        self.wavelengthPositionFrame = Frame(master)
        self.wavelengthPositionFrame.pack(side = TOP)
        
        self.positionSpecWidthFrame = Frame(master)
        self.positionSpecWidthFrame.pack(side = TOP)
        
        self.desiredWavelengthFrame = Frame(master)
        self.desiredWavelengthFrame.pack(side = TOP)
        
        self.desiredSpecWidthFrame = Frame(master)
        self.desiredSpecWidthFrame.pack(side = TOP)
        
        self.label = Label(self.widthFrame, text="Width entries")
        self.label.pack(side = LEFT)
        
        self.label = Label(self.wavelengthWidthFrame, text="Wavelength entries for width")
        self.label.pack(side=LEFT)
        
        self.label = Label(self.positionFrame, text="Position entries")
        self.label.pack(side = LEFT)
        
        self.label = Label(self.wavelengthPositionFrame, text="Wavelength entries for position")
        self.label.pack(side=LEFT)
        
        self.label = Label(self.widthSpecWidthFrame, text="Spectral width for width")
        self.label.pack(side=LEFT)
        
        self.label = Label(self.positionSpecWidthFrame, text="Spectral width for position")
        self.label.pack(side=LEFT)
        
        self.label = Label(self.desiredWavelengthFrame, text="Desired Wavelength")
        self.label.pack(side = LEFT)
        
        self.label = Label(self.desiredSpecWidthFrame, text="Desired Spectral Width")
        self.label.pack(side = LEFT)
        
        self.widthEntry = Entry(self.widthFrame)
        self.widthEntry.pack(side = LEFT)
        
        self.wavelengthWidthEntry = Entry(self.wavelengthWidthFrame)
        self.wavelengthWidthEntry.pack(side = LEFT)
        
        self.widthSpecWidthEntry = Entry(self.widthSpecWidthFrame)
        self.widthSpecWidthEntry.pack(side = LEFT)
        
        self.positionEntry = Entry(self.positionFrame)
        self.positionEntry.pack(side = LEFT)
        
        self.wavelengthPositionEntry = Entry(self.wavelengthPositionFrame)
        self.wavelengthPositionEntry.pack(side = LEFT)
        
        self.positionSpecWidthEntry = Entry(self.positionSpecWidthFrame)
        self.positionSpecWidthEntry.pack(side = LEFT)
        
        self.desiredWavelengthEntry = Entry(self.desiredWavelengthFrame)
        self.desiredWavelengthEntry.pack(side = RIGHT)
        
        self.desiredSpecWidthEntry = Entry(self.desiredSpecWidthFrame)
        self.desiredSpecWidthEntry.pack(side = RIGHT)
        
        self.submit_button = Button(master, text="Submit", command=self.submit)
        self.submit_button.pack(side = TOP)
        
        self.saveAndRecalibrate_button = Button(master, text="Save", command=self.save)
        self.saveAndRecalibrate_button.pack(side = TOP)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(side = TOP)
        
        self.width = []
        self.widthWavelength = []
        self.widthSpecWidth = []
        self.position = []
        self.positionWavelength = []
        self.positionSpecWidth = []
        

    def submit(self):
        #print(desiredSpecWidth)
        widthWavelengthRegression = linear_regression(self.width, self.widthWavelength)
        print(widthWavelengthRegression)
        positionWavelengthRegression = linear_regression(self.position, self.positionWavelength)
        print(positionWavelengthRegression)
        #Take the average of the intercepts
        intercept1 = float((widthWavelengthRegression[1]+positionWavelengthRegression[1])/2)
        #print(intercept1)
        widthSpecWidthRegression = linear_regression(self.width, self.widthSpecWidth)
        #print(widthSpecWidthRegression)
        positionSpecWidthRegression = linear_regression(self.position, self.positionSpecWidth)
        #print(positionSpecWidthRegression)
        #Take the average of the intercepts
        intercept2 = float((widthSpecWidthRegression[1]+positionSpecWidthRegression[1])/2)
        #print(intercept2)
        results = calibration(self.desiredWavelength, self.desiredSpecWidth, positionWavelengthRegression[0], widthWavelengthRegression[0], positionSpecWidthRegression[0], widthSpecWidthRegression[0], intercept1, intercept2)
        #print(desiredWavelength, desiredSpecWidth, positionWavelengthRegression[0], widthWavelengthRegression[0], positionSpecWidthRegression[0], widthSpecWidthRegression[0], intercept1, intercept2)
        #print(results)
            
    def save(self):
        self.width += [self.widthEntry.get()]
        print("Width:", self.width)
        self.widthWavelength += [self.wavelengthWidthEntry.get()]
        print("Width Wavelength:",self.widthWavelength)
        self.widthSpecWidth += [self.widthSpecWidthEntry.get()]
        print("Width SpecWidth:",self.widthSpecWidth)
        self.position += [self.positionEntry.get()]
        print("Position:", self.position)
        self.positionWavelength += [self.wavelengthPositionEntry.get()]
        print("Position Wavelength:", self.positionWavelength)
        self.positionSpecWidth += [self.positionSpecWidthEntry.get()]
        print("Position SpecWidth", self.positionSpecWidth)
        self.desiredWavelength = float(self.desiredWavelengthEntry.get())
        print("Desired Wavelength:", self.desiredWavelength)
        self.desiredSpecWidth = float(self.desiredSpecWidthEntry.get())
        print("Desired SpecWidth:", self.desiredSpecWidth)
        print("Save Complete")

def linear_regression(slitParameter, opticalParameter):
    #Determine slope and y-intercept for the position/wavelength data points
    #First, generate dictionary with user inputs from width and corresponding wavelength
    inputsDictionary = {'slitParameter': slitParameter, 'opticalParameter': opticalParameter}
    #Next, generate a dataframe with all data
    data = pd.DataFrame(inputsDictionary)
    #print(data)
    #Split up data into two arrays from each column of data
    slitParameterData = data["slitParameter"]
    opticalParameterData = data["opticalParameter"]
    #slice array into individual indices
    slitParameterArray = []
    length = len(slitParameter)
    i1 = 0
    while length > 0:
        slitParameterArray = np.insert(slitParameterArray,0,slitParameter[i1])
        i1 = i1 + 1
        length = length - 1
    #print(slitParameterArray)
    #splice array into individual indices
    opticalParameterArray = []
    length = len(opticalParameter)
    i2 = 0
    while length > 0:
        opticalParameterArray = np.insert(opticalParameterArray,0,opticalParameter[i2])
        i2 = i2 + 1
        length = length - 1
    #print(opticalParameterArray)
    #calculate slope and y-intercept using the scipy library function linregress
    slope, intercept, _, _, _ = stats.linregress(slitParameterArray,opticalParameterArray)
    

    return slope, intercept

def calibration(yPeak, ySpec, m1, m2, m3, m4, b1, b2):

    A_matrix = np.matrix([[m1, m2], [m3, m4]])
    #print(A_matrix)
    b_vector = np.matrix([[int(yPeak)-b1], [int(ySpec)-b2]])
    #print(b_vector)
    x_vector = inv(A_matrix.transpose()*A_matrix)*(A_matrix.transpose()*b_vector)
    print("Slit Width", x_vector[0])
    print("Slit Position", x_vector[1])
    
    return x_vector

def main():
    
    root = Tk()
    my_gui = GUI(root)
    root.mainloop()  
    root.destroy()
    
    print("Calibration complete")
    
if(__name__ == "__main__"):
    main()