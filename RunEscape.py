# Title and main screen background from https://pixabay.com/, title text generated with https://cooltext.com/, torches and tombstone taken from https://pngimg.com/search_image

# Resolution: 1280x720 

# Global Variables:

# loginWindow = window of the login screen
# mainCanvas = canvas of main screen

# usernameInput = username input field on login screen
# passwordInput = password input field on login screen
# errorOutput = output label on login screen

# -=-=- Stats -=-=-
# user = username
# attack = Damage exp of the player
# hp = hp exp of the player

# pEntity = player model

import tkinter as tk
from tkinter import messagebox
import os 

# -=-=-=-=- General functions -=-=-=-=-

def data(line): # Seperates the number in a file line
	data = ""
	trigger = 0
	for i in range (0, len(line)):
		if trigger == 1:
			data = data + line[i]
		if line[i] == ":":
			trigger = 1

	return(data) 

# -=-=-=-=- Functions for login screen -=-=-=-=-

def login():
	global user
	user = usernameInput.get()
	password = passwordInput.get()

	errorOutput.config(text="")

	if user == "" or user.isspace():
		errorOutput.config(text="Username cannot be empty")
	elif password == "" or password.isspace():
		errorOutput.config(text="Password cannot be empty")
	elif os.path.exists(os.path.join(os.getcwd(), "accounts", user + ".txt")):
		newFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r")
		for i, line in enumerate(newFile):
			if i == 0:
				usernameFile = data(line)
			elif i == 1:
				passwordFile = data(line)
			elif i > 1:
				break

		newFile.close()

		if usernameFile != user + "\n":
			errorOutput.config(text="Username is incorrect")
		elif passwordFile != password + "\n":
			errorOutput.config(text="Password is incorrect")
		else:
			errorOutput.config(text="Welcome Adventurer!")
			loginWindow.destroy()
	else:
		errorOutput.config(text="Username does not exist")

def createAccount():
	global user

	user = usernameInput.get()
	password = passwordInput.get()
	errorOutput.config(text="")

	if os.path.isdir("accounts") == False:
		os.mkdir("accounts")
	
	if user == "" or user.isspace():
		errorOutput.config(text="Username cannot be empty")
	elif password == "" or password.isspace():
		errorOutput.config(text="Password cannot be empty")
	elif os.path.exists(os.path.join(os.getcwd(), "accounts", user + ".txt")):
		errorOutput.config(text="Account Already Exists")
	else:
		newFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "w")
		newFile.write("Username:"+ user + "\n")
		newFile.write("Password:"+ password + "\n")
		newFile.write("HP:100\n")
		newFile.write("Attack:100\n")
		newFile.close()
		errorOutput.config(text="Account Successfully Created!")

# -=-=-=-=- Functions for menu -=-=-=-=-  

def save():

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r")
	
	lines = userFile.readlines()
	lines[2] = "HP:" + str(hp) + "\n"
	lines[3] = "Attack:" + str(attack) + "\n"

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "w")
	userFile.writelines(lines)

	userFile.close()

	tk.messagebox.showinfo("Save confirmed","Save has been confirmed")

	popup.mainloop()

def leaderboardFloors():
	pass

def leaderboardHP():
	pass

def leaderboardAttack():
	pass

def statsScreen():
	pass

def inventoryScreen():
	pass

# -=-=-=-=- Functions for player -=-=-=-=-   

def control(event):
    coords = mainCanvas.coords(pEntity)
    if event.char == "a":
        if coords[0] > 0:
            mainCanvas.move(pEntity, -10, 0)
    elif event.char == "d":
        if coords[0] < 1280:
            mainCanvas.move(pEntity, 10, 0)
    elif event.char == "w":
        if coords[1] > 0:
            mainCanvas.move(pEntity, 0, -10)
    elif event.char == "s":
        if coords[1] < 720:
            mainCanvas.move(pEntity, 0, 10)

