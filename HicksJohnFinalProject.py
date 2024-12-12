'''
Author: John Hicks
Date written: 12/1/2024
Assignment: Final Project

"From a Hat" is a fun way to match gift givers and receivers in a holiday gift exchange.
It allows an organizer to enter the names of the participants and throw the names into a hat.
Participants then select their own name from a list and click the hat to get a random
drawing of another participant. 

This script is a GUI that starts off with a name being inserted into an entry box. Pressing the 
enter key or clicking the Add Participant button adds the name to the participants list and 
appends it to a listbox. Once all names are entered and the Finalize List button is pressed.
The current window is destroyed, the names from participants list is appended to pickers list
that will represent the drawers, and the names are appended to a listbox. Each person will then
select their name from the listbox and click a hat image that represents a button. The button 
commands a function to randomly select a name from the participants list, append the drawer and 
drawn names as a pair to a list, and remove those names from participants and pickers to prevent
duplicates. Once the last name is drawn, the paired names are displayed in a list for all to see.

'''
import tkinter as tk 
import random

#Global declarations
participants = [] #Holds the names of everyone in the gift exchange
pickers = [] #Copy of participants that will be used for the user drawing the name
pairs = [] #List that holds the pairing of name drawers and gift recipients
pickedName = "" #needed to hold a temporary value and pass value to a label

#Function definitions:
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
    participants.sort()
    for participant in participants:
        pickerList.insert(tk.END,participant)
        pickers.append(participant)

def drawName():
    #Assigns drawer to a random name from the hat, fills a list of name name pairings,
    #removes names from picker list and hat to prevent duplicates
    if pickerList.curselection():
        global participants
        global pickedName
        global pairs
        global pickers
        random.shuffle(participants)   
        for participant in participants:
            selected = pickerList.get(pickerList.curselection())
            if participant != selected:
                if len(participants) == 1:
                    pickedName = participants[0]
                    pairs.append([selected, participants[0]])
                    pickerList.delete(0,tk.END)
                    showPick()
                    root.after(2000,finishList)
                    print(pairs)
                elif len(participants) == 2:
                    #This statement handles the special case when the last drawer picks their own name                   
                    pickedName = participant
                    pairs.append([selected,participant])                 
                    participants.remove(participant)
                    pickers.remove(selected)                    
                    if participants[0] == pickers[0]:
                        #If the last item in both lists are the same, the pairs are swapped.
                        participants.append(pickedName)
                        pickers.append(selected)
                        pickedName = participants[0]
                        pairs[-1] = [selected,participants[0]] 
                    if selected in pickers:
                        pickers.remove(selected)  
                    showPick()                                                                           
                    pickerList.delete(0,tk.END)
                    for picker in pickers:
                        pickerList.insert(tk.END,picker)
                    print(pairs)
                                    
                else:                                      
                    pickedName = participant
                    pairs.append([selected, participant])
                    showPick()
                    participants.remove(participant)
                    pickers.remove(selected)                                                    
                    pickerList.delete(0,tk.END)
                    for picker in pickers:
                        pickerList.insert(tk.END,picker)
                    print(pairs)
                    break           
                                    
    else:
        reveal.configure(text="You must select your name.")

def showPick():
    #Displays the user's pick under the name selection box
    reveal.configure(text=f"You drew {pickedName}")
    root.after(2000,hidePick)

def hidePick():
    #clears the name in the reveal label
    reveal.configure(text="")

def finishList():
    #Reveals the final list of pairings
    hat.destroy()    
    gift.grid(row=1,column=1,sticky="nsew",columnspan=4)
    pickerList.insert(tk.END,"THE FINAL LIST!")
    for pair in pairs:
        pickerList.insert(tk.END,f"{pair[0]} buys for {pair[1]}")
    rootHeader.configure(text="ALL NAMES HAVE BEEN DRAWN!!!", justify="center",font=30,fg="green")

#Class definitions
#Creates an instance of the Tk class and makes root the main window
root = tk.Tk()
root.title("From a Hat")
root.minsize(400,200)
root.configure(bg="silver")
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
GIFTIMAGE =tk.PhotoImage(file="gift.png")
gift = tk.Button(root,image=GIFTIMAGE,height=437,width=550)


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