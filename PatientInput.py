from tkinter import *
import sys
from datetime import datetime
patient_data_file = []
high_severity_threshold = 10
low_severity_threshold = 5

patient_input_window = Tk()
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
'''
        self.patient_name = patient_name_input.get()
        self.admission_date = patient_date_input.get()
        self.treatment_needs = list(map(int, patient_treatment_input.get().split()))
        '''
        


        #need to code 'exit' button to close window without saving data
patient_cancel_input_button = Button(patient_input_window,
                                    text="Back to menu",
                                    bg="white",
                                    fg="black",
                                    command=lambda: OpenNewWindow(menu_window, patient_input_window),
                                    width=20,
                                    height=2)

patient_cancel_input_button.place(x=20, y=20)


class Patient:
    
    patient_categories = ["Neuro", "Psychosocial", "Safety", "Hemodynamic Stability", 
            "Drains", "ADLs", "Meds", "Wound Care", "Discharge"]
    def __init__(self, patient_name, admission_date, treatment_needs):
        self.patient_name = ""
        self.admission_date = ""
        self.treatment_needs = []
        self.severity_vector = []
        self.severity_sum = 0
        self.patient_record = {"Name": self.patient_name,
                               "Admission Date": self.admission_date,
                               "Treatment Needs": self.treatment_needs,
                               "Severity Vector": self.severity_vector}

    
    def get_patient_info(self):
        
        new_patient = Patient("", "", [], [])


        
        

        #Fill in admission date   
        self.admission_date = input("Enter admission date (MM/DD/YYYY): ")
       
        #Fill in treatment needs

        
        print("On a scale of 0-2, rate the level of care needed for each of the following categories:")
        for category in self.patient_categories:
            print(f"{category}: ")
            input_value=input()
            if input_value >= '0' and input_value <= '2':
                self.treatment_needs.append(int(input_value))
            else:
                print("Invalid input. Please enter a number between 0 and 2.")
                return
        
        #Create severity vector
        for i in self.treatment_needs:
            self.severity_sum += i
        if self.severity_sum < low_severity_threshold:
            self.severity_vector = [1, 0, 0]
        elif self.severity_sum < high_severity_threshold:
            self.severity_vector = [0, 1, 0]
        elif self.severity_sum >= high_severity_threshold and high_severity_threshold < 19:
            self.severity_vector = [0, 0, 1]

        #Update patient record
        self.patient_record = {"Name": self.patient_name,
                               "Admission Date": self.admission_date,
                               "Treatment Needs": self.treatment_needs,
                               "Severity Vector": self.severity_vector}
        #Add patient record to list
        print(self.patient_record)

'''
11/20 12.31p - I am trying to debug the function that returns to the main window from the patient input window,
but I can't compile because both scripts call each other. So I am debating defining my patient window outside 
of this function and moving the function that opens it to the MenuGUI script.

'''
#def open_patient_input():
    #tkinter input labels and entry boxes
        #ask Nan how to fix this so it doesnt need to be global
        
       # patient_input_window.mainloop()
      #  return patient_input_window

#def close_patient_window(patient_input_window):
   # patient_input_window.destroy()
   # menu_window.mainloop()

def OpenNewWindow(open_window, close_window):
    close_window.withdraw()
    open_window.deiconify()

#Call function to get patient info
patient_input_window.mainloop()