import tkinter as tk
import os
  
def data(line):
	data = ""
	trigger = 0
	for i in range (0, len(line)):
		if trigger == 1:
			data = data + line[i]
		if line[i] == ":":
			trigger = 1

	return(data)

def login():
    usernameFinal= username.get()
    passwordFinal= password.get()
    errorOutput.config(text="")

    if usernameFinal == "" or usernameFinal.isspace():
    	errorOutput.config(text="Username cannot be empty")
    elif passwordFinal == "" or passwordFinal.isspace():
    	errorOutput.config(text="Password cannot be empty")
    elif os.path.exists(os.path.join(os.getcwd(), "accounts", usernameFinal + ".txt")):
    	newFile = open(os.path.join(os.getcwd(), "accounts", usernameFinal + ".txt"), "r")
    	for i, line in enumerate(newFile):
    		if i == 0:
    			usernameFile = data(line)
    		elif i == 1:
    			passwordFile = data(line)
    		elif i > 1:
    			break

    	newFile.close()

    	if usernameFile != usernameFinal + "\n":
    		errorOutput.config(text="Username is incorrect")
    	elif passwordFile != passwordFinal + "\n":
    		errorOutput.config(text="Password is incorrect")
    	else:
    		errorOutput.config(text="Welcome Adventurer!")



    else:
    	errorOutput.config(text="Username does not exist")
    	
def create():
	usernameFinal= username.get()
	passwordFinal= password.get()
	errorOutput.config(text="")

	if os.path.isdir("accounts") == False:
		os.mkdir("accounts")
	
	if usernameFinal == "" or usernameFinal.isspace():
		errorOutput.config(text="Username cannot be empty")
	elif passwordFinal == "" or passwordFinal.isspace():
		errorOutput.config(text="Password cannot be empty")
	elif os.path.exists(os.path.join(os.getcwd(), "accounts", usernameFinal + ".txt")):
		errorOutput.config(text="Account Already Exists")
	else:
		newFile = open(os.path.join(os.getcwd(), "accounts", usernameFinal + ".txt"), "w")
		newFile.write("Username:"+ usernameFinal + "\n")
		newFile.write("Password:"+ passwordFinal + "\n")
		newFile.close()
		errorOutput.config(text="Account Successfully Created!")
		
loginWindow= tk.Tk()
loginWindow.geometry("600x600")
loginWindow.title("RunEscape Login")
loginWindow.resizable(0, 0)
  
username= tk.StringVar()
password= tk.StringVar()

nameLabel= tk.Label(loginWindow, text = "Username:")
nameFetch= tk.Entry(loginWindow,textvariable = username)

passwordLabel= tk.Label(loginWindow, text = "Password:")
passwordFetch= tk.Entry(loginWindow, textvariable = password, show = '*')
 
loginButton= tk.Button(loginWindow,text = "Submit", command = login)
accountButton= tk.Button(loginWindow,text = "Create Account", command = create)

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