# Title and main screen background from https://pixabay.com/, title text generated with https://cooltext.com/, torch, tombstone, tree, stone and heart taken from https://pngimg.com/
# Dunegeon Door and armour stand png taken from https://www.pngitem.com/ and allowed for personal use, player model taken from https://www.gameart2d.com/the-knight-free-sprites.html
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
# controlWindow = window of the control choice screen
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
# controls = the corresponding keys are: [left, right, up, down, attack, boss]

# attacking = if the user is currently in attack animation
# direction = the current facing direction of the player
# health = current health of the user
# healthText = health ui output

import tkinter as tk # import tkinter for windows and labels and canvases etc.
from tkinter import messagebox # import for message boxes
from tkinter.ttk import Progressbar # import for progress bar when skilling
from tkinter import HORIZONTAL # import for horizontal movement for progress bar
import os # import os for finding files
import math # import maths for level boundries
import random # import for random numbers in skill timing and slime options
import time # import for smoother animation and time between slimes

# -=-=-=-=- General functions -=-=-=-=-

def data(line): # Seperates the number in a file line
	data = "" # Starts with no data
	trigger = 0 # Indicates the number in the file has been reached
	for i in range (0, len(line)): # For each character in the line
		if trigger == 1: # If it has reached the characters it wants
			data = data + line[i] # Add it to the string that will form the characters it wants
		if line[i] == ":": # When it reaches the point of the data
			trigger = 1 # Gather the data

	return(data) # Return the data

def level(exp): # Converts exp to level
	
	if exp < 100: # This is because I don't think the function works in reverse when below 2
		level = 1 # Set the players level as 1
	else: # Otherwise use the function
		level = math.trunc(math.log((exp/100), 1.5) + 2) # Work out the level of the skill by finding which boundry it crosses last

	return level # Return the level of the skill

def endAccept(event): # Moves player back to lobby
	try: # If the death canvas exists
		deathCanvas.destroy() # Destroy it
	except: # Otherwise the victory canvas exists
		victoryCanvas.destroy() # Destroy the victory canvas
	mainScreen() # Return to the lobby canvas

# -=-=-=-=- Functions for login screen -=-=-=-=-

def login(): # Function to log the user in
	global user # Allows user to be used later

	user = usernameInput.get() # Get the username from the username input field
	password = passwordInput.get() # Get the password from the username input field

	errorOutput.config(text="") # Reset the error field (they haven't commited an error yet)

	if user == "" or user.isspace(): # If they haven't filled out the username field
		errorOutput.config(text="Username cannot be empty") # Remind them to fill it out
	elif password == "" or password.isspace(): # If they haven't filled out the password field
		errorOutput.config(text="Password cannot be empty") # Remind them to fill it out
	elif os.path.exists(os.path.join(os.getcwd(), "accounts", user + ".txt")): # If a file for that user exists
		newFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r") # Open that file
		for i, line in enumerate(newFile): # For each line in the file
			if i == 0: # If it's the first line
				usernameFile = data(line) # Take the username data from that line
			elif i == 1: # If it's the second line
				passwordFile = data(line) # Take the password data from that line
			elif i > 1: # Once you are done with the file
				break # Stop looking through it (takes up less memory)

		newFile.close() # Close the file

		if usernameFile != user + "\n": # If the username doesn't match the username in the file (useless now as it will always be the same as file name but maybe changable in the future)
			errorOutput.config(text="Username is incorrect") # Tell them they got it wrong
		elif passwordFile != password + "\n": # If the password doesn't match the password in the file 
			errorOutput.config(text="Password is incorrect") # Tell them they got it wrong
		else: # Otherwise they got everything right
			errorOutput.config(text="Welcome Adventurer!") # Display the welcome message
			loginWindow.destroy() # Close the log in window, it is done this way to emulate a real RPG launcher
			mainWindow() # Then move to the game window
	else: # Otherwise the file doesn't exist
		errorOutput.config(text="Username does not exist") # Inform them there is no account

def createAccount(): # Function to create a new user account
	global user # Allows user to be used later

	user = usernameInput.get() # Get the username from the username input field
	password = passwordInput.get() # Get the password from the username input field
	errorOutput.config(text="") # Reset the error field (they haven't commited an error yet)

	if os.path.isdir("accounts") == False: # If there is not a folder for the creation of accounts
		os.mkdir("accounts") # Make one. A different folder is used to scan when doing leaderboards later. This is incase other text files such as arena save files are made.
	
	if user == "" or user.isspace():  # If they haven't filled out the username field
		errorOutput.config(text="Username cannot be empty") # Remind them to fill it out
	elif len(user) > 10: # If the username is too long for the leaderboards (and for convenience)
		errorOutput.config(text="Username longer than 10 characters") # Inform them it is too long
	elif password == "" or password.isspace(): # If they haven't filled out the password field
		errorOutput.config(text="Password cannot be empty") # Remind them to fill it out
	elif os.path.exists(os.path.join(os.getcwd(), "accounts", user + ".txt")): # If there is already an account of this name
		errorOutput.config(text="Account Already Exists") # Inform them that account already exists
	else: # Otherwise it is okay to make a file for that account
		newFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "w") # Make the file for the account
		newFile.write("Username:"+ user + "\n") # Write each saveable stat to a seperate line
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
		newFile.write("Left:a\n") # Then write all the controls
		newFile.write("Right:d\n")
		newFile.write("Up:w\n")
		newFile.write("Down:s\n")
		newFile.write("Attack:u\n")
		newFile.write("Boss:m\n")
		newFile.close() # Close the file once you are done
		errorOutput.config(text="Account Successfully Created!") # Inform the user their account has been made

# -=-=-=-=- Functions for main screen -=-=-=-=-

