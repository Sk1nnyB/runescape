# Title and main screen background from https://pixabay.com/, title text generated with https://cooltext.com/, torch, tombstone, tree and heart taken from https://pngimg.com/
# Dunegeon Door png taken from https://www.pngitem.com/ and allowed for personal use, player model taken from https://www.gameart2d.com/the-knight-free-sprites.html

# -=-=- Resolution: 1280x720 -=-=-

#  -=-=- Global Variables: -=-=-

# loginWindow = window of the login screen
# mainWindow = window of the main/game screen
# mainCanvas = canvas of main screen
# gameCanvas = canvas of game screen
# deathCanvas = canvas of death screen

# usernameInput = username input field on login screen
# passwordInput = password input field on login screen
# errorOutput = output label on login screen

# pEntity = player entity in lobby
# gEntity = player entity in game
# dEntity = door entity in lobby
# tEntity = tree entity in lobby

# playerModel = player model
# heartModel = heart model
# attackFrameX = attack model frame x (1 - 10)
# slimeList = list of all slimes on the screen

# mov(x/y) = velocity of x/y

# menubar = top menu

# -=-=- Stat File -=-=-
# user = username
# attack = Damage exp of the player
# hp = hp exp of the player
# woodcutting = woodcutting exp of the player
# mining = mining exp of the player
# crafting = crafting exp of the player
# floor = current completed floor of the player
# wood = wood of the player
# metal = metal of the player
# swordLevel = sword level of the player

# attacking = if the user is currently in attack animation
# direction = the current facing direction of the player
# health = current health of the user
# healthText = health ui output

import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import HORIZONTAL
import os 
import math
import random
import time

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

def level(exp): # Converts exp to level
	
	if exp < 100:
		level = 1
	else:
		level = math.trunc(math.log((exp/100), 1.5) + 2)

	return level

def deathAccept(event): # Moves player back to lobby
	deathCanvas.destroy()
	mainScreen()

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
		newFile.write("HP:0\n")
		newFile.write("Attack:0\n")
		newFile.write("Woodcutting:0\n")
		newFile.write("Mining:0\n")
		newFile.write("Crafting:0\n")
		newFile.write("Floor:0\n")
		newFile.write("Wood:0\n")
		newFile.write("Metal:0\n")
		newFile.write("Sword Level:1")
		newFile.close()
		errorOutput.config(text="Account Successfully Created!")

# -=-=-=-=- Functions for main screen -=-=-=-=-

def mainScreenHit(coords):
	doorCoords = mainCanvas.bbox(dEntity)
	treeCoords = mainCanvas.bbox(tEntity)
	
	if doorCoords[0] < coords[0] < doorCoords[2]:
		if doorCoords[1] < coords[1] < doorCoords[3]:
			prompt= tk.messagebox.askquestion("Enter the Dungeon","You are entering floor: " + str(floor + 1) + ". Game will autosave but saving will be disabled. Do you want to continue?")
			if prompt=='yes':
				save()
				floorScreen() 

	if treeCoords[0] < coords[0] < treeCoords[2]:
		if treeCoords[1] < coords[1] < treeCoords[3]:
			prompt= tk.messagebox.askquestion("Woodcutting","Would you like to chop wood?")
			if prompt=='yes':
				skilling("woodcutting")

# -=-=-=-=- Functions for menu -=-=-=-=-  

def save():

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r")
	
	lines = userFile.readlines()
	lines[2] = "HP:" + str(hp) + "\n"
	lines[3] = "Attack:" + str(attack) + "\n"
	lines[4] = "Woodcutting:" + str(woodcutting) + "\n"
	lines[5] = "Mining:" + str(mining) + "\n"
	lines[6] = "Crafting:" + str(crafting) + "\n"
	lines[7] = "Floor:" + str(floor) + "\n"
	lines[8] = "Wood:" + str(wood) + "\n"
	lines[9] = "Sword Level:" + str(metal) + "\n"

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "w")
	userFile.writelines(lines)

	userFile.close()

	tk.messagebox.showinfo("Save confirmed","Save has been confirmed")

def leaderboard(type):
	pass

