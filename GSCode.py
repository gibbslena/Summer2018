from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties
from tkinter import *
###MAKE SURE THE BACKGROUND UNDER PREFERENCES IS SET TO TKinter!!! Then you must restart spyder.###
###The interactive graphics will not work if this is not done.###


#This creates a popup window that presents the rock faces within the foulder which you can select one to view
def raise_above_all(master):
    master.attributes('-topmost', True)
master = Tk()
raise_above_all(master)
master.winfo_toplevel().title('CRB Goniometer Spectra') #Laeling the popup window

#Instructions to the user
Label(master, text="Please select the rock face you wish to view from the \nlist below. Then select ''Show Spectra'' at the bottom of the screen. \nTo quit the program, click on the exit button at the top of this box.").grid(row=1,column=1)

options = Listbox(selectmode='SINGLE', exportselection=False)#This extracts all of the file names within the foulder.
for file in os.listdir('//volumes/ricedata/Lena/CRB_Goniometer_Spectra/GS/Spectra'): #//volumes/ricedata/Lena/CRB_Goniometer_Spectra/Individual_Rocks
    if not file.startswith('.'):#This cleans up what files are shown
        options.insert(END, file.strip('.txt'))#This removes the .txt from being shown to clean up what is seen, so that just a rock face is presented.
options.grid(row=2, column=1) #This is the location on the popup window where the list is shown

#This creates the frame in which the scrollbar is going to be placed
frame = Frame(master)
frame.grid(row=2, column=2, sticky='NS')

#This creates the scrollbar and places it in the frame
scrollbar = Scrollbar(frame, orient="vertical")
scrollbar.pack(side="right", fill="y")

#This syncs the scrollbar and the mouse so that you can scroll with either and they both track
options.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=options.yview)

#This creates the show spectra button that starts the function to plot the spectra of the selected rock face.
plot_button = Button(text = 'Show Spectra', command = lambda: display(options.get(ACTIVE)))
plot_button.grid(row=3,column=1)


#Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)

