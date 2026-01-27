from dataclasses import dataclass
from tkinter import *
from tkinter import filedialog
from typing import List
import csv


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
menu_workload_frame.place(x=450, y=150)

#Labels

menu_welcome_text = "UTK Nursing Portal"  # Placeholder for dynamic nurse name
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
                        text="Portal Menu",
                        font=("Arial", 12),
                        bg="#DB7E0E",
                        fg="White",
                        padx=10,
                        pady=10)  # Placeholder for dynamic patient count)
menu_workload_text.pack()



#Buttons

# menu_button_nurse_prof = Button(menu_button_frame,
#                                 text="My Profile",
#                                 bg="#ECBD83",
#                                 fg="Black",
#                                 width=20,
#                                 height=5)    
# menu_button_nurse_prof.place(x=50, y=50)
#what if on this page we display the nurse's assigned patients and workload etc?

menu_button_new_patient = Button(menu_button_frame,
                                command=lambda : OpenNewWindow(patient_input_window, menu_window),
                                text="New Patient",
                                bg="#ECBD83",
                                fg="Black",
                                width=20,
                                height=5)   
menu_button_new_patient.place(x=25, y=50)

menu_button_new_nurse = Button(menu_button_frame,
                                     text="New Nurse Profile",
                                     bg="#ECBD83",
                                     fg="black",
                                     command=lambda : OpenNewWindow(new_nurse_window, menu_window),
                                     width=20,
                                     height=5)
menu_button_new_nurse.place(x=25, y=150)

menu_button_nurse_directory = Button(menu_button_frame,
                                     text="Nurse Directory",
                                     bg="#ECBD83",
                                     fg="black",
                                     command=lambda : OpenNewWindow(nurse_directory_window, menu_window),
                                     width=20,
                                     height=5)
menu_button_nurse_directory.place(x=175, y=150)

menu_button_patient_directory = Button(menu_button_frame,
                                     text="Patient Directory",
                                     bg="#ECBD83",
                                     fg="black",
                                     command=lambda : OpenNewWindow(patient_directory_window, menu_window),
                                     width=20,
                                     height=5)
menu_button_patient_directory.place(x=175, y=50)

menu_button_import_nurse_data = Button(menu_button_frame,
                            command=lambda : select_nurse_data(),
                            text="Import Nurse Data",
                            bg="#ECBD83",
                            fg="Black",
                            width=20,
                            height=5)
menu_button_import_nurse_data.place(x=325, y=50)

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
                          width=400,
                          height=400
                          )
nurse_directory_frame.place(x=350, y=150)
nurse_directory_frame.pack_propagate(False)

nurse_directory_exit_button = Button(nurse_directory_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, nurse_directory_window),
                                    width=20,
                                    height=2)
nurse_directory_exit_button.place(x=20, y=20)



#                               PATIENT DIRECTORY WINDOW HERE

patient_directory_window = Tk()
patient_directory_window.geometry("1000x600")
patient_directory_window.title("Patient Directory")
patient_directory_window.config(bg="#ECBD83")

patient_directory_frame = Frame(patient_directory_window,
                          bg="#DB7E0E",
                          relief=RIDGE,
                          borderwidth=5,
                          width=800,
                          )
patient_directory_frame.place(x=500, y=150)
patient_directory_frame.pack(fill="y")

patient_directory_exit_button = Button(patient_directory_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, patient_directory_window),
                                    width=20,
                                    height=2)
patient_directory_exit_button.place(x=30, y=20)


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


patient_cancel_input_button = Button(patient_input_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, patient_input_window),
                                    width=20,
                                    height=2)
patient_cancel_input_button.place(x=20, y=20)

new_patient_save_button = Button(patient_input_frame,
                                text="Save Patient",
                                bg="white",
                                fg="black",
                                command=lambda: SaveNewPatient(patient_name_input.get(), patient_date_input.get(), patient_treatment_input.get()),
                                #check function here ^^^^
                                
                                width=20,
                                height=2)
new_patient_save_button.place(x=400, y=350)


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


#                                               NOTIFICATION WINDOW
notification_window = Toplevel()
notification_window.geometry("400x300")
notification_window.title("Patient Assigned!")
notification_window.config(bg="#ECBD83")

notification_frame = Frame(notification_window,
                    bg="#DB7E0E",
                    relief=RIDGE,
                    borderwidth=5,
                    width=300,
                    height=200)
notification_frame.place(x=200, y=150, anchor=CENTER)