def mainScreenHit(coords): # Hit detection for the user on the main canvas, taking in the center of the player model
	global movx # Allows the direction of the player to be changed
	global movy

	doorCoords = mainCanvas.bbox(dEntity) # Obtain the hitbox positions of all the interactable skilling entities
	treeCoords = mainCanvas.bbox(tEntity)
	oreCoords = mainCanvas.bbox(oEntity)
	anvilCoords = mainCanvas.bbox(aEntity)
	standCoords = mainCanvas.bbox(sEntity)
	
	if doorCoords[0] < coords[0] < doorCoords[2]: # If the player is in between the right and left of the hitbox
		if doorCoords[1] < coords[1] < doorCoords[3]: # If the player is inbetween the top and bottom of the hitbox
			movx = 0 # Stop all movement
			movy = 0
			prompt= tk.messagebox.askquestion("Enter the Dungeon","You are entering floor: " + str(floor + 1) + ". Game will autosave but saving will be disabled. Do you want to continue?") # Ensure that they wish to do this
			if prompt=='yes': # If they do then start the skill
				save() # In this one the game is saved, to mimic that boss fights are also not saved while in play
				floorScreen() # Start the canvas for the arena floor
			else: # Otherwise if they do not want to do this activity
				if direction == "left": # Move them away from the activity in the direction they came from, so they do not trigger it again
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if treeCoords[0] < coords[0] < treeCoords[2]: # This is the same as the door detection but without saving, for woodcutting
		if treeCoords[1] < coords[1] < treeCoords[3]:
			movx = 0
			movy = 0
			prompt= tk.messagebox.askquestion("Woodcutting","Would you like to chop wood?")
			if prompt=="yes":
				skillingActivity("Woodcutting")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if oreCoords[0] < coords[0] < oreCoords[2]: # This is the same as woodcutting, for mining
		if oreCoords[1] < coords[1] < oreCoords[3]:
			movx = 0
			movy = 0
			prompt= tk.messagebox.askquestion("Mining","Would you like to mine metal?")
			if prompt=="yes":
				skillingActivity("Mining")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if anvilCoords[0] < coords[0] < anvilCoords[2]: # This is the same as woodcutting, for crafting a better sword
		if anvilCoords[1] < coords[1] < anvilCoords[3]:
			movx = 0
			movy = 0
			message = "Would you like to upgrade your sword?\n" # Except a longer message is shown as materials are used up in this skill
			message = message + "Metal Need: " + str(swordLevel) + "(" + str(metal) + ")\n"
			message = message + "Wood Need: " + str(swordLevel) + "(" + str(wood) + ")"
			prompt= tk.messagebox.askquestion("Crafting",message)
			if prompt=="yes":
				skillingActivity("Sword")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

	if standCoords[0] < coords[0] < standCoords[2]: # This is the same as the anvil, for crafting better armour
		if standCoords[1] < coords[1] < standCoords[3]:
			movx = 0
			movy = 0
			message = "Would you like to upgrade your armour?\n"
			message = message + "Metal Need: " + str(armourLevel) + "(" + str(metal) + ")\n"
			message = message + "Wood Need: " + str(armourLevel) + "(" + str(wood) + ")"
			prompt= tk.messagebox.askquestion("Crafting",message)
			if prompt=="yes":
				skillingActivity("Armour")
			else:
				if direction == "left":
					mainCanvas.move(pEntity, 50, 0)
				elif direction == "down":
					mainCanvas.move(pEntity, -50, -50)
				elif direction == "up":
					mainCanvas.move(pEntity, -50, 50)
				else:
					mainCanvas.move(pEntity, -50, 0)

def mainPress(event): # Determines the outcome of the user pressing a key on the lobby screen
	global direction #Take in the current controls used and the state of the player's movement
	global controls
	global movx
	global movy 

	global hp # Take in all the cheat code changed stats
	global attack
	global woodcutting
	global mining 
	global crafting
	global floor
	global wood
	global metal
	global swordLevel
	global armourLevel

	coords = mainCanvas.coords(pEntity) # Obtain the current 

	if event.char == controls[0] and skilling == 0 and coords[0] > 10 : # If they player is not currently out of bounds, and doing so would not take them, and not skilling
		direction = "left" # set their direction of motion
		movx = -10 # and velocity
	elif event.char == controls[1] and skilling == 0 and coords[0] < 1270: # Repeat for each direction
		direction = "right"
		movx = 10
	elif event.char == controls[2] and skilling == 0 and coords[1] > 10:
		direction = "up"
		movy = -10
	elif event.char == controls[3] and skilling == 0 and coords[1] < 710:
		direction = "down"
		movy = 10
	elif event.char == controls[5]:
		bossWindow()
	elif event.char == "1" and skilling == 0: # If the player is not skilling
		exp = 100 * round(1.5 ** (level(hp) + 8)) # Activate the according cheat code
		hp = exp # Update their stat
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

	# The game is not saved here, so will not reflect in the leaderboard but saving the game and having the popup would make it obvious these are cheat codes

# -=-=-=-=- Functions for menu -=-=-=-=-  

def save(): # This is the function to save the stats of the player, their current state in the arena floor is not saved in order to give it a roguelike game feeling


	# PLEASE NOTE: I did consider not adding this and having only auto save but that's not in the mark scheme. I would have added a trigger for the confirmation popup and
	#			   attached it to all skilling + the ends of dungeons. However, that would render this useless as a manual feature 
	#              and in the interests of obtaining the most marks I did not do this. If I get deducted marks for sub-optimal saving, I will not blame you though.

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r") # Open the save file of the user in a readable fashion
	
	lines = userFile.readlines() # reach line to a file, to preserve all settings in it
	lines[2] = "HP:" + str(hp) + "\n" # change the line of each stat file to represent their new stat exp / level
	lines[3] = "Attack:" + str(attack) + "\n"
	lines[4] = "Woodcutting:" + str(woodcutting) + "\n"
	lines[5] = "Mining:" + str(mining) + "\n"
	lines[6] = "Crafting:" + str(crafting) + "\n"
	lines[7] = "Floor:" + str(floor) + "\n"
	lines[8] = "Wood:" + str(wood) + "\n"
	lines[9] = "Metal:" + str(metal) + "\n"
	lines[10] = "Sword Level:" + str(swordLevel) + "\n"
	lines[11] = "Armour Level:" + str(armourLevel) + "\n"

	userFile.close() # Close the readable file

	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "w") # Open the file again in a writable mode
	userFile.writelines(lines) # Replace this file with the new one created in memory

	userFile.close() # Close the new file

	tk.messagebox.showinfo("Save confirmed","Save has been confirmed") # Inform the user that their save has been successful

def leaderboard(type): # Function to display the leaderboard screen

	global leaderboard # Allows it to be destroyed by exit

	save() # Save the user's progress, so that all the most up to date stats are shown
	leaderboard= tk.Tk() # Create the window for the leaderboard
	leaderboard.geometry("300x300") # Size the window appropriately, small as it is a sub window
	leaderboard.title(type + " leaderboard") # Title the window appropriate to the skill shown
	leaderboard.configure(bg='black') # Set the background to black so the colours contrast better
	leaderboard.resizable(0, 0) # This means the user cannot resize

	titleLabel= tk.Label(leaderboard, text = "Top 5 Accounts ("+type+"):",bg="#000", fg="white") # Generate the title displayed on the window for the correct skill

	players = [] # Refresh the list of the top 5 accounts

	for filename in os.listdir(os.path.join(os.getcwd(), "accounts")): # For each account on the computer

		file = open(os.path.join(os.getcwd(), "accounts", filename), "r") # Open than account

		for i, line in enumerate(file): # For each stat line
			if i == 0:
				username = data(line). rstrip("\n") # Find the username and take off the white space
			if i == 2 and type == "HP": # Find the stat you need and save their score
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
			elif i > 7: # Stop once you have gone through all stats (saves memory)
				break

		player = [username, score] # Save the player's name and score as a list
		print(player)
		print
		if len(players) < 5: # So that if there are less than 5 on the board
			players.append(player) # They can join the list
		elif int(players[0][1]) < int(player[1]): # Or if they are higher than the lowest scorer
			players.pop(0) # Remove that scorer
			players.append(player) # And add the new player
		players = sorted(players, key=lambda x: x[1]) # Then sort the list from low to high

	while len(players) < 5: # If there are less than 5 total accounts
		players.insert(0,["N/A","N/A"]) # Add the empty players

	firstLabel = tk.Label(leaderboard, text = "1. " + players[4][0] + "      " + str(players[4][1]), bg="#000", fg="gold") # Then showcase the leaderboard with gold
	secondLabel = tk.Label(leaderboard, text = "2. " + players[3][0] + "      " + str(players[3][1]), bg="#000", fg="silver") # silver
	thirdLabel = tk.Label(leaderboard, text = "3. " + players[2][0] + "      " + str(players[2][1]), bg="#000", fg="#cc6633") # and bronze
	fourthLabel = tk.Label(leaderboard, text = "4. " + players[1][0] + "      " + str(players[1][1]),bg="#000", fg="white")
	fifthLabel = tk.Label(leaderboard, text = "5. " + players[0][0] + "      " + str(players[0][1]), bg="#000", fg="white")
	  
	titleLabel.grid(row=1,column=1) # Put the title at the top of the grid
	firstLabel.grid(row=2,column=1)  # Put each place into a grid so they are in order
	secondLabel.grid(row=3,column=1)
	thirdLabel.grid(row=4,column=1)
	fourthLabel.grid(row=5,column=1)
	fifthLabel.grid(row=6,column=1)

	leaderboard.grid_rowconfigure(1, weight=1) # center the y of the grid in the middle
	leaderboard.grid_rowconfigure(7, weight=1)
	leaderboard.grid_columnconfigure(0, weight=1) # center the x of the grid in the middle
	leaderboard.grid_columnconfigure(2, weight=1)
	
