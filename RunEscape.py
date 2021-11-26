# Title and main screen background from https://pixabay.com/, title text generated with https://cooltext.com/, torch, tombstone, tree, stone and heart taken from https://pngimg.com/
# Dunegeon Door png taken from https://www.pngitem.com/ and allowed for personal use, player model taken from https://www.gameart2d.com/the-knight-free-sprites.html
# Anvil taken from https://www.cleanpng.com/
# All images used are not subject to copyright as this is for personal use

# -=-=- Resolution: 1280x720 -=-=-

# -=-=- CHEAT GUIDE -=-=-
# On main menu (key):
# 1 = 10 levels in HP
# 2 = 10 levels in Attack
# 3 = 10 levels in Woodcutting
# 4 = 10 levels in Mining
# 5 = 10 levels in Crafting
# 6 = 25 floors
# 7 = 100 wood
# 8 = 100 metal
# 9 = 10 sword levels
# 0 = 10 armour levels

#  -=-=- Global Variables: -=-=-

# loginWindow = window of the login screen
# mainWindow = window of the main/game screen
# mainCanvas = canvas of main screen
# gameCanvas = canvas of game screen
# deathCanvas = canvas of death screen
# choicePopup = popup for crafting choice

# usernameInput = username input field on login screen
# passwordInput = password input field on login screen
# errorOutput = output label on login screen

# pEntity = player entity in lobby
# gEntity = player entity in game
# dEntity = door entity in lobby
# tEntity = tree entity in lobby
# oEntity = ore entity in lobby
# aEntity = anvil entity in lobby
# sEntity = armour stand entity in lobby
# aimTriangle = triangle used to aim in game

# playerModel = player model
# heartModel = heart model
# attackFrameX = attack model frame x (1 - 10)
# slimeList = list of all slimes on the screen

# mov(x/y) = velocity of x/y

# floorExp = exp gained from that floor

# menubar = top menu

# -=-=- Stat File -=-=-
# user = username
# hp = hp exp of the player
# attack = Damage exp of the player
# woodcutting = woodcutting exp of the player
# mining = mining exp of the player
# crafting = crafting exp of the player
# floor = current completed floor of the player
# wood = wood of the player
# metal = metal of the player
# swordLevel = sword level of the player
# armourLevel = amour level of the player

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

def endAccept(event): # Moves player back to lobby
	try:
		deathCanvas.destroy()
	except:
		victoryCanvas.destroy()
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
	elif len(user) > 10:
		errorOutput.config(text="Username longer than 10 characters")
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
		newFile.write("Sword Level:1\n")
		newFile.write("Armour Level:1\n")
		newFile.close()
		errorOutput.config(text="Account Successfully Created!")

# -=-=-=-=- Functions for main screen -=-=-=-=-

def mainScreenHit(coords):
	global movx
	global movy

	doorCoords = mainCanvas.bbox(dEntity)
	treeCoords = mainCanvas.bbox(tEntity)
	oreCoords = mainCanvas.bbox(oEntity)
	anvilCoords = mainCanvas.bbox(aEntity)
	standCoords = mainCanvas.bbox(sEntity)
	
	if doorCoords[0] < coords[0] < doorCoords[2]:
		if doorCoords[1] < coords[1] < doorCoords[3]:
			movx = 0
			movy = 0
			prompt= tk.messagebox.askquestion("Enter the Dungeon","You are entering floor: " + str(floor + 1) + ". Game will autosave but saving will be disabled. Do you want to continue?")
			if prompt=='yes':
				save()
				floorScreen() 
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if treeCoords[0] < coords[0] < treeCoords[2]:
		if treeCoords[1] < coords[1] < treeCoords[3]:
			movx = 0
			movy = 0
			prompt= tk.messagebox.askquestion("Woodcutting","Would you like to chop wood?")
			if prompt=="yes":
				skillingActivity("woodcutting")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if oreCoords[0] < coords[0] < oreCoords[2]:
		if oreCoords[1] < coords[1] < oreCoords[3]:
			movx = 0
			movy = 0
			prompt= tk.messagebox.askquestion("Mining","Would you like to mine metal?")
			if prompt=="yes":
				skillingActivity("mining")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if anvilCoords[0] < coords[0] < anvilCoords[2]:
		if anvilCoords[1] < coords[1] < anvilCoords[3]:
			movx = 0
			movy = 0
			message = "Would you like to upgrade your sword?\n"
			message = message + "Metal Need: " + str(swordLevel) + "(" + str(metal) + ")\n"
			message = message + "Wood Need: " + str(swordLevel) + "(" + str(wood) + ")"
			prompt= tk.messagebox.askquestion("Crafting",message)
			if prompt=="yes":
				skillingActivity("sword")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if standCoords[0] < coords[0] < standCoords[2]:
		if standCoords[1] < coords[1] < standCoords[3]:
			movx = 0
			movy = 0
			message = "Would you like to upgrade your armour?\n"
			message = message + "Metal Need: " + str(armourLevel) + "(" + str(metal) + ")\n"
			message = message + "Wood Need: " + str(armourLevel) + "(" + str(wood) + ")"
			prompt= tk.messagebox.askquestion("Crafting",message)
			if prompt=="yes":
				skillingActivity("armour")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

