import tkinter as tk
  

def login():
    usernameFinal= username.get()
    passwordFinal= password.get()

def create():
	pass
     
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
 
loginButton= tk.Button(loginWindow,text = 'Submit', command = login)
accountButton= tk.Button(loginWindow,text = 'Create Account', command = create)
  
nameLabel.grid(row=1,column=1)
nameFetch.grid(row=1,column=2)
passwordLabel.grid(row=2,column=1)
passwordFetch.grid(row=2,column=2)
loginButton.grid(row=4,column=2)
accountButton.grid(row=5,column=2)

loginWindow.grid_rowconfigure(0, weight=1)
loginWindow.grid_rowconfigure(6, weight=1)
loginWindow.grid_columnconfigure(0, weight=1)
loginWindow.grid_columnconfigure(3, weight=1)
  
loginWindow.mainloop()