#Function to create spectra of selected rock face
def display(file):
    #Replace this with the path to your file
    filename='//volumes/ricedata/Lena/CRB_Goniometer_Spectra/GS/Spectra/'+file+'.txt'
    #Load your data into this program
    #filename is the name of your file, which you defined above
    #skip_header tells the program how many rows to skip at the start of your file (i.e. column headers)
    #dtype tells your program what kind of data you are looking at. If it is all numbers, use float
    #If your data is not all numbers, use None. You'll have to do more processing before you plot though.
    #delimiter tells the program how to separate different values. I am using tab-separated values which means I use \t. If you are using comma-separated values use ',' as your delimiter. If you are using data separated by newline characters, use '\n'.    
    
    data = np.genfromtxt(filename, skip_header=1, dtype=float,delimiter='\t')
    
    #data starts out as a list where every row is a pair of (wavelength, reflectance). I want 2 lists, one of all of my wavelengths, which will go on the x axis, the other of my reflectance values, which will go on the y-axis.
    data=zip(*data)
    
    nm=[]
    reflectance=[]
    for i, d in enumerate(data):
        if i==0: nm=d #the first column in my .tsv (now first row) was wavelength in nm
        else:
            d=np.array(d)
            #d2=d/np.max(d)
            reflectance.append(d) #the second columnn in my .tsv (now 2nd row) was reflectance
            #reflectance[1].append(d2)
    
    labels=['i=50 e=40 g=10','i=50 e=20 g=30','i=50 e=0 g=50','i=50 e=-20 g=70','i=50 e=-40 g=90'] #i= e= and g=
    offset=[0,.02,.03,.04,.02]
    #Colors=[(.38,.55,.33),(.65,.38,.09),(.11,.48,.54),'r','g']
    Thickness=[1,1,1,1,1]  
        
    #make a plot
    fig = plt.figure(figsize=(20,10))
    #figs.append(plt.figure(figsize=(20,10)))
    
    ax=fig.add_axes((0.1,0.2,0.8,0.7))
    
    #plot your data
    for j, spectrum in enumerate(reflectance):
        if labels[j] in ['i=50 e=40 g=10','i=50 e=20 g=30','i=50 e=0 g=50','i=50 e=-20 g=70','i=50 e=-40 g=90']:
            #ax.plot(nm, spectrum, label=labels[j], color=Colors[j],linewidth=Thickness[j])
            ax.plot(nm, spectrum + offset[j], label=labels[j],linewidth=Thickness[j])
    
        ax.legend()
        
        #Decide how big you want your tick markers to be
    ax.tick_params(labelsize=14)
        #ax.set_yticklabels([])
    ax.grid()
    
    #Decide on a title and font size for that title
    ax.set_title(file, size=24)
    
    #Decide on x-axis label and size
    ax.set_xlabel('Wavelength (nm)', size=20)
    
    #Setting the y axis for the first plot
    ax.set_ylabel("Reflectance",size=20)
    
    #Show your plot
    plt.show()
    
    def raise_above_all(master):
        master.attributes('-topmost', 1)
    master = Tk()
    raise_above_all(master)
    master.winfo_toplevel().title('Instructions') #Labeling the popup window

    #Instructions to the user
    Label(master, text="Please, click on an x value to normalize data. \nOr enter a value for x to which you would like to normalize. \nIn the space below.").grid(row=1,column=1)
    #e1 = Entry(master)
    #e1.grid(row=2, column=1)
    #Button(master, text='Normalize', command=master.quit).grid(row=3,column=1)
    
    #mainloop( )
    #norm=e1.get()
    #print(norm)
    
    x = plt.ginput(1)  #or norm ####THIS DOESNT WORK YET!!!!
    
    #NEW NORMALIZED FIGURE
    
    data = np.genfromtxt(filename, skip_header=1, dtype=float,delimiter='\t')
    
    #data starts out as a list where every row is a pair of (wavelength, reflectance). I want 2 lists, one of all of my wavelengths, which will go on the x axis, the other of my reflectance values, which will go on the y-axis.
    data=zip(*data)
    
    x_point = int(round(x[0][0])) #Rounding x to the nearest whole number
    y_point = x[0][1]
    
    nm=[]
    reflectance=[]
    for i, d in enumerate(data):
        if i==0: nm=np.array(d).astype(int) #the first column in my .tsv (now first row) was wavelength in nm
        else:
            d=np.array(d)
            index = np.where(nm == x_point)
            y = d[index]
            d = d * 1 / y
            reflectance.append(d) #the second columnn in my .tsv (now 2nd row) was reflectance
    
    labels=['i=50 e=40 g=10','i=50 e=20 g=30','i=50 e=0 g=50','i=50 e=-20 g=70','i=50 e=-40 g=90'] #i= e= and g=
    #Colors=[(.38,.55,.33),(.65,.38,.09),(.11,.48,.54),'r','g']
    Thickness=[1,1,1,1,1]      
   
    #make a plot
    fig2 = plt.figure(figsize=(20,10))
    #figs.append(plt.figure(figsize=(20,10)))
    
    ax=fig2.add_axes((0.1,0.2,0.8,0.7))
    
    #plot your data
    for j, spectrum in enumerate(reflectance):
        if labels[j] in ['i=50 e=40 g=10','i=50 e=20 g=30','i=50 e=0 g=50','i=50 e=-20 g=70','i=50 e=-40 g=90']:
            #ax.plot(nm, spectrum, label=labels[j], color=Colors[j],linewidth=Thickness[j])
            ax.plot(nm, spectrum, label=labels[j],linewidth=Thickness[j])
    
        ax.legend()
        
        #Decide how big you want your tick markers to be
    ax.tick_params(labelsize=14)
        #ax.set_yticklabels([])
    ax.grid()
    
    #Decide on a title and font size for that title
    ax.set_title(file, size=24)
    
    #Decide on x-axis label and size
    ax.set_xlabel('Wavelength (nm)', size=20)
    #Labeling yaxis
    ax.set_ylabel("Normalized Reflectance",size=20)
    
    plt.text(200,-.05, r"$\bf{Figure:}$" + 'Spectra were taken from '+file+'. Plot 1 is absolute reflectance, Plot 2 \nis the reflectance that has been normalized to 1.0 at '+str(x_point)+' nm.',fontsize = 20)
    #plt.text(200,-.1, r"$\bf{Figure:}$" + 'Spectra were taken from '+file+' with three different orientations of incidence and emission \nangles as indicated by their color and the legend. Each spectra was taken from the exact same location with a white \nreference to periodically callobrate the spectrum was taken using spectralon. Plot 1 is absolute reflectance, Plot 2 \nis the reflectance that has been normalized to 1.0 at '+str(x_point)+' nm.',fontsize = 20) 
    
    #Set range of your plot (will do this automatically, but not always how you'd like).
    #plt.ylim([0,1])
    
    #Show your plot
# =============================================================================
#      
#     def raise_above_all(master):
#         master.attributes('-topmost', 1)
#     master = Tk()
#     raise_above_all(master)
#     master.winfo_toplevel().title('Instructions') #Labeling the popup window
# 
#     #Instructions to the user
#     Label(master, text="Please select points A,B and C, between which you would like to determine slope.").grid(row=1,column=1)
#     
#     
#     #This is great! But... I want this to show up as a button as an option for someone to click on if they would like to determine slope. And for them to choose to do this before or after normalizing
#     xy1= plt.ginput(1)   
#     x1_point = int(round(xy1[0][0])) 
#     y1_point = xy1[0][1]
#     xy2=plt.ginput(1)
#     x2_point = int(round(xy2[0][0]))
#     y2_point = xy2[0][1]
#     xy3=plt.ginput(1)
#     x3_point = int(round(xy3[0][0]))
#     y3_point = xy3[0][1]
#     print (x1_point)
#     print ("{:.2e}".format(y1_point))
#     print (x2_point)
#     print ("{:.2e}".format(y2_point))
#     print (x3_point)
#     print ("{:.2e}".format(y3_point))
#     slope1=(y2_point - y1_point)/(x2_point - x1_point)
#     print ("The slope from point A to B is, "+"{:.2e}".format(slope1)+".")
#     slope2=(y3_point - y2_point)/(x3_point - x2_point)
#     print ("The slope from point B to C is, "+"{:.2e}".format(slope2)+".")
# =============================================================================

mainloop( )