def mainPress(event):
	global direction
	global controls
	global movx
	global movy 

	global hp
	global attack
	global woodcutting
	global mining 
	global crafting
	global floor
	global wood
	global metal
	global swordLevel
	global armourLevel

	coords = mainCanvas.coords(pEntity)

	if event.char == "a" and skilling == 0 and coords[0] > 0 :
		direction = "left"
		movx = -10
	elif event.char == "d" and skilling == 0 and coords[0] < 1280:
		direction = "right"
		movx = 10
	elif event.char == "w" and skilling == 0 and coords[1] > 0:
		direction = "up"
		movy = -10
	elif event.char == "s" and skilling == 0 and coords[1] < 720:
		direction = "down"
		movy = 10
	elif event.char == "1" and skilling == 0:
		print("test")
		exp = 100 * round(1.5 ** (level(hp) + 8))
		hp = exp
	elif event.char == "2"  and skilling == 0:
		exp = 100 * round(1.5 ** (level(attack) + 8))
		attack = exp
	elif event.char == "3" and skilling == 0:
		exp = 100 * round(1.5 ** (level(woodcutting) + 8))
		woodcutting = exp
	elif event.char == "4" and skilling == 0:
		exp = 100 * round(1.5 ** (level(mining) + 8))
		mining = exp
	elif event.char == "5" and skilling == 0:
		exp = 100 * round(1.5 ** (level(crafting) + 8))
		crafting = exp
	elif event.char == "6" and skilling == 0:
		floors = floors + 25
	elif event.char == "7" and skilling == 0:
		wood = wood + 100
	elif event.char == "8" and skilling == 0:
		metal = metal + 100
	elif event.char == "9" and skilling == 0:
		swordLevel = swordLevel + 10
	elif event.char == "0" and skilling == 0:
		armourLevel = armourLevel + 10

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
	lines[9] = "Metal:" + str(metal) + "\n"
	lines[10] = "Sword Level:" + str(swordLevel) + "\n"
	lines[11] = "Armour Level:" + str(armourLevel) + "\n"

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "w")
	userFile.writelines(lines)

	userFile.close()

	tk.messagebox.showinfo("Save confirmed","Save has been confirmed")