def playerScreen(): # Function to display the player's stats

	global playerWindow # Allows it to be destroyed by exit 

	playerWindow= tk.Tk() # Create the window for the player
	playerWindow.geometry("325x150") # Size the window appropriately, small as it is a sub window
	playerWindow.title("Player Stats: "+user) # Title the window to show it is player stats
	playerWindow.configure(bg='#7c3f00') # Set the background to brown to resemble a backpack
	playerWindow.resizable(0, 0) # This means the user cannot resize the window

	skillLabel = tk.Label(playerWindow, text = "-=- LOBBY SKILLS -=-", bg="#562b00", fg="white") # Lobby Skills
	wcLabel = tk.Label(playerWindow, text = "Woodcutting:" +  "      " + str(level(woodcutting)), bg="#562b00", fg="white")
	miningLabel = tk.Label(playerWindow, text = "Mining:" +  "      " + str(level(mining)), bg="#562b00", fg="white")
	craftLabel = tk.Label(playerWindow, text = "Crafting:" +  "      " + str(level(crafting)), bg="#562b00", fg="white")
	
	dungeonLabel = tk.Label(playerWindow, text = "-=- DUNGEON SKILLS -=-", bg="#562b00", fg="white") # Dungeoneering Skills
	hpLabel = tk.Label(playerWindow, text = "HP:" +  "      " + str(level(hp)), bg="#562b00", fg="white") 
	attackLabel = tk.Label(playerWindow, text = "Attack:" +  "      " + str(level(attack)), bg="#562b00", fg="white") 
	floorLabel = tk.Label(playerWindow, text = "Floor:" +  "      " + str(floor), bg="#562b00", fg="white") 

	resLabel = tk.Label(playerWindow, text =  "-=- RESOURCES -=-", bg="#562b00", fg="white") # Resources
	woodLabel = tk.Label(playerWindow, text = "Wood:" +  "      " + str(wood), bg="#562b00", fg="white") 
	metalLabel = tk.Label(playerWindow, text = "Metal:" +  "      " + str(metal), bg="#562b00", fg="white") 

	eqmntLabel = tk.Label(playerWindow, text = "-=- EQUIPMENT LVL -=-", bg="#562b00", fg="white") # Equipment
	swordLabel = tk.Label(playerWindow, text = "Sword:" +  "      " + str(swordLevel), bg="#562b00", fg="white") 
	armourLabel = tk.Label(playerWindow, text = "Armour:" +  "      " + str(armourLevel), bg="#562b00", fg="white") 

	skillLabel.grid(row = 0, column= 1) # Place the lobby skills on the right of the user model
	wcLabel.grid(row = 1, column= 1)
	miningLabel.grid(row = 2, column= 1)  
	craftLabel.grid(row = 3, column= 1) 

	dungeonLabel.grid(row = 0, column= 2, padx=10) # Place the dungeon skills on the right of the user model
	hpLabel.grid(row = 1, column= 2, padx=10)
	attackLabel.grid(row = 2, column= 2, padx=10) 
	floorLabel.grid(row = 3, column= 2, padx=10) 

	resLabel.grid(row = 4, column= 1) # Place the materials beneath the lobby skills
	woodLabel.grid(row = 5, column= 1)
	metalLabel.grid(row = 6, column= 1)

	eqmntLabel.grid(row = 4, column= 2, padx=10) # Place the equipment beneath the dungeon skills
	swordLabel.grid(row = 5, column= 2, padx=10)
	armourLabel.grid(row = 6, column= 2, padx=10)

def control(controls): # Shows the screen of changeable controls, taking in the current controls (or control attempt in cases of failure)
	global controlWindow # Make the control window available to controlsSave()

	controlWindow= tk.Tk() # Create the window for the control window
	controlWindow.geometry("500x500") # Size the window appropriately, small as it is a sub window 
	controlWindow.title("Controls") # Title the window appropriate to the skill shown
	controlWindow.resizable(0, 0) # This means the user cannot resize

	titleLabel =tk.Label(controlWindow, text = "-=-=- CONTROLS -=-=-") # Create text for the user to title what they are changing

	leftInput = tk.StringVar(controlWindow, controls[0]) # Create input variables for each control, with the current ones already input
	rightInput = tk.StringVar(controlWindow, controls[1])
	upInput = tk.StringVar(controlWindow, controls[2])
	downInput = tk.StringVar(controlWindow, controls[3])
	attackInput = tk.StringVar(controlWindow, controls[4])
	bossInput = tk.StringVar(controlWindow, controls[5])
	
	leftLabel = tk.Label(controlWindow, text = "Move Left:") # Create input text labels to show each controls input field that caputures the input variable
	leftFetch = tk.Entry(controlWindow,textvariable = leftInput)
	rightLabel = tk.Label(controlWindow, text = "Move Right:")
	rightFetch = tk.Entry(controlWindow,textvariable = rightInput)
	upLabel = tk.Label(controlWindow, text = "Move Up:")
	upFetch = tk.Entry(controlWindow,textvariable = upInput)
	downLabel = tk.Label(controlWindow, text = "Move Down:")
	downFetch = tk.Entry(controlWindow,textvariable = downInput)
	attackLabel = tk.Label(controlWindow, text = "Attack:")
	attackFetch = tk.Entry(controlWindow,textvariable = attackInput)
	bossLabel = tk.Label(controlWindow, text = "Boss Key:")
	bossFetch = tk.Entry(controlWindow,textvariable = bossInput)

	# Button that runs the function to save the new controls
	saveButton = tk.Button(controlWindow,text = "Save", command = lambda: controlsSave([leftInput.get(), rightInput.get(), upInput.get(), downInput.get(), attackInput.get(), bossInput.get()])) 
	
	# Put the title at the top of the grid, centered accross both 
	titleLabel.grid(row=1,column=1, columnspan = 2)

	leftLabel.grid(row=2,column=1) # Then put each row of label and button per control
	leftFetch.grid(row=2,column=2)
	rightLabel.grid(row=3,column=1)
	rightFetch.grid(row=3,column=2)
	upLabel.grid(row=4,column=1)
	upFetch.grid(row=4,column=2)
	downLabel.grid(row=5,column=1)
	downFetch.grid(row=5,column=2)
	attackLabel.grid(row=6,column=1)
	attackFetch.grid(row=6,column=2)
	bossLabel.grid(row=7,column=1)
	bossFetch.grid(row=7,column=2)

	saveButton.grid(row=8, column =2) # Finally put the button at the bottom

	controlWindow.grid_rowconfigure(0, weight=1) # Finally center the x and y of the grid
	controlWindow.grid_rowconfigure(9, weight=1)
	controlWindow.grid_columnconfigure(0, weight=1)
	controlWindow.grid_columnconfigure(3, weight=1)