def statsScreen():
	pass

def inventoryScreen():
	pass

# -=-=-=-=- Functions for game window -=-=-=-=-

class slime:
	def __init__(self, type):

		self.type = type

		if type == 1:
			self.sModel = slimeModel1
			self.attack = 1
			self.health = 10
			self.speed = 2
		if type == 2:
			self.sModel = slimeModel2
			self.attack = 2
			self.health = 40
			self.speed = 3
		if type == 3:
			self.sModel = slimeModel3
			self.attack = 5
			self.health = 100
			self.speed = 4
		if type == 4:
			self.sModel = slimeModel4
			self.attack = 10
			self.health = 200
			self.speed = 6
		if type == 5:
			self.sModel = slimeModel5
			self.attack = 15
			self.health = 400
			self.speed = 9
		if type == 6:
			self.sModel = slimeModel6
			self.attack = 25
			self.health = 700
			self.speed = 12

		pCoords = gameCanvas.coords(gEntity)
		xCoord = random.randint(0, 1280)
		yCoord = random.randint(0, 720)
		self.sCoords = [xCoord, yCoord]
		while (pCoords[0] - 100 < xCoord < pCoords[0] + 100) and (pCoords[1] - 100 < yCoord < pCoords[1] + 100):
			xCoord = random.randint(0, 1280)
			yCoord = random.randint(0, 720)

		self.sEntity =  gameCanvas.create_image(xCoord, yCoord, image = self.sModel)

	def move(self):

		global health

		pCoords = gameCanvas.coords(gEntity)
		self.sCoords = gameCanvas.coords(self.sEntity)

		if pCoords[0] > self.sCoords[0]:
			gameCanvas.move(self.sEntity, self.speed, 0)
			slimeDirection = "right"

		elif pCoords[0] < self.sCoords[0]:
			gameCanvas.move(self.sEntity, -self.speed, 0)
			slimeDirection = "left"

		if pCoords[1] > self.sCoords[1]:
			gameCanvas.move(self.sEntity, 0, self.speed)
			slimeDirection = "down"

		elif pCoords[1] < self.sCoords[1]:
			gameCanvas.move(self.sEntity, 0, -self.speed)
			slimeDirection = "up"

		pHitBox = gameCanvas.bbox(gEntity)
		if pHitBox[0] < self.sCoords[0] < pHitBox[2]:
			if pHitBox[1] < self.sCoords[1] < pHitBox[3]:
				
				health = health - self.attack
				gameCanvas.itemconfig(healthText,text=health)
		
def playerAttack(coords):
	
	global attacking
	global slimeList
	global direction

	if attacking == 0:
		attacking = 1
		pCoords = coords
		count = 0

		attackFrames = [attackFrame1, attackFrame2, attackFrame3, attackFrame4, attackFrame5, attackFrame6, attackFrame7, attackFrame8, attackFrame9, attackFrame10]

		for frame in attackFrames:
			count = count + 1
			gameCanvas.itemconfig(gEntity, image=frame)
			mainWindow.update()
			time.sleep(0.04)
			if count == 5:
				for slime in slimeList:
					if direction == "left":
						if (pCoords[0] - 120 < slime.sCoords[0] < pCoords[0]) and (pCoords[1] - 30 < slime.sCoords[1] < pCoords[1] + 60):
							gameCanvas.delete(slime.sEntity)
							slimeList.remove(slime)
					elif direction == "up":
						if (pCoords[1] - 120 < slime.sCoords[1] < pCoords[1]) and (pCoords[0] - 30 < slime.sCoords[0] < pCoords[0] + 60):
							gameCanvas.delete(slime.sEntity)
							slimeList.remove(slime)
					elif direction == "down":
						if (pCoords[1] < slime.sCoords[1] < pCoords[1] + 120) and (pCoords[0] - 30 < slime.sCoords[0] < pCoords[0] + 60):
							gameCanvas.delete(slime.sEntity)
							slimeList.remove(slime)
					else:
						if (pCoords[0] < slime.sCoords[0] < pCoords[0] + 120) and (pCoords[1] - 30 < slime.sCoords[1] < pCoords[1] + 60):
							gameCanvas.delete(slime.sEntity)
							slimeList.remove(slime)

				if len(slimeList) == 0:
					print("You win")

		gameCanvas.itemconfig(gEntity, image=playerModel)
		mainWindow.update()
				
		attacking = 0