def leaderboard(type):
	leaderboard= tk.Tk()
	leaderboard.geometry("300x300")
	leaderboard.title(type + " leaderboard")
	leaderboard.resizable(0, 0)

	titleLabel= tk.Label(leaderboard, text = "Top 5 Accounts by EXP ("+type+"):")

	players = []

	for filename in os.listdir(os.path.join(os.getcwd(), "accounts")):

		file = open(os.path.join(os.getcwd(), "accounts", filename), "r")

		for i, line in enumerate(file):
			if i == 0:
				username = data(line)
			if i == 2 and type == "HP":
				score = int(data(line))
			elif i == 3 and type == "Attack":
				score = int(data(line))
			elif i == 4 and type == "Woodcutting":
				score = int(data(line))
			elif i == 5 and type == "Mining":
				score = int(data(line))
			elif i == 6 and type == "Crafting":
				score = int(data(line))
			elif i == 7 and type == "Floor":
				score = int(data(line))
			elif i > 7:
				break

		player = [username, score]
		if len(players) < 5:
			players.append(player)
		elif players[4][1] < player[4][1]:
			players.pop(4)
			players.append(player)
		players = sorted(players, key=lambda x: x[1])

	while len(players) < 5:
		players.insert(0,["N/A","N/A"])

	firstLabel = tk.Label(leaderboard, text = "1. " + players[4][0]. rstrip("\n")+ "      " + str(players[4][1]))
	secondLabel = tk.Label(leaderboard, text = "2. " + players[3][0]. rstrip("\n")+ "      " + str(players[3][1]))
	thirdLabel = tk.Label(leaderboard, text = "3. " + players[2][0]. rstrip("\n")+ "      " + str(players[2][1]))
	fourthLabel = tk.Label(leaderboard, text = "4. " + players[1][0]. rstrip("\n")+ "      " + str(players[1][1]))
	fifthLabel = tk.Label(leaderboard, text = "5. " + players[0][0]. rstrip("\n") + "      " + str(players[0][1]))
	  
	titleLabel.grid(row=1,column=1)
	firstLabel.grid(row=2,column=1)
	secondLabel.grid(row=3,column=1)
	thirdLabel.grid(row=4,column=1)
	fourthLabel.grid(row=5,column=1)
	fifthLabel.grid(row=6,column=1)

	leaderboard.grid_rowconfigure(1, weight=1)
	leaderboard.grid_rowconfigure(7, weight=1)
	leaderboard.grid_columnconfigure(0, weight=1)
	leaderboard.grid_columnconfigure(2, weight=1)
	
def playerScreen():
	pass

def controls():
	#[left, right, up, down, attack]
	protectedCharacters = ["1","2","3","4,","5", "6", "7", "8", "9", "0", "Ctrl"]
	pass

# -=-=-=-=- Functions for game window -=-=-=-=-

class slime:
	def __init__(self, type):

		self.type = type

		if type == 1:
			self.sModel = slimeModel1
			self.attack = 1
			self.health = 2
			self.speed = 4
		if type == 2:
			self.sModel = slimeModel2
			self.attack = 2
			self.health = 4
			self.speed = 6
		if type == 3:
			self.sModel = slimeModel3
			self.attack = 5
			self.health = 10
			self.speed = 10
		if type == 4:
			self.sModel = slimeModel4
			self.attack = 10
			self.health = 20
			self.speed = 14
		if type == 5:
			self.sModel = slimeModel5
			self.attack = 15
			self.health = 40
			self.speed = 18
		if type == 6:
			self.sModel = slimeModel6
			self.attack = 25
			self.health = 70
			self.speed = 25

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
			self.slimeDirectionX = "right"

		elif pCoords[0] < self.sCoords[0]:
			gameCanvas.move(self.sEntity, -self.speed, 0)
			self.slimeDirectionX = "left"

		if pCoords[1] > self.sCoords[1]:
			gameCanvas.move(self.sEntity, 0, self.speed)
			self.slimeDirectionY = "down"

		elif pCoords[1] < self.sCoords[1]:
			gameCanvas.move(self.sEntity, 0, -self.speed)
			self.slimeDirectionY = "up"

		pHitBox = gameCanvas.bbox(gEntity)
		if pHitBox[0] < self.sCoords[0] < pHitBox[2]:
			if pHitBox[1] < self.sCoords[1] < pHitBox[3]:
				health = health - self.attack
				gameCanvas.itemconfig(healthText,text=health)
				rebound = (self.speed * 18)
				if self.slimeDirectionX == "right":
					gameCanvas.coords(self.sEntity, self.sCoords[0] - rebound, self.sCoords[1])
				elif self.slimeDirectionX == "left":
					gameCanvas.coords(self.sEntity, self.sCoords[0], self.sCoords[1] + rebound)
				if self.slimeDirectionY == "down":
					gameCanvas.coords(self.sEntity, self.sCoords[0], self.sCoords[1] - rebound)
				elif self.slimeDirectionY == "up":
					gameCanvas.coords(self.sEntity, self.sCoords[0], self.sCoords[1] + rebound) 

	def hit(self, damage):
		self.health = self.health - damage
		
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
					hit = False
					if direction == "left":
						if (pCoords[0] - 120 < slime.sCoords[0] < pCoords[0]) and (pCoords[1] - 30 < slime.sCoords[1] < pCoords[1] + 60):
							hit = True
							gameCanvas.move(slime.sEntity, -180, 0)
					elif direction == "up":
						if (pCoords[1] - 120 < slime.sCoords[1] < pCoords[1]) and (pCoords[0] - 30 < slime.sCoords[0] < pCoords[0] + 60):
							hit = True
							gameCanvas.move(slime.sEntity, 0, -180)
					elif direction == "down":
						if (pCoords[1] < slime.sCoords[1] < pCoords[1] + 120) and (pCoords[0] - 30 < slime.sCoords[0] < pCoords[0] + 60):
							hit = True
							gameCanvas.move(slime.sEntity, 0, 180)
					else:
						if (pCoords[0] < slime.sCoords[0] < pCoords[0] + 120) and (pCoords[1] - 30 < slime.sCoords[1] < pCoords[1] + 60):
							hit = True
							gameCanvas.move(slime.sEntity, 180, 0)

					if hit == True:
						damage = 1 * level(attack) * swordLevel
						slime.hit(damage)
						if slime.health <= 0:
							gameCanvas.delete(slime.sEntity)
							slimeList.remove(slime)


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