notification_label = Label(notification_frame,
                            text="",
                            fg="white",
                            bg="#DB7E0E",
                            font=("Arial", 10))
notification_label.place(x=40, y=50)

notification_button = Button(notification_frame,
                             text="Return to menu",
                             bg="white",
                             fg="black",
                             command=lambda : OpenNewWindow(menu_window, notification_window),
                             width=20,
                             height=2)
notification_button.place(x=80, y=100)




'''
                                                NURSE CLASS
'''
@dataclass
class Nurse:
    def __init__(self, name : str, id : int):
        self.name = name.strip()
        self.id = int(id)
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
        print(nurse_list)
        return nurse
    
    def __repr__(self):
        return f"{self.name}, ID: {self.id}"
    
    def refresh_patient_display(self):
    # Clear existing labels
        for widget in self.nurse_profile_main_frame.winfo_children():
            widget.destroy()

    # Re-add all patients in the list
        for p in self.patient_list:
            Label(
            self.nurse_profile_main_frame,
            text=f"Patient: {p['Name']}  |  Admission Date: {p['Admission Date']}  |  Treatments: {p['Treatment Needs']}  |  Severity: {p['Severity Vector']}",
            font=("Arial", 14),
            bg="#DB7E0E",
            fg="white"
            ).pack()

'''
                                                PATIENT CLASS
'''

class Patient:
    
    patient_categories = ["Neuro", "Psychosocial", "Safety", "Hemodynamic Stability", 
            "Drains", "ADLs", "Meds", "Wound Care", "Discharge"]
    def __init__(self, patient_name, admission_date, treatment_needs):
        self.patient_name = patient_name
        self.admission_date = admission_date
        self.treatment_needs = treatment_needs
        self.severity_vector = [0, 0, 0]
        #this is internal VVV
        self.severity_sum = 0
        self.patient_record = {"Name": self.patient_name,
                               "Admission Date": self.admission_date,
                               "Treatment Needs": self.treatment_needs,
                               "Severity Vector": self.severity_vector}
    
    @classmethod
    def create_patient(cls, name, date, treatment_needs):
        treatment_needs = list(map(int, treatment_needs.split()))
        patient = Patient(name, date, treatment_needs)
        patient_data_file.append(patient)
        
         #Create severity vector
        for treatment in patient.treatment_needs:
            patient.severity_sum += treatment
        if patient.severity_sum < low_severity_threshold:
            patient.severity_vector = [1, 0, 0]     
        elif patient.severity_sum < high_severity_threshold:
            patient.severity_vector = [0, 1, 0]
        elif patient.severity_sum >= high_severity_threshold and high_severity_threshold < 19:
            patient.severity_vector = [0, 0, 1]

         #Update patient record
        patient.patient_record = {"Name": patient.patient_name,
                       "Admission Date": patient.admission_date,
                       "Treatment Needs": patient.treatment_needs,
                       "Severity Vector": patient.severity_vector}
         
        return patient   
     
    def __repr__(self):
        return f"{self.patient_name}"


#DECISION FUNCTION

def assign_patient_to_nurse(patient):
    #Zero all indices and sums
    workload_avg = 0
    workload_sum = 0
    eligible_nurse_list = []
    for nurse in nurse_list:
        nurse.Q_Index = 0
        nurse.T_Index = 0
        nurse.S_Index = 0
        nurse.T_sum = 0
        nurse.num_Ts = 0
    

    #STEP 1(Get nurses with work < avg work)
    workload_sum = sum(nurse.workload for nurse in nurse_list)
    workload_avg = workload_sum / len(nurse_list)

    #STEP 2(Assign eligible nurses to new list)
    eligible_nurse_list = [nurse for nurse in nurse_list if nurse.workload <= workload_avg]

    #STEP 3(Select appropriate nurse for assignment)
    for nurse in eligible_nurse_list:
        
        #Calculate Q, T, S indices
        #T calculated by sum of treatment calegories of same index where patient treatment = 2
        for i in range (len(patient.treatment_needs)):
            if patient.treatment_needs[i] == 2:
                nurse.T_sum += nurse.treatment_workload[i]
                nurse.num_Ts += 1
            
        if nurse.num_Ts > 0:
            nurse.T_Index = nurse.T_sum / nurse.num_Ts
        else: nurse.num_Ts = 0
        
        #S calculated by finding nurse severity workload with same index as patient severity    
        for index, item in enumerate(patient.severity_vector):
                if item == 1:
                    nurse.S_Index = nurse.severity_workload[index]

        #Calculate Q from S and T
        nurse.Q_Index = ((1/(1 + nurse.T_Index)) + (1/(1 + nurse.S_Index)))

    #Assignment
    assign_to_this_nurse= max(eligible_nurse_list, key=lambda nurse: nurse.Q_Index)
        
    assign_to_this_nurse.patient_list.append(patient.patient_record)
    
    #Update treatment workload and total workload
    for i in range(len(assign_to_this_nurse.treatment_workload)):
        assign_to_this_nurse.treatment_workload[i] += patient.treatment_needs[i]
        assign_to_this_nurse.workload += patient.treatment_needs[i]
    #Update severity workload
    for i in range(len(assign_to_this_nurse.severity_workload)):
        assign_to_this_nurse.severity_workload[i] += patient.severity_vector[i]
    
    assign_to_this_nurse.refresh_patient_display()
    
    print(patient.treatment_needs)
    print(patient.severity_vector)
    print(nurse.treatment_workload)
    print(nurse.severity_workload)
    return assign_to_this_nurse

    
   
 