def gamePress(event):
	global direction
	global movx
	global movy 

	coords = gameCanvas.coords(gEntity)

	if event.char == "a" and attacking == 0 and coords[0] > 0 :
		direction = "left"
		movx = -10
	elif event.char == "d" and attacking == 0 and coords[0] < 1280:
		direction = "right"
		movx = 10
	elif event.char == "w" and attacking == 0 and coords[1] > 0:
		direction = "up"
		movy = -10
	elif event.char == "s" and attacking == 0 and coords[1] < 720:
		direction = "down"
		movy = 10
	elif event.char == "u" and attacking == 0:
		playerAttack(coords)

# -=-=-=-=- Functions for player -=-=-=-=-   

def controlMain(event):
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

	mainScreenHit(coords)

def statsCollect():

	global hp
	global attack
	global woodcutting
	global mining 
	global crafting
	global floor
	global wood
	global metal
	global swordLevel
	
	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r")

	for i, line in enumerate(userFile):
		if i == 2:
			hp = int(data(line))
		elif i == 3:
			attack = int(data(line))
		elif i == 4:
			woodcutting = int(data(line))
		elif i == 5:
			mining = int(data(line))
		elif i == 6:
			crafting = int(data(line))
		elif i == 7:
			floor = int(data(line))
		elif i == 8:
			wood = int(data(line))
		elif i == 9:
			metal = int(data(line))
		elif i == 10:
			swordLevel = int(data(line))
		elif i > 10:
			break

	userFile.close()  

def skilling(skill):

	global hp
	global attack
	global woodcutting
	global mining 
	global crafting
	global floor
	global wood
	global metal
	global swordLevel

	if skill == "woodcutting":

		mainCanvas.destroy()
		pauseCanvas= tk.Canvas(mainWindow, bg="brown", height=720, width=1280)
		pauseCanvas.pack()
		healthText = pauseCanvas.create_text(640, 360, fill= "green", font = ('Helvetica','50','bold'), text="Game is paused.\n You are woodcutting.")			
			
		delay = random.randint(2, 5)

		newWood = (round(level(woodcutting) * 1.3))
		exp = (10 * level(woodcutting))

		wood = wood + newWood
		woodcutting = woodcutting + exp

		loadingPopup = tk.Tk()
		loadingPopup.title("Woodcutting")
		loadingPopup.geometry("150x100")
		
		loadingBar = Progressbar(loadingPopup, orient = HORIZONTAL, length = 100, mode = "determinate")

		loadingBar.place(x=25, y=20)

		skillLabel = tk.Label(loadingPopup, text = "Woodcutting...")
		skillLabel.place(x=25 ,y=40)
		
		for i in range(5):
			loadingPopup.update_idletasks()
			loadingBar['value'] += 20
			time.sleep(delay/5)
			if i == 4:
				loadingPopup.destroy()
				newLevel = level(woodcutting)
				expLeft = (100 * (1.5 ** (newLevel - 1))) - woodcutting

				message = "You have cut "+ str(newWood) + " wood!\nYou have earnt " + str(exp) + " exp!\nYou are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!"

				finishPopup = tk.messagebox.showinfo(title="Completed", message= message)

				pauseCanvas.destroy() # would auto save here but I need to prove the user can save so :/
				mainScreen()

		loadingPopup.mainloop()

# -=-=-=-=- Functions for movement -=-=-=-=-  

def keyRelease(event):
	global movx
	global movy

	movx = 0
	movy = 0

def playerMove():
	gameCanvas.move(gEntity, movx, movy)
	gameCanvas.after(10, playerMove)

# -=-=-=-=- Functions for making windows -=-=-=-=-