# -=-=-=-=- Functions for skilling -=-=-=-=-   

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
	global armourLevel
	
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
		elif i == 11:
			armourLevel = int(data(line))
		elif i > 11:
			break

	userFile.close()   

def skillingActivity(skill):

	global woodcutting
	global mining 
	global crafting
	global wood
	global metal
	global armourLevel
	global swordLevel

	global skilling
	global movx
	global movy

	skilling = 1

	if skill == "woodcutting":		
			
		delay = random.randint(2, 4)

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
				skilling = 0
				movx = 0
				movy = 0 # would auto save here but I need to prove the user can save 
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)
				mainMove()
				
				loadingPopup.destroy()

				newLevel = level(woodcutting)
				expLeft = (100 * (1.5 ** (newLevel - 1))) - woodcutting

				message = "You have cut "+ str(newWood) + " wood!("+str(wood)+")!\n"
				message = message + "You have earnt " + str(exp) + " exp!\n"
				message = message + "You are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!"

				finishPopup = tk.messagebox.showinfo(title="Completed", message= message)

		loadingPopup.mainloop()

	if skill == "mining":		
			
		delay = random.randint(2, 4)

		newOre = (round(level(mining) * 1.3))
		exp = (10 * level(mining))

		metal = metal + newOre
		mining = mining + exp

		loadingPopup = tk.Tk()
		loadingPopup.title("Mining")
		loadingPopup.geometry("150x100")
		
		loadingBar = Progressbar(loadingPopup, orient = HORIZONTAL, length = 100, mode = "determinate")

		loadingBar.place(x=25, y=20)

		skillLabel = tk.Label(loadingPopup, text = "Mining...")
		skillLabel.place(x=25 ,y=40)
		
		for i in range(5):
			loadingPopup.update_idletasks()
			loadingBar['value'] += 20
			time.sleep(delay/5)
			if i == 4:
				skilling = 0
				movx = 0
				movy = 0 
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)
				mainMove()
				
				loadingPopup.destroy()

				newLevel = level(mining)
				expLeft = (100 * (1.5 ** (newLevel - 1))) - mining

				message = "You have mined "+ str(newOre) + " metal("+str(metal)+")!\n"
				message = message + "You have earnt " + str(exp) + " exp!\n"
				message = message + "You are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!"

				finishPopup = tk.messagebox.showinfo(title="Completed", message= message)

		loadingPopup.mainloop()

	if skill == "sword":		
			
		delay = random.randint(2, 4)

		exp =  10 * level(crafting)

		if metal >= swordLevel and wood >= swordLevel:
			loadingPopup = tk.Tk()
			loadingPopup.title("Crafting")
			loadingPopup.geometry("150x100")
		
			loadingBar = Progressbar(loadingPopup, orient = HORIZONTAL, length = 100, mode = "determinate")

			loadingBar.place(x=25, y=20)

			skillLabel = tk.Label(loadingPopup, text = "Crafting...")
			skillLabel.place(x=25 ,y=40)
		
			for i in range(5):
				loadingPopup.update_idletasks()
				loadingBar['value'] += 20
				time.sleep(delay/5)
				if i == 4:
					crafting = crafting + exp
					metal = metal - swordLevel
					wood = wood - swordLevel
					swordLevel = swordLevel + 1
					skilling = 0
					movx = 0
					movy = 0 
					if direction == "left":
						mainCanvas.move(pEntity, 50, 0)
					elif direction == "down":
						mainCanvas.move(pEntity, -50, -50)
					elif direction == "up":
						mainCanvas.move(pEntity, -50, 50)
					else:
						mainCanvas.move(pEntity, -50, 0)
					mainMove()
					
					loadingPopup.destroy()

					newLevel = level(crafting)
					expLeft = (100 * (1.5 ** (newLevel - 1))) - crafting

					message = "New sword level:"+str(swordLevel)+"\n"
					message = message + "You have earnt " + str(exp) + " exp!\n"
					message = message + "You are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!"

					finishPopup = tk.messagebox.showinfo(title="Completed", message= message)

			loadingPopup.mainloop()

		else:
			tk.messagebox.showinfo(title="Crafting", message="Not enough resources")
			skilling = 0
			movx = 0
			movy = 0 
			if direction == "left":
				mainCanvas.move(pEntity, 50, 0)
			elif direction == "down":
				mainCanvas.move(pEntity, -50, -50)
			elif direction == "up":
				mainCanvas.move(pEntity, -50, 50)
			else:
				mainCanvas.move(pEntity, -50, 0)

	if skill == "armour":
		delay = random.randint(2, 4)

		exp =  10 * level(crafting)

		if metal >= armourLevel and wood >= armourLevel:
			loadingPopup = tk.Tk()
			loadingPopup.title("Crafting")
			loadingPopup.geometry("150x100")
		
			loadingBar = Progressbar(loadingPopup, orient = HORIZONTAL, length = 100, mode = "determinate")

			loadingBar.place(x=25, y=20)

			skillLabel = tk.Label(loadingPopup, text = "Crafting...")
			skillLabel.place(x=25 ,y=40)
		
			for i in range(5):
				loadingPopup.update_idletasks()
				loadingBar['value'] += 20
				time.sleep(delay/5)
				if i == 4:
					crafting = crafting + exp
					metal = metal - armourLevel
					wood = wood - armourLevel
					armourLevel = armourLevel + 1
					skilling = 0
					movx = 0
					movy = 0 
					if direction == "left":
						mainCanvas.move(pEntity, 50, 0)
					elif direction == "down":
						mainCanvas.move(pEntity, -50, -50)
					elif direction == "up":
						mainCanvas.move(pEntity, -50, 50)
					else:
						mainCanvas.move(pEntity, -50, 0)
					mainMove()
					
					loadingPopup.destroy()

					newLevel = level(crafting)
					expLeft = (100 * (1.5 ** (newLevel - 1))) - crafting

					message = "New armour level:"+str(armourLevel)+"\n"
					message = message + "You have earnt " + str(exp) + " exp!\n"
					message = message + "You are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!"

					finishPopup = tk.messagebox.showinfo(title="Completed", message= message)

			loadingPopup.mainloop()

		else:
			tk.messagebox.showinfo(title="Crafting", message="Not enough resources")
			skilling = 0
			movx = 0
			movy = 0 
			if direction == "left":
				mainCanvas.move(pEntity, 50, 0)
			elif direction == "down":
				mainCanvas.move(pEntity, -50, -50)
			elif direction == "up":
				mainCanvas.move(pEntity, -50, 50)
			else:
				mainCanvas.move(pEntity, -50, 0) 

