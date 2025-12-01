from tkinter import *



'''

                                            MENU WINDOW

'''
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
                                width=20,
                                height=5)    
menu_button_nurse_prof.place(x=50, y=50)
#what if on this page we display the nurse's assigned patients and workload etc?

menu_button_new_patient = Button(menu_button_frame,
                                command=lambda : OpenNewWindow(patient_input_window, menu_window),
                                text="New Patient",
                                bg="#ECBD83",
                                fg="Black",
                                width=20,
                                height=5)   
menu_button_new_patient.place(x=200, y=50)

menu_button_new_nurse = Button(menu_button_frame,
                                     text="New Nurse Profile",
                                     bg="#ECBD83",
                                     fg="black",
                                     command=lambda : OpenNewWindow(new_nurse_window, menu_window),
                                     width=20,
                                     height=5)
menu_button_new_nurse.place(x=50, y=150)

menu_button_nurse_directory = Button(menu_button_frame,
                                     text="Nurse Directory",
                                     bg="#ECBD83",
                                     fg="black",
                                     command=lambda : OpenNewWindow(nurse_directory_window, menu_window),
                                     width=20,
                                     height=5)
menu_button_nurse_directory.place(x=200, y=150)

'''
                                            NURSE DIRECTORY WINDOW
'''

nurse_directory_window = Tk()
nurse_directory_window.geometry("1000x600")
nurse_directory_window.title("Nurse Directory")
nurse_directory_window.config(bg="#ECBD83")

nurse_directory_frame = Frame(nurse_directory_window,
                          bg="#DB7E0E",
                          relief=RIDGE,
                          borderwidth=5,
                          width=800,
                          )
nurse_directory_frame.place(x=350, y=150)
nurse_directory_frame.pack(fill="y")

nurse_directory_exit_button = Button(nurse_directory_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, nurse_directory_window),
                                    width=20,
                                    height=2)
nurse_directory_exit_button.place(x=20, y=20)


'''
                                            PATIENT INPUT WINDOW
'''
# PATIENT INPUT WINDOW

patient_data_file = []
high_severity_threshold = 10
low_severity_threshold = 5

patient_input_window = Toplevel()
patient_input_window.geometry("1000x600")
patient_input_window.title("New Patient Input")
patient_input_window.config(bg="#ECBD83")
        
patient_input_frame = Frame(patient_input_window,
                    bg="#DB7E0E",
                    relief=RIDGE,
                    borderwidth=5,
                    width=600,
                    height=400)
patient_input_frame.place(x=500, y=300, anchor=CENTER)

patient_title = Label(patient_input_frame,
                    text="Enter New Patient Information",
                    font=('Arial', 20),
                    bg="#DB7E0E",
                    fg="white")
patient_title.place(x=250, y=30, anchor=CENTER)


patient_name_label = Label(patient_input_frame,
                        text="Enter patient name:",
                        fg="white",
                        bg="#DB7E0E",
                        font=("Arial", 16))
patient_name_label.place(x=15, y=60)

patient_name_input = Entry(patient_input_frame,
                        font=("Arial", 16),
                        bg="#FFFFFF",
                        fg="Black",
                        width=30,)
patient_name_input.place(x=15, y=100)

patient_date_label = Label(patient_input_frame,
                        text="Enter patient admission date:",
                        fg="white",
                        bg="#DB7E0E",
                        font=("Arial", 16))
patient_date_label.place(x=15, y=140)
        
patient_date_input = Entry(patient_input_frame,
                        font=("Arial", 16),
                        bg="#FFFFFF",
                        fg="Black",
                        width=30,)
patient_date_input.place(x=15, y=180)

patient_treatment_label = Label(patient_input_frame,
                            text="Without commas, enter treatment needs (0-2) for the \nfollowing categories: Neuro, Psychosocial, \nSafety, Hemodynamic Stability, Drains, \nADLs, Meds, Wound Care, Discharge",
                            anchor="w",
                            justify=LEFT,
                            fg="white",
                            bg="#DB7E0E",
                            font=("Arial", 16))
patient_treatment_label.place(x=15, y=220)

patient_treatment_input = Entry(patient_input_frame,
                            font=("Arial", 16),
                            bg="#FFFFFF",
                            fg="Black",
                            width=30,)
patient_treatment_input.place(x=15, y=330)
        
        

        #self.patient_name = patient_name_input.get()
        #self.admission_date = patient_date_input.get()
        #self.treatment_needs = list(map(int, patient_treatment_input.get().split()))

        


        #need to code 'exit' button to close window without saving data
patient_cancel_input_button = Button(patient_input_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, patient_input_window),
                                    width=20,
                                    height=2)
patient_cancel_input_button.place(x=20, y=20)

'''
                                                NEW NURSE WINDOW
'''

nurse_list = []

new_nurse_window = Toplevel()
new_nurse_window.geometry("1000x600")
new_nurse_window.title("New Nurse Profile")
new_nurse_window.config(bg="#ECBD83")