def loginWindow():

	global loginWindow	
	global usernameInput
	global passwordInput
	global errorOutput

	loginWindow= tk.Tk()
	loginWindow.geometry("1280x720")
	loginWindow.title("Run Escape Login")
	loginWindow.resizable(0, 0)

	bg_login = tk.PhotoImage(file = "background_login.png")
	bg = tk.Label(loginWindow, image=bg_login)
	bg.place(x=0, y=0)
	
	usernameInput= tk.StringVar()
	passwordInput= tk.StringVar()

	nameLabel= tk.Label(loginWindow, text = "Username:")
	nameFetch= tk.Entry(loginWindow,textvariable = usernameInput)

	passwordLabel= tk.Label(loginWindow, text = "Password:")
	passwordFetch= tk.Entry(loginWindow, textvariable = passwordInput, show = '*')
	 
	loginButton= tk.Button(loginWindow,text = "Submit", command = login)
	loginWindow.bind("<Return>", login)
	accountButton= tk.Button(loginWindow,text = "Create Account", command = createAccount)

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

def mainWindow():
	
	global mainWindow
	global menubar

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
	menuLeaderboard.add_command(label="Floors", command= leaderboard("floor"))
	
	menuLevels = tk.Menu(menuLeaderboard, tearoff = 0)
	menuLevels.add_command(label="HP", command= leaderboard("hp"))
	menuLevels.add_command(label="Attack", command = leaderboard("attack"))
	menuLeaderboard.add_cascade(label="Levels", menu= menuLevels)

	menubar.add_command(label="Exit", command= mainWindow.destroy)
	menubar.add_cascade(label="Player", menu= menuPlayer)
	menubar.add_cascade(label="Leaderboard", menu= menuLeaderboard)

	statsCollect()

	mainScreen()

# -=-=-=-=- Functions for making screens -=-=-=-=-

def mainScreen():
	
	global mainCanvas

	global playerModel
	global heartModel
	global treeModel
	global attackFrame1
	global attackFrame2
	global attackFrame3
	global attackFrame4
	global attackFrame5
	global attackFrame6
	global attackFrame7
	global attackFrame8
	global attackFrame9
	global attackFrame10

	global slimeModel1
	global slimeModel2
	global slimeModel3
	global slimeModel4
	global slimeModel5
	global slimeModel6

	global pEntity
	global dEntity
	global tEntity
	
	mainCanvas= tk.Canvas(mainWindow, bg="green", height=720, width=1280)
	mainCanvas.pack()

	doorModel = tk.PhotoImage(file="dungeon_door.png")
	doorModel = doorModel.subsample(6)
	heartModel = tk.PhotoImage(file="heart.png")
	heartModel = heartModel.subsample(10)
	treeModel = tk.PhotoImage(file="tree.png")
	treeModel = treeModel.subsample(2)
	playerModel = tk.PhotoImage(file="player.png")
	playerModel = playerModel.subsample(5)

	attackFrame1 = tk.PhotoImage(file = "attack1.png")
	attackFrame1 = attackFrame1.subsample(5)
	attackFrame2 = tk.PhotoImage(file = "attack2.png")
	attackFrame2 = attackFrame2.subsample(5)
	attackFrame3 = tk.PhotoImage(file = "attack3.png")
	attackFrame3 = attackFrame3.subsample(5)
	attackFrame4 = tk.PhotoImage(file = "attack4.png")
	attackFrame4 = attackFrame4.subsample(5)
	attackFrame5 = tk.PhotoImage(file = "attack5.png")
	attackFrame5 = attackFrame5.subsample(5)
	attackFrame6 = tk.PhotoImage(file = "attack6.png")
	attackFrame6 = attackFrame6.subsample(5)
	attackFrame7 = tk.PhotoImage(file = "attack7.png")
	attackFrame7 = attackFrame7.subsample(5)
	attackFrame8 = tk.PhotoImage(file = "attack8.png")
	attackFrame8 = attackFrame8.subsample(5)
	attackFrame9 = tk.PhotoImage(file = "attack9.png")
	attackFrame9 = attackFrame9.subsample(5)
	attackFrame10 = tk.PhotoImage(file = "attack10.png")
	attackFrame10 = attackFrame10.subsample(5)
		
	slimeModel1 = tk.PhotoImage(file="jelly1.png")
	slimeModel1 = slimeModel1.subsample(5)
	slimeModel2 = tk.PhotoImage(file="jelly2.png")
	slimeModel2 = slimeModel2.subsample(5)
	slimeModel3 = tk.PhotoImage(file="jelly3.png")
	slimeModel3 = slimeModel3.subsample(5)
	slimeModel4 = tk.PhotoImage(file="jelly4.png")
	slimeModel4 = slimeModel4.subsample(5)
	slimeModel5 = tk.PhotoImage(file="jelly5.png")
	slimeModel5 = slimeModel5.subsample(5)
	slimeModel6 = tk.PhotoImage(file="jelly6.png")
	slimeModel6 = slimeModel6.subsample(5)

	dEntity = mainCanvas.create_image(640, 70, image = doorModel)
	tEntity = mainCanvas.create_image(1200, 360, image = treeModel)
	
	pEntity = mainCanvas.create_image(640, 360, anchor="center", image = playerModel)

	mainCanvas.bind("<Key>", controlMain)
	mainCanvas.focus_set()

	mainWindow.mainloop()

