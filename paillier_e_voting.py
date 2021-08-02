import binascii
import itertools
import random
import string
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3
from random import randint
import libnum

conn = sqlite3.connect('e_voting_user_data.db')
c = conn.cursor()

def registerVoter():
    #Get username and password from form
    usernameForm = (e1.get())
    passwordForm = (e2.get())
    unique = True

    #Check database if username already exists
    for value in c.execute('SELECT username FROM users'):
        username = value[0]
        if username == usernameForm:
            print('Username already exists')
            tk.Label(adminWindow,text='Username already exists',foreground='red').grid(row=13,column=0,columnspan=2,padx=10,sticky=tk.W)
            unique = False
            break

    #If username unique, add username and hashed password to database
    if unique == True:
        letters = string.ascii_letters
        h = hashlib.md5(passwordForm.encode())
        passwordHash = h.hexdigest()
        c.execute("INSERT INTO users (userName, password) VALUES (?, ?)",
        (usernameForm, passwordHash))
        conn.commit()
        tk.Label(adminWindow,text='Voter added successfuly!',foreground='green').grid(row=13,column=0,columnspan=2,padx=10,sticky=tk.W)
        print('Voter added successfully!')
        
def changeAdminPassword():
    #Get password from form and update database
    passwordForm = (e5.get())
    h = hashlib.md5(passwordForm.encode())
    passwordHash = h.hexdigest()
    c.execute("UPDATE admin SET password =? WHERE userName = 'Admin'", (passwordHash,))
    conn.commit()
    print ('Password updated successfully!')
    tk.Label(changePasswordWindow, text='Password updated',foreground='green').grid(row=5,column=0,padx=10,sticky=tk.W)

def exitChangePasswordWindow():
    #Close changePasswordWindow and open adminWindow
    changePasswordWindow.withdraw()
    adminWindow.deiconify()
    