new_nurse_frame = Frame(new_nurse_window,
                    bg="#DB7E0E",
                    relief=RIDGE,
                    borderwidth=5,
                    width=600,
                    height=400)
new_nurse_frame.place(x=350, y=270, anchor=CENTER)

new_nurse_title = Label(new_nurse_frame,
                    text="Enter New Nurse Information",
                    font=('Arial', 20),
                    bg="#DB7E0E",
                    fg="white")
new_nurse_title.place(x=250, y=30, anchor=CENTER)


new_nurse_name_label = Label(new_nurse_frame,
                        text="Enter nurse name:",
                        fg="white",
                        bg="#DB7E0E",
                        font=("Arial", 16))
new_nurse_name_label.place(x=15, y=60)

new_nurse_name_input = Entry(new_nurse_frame,
                            font=("Arial", 16),
                            bg="#FFFFFF",
                            fg="Black",
                            width=30,)
new_nurse_name_input.place(x=15, y=100)

new_nurse_id_label = Label(new_nurse_frame,
                        text="Enter nurse ID number (4 digits):",
                        fg="white",
                        bg="#DB7E0E",
                        font=("Arial", 16))
new_nurse_id_label.place(x=15, y=140)

new_nurse_id_input = Entry(new_nurse_frame,
                            font=("Arial", 16),
                            bg="#FFFFFF",
                            fg="Black",
                            width=30,)
new_nurse_id_input.place(x=15, y=180)

new_nurse_cancel_input_button = Button(new_nurse_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, new_nurse_window),
                                    width=20,
                                    height=2)
new_nurse_cancel_input_button.place(x=20, y=20)

new_nurse_save_input_button = Button(new_nurse_frame,
                                    text="Save new nurse",
                                    bg="white",
                                    fg="black",
                                    command=lambda: SaveNewNurse(new_nurse_name_input.get(), new_nurse_id_input.get()),
                                    width=20,
                                    height=2)
new_nurse_save_input_button.place(x=300, y=250)



'''
                                                NURSE CLASS
'''

class Nurse:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.patient_list = []
        self.workload = 0
        self.severity_workload = [0, 0, 0]
        self.treatment_workload = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Q_Index = 0
        self.T_Index = 0
        self.S_Index = 0
        self.num_Ts = 0
        self.T_sum = 0
        
        '''Nurse profile GUI'''
        
        self.nurse_profile = Toplevel()
        self.nurse_profile.title(f"Nurse Profile: {self.name}")
        self.nurse_profile.config(bg="#ECBD83")
        self.nurse_profile.geometry("1000x600")
        
        #Labels

        self.welcome_label = Label(self.nurse_profile,
                                   text=f"Nurse profile for: {self.name}",
                                   font=("Arial", 24),
                                   bg="#DB7E0E",
                                   fg="white",
                                   padx=20,
                                   pady=20,
                                   relief=RIDGE,
                                   borderwidth=5)
        self.welcome_label.place(x=500, y=100, anchor=CENTER)

        for patient in self.patient_list: #Ensure that objects in the list are accesible. Can use patient.patient_record[1, 2, etc.]?
            patient_label = Label(self.nurse_profile_main_frame,
                                  text=f"Patient: {patient.patient_name}, Admission Date: {patient.admission_date}, Treatments: {patient.treatment_description}, Severity: {patient.severity_description}",
                                  font=("Arial", 14),
                                  bg="#DB7E0E",
                                  fg="white")
            patient_label.pack()

        #Frames
        self.nurse_profile_main_frame = Frame(self.nurse_profile,
                                               bg="#DB7E0E",
                                               relief=RIDGE,
                                               borderwidth=5,
                                               width=800,
                                               height=400)
        self.nurse_profile_main_frame.place(x=500, y=350, anchor=CENTER)
      
        #Buttons
        nurse_profile_exit_button = Button(self.nurse_profile,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, self.nurse_profile),
                                    width=20,
                                    height=2)
        nurse_profile_exit_button.place(x=20, y=20)
 
    
    @classmethod
    def create_nurse_profile(cls, nurse_name, nurse_id):
        nurse = Nurse(nurse_name, nurse_id)
        nurse_list.append(nurse)
        add_to_nurse_directory(nurse_name, nurse_id)
        return nurse
        
    def add_patient(self, patient):
        self.patient_list.append(patient) #Should I make a list instance variable for a patient that includes name, admission date, treatement list, and severity level?
        for treatment in patient.treatment_needs:
            self.treatment_workload[treatment] += treatment
            self.workload += treatment
        for severity in patient.severity_vector:
            self.severity_workload[severity] += severity

'''
                                                PATIENT CLASS
'''