# -=-=-=-=- Functions for movement -=-=-=-=-  

def keyRelease(event):
	global movx
	global movy

	movx = 0
	movy = 0 

def mainMove():
	coords = mainCanvas.coords(pEntity)
	mainScreenHit(coords)
	mainCanvas.move(pEntity, movx, movy)
	mainCanvas.after(30, mainMove) 

def gameMove():

	global aimTriangle

	gameCanvas.move(gEntity, movx, movy)
	pCoords = gameCanvas.coords(gEntity)

	if direction == "left":
		coords = [pCoords[0] - 70, pCoords[1], pCoords[0] - 50, pCoords[1] - 20, pCoords[0] - 50, pCoords[1] + 20]
	elif direction == "down":
		coords = [pCoords[0], pCoords[1] + 90, pCoords[0] - 20, pCoords[1] + 70, pCoords[0] + 20, pCoords[1] + 70]
	elif direction == "up":
		coords = [pCoords[0], pCoords[1] - 90, pCoords[0] - 20, pCoords[1] - 70, pCoords[0] + 20, pCoords[1] - 70]
	else:
		coords = [pCoords[0] + 70, pCoords[1], pCoords[0] + 50, pCoords[1] - 20, pCoords[0] + 50, pCoords[1] + 20]
	
	try:
		gameCanvas.delete(aimTriangle)
	except:
		pass

	aimTriangle = gameCanvas.create_polygon(coords, fill="red",outline="black")

	gameCanvas.after(10, gameMove) 

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
	menuPlayer.add_command(label="Stats", command= playerScreen)

	menuLeaderboard = tk.Menu(menubar, tearoff = 0)
	menuLeaderboard.add_command(label="Floors", command= lambda: leaderboard("Floors"))
	menuLevels = tk.Menu(menuLeaderboard, tearoff = 0)
	menuLevels.add_command(label="HP", command= lambda: leaderboard("HP"))
	menuLevels.add_command(label="Attack", command= lambda: leaderboard("Attack"))
	menuLevels.add_command(label="Woodcutting", command= lambda: leaderboard("Woodcutting"))
	menuLevels.add_command(label="Mining", command= lambda: leaderboard("Mining"))
	menuLevels.add_command(label="Crafting", command= lambda: leaderboard("Crafting"))
	menuLeaderboard.add_cascade(label="Levels", menu= menuLevels)

	menubar.add_command(label="Exit", command= mainWindow.destroy)
	menubar.add_cascade(label="Player", menu= menuPlayer)
	menubar.add_cascade(label="Leaderboard", menu= menuLeaderboard)
	menubar.add_command(label="Controls", command=controls)

	statsCollect()

	mainScreen() 

