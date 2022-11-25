#imports
import socket
import threading
from tkinter import* 
import tkinter as tk 
import tkinter.font as font 
from tkinter import messagebox 
import sys
from PIL import ImageTk,Image
from plyer import notification
import os
from urllib.request import Request, urlopen
from random import randint
from playsound import playsound
import Packages.passwordHasher as passwordHasher
import Packages.login as ringerLogin
import re
import time
import customtkinter
from customtkinter import *


global serverIp #global variable for the server ip
serverIp ="127.0.0.1" 

global recoveryIp #ip address for the recovery server. Recovery server responsible for the "forget password" functionality 
recoveryIp = "127.0.0.1" 

print("import complete")
print(sys.executable)

global infoCheck
infoCheck = 0

global Online
Online = False

global audioPlayed # ensures that the audio for ringer startup is only played once 
audioPlayed = False

global ringerVersion 
ringerVersion = "SNAPSHOT-3.0"

global createAccountOpen
createAccountOpen = False


def welcomeWindow(): #this window is triggered when ringer is installed for the first time
    global audioPlayed
    if audioPlayed == False:
        playsound('Sounds/Ringer Startup.wav')
        audioPlayed = True

    welcome = Tk()
    welcome.config(background='#202225', pady=20, padx=30)
    welcome.title('Welcome To Ringer!')
    welcome.iconbitmap("Icons/Ringer-Icon.ico")
    #welcome.eval('tk::PlaceWindow . top')
    welcome.geometry("500x700")
    welcome.wm_resizable(False, False)
    myFont = font.Font(family='Arial', weight=font.BOLD)

    def selectScreen():
        welcomeLabel.destroy()
        getStarted.destroy()
        logo.destroy()

        def ringerlogin():
            ringerLabel.destroy()
            login.destroy()
            createAccount.destroy()

            def enterPassword(): 
                password.delete('0', 'end')
                password.config(show="*")

            def Connect():
                welcome.destroy()
                os.remove("First-Time-Use.txt")
                playsound("Sounds/Ringer Welcome Login.wav")
                

            ringerLogin = Label(welcome, text="Login To Your Lif Account.", font=myFont, bg='#202225', fg='white')
            ringerLogin.pack()

            user = Entry(welcome, width = 50, borderwidth = '0', bg = 'white', fg = 'black') 
            user.pack(side=TOP, pady= 50, padx=20) 
            if os.path.isdir(os.path.expanduser('~') + "/AppData/Roaming/RingerLoginData"):
                if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
                    f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt", "r")
                    user.insert(0, f.read())
                    f.close()
                else:
                    user.insert(0, 'username')
                    user.bind("<FocusIn>", lambda args: user.delete('0', 'end')) 
            else: 
                os.mkdir(os.path.expanduser('~') + "/AppData/Roaming/RingerLoginData")

            password = Entry(welcome, width = 50, borderwidth = '0', bg = 'white', fg = 'black') 
            password.pack(side=TOP, padx=20) 
            if os.path.isdir(os.path.expanduser('~') + "/AppData/Roaming/RingerLoginData"):
                if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
                    f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt", "r")
                    password.config(show="*")
                    password.insert(0, f.read())
                    f.close()
                else:
                    password.insert(0, 'password')
                    password.bind("<FocusIn>", (lambda event: enterPassword()))
            else:
                os.mkdir(os.path.expanduser('~') + "/AppData/Roaming/RingerLoginData")

            def Getnick(): #gets the login credentials and sends them to the server
                global nickname
                global display
                nickname = f"{user.get()}{password.get()}"
                print(nickname)
                display = user.get() 
                print(display) 
                SubmitNick.config(state=DISABLED)

                if not os.path.isdir(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData"):
                    os.mkdir(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData")
                
                if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
                    os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt")
                f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt", "a")
                f.write(user.get())
                f.close()
                if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
                    os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt")
                f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt", "a")
                f.write(password.get())
                f.close()

                Connect()

            SubmitNick = Button(welcome, bg='white', text='Login', borderwidth='0',command=Getnick)  
            SubmitNick.pack(pady='20')
            
        def CreateAccount():
            ringerLabel.destroy()
            login.destroy()
            createAccount.destroy()

            def enterPassword2(): 
                passwordinput.delete('0', 'end')
                passwordinput.config(show="*")

            def sendAccount(): #sends account to server
                def sendAccount2():
                    def diveIn():
                        ringerLabel.destroy()
                        ringerAccount.destroy()
                        createAccount.destroy()
                        username.destroy()
                        passwordinput.destroy()
                        emailInput.destroy()
                        submitAccount.destroy()

                        os.remove("First-Time-Use.txt")

                        def close():
                            welcome.destroy()
                            playsound("Ringer Welcome Login.wav")

                        DiveIn = Label(welcome, text="Account Created! Lets Go!", font=myFont, bg='#202225', fg='white')
                        DiveIn.pack()

                        getStarted = Button(welcome, image=myImage2, command=close, bg='#202225', fg='white', borderwidth=0, activebackground='#202225')
                        getStarted.pack()
                    try:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((serverIp, 20200)) 
                        client.send("CREATEACCOUNT".encode('ascii'))
                    except:
                        messagebox.showerror("Error", "Could not connect to server!")
                        createAccount.destroy()
                    while True:
                        Message = client.recv(1024).decode('ascii')
                        if Message == 'ACCOUNTCREATED':
                            if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
                                os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt")
                            f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt", "a")
                            f.write(username.get())
                            f.close()
                            if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
                                os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt")
                            f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt", "a")
                            f.write(passwordinput.get())
                            f.close()
                            diveIn()
                            break
                        if Message == 'USERNAME?':
                            client.send(username.get().encode('ascii'))
                            print('sent username')

                        if Message == 'PASSWORD?':
                            password = passwordinput.get()
                            print('got password')
                            
                            client.send(passwordHasher.get_initial_hash(password).encode('ascii')) 
                            print('sent password')

                        if Message == 'EMAIL?':
                            client.send(checkEmail.encode('ascii'))
                            print('sent email')

                        if Message == 'CREDENTIALS?':
                            credentials = username.get() + passwordinput.get()
                            client.send(credentials.encode('ascii'))

                        if Message == 'ERROR_ACOUNT_EXSISTING':
                            print(Message)
                            client.close()
                            messagebox.showerror("Opps!", "Account already exists!")
                            break

                checkEmail = emailInput.get()

                pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
                if re.match(pat,checkEmail):
                    messagebox.showerror("Error", "Provided Email is Invalid!")
                    return True
                else:
                    sendAccount2()

            ringerAccount = Label(welcome, text="Lets Create Your Lif Account.", font=myFont, bg='#202225', fg='white')
            ringerAccount.pack()

            username = Entry(welcome, width='50', borderwidth='0')
            username.pack(pady='10', padx='5')
            username.insert(0, 'username')
            username.bind("<FocusIn>", lambda args: username.delete('0', 'end'))    

            emailInput = Entry(welcome, width='50', borderwidth='0')
            emailInput.pack(pady='10', padx='5')
            emailInput.insert(0, 'Email')
            emailInput.bind("<FocusIn>", lambda args: emailInput.delete('0', 'end'))    

            passwordinput = Entry(welcome, width='50', borderwidth='0')
            passwordinput.pack(padx='5', pady=10)
            passwordinput.insert(0, 'password')
            passwordinput.bind("<FocusIn>", (lambda event: enterPassword2()))

            submitAccount = Button(welcome, borderwidth='0', text='Create', command=sendAccount, bg='white')
            submitAccount.pack(pady='10')

        ringerLabel = Label(welcome, text="Do you Have A Lif Account?", font=myFont, bg='#202225', fg='white')
        ringerLabel.pack()

        login = Button(welcome, text="Yes, Log Me In!", bg='orange', fg='white', font=myFont, borderwidth="0", command=ringerlogin)
        login.pack(pady=100)

        createAccount = Button(welcome, text="No, Create One.", bg='orange', fg='white', font=myFont, borderwidth="0", command=CreateAccount)
        createAccount.pack()

        

    def on_closing():
        welcome.destroy()
        sys.exit()

    myImage = ImageTk.PhotoImage(Image.open('Images/Ringer-Bot.png'))

    logo = Label(welcome, image=myImage, bg='#202225')
    logo.pack()

    welcomeLabel = Label(welcome, bg='#202225', fg='white', text='Welcome to Ringer', font=myFont)
    welcomeLabel.pack()

    myImage2 = ImageTk.PhotoImage(Image.open('Images/lets go.png'))

    getStarted = Button(welcome, image=myImage2, command=selectScreen, bg='#202225', fg='white', borderwidth=0, activebackground='#202225')
    getStarted.pack()

    welcome.protocol("WM_DELETE_WINDOW", on_closing)
    welcome.mainloop()

if os.path.isfile("First-Time-Use.txt"):
    welcomeWindow()

def LOGIN():
    login = CTk()  
    login.focus()
    global attempts
    attempts = 0
    global audioPlayed

    if audioPlayed == False:
        #playsound("Sounds/Ringer Startup.wav")
        audioPlayed = True

    def resetAccount():
        reset = Toplevel()
        reset.geometry("500x500")
        reset.config(background='#1e1e1e')
        reset.resizable(False,False)
        reset.title("Reset Your Account")
        reset.iconbitmap("Icons/Ringer-Icon.ico")

        resetLabel = Label(reset, bg='#1e1e1e', text='Please Enter Your Username And Email', fg='white', font="Arial 15 bold")
        resetLabel.pack()

        username = Entry(reset, width='50', borderwidth='0')
        username.pack(pady='10', padx='5')
        username.insert(0, 'Username')
        username.bind("<FocusIn>", lambda args: username.delete('0', 'end'))    

        emailInput = Entry(reset, width='50', borderwidth='0')
        emailInput.pack(pady='10', padx='5')
        emailInput.insert(0, 'Email')
        emailInput.bind("<FocusIn>", lambda args: emailInput.delete('0', 'end'))    

        def verify():
            sendCode = False
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((recoveryIp, 20203)) 
                print("connected to recovery server")
                while True:
                    Message = client.recv(1024).decode('ascii')
                    print(Message)

                    if Message == 'EMAIL':
                        client.send(emailInput.get().encode('ascii'))
                        print('lif login')
                    
                    if Message == 'USERNAME':
                        client.send(username.get().encode('ascii'))
                        print('lif login')

                    if Message == 'SEND_CODE':
                        sendCode = True
                        break

                    if Message == "BAD_LOGIN_ERROR":
                        messagebox.showerror('Error', 'Username or Email is incorrect')
                        break

            except Exception as e:
                print(e)

            if sendCode == True:
                resetLabel.destroy()
                emailInput.destroy()
                username.destroy()
                submit.destroy()

                verify2 = Label(reset, text="Verify Its You", font=myFont, bg='#1e1e1e', fg='white')
                verify2.pack()
                verify3 = Label(reset, text="We sent a code to your inbox. Enter the code below.", bg='#1e1e1e', fg='white')
                verify3.pack()

                codeEntry = Entry(reset, width='50', borderwidth='0')
                codeEntry.pack(pady='10', padx='5')
                codeEntry.insert(0, 'Code')
                codeEntry.bind("<FocusIn>", lambda args: codeEntry.delete('0', 'end'))  

                global codeGood
                codeGood = False

                def sendCode2Server():
                    global codeGood
                    client.send("SENDING...".encode('ascii'))
                    client.send(codeEntry.get().encode('ascii'))
                    while True:
                        Message = client.recv(1024).decode('ascii')
                        if Message == "SEND_NEW_PASSWORD":
                            codeGood = True
                            break
                        if Message == "CODE_ERROR":
                            messagebox.showerror('Bad Code', 'The code you provided is incorrect. Double check your email.')
                            break

                    if codeGood == True:
                        verify2.destroy()
                        verify3.destroy()
                        codeEntry.destroy()
                        submitCode.destroy()

                        codeLabel = Label(reset, bg='#1e1e1e', text="Enter New Password", font=myFont, fg='white')
                        codeLabel.pack()
                        subCodeLabel = Label(reset, bg='#1e1e1e', text="Make it unique.", fg='white')
                        subCodeLabel.pack()

                        passwordEntry = Entry(reset, width='50', borderwidth='0')
                        passwordEntry.pack(pady='10', padx='5')
                        passwordEntry.insert(0, 'Password')
                        passwordEntry.bind("<FocusIn>", lambda args: passwordEntry.delete('0', 'end'))  

                        def sendPassword():
                            global resetSuccess
                            resetSuccess = False
                            client.send("SENDING...".encode('ascii'))
                            password = passwordEntry.get()
                           
                            client.send(passwordHasher.get_initial_hash(password).encode('ascii')) 
                            
                            while True:
                                resetStatus = client.recv(1024).decode('ascii')
                                if resetStatus == "RESET_SUCCESS":
                                    resetSuccess = True
                                    break

                            if resetSuccess == True:
                                codeLabel.destroy()
                                subCodeLabel.destroy()
                                passwordEntry.destroy()
                                subCodeLabel.destroy()
                                submitPassword.destroy()

                                successLabel = Label(reset, text="Password Reset!", font=myFont, bg='#1e1e1e', fg='white')
                                successLabel.pack()
                                subSuccessLabel = Label(reset, text="Try to remember your password this time!", bg='#1e1e1e', fg='white')
                                subSuccessLabel.pack()

                                def gotIt():
                                    reset.destroy()
                                    SubmitNick.config(command=Getnick, text="Login")
                                    
                                successButton = Button(reset, text="Got It!✅", borderwidth=0, command=gotIt)
                                successButton.pack(pady=10)
                
                        submitPassword = Button(reset, text="Submit", borderwidth=0, command=sendPassword)
                        submitPassword.pack()


                submitCode = Button(reset, text='Submit', command=sendCode2Server, borderwidth=0)
                submitCode.pack(pady='10', padx='5')

        submit = Button(reset, text="Ok", borderwidth=0, command=verify)
        submit.pack(pady='10', padx='5')

        #reset.protocol("WM_DELETE_WINDOW", on_closing) 
        
    def Connect(): #handles connecting and logging into the server
        global client
        global attempts
        print("connecting...")
        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((serverIp, 20200)) 
            loginStatus = ringerLogin.login(username=nickname, password=passwrd, client=client)

            if loginStatus == "Success":
                print("login Successful")
                SubmitNick.configure(text="Success ✔️")
                #playsound("Sounds/Ringer Welcome Login.wav")
                login.destroy()

            if loginStatus == "Bad_Login":
                 messagebox.showerror('Error', 'Username or password is incorrect.')
                 SubmitNick.configure(state=NORMAL)

            if loginStatus == "Banned":
                messagebox.showerror("BANNED!", "You Have Been Banned From The Ringer Service")
                SubmitNick.configure(state=NORMAL)

        except Exception as e:
            messagebox.showerror("ERROR!", "Failed to connect to server!")
            print(e)
            SubmitNick.config(state=NORMAL)

    bg = PhotoImage(file="Images/login_bg.png")

    c = Canvas(login, width=100, height=10, borderwidth=0)
    c.pack(expand=True, fill=BOTH)

    c.create_image(0,0, image=bg, anchor="nw")

    login.configure(background="blue") 
    login.geometry("1000x600")   
    StartFont = font.Font(family='monospace', weight=font.BOLD, size=30)
    login.title('Ringer | Login')
    login.iconbitmap("Icons/Ringer-Icon.ico")
    #login.config(pady=90)

    global recviveMessage
    recviveMessage = True

    global writeMessage
    writeMessage = False

    global focus_check
    focus_check = True


    def statusBar():
        statusbar = Label(login, bg='white', text="Connecting...", width='111', fg='black')
        statusbar.pack(side=TOP, fill=X)

        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((serverIp, 20200))
                receive = client.recv(1024).decode('ascii')

                if receive == "LOGIN":
                    client.close()
                    statusbar.config(bg='green', text="✔️ Connected to Ringer Service", fg='white')
            except:
                statusbar.config(bg='red', text='❌ Unable to Connect to Ringer Service', fg='white')
                
            time.sleep(3)
            print("status updated")



    def CreateAccount(): #deals with creating accounts
        createAccount = Toplevel()
        createAccount.geometry("500x400")
        createAccount.configure(background="#202020")
        createAccount.iconbitmap("Icons/Ringer-Icon.ico")
        createAccount.title('Ringer | Create Account')
        createAccount.resizable(False, False)
        

        def enterPassword2(): 
            passwordinput.delete('0', 'end')
            passwordinput.config(show="*")

        def gererateUser(): #generates a random username
            messagebox.showerror("Feature Removed!", "Due to issues with this feature it has been removed and will return in a future update.")
            createAccount.focus()
            '''
            url="https://svnweb.freebsd.org/csrg/share/dict/words?revision=61569&view=co"
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

            web_byte = urlopen(req).read()

            webpage = web_byte.decode('utf-8')
            words = webpage.split()

            random_number = randint(0, len(words))
            username.delete('0', 'end')
            username.insert(0, randint(100, 999))
            username.insert(0, words[random_number])
            '''

        def sendAccount(): #sends account to server
            def sendAccount2():
                try:
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((serverIp, 20200)) 
                    print('conected')
                    client.send("CREATEACCOUNT".encode('ascii'))
                    print('requested account creation')
                except:
                    messagebox.showerror("Error", "Could not connect to server!")
                    createAccount.destroy()
                while True:
                    Message = client.recv(1024).decode('ascii')
                    if Message == 'ACCOUNTCREATED':
                        messagebox.showinfo("Success!", "Account successfully created!")
                        createAccount.destroy()
                        break

                    if Message == 'USERNAME?':
                        client.send(username.get().encode('ascii'))
                        print('sent username')

                    if Message == 'PASSWORD?':
                        password = passwordinput.get()
                        print('got password')
                        # adding 5gz as password
                       
                        client.send(passwordHasher.get_initial_hash(password).encode('ascii')) 

                    if Message == 'EMAIL?':
                        client.send(checkEmail.encode('ascii'))
                        print('sent email')

                    if Message == 'ERROR_ACOUNT_EXSISTING':
                        print(Message)
                        client.close()
                        messagebox.showerror("Opps!", "Account already exsists!")
                        createAccount.focus()
                        break

            checkEmail = emailInput.get()

            pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
            if re.match(pat,checkEmail):
                messagebox.showerror("Error", "Provided Email is Invalid!")
            else:
                sendAccount2()
            
        headerLabel = Label(createAccount, text='Create Account', bg='#202020', fg='white', font=StartFont)
        headerLabel.pack(side=TOP)
        headerLabel.focus_set()

        username = Entry(createAccount, width='50', borderwidth='0')
        username.pack(pady='10', padx='5')
        username.insert(0, 'Username')
        username.bind("<FocusIn>", lambda args: username.delete('0', 'end'))    

        magicUsername = Button(createAccount, command=gererateUser, text='Magic Username', borderwidth='0', bg='white')
        magicUsername.pack(padx='5')

        emailInput = Entry(createAccount, width='50', borderwidth='0')
        emailInput.pack(pady='10', padx='5')
        emailInput.insert(0, 'Email')
        emailInput.bind("<FocusIn>", lambda args: emailInput.delete('0', 'end'))    

        passwordinput = Entry(createAccount, width='50', borderwidth='0')
        passwordinput.pack(pady='10', padx='5')
        passwordinput.insert(0, 'Password')
        passwordinput.bind("<FocusIn>", (lambda event: enterPassword2()))

        submitAccount = Button(createAccount, borderwidth='0', text='Create', command=sendAccount, bg='white')
        submitAccount.pack(pady='10')

    def Getnick(): #gets the login credentials
        global nickname
        global passwrd
        nickname = user.get()
        print(nickname)
        passwrd = password.get()  
        SubmitNick.configure(state=DISABLED)

        if not os.path.isdir(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData"):
            os.mkdir(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData")

        if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
            os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt")
        f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt", "a")
        f.write(user.get())
        f.close()
        if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
            os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt")
        f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt", "a")
        f.write(password.get())
        f.close()
        
        Connect() 

    def enterPassword(): 
        password.delete('0', 'end')
        password.configure(show="•")


    global username

    myFont = font.Font(family='Arial', weight=font.BOLD, size=25)
    anounceFont = font.Font(family='Arial', weight=font.BOLD)

    frame = Frame(c, bg="#202020", width=100)
    frame.pack(side=LEFT, fill=Y)

    myImage = ImageTk.PhotoImage(Image.open('Images/Ringer-Bot.png'))

    #Ringer = Label(frame, bg='#202020', image=myImage)
    #Ringer.pack(side=TOP, pady=20, padx=190) 

    welcome = Label(frame, text="Login With Lif", bg='#202020', font=myFont, fg='orange')
    welcome.pack(padx=230, pady=50)

    var = IntVar()
    infoCheck = IntVar()
    infoCheck = 0

    user = customtkinter.CTkEntry(frame, width= 350, border_width = 2) 
    #user.config(highlightbackground = "orange", highlightcolor= "orange")
    user.pack(side=TOP, pady= 10, padx=20) 
    if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
        f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt", "r")
        user.insert(0, f.read())
        f.close()
        infoCheck = infoCheck + 1
    else:
        user.insert(0, 'username')
    user.bind("<FocusIn>", lambda args: user.delete('0', 'end')) 

    password = customtkinter.CTkEntry(frame, width = 350, border_width= 2) 
    #password.configure(highlightbackground = "orange", highlightcolor= "orange")
    password.pack(side=TOP, pady= 10, padx=20) 
    if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
        f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt", "r")
        password.configure(show="*")
        password.insert(0, f.read())
        f.close()
        infoCheck = infoCheck + 1
    else:
        password.insert(0, 'password')
    password.bind("<FocusIn>", (lambda event: enterPassword()))
        
    #checkbox = Checkbutton(frame, text="Remember Me", variable=var, bg='#ffb85c', activebackground='#36393f', onvalue=1, offvalue=0, fg='orange', borderwidth=0)
    #checkbox.pack(side=BOTTOM)

    #if infoCheck == 2:
        #checkbox.select()
        #print(var.get())

    #label = Label(frame, text="     ", bg='#ffcb7e', fg='white')
    #label.pack(side=BOTTOM)

    SubmitNick = customtkinter.CTkButton(frame, text='Login', border_width=0, command=Getnick, fg_color='orange', text_font="Arial 15 bold", hover_color="#ffb85c", corner_radius=10)  
    SubmitNick.pack(pady='10') 

    Createaccount = customtkinter.CTkButton(c, text='Create Account', border_width=0, command=CreateAccount, bg_color='#ffcb7e', fg_color="white", text_color='black', corner_radius=8, hover_color='#e7e7e7')
    Createaccount.pack(pady=160) 

    c.create_text(850, 100, text="New Here? \n Sign Up!", fill="white", font=('Arial 20 bold'))
    c.pack(side=RIGHT)

    forgotPassoword = Button(frame, bg='#202020', borderwidth=0, fg="cyan", command=resetAccount, text="Forgot Password?", font= ('Helvetica 10 underline'), activebackground='#202020')
    forgotPassoword.pack(pady='10')

    lifLogoImage = ImageTk.PhotoImage(Image.open("Images/LifLogo.png"))

    lifLogo= Label(frame,image= lifLogoImage, bg='#202020')
    lifLogo.pack(pady=60)

    #statusThread = threading.Thread(target=statusBar, daemon=True)
    #statusThread.start()

    def on_closing(): #handles closing the software
        login.destroy()
        sys.exit() 
    
    login.bind('<Return>', (lambda event: Getnick()))
    login.resizable(False, False) 
    login.protocol("WM_DELETE_WINDOW", on_closing)  
    login.mainloop() 

def autoConnect(): #handles connecting and logging into the server
        global client
        print("conecting...")
        isBanned = False
        try: 
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((serverIp, 20200)) 
            autoLoginStatus = ringerLogin.login(username=nickname, password=passwrd, client=client)

            if autoLoginStatus == "Success":
                pass
            
            if autoLoginStatus == "Bad_Login":
                messagebox.showerror("ERROR!", "Username or password is incorrect!")
                LOGIN()

            if autoLoginStatus == "Banned":
                isBanned = True
                messagebox.showerror("BANNED!", "You Have Been Banned From The Ringer Service")
                sys.exit()

        except:
            ErrorWindow = Tk()
            ErrorWindow.geometry("500x600")
            ErrorWindow.title("Failed To Connect To Server")
            ErrorWindow.config(background='#1e1e1e')
            ErrorWindow.resizable(False,False)
            ErrorWindow.iconbitmap("Icons/Ringer-Icon.ico")

            wifiImage = PhotoImage(file="Images/Uh Oh.png")

            loginImage = PhotoImage(file="Images/Proceed.png")

            wifiLabel = Label(ErrorWindow, image=wifiImage, background='#1e1e1e')
            wifiLabel.pack()

            def Proceed():
                ErrorWindow.destroy()

            proceed = Button(ErrorWindow, image=loginImage, bg='#1e1e1e', borderwidth=0, activebackground='#1e1e1e', command=Proceed)
            proceed.pack()

            ErrorWindow.mainloop()
            #messagebox.showerror("ERROR!", "Failed to connect to server!")
            LOGIN()

if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
    f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt", "r")
    displayName = f.read()
    f.close()
    infoCheck = infoCheck + 1

if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
    f = open(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt", "r")
    passwordCheck = f.read()
    f.close()
    infoCheck = infoCheck + 1

if infoCheck == 2:
    nickname = displayName
    passwrd = passwordCheck
    print("logging in...")
    autoConnect()#Handles connections outside of the login window.

else: 
    LOGIN()#login window

global outdated
outdated = False

def updateCheck():
    global ringerVersion
    global outdated
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((serverIp, 20200))

        updateCheck = client.recv(1024).decode('ascii')
        if updateCheck == "LOGIN":
            client.send('Check_Version'.encode('ascii'))

        while True:
            updateCheck = client.recv(1024).decode('ascii')
            client.close()

            if updateCheck == ringerVersion:
                outdated = False
                break
            else:
                messagebox.showwarning("Ringer Out Of Date!", "You are using an outdated version of ringer. To continue, you must be on the latest version of ringer. Please run the ringer installer to update.")
                print(updateCheck)
                outdated = True
                break
    except:
        messagebox.showwarning("Failed to Check for Updates!", "You may be using an outdated version of ringer. We were unable to check.")

updateCheck()

if outdated == True:
    sys.exit()


root = customtkinter.CTk() #main window for sending messages

if audioPlayed == False:
        #playsound("Sounds/Ringer Startup.wav")
        audioPlayed = True

#configuring root
windowTitle = f"Ringer (Beta v{ringerVersion})"
root.state("zoomed")
root.title(windowTitle)   
root.configure(background="black")

#fonts
sendFont = ('Arial',20)
reciveFont = ('Arial')

#colors
bgColor = "black"
midgroundColor = "#141414" #color for ui elements like frames and buttons
fgColor = "white"

Online = True

def reconnect():
    global client
    print("conecting...")
    root.title(windowTitle + " | Connecting...")
    try: 
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((serverIp, 20200)) 
        ringerLogin.login(username=nickname, password=passwrd, client=client)
    
    except:
        reconnect()
    root.title(windowTitle)

def LogOut():
    if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt"):
        os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Display_name.txt")

    if os.path.isfile(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt"):
        os.remove(os.path.expanduser('~') + "\AppData\Roaming\RingerLoginData\Super_Secret_Password.txt")

    messagebox.showinfo("Logout", "You logged out of Ringer.")

def VCWIN():
    messagebox.showinfo("Ringer Vc", "Voice calls aren't out yet but they will be soon!")

global DMadd
DMadd = "none"

def addDm():
    addDmWindow = Toplevel()
    addDmWindow.title("Add DM") 
    addDmWindow.focus()                    
    addDmWindow.config(bg= bgColor) 
    addDmWindow.geometry("500x500")
    #addDmWindow.iconbitmap("Ringer-Icon.ico")

    def send():
        socket.setdefaulttimeout(5)
    
        lifAccountServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lifAccountServer.connect((serverIp, 20205))

        while True:
            DMmessage = lifAccountServer.recv(1024).decode('ascii')
            if DMmessage:
                print(DMmessage)

            if DMmessage == 'USERNAME':
                lifAccountServer.send(nickname.encode('ascii'))
                print(nickname)

            if DMmessage == 'PASSWORD':
                password = passwrd

                lifAccountServer.send(passwordHasher.get_initial_hash(password).encode('ascii')) 

            if DMmessage == 'LOGIN_GOOD':
                print("login Successful")
                lifAccountServer.send("ADD_DM".encode('ascii'))
                #playsound("Sounds/Ringer Welcome Login.wav")

            if DMmessage == 'BAD_LOGIN_ERROR':
                #response = messagebox.askquestion("Error", "Username or Password is Incorrect. Would You Like to reset Your Password?")
                messagebox.showerror('Error', 'Username or password is incorrect.')

            if DMmessage == "DM_NAME?":
                lifAccountServer.send(dmEntry.get().encode('ascii'))
                print("sent dm name")

            if DMmessage == "SUCCESS!":
                print('success')
                addDmWindow.destroy() 
                break

    dmTitle = Label(addDmWindow, text="Add a Conversation", bg=bgColor, fg='white')
    dmTitle.pack()

    dmEntry = Entry(addDmWindow, width=20, borderwidth=0)
    dmEntry.pack(padx=5, pady=10)

    sendDm = Button(addDmWindow, text="Add", command=send, borderwidth=0)
    sendDm.pack()

    addDmWindow.resizable(False, False)

myFont = font.Font(family='Arial')

GUI = Frame(root, bg=bgColor)
GUI.pack(side=BOTTOM, fill=BOTH, expand=True, pady=20)

text_scroll = customtkinter.CTkScrollbar(root) 
text_scroll.pack(side=RIGHT, fill=Y, pady=20) 

logOut = Button(root, text="Logout", command=LogOut, bg=midgroundColor, borderwidth='0', fg='white')
logOut.pack(side=TOP, anchor=NE, padx='20')

#joinVC = Button(root, text='Join VC', command=VCWIN, bg=midgroundColor, borderwidth='0', fg='white')
#joinVC.place(bordermode=OUTSIDE)
#joinVC.pack(side=TOP, anchor=NE, padx='20')

sidePanel = Frame(root, width = 400, height= 53, borderwidth=0, bg = midgroundColor)
sidePanel.pack(fill=Y, pady=20, side=LEFT)

topBar = Frame(sidePanel, width = 400, bg = midgroundColor, borderwidth=0)
topBar.pack(side=TOP)

dmLabel = Label(topBar, text="Direct Messages", bg= midgroundColor, fg='white', font=myFont, width=20)
dmLabel.pack(side=LEFT)

#addDMThread = threading.Thread(target=addDm)

addDmButton = Button(topBar, text="➕", bg=midgroundColor, fg='white', font=myFont, borderwidth=0, activebackground=midgroundColor, command=addDm)
addDmButton.pack(side=RIGHT)

text = Text(root, width = 500, height = 53, borderwidth = '0', bg = midgroundColor, fg = 'white', yscrollcommand=text_scroll.set, font=reciveFont, wrap=tk.WORD) 
text.config(state='disabled') 
text.yview('end')
text.pack(fill=BOTH, expand=True, padx=20, pady=20)  

text_scroll.configure(command=text.yview)

global myimage
myimage = PhotoImage(file="Images/Ringer-Bot-Small.png")

print('phase 1 compleate')

def recive(): 
    global client
    global recviveMessage
    global myImage
    global DMadd
    while True:
        try: #tries to receive messages from the server
            Message = client.recv(1024).decode('ascii')
            text.config(state='normal') 
            text.insert(END, Message) 
            text['font'] = myFont
            text.config(state='disabled')
            text.see('end') 
            '''
            if not focus_check.get():
                print("notify sent")
                notification.notify(title = 'Message', message = Message, app_icon = 'Ringer-Icon.ico', timeout = 10, app_name = "Ringer")
                #playsound('RingerNotification.wav')
            '''

        except: 
            reconnect()

def write(): 
    global recviveMessage
    
    #sending messages to the server
    Checkentry = e.get()
    if Checkentry == "":
        pass
    else: 
        try:
        
            Message = f'''{message2.get()}
    [{nickname}]
    {e.get()}
    ''' 
            client.send(Message.encode('ascii'))
            e.delete('0', END)
        except:
            messagebox.showerror("ERROR!", "Failed To Send Message") 

def on_closing():
    client.close()
    root.destroy() 
    sys.exit()


def clearText():
    e.delete('0', END)

myImage2 = ImageTk.PhotoImage(Image.open('Images/sendButton.png')) #send button icon

message2 = Entry(GUI, width=10, borderwidth='0', bg = midgroundColor, fg = 'white', font=sendFont)
message2.pack(side=LEFT,)

e = Entry(GUI, width= 100, borderwidth = '0', bg = midgroundColor, fg = 'white', font=sendFont) 
e.pack(side=LEFT, fill=X, expand=True, padx=20) 
e.focus_set()

#SendButton = Button(GUI, image=myImage2, borderwidth = '0', bg='#202225', activebackground='#202225', padx=10, command = write)
#SendButton.pack(side = RIGHT)   

recive_thread = threading.Thread(target=recive, daemon=True)
recive_thread.start()

write_thread = threading.Thread(target=write, daemon=True)
write_thread.start() 

root.iconbitmap("Icons/Ringer-Icon.ico")

focus_check = tk.BooleanVar()
root.bind('<FocusIn>', lambda _: focus_check.set(True))
root.bind('<FocusOut>', lambda _: focus_check.set(False))

e.bind('<Return>', (lambda event: write())) #this is so you can press enter to send a message 
e.bind('<Control-Key-BackSpace>',(lambda event: clearText()))
root.protocol("WM_DELETE_WINDOW", on_closing) 
root.minsize(1000, 600)
root.mainloop() 