def statsCollect():

	global hp
	global attack

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r")

	for i, line in enumerate(userFile):
		if i == 2:
			hp = int(data(line))
		elif i == 3:
			attack = int(data(line))
		elif i > 3:
			break

	userFile.close()  

# -=-=-=-=- Functions for making  main windows -=-=-=-=-

def loginScreen():
	global loginWindow		
	loginWindow= tk.Tk()
	loginWindow.geometry("1280x720")
	loginWindow.title("Run Escape Login")
	loginWindow.resizable(0, 0)

	bg_login = tk.PhotoImage(file = "background_login.png")
	bg = tk.Label(loginWindow, image=bg_login)
	bg.place(x=0, y=0)

	global usernameInput
	global passwordInput
	  
	usernameInput= tk.StringVar()
	passwordInput= tk.StringVar()

	nameLabel= tk.Label(loginWindow, text = "Username:")
	nameFetch= tk.Entry(loginWindow,textvariable = usernameInput)

	passwordLabel= tk.Label(loginWindow, text = "Password:")
	passwordFetch= tk.Entry(loginWindow, textvariable = passwordInput, show = '*')
	 
	loginButton= tk.Button(loginWindow,text = "Submit", command = login)
	loginWindow.bind("<Return>", login)
	accountButton= tk.Button(loginWindow,text = "Create Account", command = createAccount)

	global errorOutput

	errorOutput = tk.Label(loginWindow, text = "")
	  
	nameLabel.grid(row=1,column=1)
	nameFetch.grid(row=1,column=2)
	passwordLabel.grid(row=2,column=1)
	passwordFetch.grid(row=2,column=2)
	loginButton.grid(row=4,column=2)
	accountButton.grid(row=5,column=2)
	errorOutput.grid(row=6,column=2)

	loginWindow.grid_rowconfigure(0, weight=1)
	loginWindow.grid_rowconfigure(7, weight=1)
	loginWindow.grid_columnconfigure(0, weight=1)
	loginWindow.grid_columnconfigure(3, weight=1)
	  
	loginWindow.mainloop()  

def mainScreen():
	
	global mainCanvas
	global pEntity

	mainWindow = tk.Tk()
	mainWindow.geometry("1280x720")
	mainWindow.title("Run Escape")
	mainWindow.resizable(0, 0)

	menubar = tk.Menu(mainWindow)
	mainWindow.config(menu=menubar)

	menuPlayer = tk.Menu(menubar, tearoff = 0)
	menuPlayer.add_command(label="Save", command= save)
	menuPlayer.add_separator()
	menuPlayer.add_command(label="Stats", command= statsScreen)
	menuPlayer.add_command(label="Inventory", command= inventoryScreen)

	menuLeaderboard = tk.Menu(menubar, tearoff = 0)
	menuLeaderboard.add_command(label="Floors", command= leaderboardFloors)
	
	menuLevels = tk.Menu(menuLeaderboard, tearoff = 0)
	menuLevels.add_command(label="HP", command= leaderboardHP)
	menuLevels.add_command(label="Attack", command = leaderboardAttack)
	menuLeaderboard.add_cascade(label="Levels", menu= menuLevels)

	menubar.add_command(label="Exit", command= mainWindow.destroy)
	menubar.add_cascade(label="Player", menu= menuPlayer)
	menubar.add_cascade(label="Leaderboard", menu= menuLeaderboard)
	
	mainCanvas= tk.Canvas(mainWindow, bg="green", height=720, width=1280)
	mainCanvas.pack()

	playerModel = tk.PhotoImage(file="player.png")
	playerModel = playerModel.subsample(5)
	statsCollect()

	pEntity = mainCanvas.create_image(640, 360, anchor="center", image = playerModel)
	mainCanvas.bind("<Key>", control)
	mainCanvas.focus_set()

	mainWindow.mainloop()


loginScreen()
mainScreen()