# -=-=-=-=- Functions for making screens -=-=-=-=-

def mainScreen():
	
	global mainCanvas

	global playerModel
	global heartModel

	global attackFrame1 # I found the code worked best when images were fetched in the same function
	global attackFrame2 # that the canvas was made so here each image is fetched
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
	global oEntity 
	global aEntity
	global sEntity

	global movx
	global movy
	global direction
	global skilling
	
	mainCanvas= tk.Canvas(mainWindow, bg="green", height=720, width=1280)
	mainCanvas.pack()

	doorModel = tk.PhotoImage(file="dungeon_door.png")
	doorModel = doorModel.subsample(6)
	heartModel = tk.PhotoImage(file="heart.png")
	heartModel = heartModel.subsample(10)
	treeModel = tk.PhotoImage(file="tree.png")
	treeModel = treeModel.subsample(2)
	oreModel = tk.PhotoImage(file="ore.png")
	oreModel = oreModel.subsample(10)
	anvilModel = tk.PhotoImage(file="anvil.png")
	anvilModel = anvilModel.subsample(5)
	standModel = tk.PhotoImage(file="armour.png")
	standModel = standModel.subsample(5)
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
	oEntity = mainCanvas.create_image(80, 390, image = oreModel)
	aEntity = mainCanvas.create_image(780, 660, image = anvilModel)
	sEntity = mainCanvas.create_image(500, 640, image = standModel)
	pEntity = mainCanvas.create_image(640, 360, anchor="center", image = playerModel)

	mainCanvas.bind("<KeyPress>", mainPress)
	mainCanvas.bind("<KeyRelease>", keyRelease)
	mainCanvas.focus_set()

	skilling = 0
	direction = "right"
	movx = 0
	movy = 0

	mainMove()

	mainWindow.mainloop() 