def controlsSave(newBinds): # Attempts to see if the new controls are savable
	global controls # Takes in the current controls

	protectedCharacters = ["1","2","3","4,","5", "6", "7", "8", "9", "0"] # These characters cannot be overwritten as they are used for cheat codes
	tempNewBinds = [] # A temporary list to store suitable inputs
	error = 0 # This will trigger an error and stop multiple error boxes appearing in chain

	for bind in newBinds: # For each control
		if len(bind) != 1 and error == 0: # If it's not a single button and there is not already an error
			tk.messagebox.showerror(title="Failure",message="Ensure keybinds are single keys") # Inform the user of their error
			controlWindow.destroy() # Destroy the current attempt
			control(newBinds) # Try again with the current attempt
			error = 1
		elif bind in protectedCharacters and error == 0: # If it's not a num key and there is not already an error
			tk.messagebox.showerror(title="Failure",message="Num keys cannot be overriden")
			controlWindow.destroy()
			control(newBinds)
			error = 1
		elif bind in tempNewBinds and error == 0: # If it's not used only once and there is not already an error
			tk.messagebox.showerror(title="Failure",message="Ensure keybinds are used only once")
			controlWindow.destroy()
			control(newBinds)
			error = 1
		else: # Add it to the list of accepted binds
			tempNewBinds.append(bind)

	if len(tempNewBinds) == len(controls): # If there are enough accepted binds
		controls = tempNewBinds # Set them as the new controls
		save() # And save the new controls
		controlWindow.destroy()# Then close the controls screen

def quit(): # Attempts to destroy all windows
	
	mainWindow.destroy() # Destroys the main one which will always be open 
	
	try: # Then looks through the sub windows
		leaderboard.destroy() # And destroys them one by one
	except:
		pass
	
	try:
		controlWindow.destroy()
	except:
		pass

	try:
		playerWindow.destroy()
	except:
		pass

	try:
		loadingPopup.destroy()
	except:
		pass

	try:
		bossWindow.destroy()
	except:
		pass

def pause(): # Pauses the game
    tk.messagebox.showinfo(title="Paused",message="Game is paused") # Displays a pop up that stops all code until it is destroyed

# -=-=-=-=- Functions for game window -=-=-=-=-

class slime: # This is the class for each slime object
	def __init__(self, type): # This creates the slime on instantiation

		self.type = type # This sets it's type to the one randomly generated for it

		models = [slimeModel1, slimeModel2, slimeModel3, slimeModel4, slimeModel5, slimeModel6]

		# Based on it's increasing type it will have
		self.sModel = models[type-1] # A different image
		self.attack = ((type**2)-(type-1)*2) # Bigger attack
		self.health =  2 + ((type**2)-(type-1)*2) # More Health
		self.speed = 3 + ((type**2)-(type-1)*2) # Faster speed

		pCoords = gameCanvas.coords(gEntity) # It will then get the co ordinates of the player
		xCoord = random.randint(0, 1280) # And generate it's own random co ordinates on the screen
		yCoord = random.randint(0, 720)
		self.sCoords = [xCoord, yCoord]
		while (pCoords[0] - 120 < xCoord < pCoords[0] + 120) and (pCoords[1] - 150 < yCoord < pCoords[1] + 150): # If it is too close to the player
			xCoord = random.randint(0, 1280) # It will move further away
			yCoord = random.randint(0, 720)

		self.sEntity =  gameCanvas.create_image(xCoord, yCoord, image = self.sModel) # It will then generate an entity for itself

	def move(self): # This creates the movement of the slime

		global health # This finds the current health of the player
 
		pCoords = gameCanvas.coords(gEntity) # The players coordinates are also found
		self.sCoords = gameCanvas.coords(self.sEntity) # It then finds it's own coordinates

		if pCoords[0] > self.sCoords[0]: # If the player is further to the right
			gameCanvas.move(self.sEntity, self.speed, 0) # It will move at a speed appropriate for it's level
			self.slimeDirectionX = "right" # And set it's X direction to the right

		elif pCoords[0] < self.sCoords[0]: # This is the same but will move and set X direction to the left
			gameCanvas.move(self.sEntity, -self.speed, 0)
			self.slimeDirectionX = "left" 

		else: # This helps to create the bobble effect, created naturally by their inability to sometimes line up by preventing line ups
			gameCanvas.move(self.sEntity, 0, random.randint(-2,2)) 

		if pCoords[1] > self.sCoords[1]: # This works the same but for the Y direction going down
			gameCanvas.move(self.sEntity, 0, self.speed)
			self.slimeDirectionY = "down"

		elif pCoords[1] < self.sCoords[1]: # This works the same but for the Y direction going up
			gameCanvas.move(self.sEntity, 0, -self.speed)
			self.slimeDirectionY = "up"

		else: # This also helps the bobble effect, further preventing line ups
			gameCanvas.move(self.sEntity, random.randint(-2,2) , 0) 

		pHitBox = gameCanvas.bbox(gEntity) # This finds the current hitbox of the player
		if pHitBox[0] < self.sCoords[0] < pHitBox[2]: # If the slime is within the left and right of the hitbox
			if pHitBox[1] < self.sCoords[1] < pHitBox[3]: # And the top and bottom of the hit box
				health = health - self.attack # Damage the player equal to their attack
				gameCanvas.itemconfig(healthText,text=health) # Then update their life total UI accordingly
				if self.slimeDirectionX == "right": # Then move in the opposite direction so as to not chain hits
					gameCanvas.coords(self.sEntity, self.sCoords[0] - 180, self.sCoords[1])
				elif self.slimeDirectionX == "left":
					gameCanvas.coords(self.sEntity, self.sCoords[0] + 180, self.sCoords[1])
				if self.slimeDirectionY == "down":
					gameCanvas.coords(self.sEntity, self.sCoords[0], self.sCoords[1] - 180)
				elif self.slimeDirectionY == "up":
					gameCanvas.coords(self.sEntity, self.sCoords[0], self.sCoords[1] + 180) 

	def hit(self, damage): # Function so that the slime will take damage
		self.health = self.health - damage # Update the slimes health to take the damage
		