def changeAdminPasswordScreen():
    #Close adminWindow
    adminWindow.withdraw()
    global changePasswordWindow
    changePasswordWindow = tk.Tk()
    changePasswordWindow.title('e-voting: change password')
    changePasswordWindow.geometry('360x140')
    
    tk.Label(changePasswordWindow,foreground='black',font=1,height=1,padx=8,pady=15, 
         text="Password").grid(row=0,sticky=tk.W)
    
    global e5
    e5 = tk.Entry(changePasswordWindow,fg='black',bg='yellow',width=20,font=1)
    e5.grid(row=0, column=1)
    
    tk.Button(changePasswordWindow, 
          text='Update',font=1,width=8,bg='red',fg='yellow', 
          activebackground = "red",command=changeAdminPassword).grid(row=4, 
                                    column=0, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(changePasswordWindow, 
          text='Return',font=1,width=8,bg='red',fg='yellow', 
          activebackground = "red",command=exitChangePasswordWindow).grid(row=4, 
                                    column=1, 
                                    sticky=tk.E,
                                    padx=0,
                                    pady=5)
    
def exitAdminWindow():
    #Close adminWindow and open home window
    master.deiconify()
    adminWindow.withdraw()
    e3.delete(0, 'end')
    e4.delete(0, 'end')
    print('Exited admin window')
    
def admin():
    #Create adminWindow
    global adminWindow
    adminWindow = tk.Tk()
    adminWindow.title('e-voting admin')
    adminWindow.geometry('400x380')
    
    tk.Label(adminWindow,foreground='black',font=1,height=1,padx=8,pady=15, 
         text="Username").grid(row=0,column=0,sticky=tk.W)
    tk.Label(adminWindow,foreground='black',font=1,height=1,padx=8,pady=10,anchor='w', 
         text="Password").grid(row=1,column=0,sticky=tk.W)

    global e1
    global e2

    e1 = tk.Entry(adminWindow,fg='black',bg='yellow',width=25,font=1)
    e2 = tk.Entry(adminWindow,fg='black',bg='yellow',width=25,font=1)


    e1.grid(row=0,column=1,columnspan=1,padx=0,sticky=tk.W)
    e2.grid(row=1,column=1,columnspan=1,padx=0,sticky=tk.W)


    tk.Button(adminWindow, 
          text='Register Voter',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=registerVoter).grid(row=4, 
                                    column=0,
                                    columnspan=2,
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(adminWindow, 
          text='Change password',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=changeAdminPasswordScreen).grid(row=4, 
                                    column=1, 
                                    sticky=tk.E,
                                    padx=0,
                                    pady=5)

    tk.Button(adminWindow, 
          text='Tally Votes',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=tallyVotes).grid(row=5, 
                                    column=0,
                                    columnspan=2,
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(adminWindow, 
          text='Home',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=exitAdminWindow).grid(row=5, 
                                    column=1, 
                                    sticky=tk.E,
                                    padx=0,
                                    pady=5)

def submitVote():
    def gcd(a,b):
        while b > 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return a * b // gcd(a, b)

    #Select two prime numbers
    p = 293
    q = 433

    #Calculate n and gLambda
    gLambda = lcm(p-1,q-1)
    n = p*q

    #Randomly select g
    g = 2

    #Calculate modular multiplicative inverse
    l = (pow(g, gLambda, n*n)-1)//n
    gMu = libnum.invmod(l, n)

    eligible = True
    successful = True

    for value in c.execute('SELECT userName FROM encryptedVotes'):
        eligibleUsername = value[0]
        if username == eligibleUsername:
            print('You have already voted')
            tk.Label(window,text='You have already voted.',foreground='red').grid(row=8,column=0,columnspan=2,padx=10,sticky=tk.W)
            eligible = False
            break

    if eligible == True:
        vote = (options1.get())
        if vote == 'Bob':
            eVote = 1
        elif vote == 'Alice':
            eVote = 10
        elif vote == 'Eve':
            eVote = 100
        elif vote == 'Sam':
            eVote = 1000
        else:
            print('Vote fail')
            tk.Label(window,text='Select a candidate.',foreground='red').grid(row=8,column=0,columnspan=2,padx=10,sticky=tk.W)
            successful = False

        if successful == True:
            r1 = random.randint(100,1000)
            c1part1 = pow(g,eVote,n*n)
            c1part2 = pow(r1,n,n*n)
            c1 = (c1part1 * c1part2) % (n*n)

            c.execute("INSERT INTO encryptedVotes (userName, encryptedVote) VALUES (?, ?)",
            (username, c1))
            conn.commit()
            tk.Label(window,text='Vote added to the database.',foreground='green').grid(row=8,column=0,columnspan=2,padx=10,sticky=tk.W)
            print('Vote added to the database')
            
def tallyVotes():
    print('Tallying votes...')
    def gcd(a,b):
        while b > 0:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return a * b // gcd(a, b)

    #Select two prime numbers
    p = 293
    q = 433

    #Calculate n and gLambda
    gLambda = lcm(p-1,q-1)
    n = p*q

    #Randomly select g
    g = 2

    #Calculate modular multiplicative inverse
    l = (pow(g, gLambda, n*n)-1)//n
    gMu = libnum.invmod(l, n)

    numberVotes = 0
    batchCalculator = 0
    numberOfBatches = 1
    total = 1
    i = 0
      
    for row in c.execute('SELECT encryptedVote FROM encryptedVotes'):
        numberVotes += 1
    print('Number of votes: ' + str(numberVotes))

    for row in c.execute('SELECT encryptedVote FROM encryptedVotes'):
        batchCalculator  += 1
        if batchCalculator == 9:
            numberOfBatches += 1
            batchCalculator = 0

    print ('Number of batches: ' + str(numberOfBatches))

    bob = 0
    alice = 0
    eve = 0
    sam = 0

    end = False
    countBatch = 1
    
    for value in c.execute('SELECT encryptedVote FROM encryptedVotes'):
        if end == True:
            print ('Adding leftover votes to previous batch...')
            leftOvers = batchCalculator
            print ('Number of leftover votes: ' + str(leftOvers))
            i += 1
            total = total * value[0]
            print('Leftover vote ' + str(i) + ': ' + str(value[0]))

            if i >= batchCalculator:
                #Tally encrypted votes
                cd = (total) % (n*n)

                #Decrypt
                L = (pow(cd,gLambda,n*n)-1) // n
                m = (L*gMu) % n
                result = str(m)

                print(result)

                if m <= 9:
                    bob += int(result[0])
                elif m >= 10 and m < 99:
                    bob += int(result[1])
                    alice += int(result[0])
                elif m >= 100 and m < 999:
                    bob += int(result[2])
                    alice += int(result[1])
                    eve += int(result[0])
                else:
                    bob += int(result[3])
                    alice += int(result[2])
                    eve += int(result[1])
                    sam += int(result[0])

        elif numberVotes < 9:
                i += 1
                total = total * value[0]
                print('Total: ' + str(total))
                print('Encrypted vote ' + str(i) + ': ' + str(value[0]))

                if i >= numberVotes:
                    #Tally encrypted votes
                    cd = (total) % (n*n)

                    #Decrypt
                    L = (pow(cd,gLambda,n*n)-1) // n
                    m = (L*gMu) % n
                    result = str(m)

                    print(result)

                    if m <= 9:
                        bob += int(result[0])
                    elif m >= 10 and m < 99:
                        bob += int(result[1])
                        alice += int(result[0])
                    elif m >= 100 and m < 999:
                        bob += int(result[2])
                        alice += int(result[1])
                        eve += int(result[0])
                    else:
                        bob += int(result[3])
                        alice += int(result[2])
                        eve += int(result[1])
                        sam += int(result[0])
                       
        else:    
            i += 1
            total = total * value[0]
            print('Total: ' + str(total))
            print('Encrypted vote ' + str(i) + ': ' + str(value[0]))
            if i >= 9:
                print('Completed batch ' + str(countBatch))
                i = 0
                countBatch +=1

                #Tally encrypted votes
                cd = (total) % (n*n)

                #Decrypt
                L = (pow(cd,gLambda,n*n)-1) // n
                m = (L*gMu) % n
                result = str(m)

                print(result)

                if m <= 9:
                    bob += int(result[0])
                elif m >= 10 and m < 99:
                    bob += int(result[1])
                    alice += int(result[0])
                elif m >= 100 and m < 999:
                    bob += int(result[2])
                    alice += int(result[1])
                    eve += int(result[0])
                else:
                    bob += int(result[3])
                    alice += int(result[2])
                    eve += int(result[1])
                    sam += int(result[0])

                total = 1

                if countBatch == numberOfBatches:
                    end = True

    print ('Bob: ' + str(bob))
    print ('Alice: ' + str(alice))
    print ('Eve: ' + str(eve))
    print ('Sam: ' + str(sam))

    tk.Label(adminWindow, text='----------------------------------').grid(row=6,column=0,columnspan=2,padx=10,sticky=tk.W)
    tk.Label(adminWindow, text='Tally Results').grid(row=7,column=0,padx=10,columnspan=2,sticky=tk.W)
    tk.Label(adminWindow, text='----------------------------------').grid(row=8,column=0,columnspan=2,padx=10,sticky=tk.W)
    tk.Label(adminWindow, text='Bob: ' + str(bob)).grid(row=9,column=0,padx=10,columnspan=2,sticky=tk.W)
    tk.Label(adminWindow, text='Alice: ' + str(alice)).grid(row=10,column=0,padx=10,columnspan=2,sticky=tk.W)
    tk.Label(adminWindow, text='Eve: ' + str(eve)).grid(row=11,column=0,padx=10,columnspan=2,sticky=tk.W)
    tk.Label(adminWindow, text='Sam: ' + str(sam)).grid(row=12,column=0,padx=10,columnspan=2,sticky=tk.W)

def exitScreen():
    master.deiconify()
    window.withdraw()
    e3.delete(0, 'end')
    e4.delete(0, 'end')
    
def instructions():
    global window
    window = tk.Tk()
    window.title('e-voting terminal')
    window.geometry('360x140')
    tk.Label(window,foreground='black',font=1,height=1,padx=8,pady=15, 
         text="Select a candidate").grid(row=0,columnspan=2,sticky=tk.W)

    global options1
    options1 = tk.StringVar(window)
    options1.set('Select') # default value
    om1 =tk.OptionMenu(window,options1, 'Bob','Alice','Eve','Sam')
    om1.grid(row=1,column=0,padx=10,sticky=tk.W)

    tk.Button(window, 
          text='Vote',font=1,width=5,bg='red',fg='yellow', 
          activebackground = "red",command=submitVote).grid(row=1, 
                                    column=1, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)
    
    tk.Button(window, 
          text='Verify',font=1,width=5,bg='red',fg='yellow', 
          activebackground = "red",command=verifyVote).grid(row=1, 
                                    column=2, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(window, 
          text='Exit',font=1,width=5,bg='red',fg='yellow', 
          activebackground = "red",command=exitScreen).grid(row=1, 
                                    column=3, 
                                    sticky=tk.W,
                                    padx=15,
                                    pady=5)

def login():  
    global username
    username = (e3.get())
    password = (e4.get())

    if username == 'Admin':
        for value in c.execute('SELECT password FROM admin'):
            adminPassword = value[0]
            h = hashlib.md5(password.encode())
            passwordHash = h.hexdigest()
            if adminPassword == passwordHash:
                print ('Login success as Admin')
                master.withdraw()
                admin()
            else:
                tk.Label(master,text='Login failure',foreground='red').grid(row=5,column=0,padx=10,sticky=tk.W)
                print('Login failure')
                e3.delete(0, 'end')
                e4.delete(0, 'end')
    else:    
        for value in c.execute('SELECT username FROM users'):
            storedUsername = value[0]
            if username == storedUsername:
                found = True
                break
            else:
                found = False

        if found == True:
            username1 = (str(username),)
            for value in c.execute('SELECT password FROM users WHERE userName=?', username1):
                pass1 = value[0]
            h = hashlib.md5(password.encode())
            passwordHash = h.hexdigest()
            if pass1 == passwordHash:
                print('Login success as: ' + username)
                master.withdraw()
                instructions()
            else:
                tk.Label(master,text='Login failure :(',foreground='red').grid(row=5,column=0,padx=10,sticky=tk.W)
                print('Login failure')
                e3.delete(0, 'end')
                e4.delete(0, 'end')

def verifyVote():
    verify = tk.Tk()
    verify.title('e-voting: verify vote')
    container = ttk.Frame(verify)
    canvas = tk.Canvas(container)
    scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)

    ttk.Label(scrollable_frame, text='Username').grid(padx=10,column=0,row=0,sticky=tk.W)
    ttk.Label(scrollable_frame, text='Encrypted vote').grid(padx=10,column=1,row=0,sticky=tk.W)
    
    i=1
    for value in c.execute('SELECT * FROM encryptedVotes'):
        i += 1
        ttk.Label(scrollable_frame, text=value[0]).grid(padx=10,column=0,row=i,sticky=tk.W)
        ttk.Label(scrollable_frame, text=value[1]).grid(padx=10,column=1,row=i,sticky=tk.W)

    container.pack()
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
def readMe():
    instruct = tk.Tk()
    instruct.geometry("400x200") 
    instruct.title('e-voting: Instructions')
    T = tk.Text(instruct, height = 100, width = 100) 
    l = tk.Label(instruct, text = "e-voting: Instructions") 
    l.config(font =("Courier", 14)) 
  
    info = """Admin users login with the username 'Admin' and
the default password 'Admin'. After the initial
login, the password should be changed from the
Admin portal. The Admin portal is also used to
add new users to the system and tally votes.
Users vote by logging in and casting their vote
for one of the four candidates. Users can also
click 'validate' to ensure that their vote has
been encrypted whilst at rest."""

    l.pack() 
    T.pack(padx=5,pady=5,side=tk.LEFT)  
  
    T.insert(tk.END, info) 
              
master = tk.Tk()
master.geometry('400x180')
master.title('e-voting')

tk.Label(master,foreground='black',font=1,height=1,padx=8,pady=10,anchor='w', 
         text="Login Username").grid(row=2,sticky=tk.W)
tk.Label(master,foreground='black',font=1,height=1,padx=8,pady=10,anchor='w', 
         text="Login Password").grid(row=3,sticky=tk.W)

e3 = tk.Entry(fg='black',bg='yellow',width=20,font=1)
e4 = tk.Entry(fg='black',bg='yellow',width=20,font=1)

e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

tk.Button(master, 
          text='Login',font=1,width=9,bg='red',fg='yellow', 
          activebackground = "red",command=login).grid(row=4, 
                                    column=0, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

tk.Button(master, 
          text='Instructions',font=1,width=9,bg='red',fg='yellow', 
          activebackground = "red",command=readMe).grid(row=4, 
                                    column=1, 
                                    sticky=tk.E,
                                    padx=0,
                                    pady=5)

tk.mainloop()