class Patient:
    
    patient_categories = ["Neuro", "Psychosocial", "Safety", "Hemodynamic Stability", 
            "Drains", "ADLs", "Meds", "Wound Care", "Discharge"]
    def __init__(self, patient_name, admission_date, treatment_needs, severity_vector):
        self.patient_name = patient_name
        self.admission_date = admission_date
        self.treatment_needs = treatment_needs
        self.severity_vector = severity_vector
        #this is internal VVV
        self.severity_sum = 0
        self.patient_record = {"Name": self.patient_name,
                               "Admission Date": self.admission_date,
                               "Treatment Needs": self.treatment_needs,
                               "Severity Vector": self.severity_vector}

    
    def get_patient_info(self):
        
        new_patient = Patient("", "", [], [])

    #Fill in admission date   
        new_patient.admission_date = input("Enter admission date (MM/DD/YYYY): ")
       
    #Fill in treatment needs

        
        print("On a scale of 0-2, rate the level of care needed for each of the following categories:")
        for category in new_patient.patient_categories:
            print(f"{category}: ")
            input_value=input()
        if input_value >= '0' and input_value <= '2':
            new_patient.treatment_needs.append(int(input_value))
        else:
            print("Invalid input. Please enter a number between 0 and 2.")
        
        #Create severity vector
        for i in new_patient.treatment_needs:
            new_patient.severity_sum += i
        if new_patient.severity_sum < low_severity_threshold:
            new_patient.severity_vector = [1, 0, 0]
        elif new_patient.severity_sum < high_severity_threshold:
            new_patient.severity_vector = [0, 1, 0]
        elif new_patient.severity_sum >= high_severity_threshold and high_severity_threshold < 19:
            new_patient.severity_vector = [0, 0, 1]

        #Update patient record
        new_patient.patient_record = {"Name": new_patient.patient_name,
                       "Admission Date": new_patient.admission_date,
                       "Treatment Needs": new_patient.treatment_needs,
                       "Severity Vector": new_patient.severity_vector}
        #Add patient record to list
        print(new_patient.patient_record)
        patient_data_file.append(new_patient.patient_record)


# def assign_patient_to_nurse(patient):
#     #Zero all indices and sums

#     Workload_avg = 0
#     Workload_sum = 0
#     Step_2_list = []
#     for nurse in nurse_list:
#         nurse.Q_Index = 0
#         nurse.T_Index = 0
#         nurse.S_Index = 0
#         nurse.T_sum = 0
#         nurse.num_Ts = 0
    
#     #STEP 1
    
#     for nurse in nurse_list:
#         Workload_sum += nurse.workload
#     Workload_avg = Workload_sum / len(nurse_list)
#     for nurse in nurse_list:
#         if nurse.workload < Workload_avg:
#             Step_2_list.append(nurse)
    
#     #STEP 2
    
#     for nurse in Step_2_list:
        
#         #Calculate Q, T, S indices
#         #T calculated by sum of treatment calegories of same index where patient treatment = 2
#         for i in range (Len(patient.treatment_needs)):
#             if patient.treatment_needs[i] == 2:
#                 nurse.T_sum += nurse.treatment_capabilities[i]
#                 Num_Ts += 1
#         nurse.T_Index = nurse.T_sum / Num_Ts
#         for i in patient.severity_vector:
#             if i == 1:
#                 nurse.S_Index = nurse.sevWorkload[i]
#         nurse.Q_Index = ((1/(1 + nurse.T_Index)) + (1/(1 + nurse.S_Index)))

#     assign_this_nurse = max(Step_2_list, key=lambda nurse: nurse.Q_Index)
        
        



        

#                                                        MISC FUNCTIONS


#Button function to save new nurse and open profile
def SaveNewNurse(name, id, old_window=new_nurse_window):
    nurse = Nurse.create_nurse_profile(name, id)
    OpenNewWindow(nurse.nurse_profile, old_window)
    new_nurse_name_input.delete(0, END)
    new_nurse_id_input.delete(0, END)


#Function to open new window and close old window
def OpenNewWindow(open_window, close_window):
    close_window.withdraw()
    open_window.deiconify()

#Function to refresh nurse directory
def add_to_nurse_directory(name, id):
    nurse_label = Label(nurse_directory_frame,
                        text=f"Name: {name}, ID: {id}, Profile:",
                        font=("Arial", 12),
                        bg="#DB7E0E",
                        fg="White")
    nurse_label.pack()
    nurse_profile_button = Button(nurse_directory_frame,
                                text="View Profile",
                                bg="#ECBD83",
                                fg="Black",
                                width=10,
                                #command=lambda : OpenNewWindow(nurse_list[nurse].nurse_profile, nurse_directory_window)
                                    )
    nurse_profile_button.pack()
    #add args to this function when called to use info from nurse entries

#Call function to get patient info


patient_input_window.withdraw()
new_nurse_window.withdraw()
nurse_directory_window.withdraw()





menu_window.mainloop()
patient_input_window.mainloop()
new_nurse_window.mainloop()
nurse_directory_window.mainloop()


def foo(x,y):
    '''
    adding x and y randomly\n 
    \t hahahahhahahaha jejejejejjejejeejeje
    '''
    return x+y





foo(3,4)