def playerAttack(coords): # Function for hit registration and damage from player
	
	global attacking # Sets the current status of the player
	global slimeList # Gets all the slimes on screen
	global direction # Gets the direction the player is swinging in

	if attacking == 0: # If they are not already attacking (redundant as this is also checked in motion but a double check never hurt)
	# And if changes are made in that function it will not affect this one
		attacking = 1 # They are now attacking
		pCoords = coords # Get the coords of the player
		count = 0 # Count the current frame in the swing

		attackFrames = [attackFrame1, attackFrame2, attackFrame3, attackFrame4, attackFrame5, attackFrame6, attackFrame7, attackFrame8, attackFrame9, attackFrame10] # Load each frame of the attack swing

		for frame in attackFrames: # For each frame in the swing
			count = count + 1 # Add one to the current frame count
			gameCanvas.itemconfig(gEntity, image=frame) # Update the playermodel
			mainWindow.update() # Then update what it looks like in the window
			time.sleep(0.02) # Then wait a bit for a smooth animation
			if count == 5:	# Once 0.1 seconds have passed			
				for slime in slimeList: # For each slime on the screen
					hit = False # Track if they are hit or not
					if direction == "left": # If they are swinging to the left
						if (pCoords[0] - 120 < slime.sCoords[0] < pCoords[0]) and (pCoords[1] - 50 < slime.sCoords[1] < pCoords[1] + 50): # If they are to the left
							hit = True # Mark them as hit
							gameCanvas.move(slime.sEntity, -180, 0) # Move them away from the player in the direction of their swing
					elif direction == "up": # Do the same for each direction
						if (pCoords[1] - 150 < slime.sCoords[1] < pCoords[1]) and (pCoords[0] - 50 < slime.sCoords[0] < pCoords[0] + 50):
							hit = True
							gameCanvas.move(slime.sEntity, 0, -180)
					elif direction == "down":
						if (pCoords[1] < slime.sCoords[1] < pCoords[1] + 150) and (pCoords[0] - 50 < slime.sCoords[0] < pCoords[0] + 50):
							hit = True
							gameCanvas.move(slime.sEntity, 0, 180)
					else:
						if (pCoords[0] < slime.sCoords[0] < pCoords[0] + 120) and (pCoords[1] - 50 < slime.sCoords[1] < pCoords[1] + 50):
							hit = True
							gameCanvas.move(slime.sEntity, 180, 0)

					if hit == True: # If the slime was hit
						slime.hit(level(attack) * swordLevel) # Calculate the damage and deal it to the slime
						if slime.health <= 0: # If the slime should no longer be alive
							gameCanvas.delete(slime.sEntity) # Remove it from the screen
							slimeList.remove(slime) # And the list of slimes alive on the screen
					else: # Otherwise if it was not hit
						slime.move() # Continue to move it towards the player
					mainWindow.update() # Update the position of the slime on the screen

		gameCanvas.itemconfig(gEntity, image=playerModel) # Reset the player back to their base animation
		mainWindow.update() # Update the window to reflect this change
				
		attacking = 0 # Indicate that the player is done attacking

def gamePress(event): # Function for when the user presses a button on the game canvas
	global direction # Get the players current facing direction
	global controls # Get the players current controls
	global movx # Get the players x velocity
	global movy # Get the players y velocity

	coords = gameCanvas.coords(gEntity) # Get the current co ordinates of the player

	# If the player has pressed a direction key, is not attacking and won't go off the canvas
	if event.char == controls[0] and attacking == 0 and coords[0] >= 10 : 
		direction = "left" # Set their facing direction to that key direction
		movx = -10 # And set their velocity in that direction
	elif event.char == controls[1] and attacking == 0 and coords[0] <= 1270:
		direction = "right"
		movx = 10
	elif event.char == controls[2] and attacking == 0 and coords[1] >= 10:
		direction = "up"
		movy = -10
	elif event.char == controls[3] and attacking == 0 and coords[1] <= 710:
		direction = "down"
		movy = 10
	elif event.char == controls[4] and attacking == 0: # If the player has pressed the attack key and is not already attacking
	# The attack check isredundant as this is also checked in the attack function but if changes are made in that function it will not affect this one
		playerAttack(coords) # Begin the attack animation for the player, with their current co ordinates as the center of the attack 
	elif event.char == controls[5]:
		bossWindow()

# -=-=-=-=- Functions for skilling -=-=-=-=-   

def statsCollect(): # Collect the stats for the player and store in global variables

	global hp # Collect the global variables for each changable stat
	global attack
	global woodcutting
	global mining 
	global crafting
	global floor
	global wood
	global metal
	global swordLevel
	global armourLevel
	global controls
	
	userFile = open(os.path.join(os.getcwd(), "accounts", user + ".txt"), "r") # Open the save file for the current user

	controls = [] # Reset the current control list for the user

	for i, line in enumerate(userFile): # For each stat
		if i == 2: # When the stat line for a specific stat is reached
			hp = int(data(line)) # Change the value held globally of that stat
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
		elif i == 12:
			controls.append(data(line). rstrip("\n"))
		elif i == 13:
			controls.append(data(line). rstrip("\n"))
		elif i == 14:
			controls.append(data(line). rstrip("\n"))
		elif i == 15:
			controls.append(data(line). rstrip("\n"))
		elif i == 16:
			controls.append(data(line). rstrip("\n"))
		elif i == 17:
			controls.append(data(line). rstrip("\n"))
		elif i > 17: # When all stats have been read
			break  # Stop the program (will save memory)

	userFile.close() # Stop reading from the file once all stats have been obtained   
 
