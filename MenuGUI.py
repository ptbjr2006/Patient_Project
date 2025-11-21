from PatientInput import patient_input_window

from tkinter import *


menu_window = Tk()
menu_window.geometry("1000x600")
menu_window.title("Main Menu")
menu_window.config(bg="#ECBD83")


#Frames

menu_button_frame = Frame(menu_window,
                          bg="#DB7E0E",
                          relief=RIDGE,
                          borderwidth=5,
                          width=500,
                          height=300)
menu_button_frame.place(x=250, y=250)

menu_workload_frame = Frame(menu_window,
                          bg="#DB7E0E",
                          relief=RIDGE,
                          borderwidth=5,
                          width=300,
                          height=100)
menu_workload_frame.place(x=350, y=150)

#Labels

menu_welcome_text = "Welcome, [Nurse Name]!"  # Placeholder for dynamic nurse name
menu_title = Label(menu_window,
                text=menu_welcome_text,
                font=("Arial", 24),
                bg="#DB7E0E",
                fg="white",
                padx=20,
                pady=20,
                relief=RIDGE,
                borderwidth=5)
menu_title.place(x=500, y=100, anchor=CENTER)

menu_workload_text = Label(menu_workload_frame,
                        text="You currently have [X] patients assigned",
                        font=("Arial", 12),
                        bg="#DB7E0E",
                        fg="White",
                        padx=10,
                        pady=10)  # Placeholder for dynamic patient count)
menu_workload_text.pack()

#Buttons

menu_button_nurse_prof = Button(menu_button_frame,
                                text="My Profile",
                                bg="#ECBD83",
                                fg="Black",
                                width=12,
                                height=5)    
menu_button_nurse_prof.place(x=50, y=50)
#what if on this page we display the nurse's assigned patients and workload etc?

menu_button_new_patient = Button(menu_button_frame,
                                command=lambda : OpenNewWindow(patient_input_window, menu_window),
                                text="New Patient",
                                bg="#ECBD83",
                                fg="Black",
                                width=12,
                                height=5)   
menu_button_new_patient.place(x=200, y=50)

#open new patient window
def OpenNewWindow(open_window, close_window):
    close_window.withdraw()
    open_window.deiconify()

#can I generalize this with 2 window args  so it doesnt need to be written out for each window?

menu_window.mainloop()
patient_input_window.withdraw()
patient_input_window.mainloop()
#def Login_Success():
#    login_window.destroy()

    
    