def floorScreen():

	global gameCanvas
	global gEntity
	
	global health
	global healthText
	
	global movx
	global movy
	global direction
	global attacking
	
	global slimeList
	global floorExp

	mainCanvas.destroy()
	menubar.entryconfig("Player", state = "disabled")

	gameCanvas= tk.Canvas(mainWindow, bg="grey", height=720, width=1280)
	gameCanvas.pack()
	gameCanvas.focus_set()

	health = level(hp) * 5 * armourLevel

	floorText = gameCanvas.create_text(640, 34, fill= "black", font = ('Helvetica','35','bold'), text="Current Floor: " + str(floor + 1))
	healthText = gameCanvas.create_text(1140, 34, fill= "red", font = ('Helvetica','35','bold'), text=health)
	heartIcon =  gameCanvas.create_image(1238, 32, image = heartModel)
	gEntity = gameCanvas.create_image(640, 360, anchor="center", image = playerModel)

	statsCollect()
	
	attacking = 0
	direction = "right"
	cheatCombo = 0
	movx = 0
	movy = 0

	gameMove()

	gameCanvas.bind("<KeyPress>", gamePress)
	gameCanvas.bind("<KeyRelease>", keyRelease)
	
	types = []
	floorExp = 0

	for i in range(10 + 2*(floor)):
		if floor  >= 5:
			type = random.randint(1,2)
		elif floor  >= 10:
			type = random.randint(1,3)
		elif floor >= 20:
			type = random.randint(1,4)
		elif floor >= 30:
			type = random.randint(2,4)
		elif floor >= 40:
			type = random.randint(2,4)
		elif floor >= 50:
			type = random.randint(2,5)
		elif floor >= 75:
			type = random.randint(3,5)
		elif floor >= 100:
			type = random.randint(3,6)
		elif floor >= 150:
			type = random.randint(4,6)
		elif floor >= 200:
			type = random.randint(5,6)
		elif floor >= 250:
			type = 6
		else:
			type = 1

		types.append(type)

		floorExp = floorExp + type * 3
		
	slimeList = []
	slimeList.append(slime(types[0]))
	slimeCount = 1
	count = 0

	while health > 0 and len(slimeList) > 0: 
		for entity in slimeList:
			entity.move()
		mainWindow.update()
		time.sleep(0.1)
		count = count + 1
		if count >= 20/(floor + 1) and slimeCount != 10 + 2*floor:
			count = 0
			slimeList.append(slime(types[slimeCount]))
			slimeCount = slimeCount + 1
	
	if health < 0:
		deathScreen()
	elif len(slimeList) == 0:
		victoryScreen()
 
def deathScreen():

	global deathCanvas

	gameCanvas.destroy()
	menubar.entryconfig("Player", state = "normal")

	deathCanvas= tk.Canvas(mainWindow, bg="black", height=720, width=1280)
	deathCanvas.create_text(640, 360, fill= "white", font = ('Helvetica','50','bold'), text="You died...\nPress any key to return to safety.")
	deathCanvas.focus_set()
	deathCanvas.pack()
	time.sleep(0.4)
	deathCanvas.bind("<Key>", endAccept)

def victoryScreen():

	global victoryCanvas

	global floor
	global attack
	global hp

	gameCanvas.destroy()
	menubar.entryconfig("Player", state = "normal")
	menubar.entryconfig("Player", state = "normal")

	floor = floor + 1
	hp = hp + floorExp
	attack = attack + floorExp
	expLeftHP = (100 * (1.5 ** (level(hp) - 1))) - attack
	expLeftAttack = (100 * (1.5 ** (level(attack) - 1))) - attack

	victoryCanvas= tk.Canvas(mainWindow, bg="gold", height=720, width=1280)
	message = "You beat floor: " + str(floor) + "!\n"
	message = message + "You earnt " + str(floorExp) + " exp in attack and hp from this floor.\n"
	message = message + "Your HP is now level " + str(level(hp)) + " with " + str(expLeftHP) + " exp until the next level!\n"
	message = message + "Your attack is now level " + str(level(attack)) + " with " + str(expLeftAttack) + " exp until the next level!\n"
	message = message + "Press any key to return to safety."
	victoryCanvas.create_text(640, 360, fill= "white", font = ('Helvetica','25','bold'), text=message)
	victoryCanvas.focus_set()
	victoryCanvas.pack()
	time.sleep(0.4)
	victoryCanvas.bind("<Key>", endAccept)
	
loginWindow()
mainWindow()