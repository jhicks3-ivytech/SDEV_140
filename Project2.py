'''In a Tkinter program, it's important to organize your code in a clear and logical manner. Here's a general structure you can follow:
Import Statements: At the very top, import all the necessary modules.
Global Declarations: Declare any global variables or constants that will be used throughout your program.
Function Definitions: Define all the functions that will be used in your program.
Class Definitions: If your program uses classes, define them after the functions.
Main Function: Define the main function that sets up the Tkinter application and starts the main loop.
Entry Point: Use the if __name__ == "__main__": construct to call the main function.'''
import tkinter as tk 
import random

#Global declarations
participants = []
pool = []
pickers = []
picked = []
pickedName = ""
#Function definitions
def endProgram():
    #Ends the program without saving
    root.destroy()

def addParticipant():
    #Adds name from the entry field into a global veriable and inserts it into
    #a listbox for display. 
    global participants
    person = entry.get()
    if person:
        participants.append(person)
        inputPoolBox.insert(tk.END, person)
        entry.delete(0, tk.END)
        print(participants)

def returnEntry(event):
    #uses the bound return key to add participants
    addParticipant()

def acceptList():
    #Finalizes the list, sends it to the root window, and destroys input window
    inputWindow.destroy()
    global participants
    for participant in participants:
        pickerList.insert(tk.END,participant)
        pool.append(participant)

def drawName():
    #Assigns drawer to a random name from the pool, appends two global lists for matching,
    #removes names from picker list and pool to prevent duplicates
    if pickerList.curselection():
        global pickers
        selecter = pickerList.get(pickerList.curselection())
       
        
        pickerList.delete(0,tk.END)
        pickers.append(selecter)
        if len(participants) == len(pickers):
            finishList()
        else:
            for participant in participants:
                if participant not in pickers:
                    pickerList.insert(tk.END,participant)
        reveal.configure(text=f"Thank you {selecter}, your pick has been drawn!")
        root.after(4000,hideText)
    else:
        reveal.configure(text="You must select your name.")
def showPick():
    #Displays the user's pick under the name selection box
    reveal.configure(text=f"You drew {pickedName}")
    root.after(4000,hidePick)

def hideText():
    #clears the text in the reveal label
    reveal.configure(text="")

def finishList():
    hat.destroy()
    pickerList.destroy()
    rootHeader.destroy()
    showButton = tk.Button(root, text="Show Matches",anchor="center",font=("calibri",18),fg="green",border=3)
    showButton.grid(row=0,column=0,sticky="nsew",padx=10,pady=5)
    showButton.columnconfigure(0,weight=1)
    saveButton = tk.Button(root, text="Save Matches to File",anchor="center",font=("calibri",18),fg="green",border=3)
    saveButton.grid(row=1,column=0,sticky="nsew",padx=10,pady=5)
    saveButton.columnconfigure(0,weight=1)
#Class definitions
#Creates an instance of the Tk class and makes root the main window
root = tk.Tk()
root.title("From a Hat")
root.minsize(400,200)
root.configure(bg="silver")
root.columnconfigure(0,weight=1)
quitButton2 = tk.Button(root,text="EXIT",anchor="center",font=("calibri",18),fg="red",border=3,command=endProgram)
quitButton2.grid(row=3,column=0)

# The header gives the user directions
rootHeader = tk.Label(root,text="Select your name from the list, then click the hat to draw a name."\
                        ,font=("calibri", 24, "bold"),anchor="center",bg="silver")
rootHeader.grid(row=0,column=0,sticky="ew",columnspan=2)

#This widget is where the user selects their own name
pickerList = tk.Listbox(root,font=("calibri",18),bg="#c0C0c0",justify="left")
pickerList.grid(row=1,column=0)

#Label to display the name of the person drawn
reveal = tk.Label(root,font=("calibri",18),bg="#c0C0c0")
reveal.grid(row=2,column=0,sticky="ew")

#Button widget to draw a name from a hat
HATIMAGE =tk.PhotoImage(file="santaHat.png")
hat = tk.Button(root,image=HATIMAGE,height=437,width=550,command=drawName)
hat.grid(row=1,column=1,sticky="nsew",columnspan=4)



# Creates a first window to take input for a participants list
inputWindow = tk.Toplevel(root,bg="silver")
inputWindow.title("Add Participants")
inputWindow.grid_columnconfigure(0,weight=1)
inputWindow.grid_columnconfigure(1,weight=1)
inputWindow.grab_set() #Prevents the user from using the main window
inputWindow.focus() #Puts this window in the foreground
inputWindow.transient(root) #Forces the user to interact with this window only
inputWindow.minsize(400,200)     

#Frame for header that spans the length of the window
headingFrame = tk.Frame(inputWindow)
headingFrame.grid(row=0,column=0,columnspan=2,sticky="ew",)
headingFrame.columnconfigure(0,weight=1)
inputHeading = tk.Label(headingFrame, text="This application will randomly match gift exchange participants."\
                        ,font=("calibri", 24, "bold"),anchor="center",bg="silver")
inputHeading.grid(row=0,column=0,sticky="ew")

#Frame where user will input participants names
entryFrame = tk.Frame(inputWindow,bg="silver")
entryFrame.grid(row=1,column=0,sticky="ew")
entryFrame.columnconfigure(0,weight=1)
directions = tk.Label(entryFrame,text="Enter the name of each person that will be participating in the gift exchange."\
                    ,wraplength=300,anchor="center",font=("calibri",18),bg="silver")
directions.grid(row=0,column=0,sticky="ew")
entry = tk.Entry(entryFrame,width=20,font=("calibri",18),border=3)
entry.grid(row=1,column=0,pady=3)
entry.bind("<Return>", returnEntry)
addButton = tk.Button(entryFrame,text="Add Participant",anchor="center",font=("calibri",18),fg="green",border=3,command=addParticipant)
addButton.grid(row=2,column=0)
quitButton = tk.Button(entryFrame,text="EXIT",anchor="center",font=("calibri",18),fg="red",border=3,command=endProgram)
quitButton.grid(row=3,column=0)

#Frame that gathers names in a pool
inputPool = tk.Frame(inputWindow,bg="silver")
inputPool.grid(row=1,column=1,sticky="ew")
inputPool.columnconfigure(0,weight=1)
inputPoolBox = tk.Listbox(inputPool,font=("calibri",18),bg="#c0C0c0",justify="center")
inputPoolBox.grid(row=0,column=0,sticky="ew")
acceptButton = tk.Button(inputPool,text="Accept List",anchor="center",font=("calibri",18),fg="green",border=3,command=acceptList)
acceptButton.grid(row=2,column=0)




#Main function
def main():
    root.mainloop()

#Entry point
if __name__=="__main__":
    main()