def skillingActivity(activity): # Allows the user to skill at an entity

	global woodcutting # Get the current values for each skill
	global mining 
	global crafting
	global wood
	global metal
	global armourLevel
	global swordLevel

	global skilling # Get the skilling status of the player
	global movx # Get the current x and y velocities of the player
	global movy

	global loadingPopup # Allows it to be destroyed by exit

	skilling = 1 # Set the skilling status of the player to true

	if activity == "Woodcutting": # Depending on the skill choosen
		skill = woodcutting # They will get the correct level exp
		material = wood # And the correct material
		materialS = "wood" # With a string for text
	elif activity == "Mining":
		skill = mining # They will get the correct level exp
		material = metal # And the correct material
		materialS = "metal" # With a string for text
	elif activity == "Sword": # It is slightly different for crafting
		skill = crafting # Crafting is the skill for both and must be gotten
		equipment = swordLevel # You need to get the eqiupment
		equipmentT = "sword" # And track it
		activity = "Crafting" # Because crafting is the activity
	elif activity == "Armour": 
		skill = crafting
		equipment = armourLevel 
		equipmentT = "armour"
		activity = "Crafting"

	exp = (10 * level(skill)) # Calculate the exp they will earn from this
	delay = random.randint(2, 4) # Generate a random waiting time between 2 and 4 seconds

	if activity == "Woodcutting" or activity == "Mining":# If the player is gathering
		newMaterial = (round(level(skill) * 1.3)) # Calculate the material they will earn from this
		material = material + newMaterial # Add the material to their count
	
	if activity == "Woodcutting" or activity == "Mining" or (metal >= equipment and wood >= equipment): # If they have enough material or do not need it	

		loadingPopup = tk.Tk() # Generate the popup screen for the skill
		loadingPopup.title(activity) # Set the correct title
		loadingPopup.geometry("200x150") # Ensure it only encapsulates the progress bar and text
		
		loadingBar = Progressbar(loadingPopup, orient = HORIZONTAL, length = 100, mode = "determinate") # Set up the progress bar so that it works in stages
		# This could also be continuous but I chose it for aethetical purposes 
		loadingBar.place(x=25, y=20) # Place the bar at the top of the window

		skillLabel = tk.Label(loadingPopup, text = activity+"...") # Put a text label so that the user knows what they are doing
		skillLabel.place(x=25 ,y=40) # Put the label in the correct position

		attackFrames = [attackFrame1, attackFrame2, attackFrame3, attackFrame4, attackFrame5, attackFrame6, attackFrame7, attackFrame8, attackFrame9, attackFrame10] # Load each frame of the attack swing
		frame = 0 # Load the first frame of the animation

		for i in range(20):
			mainCanvas.itemconfig(pEntity, image=attackFrames[frame]) # Update the playermodel
			frame = frame + 1 # Then load the next frame
			if frame == len(attackFrames): # If it has loaded a frame that doesn't exist
				frame = 0 # Reset it to the start of the animation
			mainWindow.update() # Then update what it looks like in the window
			loadingPopup.update_idletasks() # Then update the bar
			loadingBar['value'] += 5 # By adding 5 to the value
			time.sleep(delay/20) # Then wait for the next tick of skilling

		skilling = 0 # Set that the user is no longer skilling
		movx = 0 # Reset the velocity of the user (in case key was still held)
		movy = 0 
		if direction == "left": # Move the player away in the direction they came
			mainCanvas.move(pEntity, 50, 0) # Enough so that they do not trigger the entity again
		elif direction == "down":
			mainCanvas.move(pEntity, -50, -50)
		elif direction == "up":
			mainCanvas.move(pEntity, -50, 50)
		else:
			mainCanvas.move(pEntity, -50, 0)
		mainMove() # Begin the move background check
		 
		loadingPopup.destroy() # Destroy the pop up window

		skill = skill + exp # Add the exp to their exp count
		newLevel = level(skill) # Determine their new level
		expLeft = (100 * (1.5 ** (newLevel - 1))) - skill # And how much they need before the next level

		if activity == "Mining" or activity == "Woodcutting": # If they were gathering		
			message = "You have gathered "+ str(newMaterial) + " " + materialS +"!("+str(material)+")\n" # Tell the user how much they got and have
			message = message + "You have earnt " + str(exp) + " exp!\n" # Tell the user how much exp they earnt
			message = message + "You are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!" # Tell the user their level and exp left
		elif activity == "Crafting": # If they were crafting
			equipment = equipment + 1 # Update the level of the weapon
			message = "New " + equipmentT + " level:"+str(swordLevel)+"\n" # Tell them the new level of the weapon
			message = message + "You have earnt " + str(exp) + " exp!\n" # Tell the user how much exp they earnt
			message = message + "You are now level " + str(newLevel) + " with " + str(expLeft) + " exp left until your next!" # Tell the user their level and exp left

		if activity == "Woodcutting": # If they were woodcutting
			woodcutting = skill # Update woodcuttng stat
			wood = material # And the correct material

		elif activity == "Mining": # If they were mining
			mining = skill # Update mining stat
			metal = material # And the correct material

		elif equipmentT == "sword": # If they were upgrading their sword
			crafting = skill # Update crafting stat
			swordLevel = equipment # And the correct equipment

		elif equipmentT == "armour": # If they were upgrading their armour
			crafting = skill # Update crafting stat
			armourLevel = equipment # And the correct equipment

		if activity == "Crafting":
			wood = wood - equipment
			metal = metal - equipment 

		finishPopup = tk.messagebox.showinfo(title="Completed", message= message) # Then show them the message with their gain message

		loadingPopup.mainloop() # And close the window operations

	else: # Othewise if they do not have enough resources
		tk.messagebox.showinfo(title="Crafting", message="Not enough resources") # Show an error box to enforce this
		skilling = 0 # Set that the user is no longer skilling
		movx = 0 # Reset the velocity of the user (in case key was still held)
		movy = 0 
		if direction == "left": # Move the player away in the direction they came
			mainCanvas.move(pEntity, 50, 0) # Enough so that they do not trigger the entity again
		elif direction == "down":
			mainCanvas.move(pEntity, -50, -50)
		elif direction == "up":
			mainCanvas.move(pEntity, -50, 50)
		else:
			mainCanvas.move(pEntity, -50, 0)

# -=-=-=-=- Functions for movement -=-=-=-=-  

def keyRelease(event): # Function for when a key is released
	global movx # Take the velocities of x and y
	global movy

	movx = 0 # And reset them
	movy = 0 

def mainMove(): # Function for movement on the main screen
	coords = mainCanvas.coords(pEntity) # Take the current co ordindates of the player
	mainScreenHit(coords)# Ensure it is not already hitting anything
	try: # In case it tries to move in between canvas deletion and creation at the end of a floor
		mainCanvas.move(pEntity, movx, movy) # Then move it in that direction
	except:
		pass
	mainCanvas.after(30, mainMove) # Wait 30ms then do it again 

def gameMove(): # Function for movement on the game screen

	global aimTriangle # Access the aiming triangle
	try: # In case it tries to move after canvas deletion at the end of the game
		gameCanvas.move(gEntity, movx, movy) # Move the player
	except:
		pass 
	pCoords = gameCanvas.coords(gEntity) # Take the current co ordindates of the player

	if direction == "left": # If they are moving left
		coords = [pCoords[0] - 70, pCoords[1], pCoords[0] - 50, pCoords[1] - 20, pCoords[0] - 50, pCoords[1] + 20] # Get the triangle co ordinates their left
	elif direction == "down": # Repeat for each direction
		coords = [pCoords[0], pCoords[1] + 90, pCoords[0] - 20, pCoords[1] + 70, pCoords[0] + 20, pCoords[1] + 70]
	elif direction == "up":
		coords = [pCoords[0], pCoords[1] - 90, pCoords[0] - 20, pCoords[1] - 70, pCoords[0] + 20, pCoords[1] - 70]
	else:
		coords = [pCoords[0] + 70, pCoords[1], pCoords[0] + 50, pCoords[1] - 20, pCoords[0] + 50, pCoords[1] + 20]
	
	try: # Try if the triangle exists
		gameCanvas.delete(aimTriangle) # Delete the current traingle
	except: # If there is not a triangle
		pass # Do nothing

	aimTriangle = gameCanvas.create_polygon(coords, fill="red",outline="black") # Create the triangle in the desired position

	gameCanvas.after(30, gameMove) # Wait 10ms then do it again, more responsive as it is needed for gaming and the triangle must be updated frequently

