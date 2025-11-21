from tkinter import *
#import nurse data for login verification


# Define the main login window
login_window = Tk()
login_window.title("Login")
login_window.config(bg="#ECBD83")
login_window.geometry("1000x600")
login_title = Label(login_window,
                    text="UT Health Nurse Login", 
                    font=("Arial", 24), 
                    bg="#DB7E0E", 
                    fg="white",
                    padx=20,
                    pady=20,
                    relief=RIDGE,
                    borderwidth=5)
login_title.place(x=500, y=100, anchor=CENTER)

login_frame = Frame(login_window,
                    bg="#DB7E0E",
                    relief=RIDGE,
                    borderwidth=5,
                    width=400,
                    height=300)
login_frame.place(x=500, y=400, anchor=CENTER)
login_frame.pack_propagate(False)

username_label = Label(login_frame,
                    text="Please enter your username to login:",
                    fg="white",
                    bg="#DB7E0E",
                    font=("Arial", 16))
username_label.pack(padx=20, pady=20)



#Username entry
user_input = Entry(login_frame,
                    font=("Arial", 16),
                    bg="#FFFFFF",
                    fg="Black",
                    width=30,)

user_input.place(x=15, y=70)
username = user_input.get() #is this line necessary?


#Password entry
password_label = Label(login_frame,
                       text="Enter your password:",
                       font=("Arial", 16),
                       bg="#DB7E0E",
                       fg="White",
                       width=30)
password_label.place(x=15, y=120)   

password_input = Entry(login_frame,
                       font=("Arial", 16),
                       bg="#FFFFFF",
                       fg="Black",
                       show="*",
                       width=30)
password_input.place(x=15, y=160)
password = password_input.get() #is this line necessary?

#Login button
login_button = Button(login_frame,
                      text="Login",
                      font=("Arial", 16),
                      bg="#ECBD83",
                      fg="Black",
                      width=10,)
login_button.place(x=130, y=220)

login_window.mainloop()


#Function to verify login credentials





class Login:
    def __init__(self, user, passwd):
        self.username = user
        self.password = passwd



#we need a method that will be called by button command
    def Login_func(self, user, passwd):
        nurse_usernames = [...] #imported from nurse data
        nurse_passwords = [...] #imported from nurse data
        for i in nurse_usernames:
            if user == nurse_usernames[i]:
                if passwd == nurse_passwords[i]:
                    return Login_Success() 
                else:
                    return False
#How do I use a boolean value to break out of both loops?
'''
should I make this a class so that the imported values are 
 a) private
 b) easier to access throughout the program
'''

login_window.mainloop()