def floorScreen():

	global gameCanvas
	global gEntity
	global attacking
	global health
	global healthText
	global movx
	global movy
	global slimeList

	mainCanvas.destroy()
	menubar.entryconfig("Player", state = "disabled")
	menubar.entryconfig("Leaderboard", state = "disabled")

	gameCanvas= tk.Canvas(mainWindow, bg="grey", height=720, width=1280)
	gameCanvas.pack()
	gameCanvas.focus_set()

	health = level(hp) * 10

	floorText = gameCanvas.create_text(640, 34, fill= "black", font = ('Helvetica','35','bold'), text="Current Floor: " + str(floor + 1))
	healthText = gameCanvas.create_text(1140, 34, fill= "red", font = ('Helvetica','35','bold'), text=health)
	heartIcon =  gameCanvas.create_image(1238, 32, image = heartModel)
	start = [640, 360]
	gEntity = gameCanvas.create_image(640, 360, anchor="center", image = playerModel)

	statsCollect()
	
	attacking = 0
	movx = 0
	movy = 0

	playerMove()

	gameCanvas.bind("<KeyPress>", gamePress)
	gameCanvas.bind("<KeyRelease>", keyRelease)
	
	types = []

	for i in range(10*(floor+1)):
		if floor > 5:
			type = random.randint(1,2)
		elif floor > 10:
			type = random.randint(1,3)
		elif floor > 20:
			type = random.randint(1,4)
		elif floor > 30:
			type = random.randint(2,4)
		elif floor > 40:
			type = random.randint(2,4)
		elif floor > 50:
			type = random.randint(2,5)
		elif floor > 75:
			type = random.randint(3,5)
		elif floor > 100:
			type = random.randint(3,6)
		elif floor > 150:
			type = random.randint(4,6)
		elif floor > 200:
			type = random.randint(5,6)
		elif floor > 250:
			type = 6
		else:
			type = 1

		types.append(type)
		
	slimeList = []
	slimeList.append(slime(types[0]))
	slimeCount = 1
	count = 0

	while health > 0: 
		for entity in slimeList:
			entity.move()
		mainWindow.update()
		time.sleep(0.1)
		count = count + 1
		if count >= 20/(floor + 1) and slimeCount != 10*(floor+1):
			count = 0
			slimeList.append(slime(types[0]))
			slimeCount = slimeCount + 1
		
	deathScreen()

def deathScreen():

	global deathCanvas

	gameCanvas.destroy()
	menubar.entryconfig("Player", state = "normal")
	menubar.entryconfig("Leaderboard", state = "normal")

	deathCanvas= tk.Canvas(mainWindow, bg="black", height=720, width=1280)
	deathCanvas.create_text(640, 360, fill= "white", font = ('Helvetica','50','bold'), text="You died...\nPress any key to return to safety.")
	deathCanvas.focus_set()
	deathCanvas.pack()
	time.sleep(0.4)
	deathCanvas.bind("<Key>", deathAccept)
	
loginWindow()
mainWindow()