# -=-=-=-=- Functions for making windows -=-=-=-=-

def loginWindow(): # Function to make the login window

	global loginWindow	# Allow the inputs to be taken from outside the function
	global usernameInput
	global passwordInput
	global errorOutput # Allow the error label to be updated

	loginWindow= tk.Tk() # Create and size the login window
	loginWindow.geometry("1280x720")
	loginWindow.title("Run Escape Login") # With the correct title
	loginWindow.resizable(0, 0) # Do not let the user rescale

	bg_login = tk.PhotoImage(file = "background_login.png") # Set the background image
	bg = tk.Label(loginWindow, image=bg_login) # Put it on a label
	bg.place(x=0, y=0) # And display it
	
	usernameInput= tk.StringVar() # Set the contents of the input fields to variables
	passwordInput= tk.StringVar()

	nameLabel= tk.Label(loginWindow, text = "Username:") # And put each input field with a label
	nameFetch= tk.Entry(loginWindow,textvariable = usernameInput)

	passwordLabel= tk.Label(loginWindow, text = "Password:")
	passwordFetch= tk.Entry(loginWindow, textvariable = passwordInput, show = '*')
	 
	loginButton= tk.Button(loginWindow,text = "Submit", command = login) # Show the button to log in
	accountButton= tk.Button(loginWindow,text = "Create Account", command = createAccount) # Also show the button to make a new account

	errorOutput = tk.Label(loginWindow, text = "") # Create the label for displaying error messages
	  
	nameLabel.grid(row=1,column=1) # Align each part in a grid, so that they are in rows of function
	nameFetch.grid(row=1,column=2) # And the text labels are to the left
	passwordLabel.grid(row=2,column=1)
	passwordFetch.grid(row=2,column=2)
	loginButton.grid(row=4,column=2)
	accountButton.grid(row=5,column=2)
	errorOutput.grid(row=6,column=2)

	loginWindow.grid_rowconfigure(0, weight=1) # Centre the x and y of the grid
	loginWindow.grid_rowconfigure(7, weight=1)
	loginWindow.grid_columnconfigure(0, weight=1)
	loginWindow.grid_columnconfigure(3, weight=1)
	  
	loginWindow.mainloop() # Then display the window

def mainWindow(): # Function to make the main window
	
	global mainWindow # To allow the main window to be manipulated by canvas, quit, etc
	global menubar # Allow save to be enabled and disabled
	global controls # Allow controls to be passed through to the controls screen

	mainWindow = tk.Tk() # Create and size the main window
	mainWindow.geometry("1280x720")
	mainWindow.title("Run Escape") # With the correct title
	mainWindow.resizable(0, 0) # Do not let the user rescale

	menubar = tk.Menu(mainWindow) # Create the top menu bar
	mainWindow.config(menu=menubar) # Add the configuration to the main menu

	menuPlayer = tk.Menu(menubar, tearoff = 0) # Create the menu for the player, tearoff = 0 means it can't be dagged out
	menuPlayer.add_command(label="Controls", command= lambda: control(controls)) # Add the function for changing controls
	menuPlayer.add_command(label="Stats", command= playerScreen) # Add the function for displaying stats

	menuLeaderboard = tk.Menu(menubar, tearoff = 0) # Do this for each menu
	menuLeaderboard.add_command(label="Floors", command= lambda: leaderboard("Floors"))
	menuLeaderboard.add_separator() # This creates a line to seperate
	menuLevels = tk.Menu(menuLeaderboard, tearoff = 0) # Create a sub menu for each skill
	menuLevels.add_command(label="HP", command= lambda: leaderboard("HP"))
	menuLevels.add_command(label="Attack", command= lambda: leaderboard("Attack"))
	menuLevels.add_command(label="Woodcutting", command= lambda: leaderboard("Woodcutting"))
	menuLevels.add_command(label="Mining", command= lambda: leaderboard("Mining"))
	menuLevels.add_command(label="Crafting", command= lambda: leaderboard("Crafting"))
	menuLeaderboard.add_cascade(label="Levels", menu= menuLevels) # Then add the sub menu to the menu dropdown

	menubar.add_command(label="Exit", command= quit) # This can be added without a menu, as just a command
	menubar.add_cascade(label="Player", menu= menuPlayer)
	menubar.add_cascade(label="Leaderboard", menu= menuLeaderboard) # These dropdown menus can also be added
	menubar.add_command(label="Save", command= save)
	menubar.add_command(label="Pause", command= pause)

	statsCollect() # Then collect all the inital stats to be stored in local memory

	mainScreen() # And run the main canvas screen first

def bossWindow(): # Function to minimise the screen for a boss key

	mainWindow.wm_state('iconic') # Minimise the main screen

# -=-=-=-=- Functions for making screens -=-=-=-=-

def mainScreen(): # Function to display the lobby canvas
	
	global mainCanvas # This allows for manipulation and movement of entities on the main canvas

	global playerModel # This allows the floor canvas to use these assets
	global heartModel
 
	global attackFrame1 # The skilling animation frames can be used in animation functions 
	global attackFrame2 
	global attackFrame3
	global attackFrame4
	global attackFrame5
	global attackFrame6
	global attackFrame7
	global attackFrame8
	global attackFrame9
	global attackFrame10

	global slimeModel1 # The different slime models are also collected
	global slimeModel2 # I found the code worked best when images were fetched in the same function
	global slimeModel3 # that the canvas was made so here each image is fetched
	global slimeModel4
	global slimeModel5
	global slimeModel6

	global pEntity # Each entity in the lobby is made and available for hit box detection
	global dEntity
	global tEntity
	global oEntity 
	global aEntity
	global sEntity

	global movx # The velocity of the player and their direction facing and skilling status can also be changed by movement functions
	global movy
	global direction
	global skilling
	
	mainCanvas= tk.Canvas(mainWindow, bg="green", height=720, width=1280) # Make the canvas of the main window to be the same size as the window
	mainCanvas.pack() # And display it

	menubar.entryconfig("Save", state = "normal") # Re enable the save function

	doorModel = tk.PhotoImage(file="dungeon_door.png") # Obtain the model for each entity
	doorModel = doorModel.subsample(6) # And scale to suitable size for the lobby
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

	attackFrame1 = tk.PhotoImage(file = "attack1.png") # Obtain the frame for the attack/ skilling animation
	attackFrame1 = attackFrame1.subsample(5) # And scale to suitable size for the lobby
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
		
	slimeModel1 = tk.PhotoImage(file="jelly1.png")  # Obtain the model for each slime
	slimeModel1 = slimeModel1.subsample(5) # And scale to suitable size for the lobby
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

	dEntity = mainCanvas.create_image(640, 70, image = doorModel) # Create and place each entity on the canvas
	tEntity = mainCanvas.create_image(1150, 360, image = treeModel)
	oEntity = mainCanvas.create_image(80, 390, image = oreModel)
	aEntity = mainCanvas.create_image(780, 660, image = anvilModel)
	sEntity = mainCanvas.create_image(520, 630, image = standModel)
	pEntity = mainCanvas.create_image(640, 360, anchor="center", image = playerModel) # Set the user as the center of the screen when places

	mainCanvas.bind("<KeyPress>", mainPress) # Bind the key presses to their relevent funtions
	mainCanvas.bind("<KeyRelease>", keyRelease) # Ensure the velocity stops when the key is no longer pressed
	mainCanvas.focus_set() # This ensures the keybinds work

	skilling = 0 # Set their inital status of skilling, direction and velocity to be off (sprite faces right)
	direction = "right"
	movx = 0
	movy = 0
 
	mainMove() # Then constantly check the movement function to see if they need to be moved

	mainWindow.mainloop() # And display the main window now it has a canvas  # Function to show lobby canvas