#                                                        MISC FUNCTIONS


#Button function to save new nurse and open profile
def SaveNewNurse(name, id):
    nurse = Nurse.create_nurse_profile(name, id)
    OpenNewWindow(nurse.nurse_profile, new_nurse_window)
    add_to_nurse_directory(name, id, nurse)
    new_nurse_name_input.delete(0, END)
    new_nurse_id_input.delete(0, END)

#Button function to save new patient and assign to nurse
def SaveNewPatient(name, admission_date, treatment_needs):
    patient = Patient.create_patient(name, admission_date, treatment_needs)
    add_to_patient_directory(name, admission_date, treatment_needs, patient.severity_vector)
    assign_to_this_nurse = assign_patient_to_nurse(patient)
    notification_label.config(text=f"Patient {getattr(patient, 'name', patient)} was assigned to nurse {getattr(assign_to_this_nurse, 'name', assign_to_this_nurse)}")
    OpenNewWindow(notification_window, patient_input_window) 
    patient_name_input.delete(0, END)
    patient_date_input.delete(0, END)
    patient_treatment_input.delete(0, END)

#Function to open new window and close old window
def OpenNewWindow(open_window, close_window):
    close_window.withdraw()
    open_window.deiconify()

def select_nurse_data():
    nurse_data = filedialog.askopenfilename(
        title="Select a CSV file",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    load_nurse(nurse_data)
    return nurse_data

def load_nurse(nurse_data: str) -> List[Nurse]:
    with open(nurse_data, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            nurse = Nurse(
                name=row['name'],
                id=row['id']
            )
            nurse_list.append(nurse)
            add_to_nurse_directory(nurse.name, nurse.id, nurse)
    return nurse_list


#Function to read data into nurse list, directory

#Function to refresh nurse directory
def add_to_nurse_directory(name, id, nurse):
    next_row = nurse_directory_frame.grid_size()[1]
    nurse_label = Label(nurse_directory_frame,
                        text=f"Name: {name},   |    ID: {id},     |  Profile:",
                        font=("Arial", 12),
                        bg="#DB7E0E",
                        fg="White")
    nurse_label.grid(row=next_row, column=0, padx=10, pady=10)
    
    nurse_profile_button = Button(nurse_directory_frame,
                                text="View Profile",
                                bg="#ECBD83",
                                fg="Black",
                                width=10,
                                command=lambda : OpenNewWindow(nurse.nurse_profile, nurse_directory_window)
                                    )
    nurse_profile_button.grid(row=next_row, column=1, padx=10, pady=10)
    #add args to this function when called to use info from nurse entries

#Function to refresh patient directory
def add_to_patient_directory(name, admission_date, treatment_needs, severity_vector):
    patient_label = Label(patient_directory_frame,
                        text=f"Name: {name}, Admission Date: {admission_date}, Treatments: {treatment_needs}, Severity: {severity_vector}",
                        font=("Arial", 12),
                        bg="#DB7E0E",
                        fg="White")
    patient_label.pack()

patient_input_window.withdraw()
new_nurse_window.withdraw()
nurse_directory_window.withdraw()
patient_directory_window.withdraw()
notification_window.withdraw()

menu_window.mainloop()
patient_input_window.mainloop()
new_nurse_window.mainloop()
nurse_directory_window.mainloop()
patient_directory_window.mainloop()
notification_window.mainloop()