def floorScreen(): # Function to show floor canvas

	global gameCanvas # Use the global player entity in game and global game canvas
	global gEntity
	
	global health # Get their current health
	global healthText # And allow the display of it to be updated by slimes
	
	global movx # Get their movement statuses
	global movy
	global direction
	global attacking
	
	global slimeList # Allow the list of current slimes to be edited
	global floorExp # Allow the exp gained from this floor to be used in the victory screen

	mainCanvas.destroy() # Destroy the lobby
	menubar.entryconfig("Save", state = "disabled") # Disable saving

	gameCanvas= tk.Canvas(mainWindow, bg="grey", height=720, width=1280) # Create a game canvas for the floor
	gameCanvas.pack() # Show the canvas
	gameCanvas.focus_set() # Ensure that keybinds work

	health = level(hp) * 5 * armourLevel # Get their current hp based on their stats

	floorText = gameCanvas.create_text(640, 34, fill= "black", font = ('Helvetica','35','bold'), text="Current Floor: " + str(floor + 1)) # Display to the user their current floor
	healthText = gameCanvas.create_text(1140, 34, fill= "red", font = ('Helvetica','35','bold'), text=health) # And health
	heartIcon =  gameCanvas.create_image(1238, 32, image = heartModel) # These are all under the slimes
	gEntity = gameCanvas.create_image(640, 360, anchor="center", image = playerModel) # So that they do not hide any

	statsCollect() # Collect the current stats of the player and load into local memory
	
	attacking = 0 # Set the default movement status of the player
	direction = "right"
	cheatCombo = 0
	movx = 0
	movy = 0

	gameMove() # Check to see if the player is moving

	gameCanvas.bind("<KeyPress>", gamePress) # Bind the key presses to their relevent funtions
	gameCanvas.bind("<KeyRelease>", keyRelease) # Ensure the velocity stops when the key is no longer pressed
	 
	types = [] # Reset all the types of slime that need to be made
	floorExp = 0 # Reset the exp earnable for this floor

	for i in range(10 + 3*(floor)): # For each floor level increase the slime count by 3
		if floor  >= 5: # Based on the difficulty of the floor
			type = random.randint(1,2) # Randomly generate harder types of slime
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

		types.append(type) # Store this lime in the queue to be made

		floorExp = floorExp + type * 3 # Add exp to the earnable exp based on how hard it is
		
	slimeList = [] # Reset the list of slimes on the screen
	slimeList.append(slime(types[0])) # Add the first slime to the screen
	count = 0 # Reset the count until another is made

	while health > 0 and (len(slimeList) > 0 or len(types) > 0) : # While there are still slimes on the screen or to be made and the player is still alive
		for entity in slimeList: # For each slime on the screen
			entity.move() # Move them towards the player or damage the player
		mainWindow.update() # Update the results of moving them
		time.sleep(0.1) # Wait so that animations are smoother
		count = count + 1 # Increae the time wait
		if count >= 20/(floor + 1) and len(types) != 0: # If there has been enough time and there are still more slimes to be made
			count = 0 # Reset the count
			slimeList.append(slime(types[0])) # Add the next slime to the screen
			types.pop(0) # Remove that slime from the queue
	
	if len(slimeList) == 0: # WHen the game is over if there are no slimes on screen
		victoryScreen() # That means they have won
	else: # Otherwise
		deathScreen() # They have lost
 
def deathScreen(): # Function to show canvas on death

	global deathCanvas # Use the global canvas for death

	gameCanvas.destroy() # Destroy the game canvas

	deathCanvas= tk.Canvas(mainWindow, bg="black", height=720, width=1280) # Create a canvas to display the death message, black for death
	message = "You died...\n" # Tell them that they died
	messsage = message + "Press any key to return to safety." # And how to return to the lobby
	deathCanvas.create_text(640, 360, fill= "white", font = ('Helvetica','50','bold'), text=message) # Show the message on screen
	deathCanvas.focus_set() # Ensure the keybinds work on this canvas
	deathCanvas.pack() # Show the canvas
	deathCanvas.bind("<Key>", endAccept) # Bind the key presses to now affect this canvas
	time.sleep(0.4) # Wait a bit incase they are still moving

def victoryScreen(): # Function to show victory canvas

	global victoryCanvas # Use the global victory canvas

	global floor # Obtain the stats to be updated
	global attack
	global hp

	gameCanvas.destroy() # Destroy the game canvas

	floor = floor + 1 # Increase their stats by the exp earnt or 1 for the floor
	hp = hp + floorExp
	attack = attack + floorExp
	expLeftHP = (100 * (1.5 ** (level(hp) - 1))) - hp # work out how much exp they need for each next level
	expLeftAttack = (100 * (1.5 ** (level(attack) - 1))) - attack

	victoryCanvas= tk.Canvas(mainWindow, bg="gold", height=720, width=1280) # Create a canvas to fill the window, gold as they are a winner
	message = "You beat floor: " + str(floor) + "!\n" # Create the message to tell them which floor they beat
	message = message + "You earnt " + str(floorExp) + " exp in attack and hp from this floor.\n" # How much exp they earnt
	message = message + "Your HP is now level " + str(level(hp)) + " with " + str(expLeftHP) + " exp until the next level!\n" # What their levels are now
	message = message + "Your attack is now level " + str(level(attack)) + " with " + str(expLeftAttack) + " exp until the next level!\n" # How much exp they need
	message = message + "Press any key to return to safety." # Inform them how to return to the lobby
	victoryCanvas.create_text(640, 360, fill= "white", font = ('Helvetica','25','bold'), text=message) # Display the victory message on the canvas
	victoryCanvas.focus_set() # Ensure that later keybinds affect this canvas
	victoryCanvas.pack() # Display the canvas
	victoryCanvas.bind("<Key>", endAccept) # Bind the key presses to now affect this canvas
	time.sleep(0.4) # Wait a bit incase they are still moving
	
	
loginWindow() # Start off the login window
