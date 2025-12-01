from tkinter import *


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
        
        self.nurse_profile = Tk()
        self.nurse_profile.title(f"Nurse Profile: {self.name}")
        self.nurse_profile.config(bg="#ECBD83")
        self.nurse_profile.geometry("1000x600")
        
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

        self.nurse_profile_main_frame = Frame(self.nurse_profile,
                                               bg="#DB7E0E",
                                               relief=RIDGE,
                                               borderwidth=5,
                                               width=800,
                                               height=400)
        self.nurse_profile_main_frame.place(x=500, y=350, anchor=CENTER)
        for patient in self.patient_list:
            patient_label = Label(self.nurse_profile_main_frame,
                                  text=f"Patient: {patient.name}, Admission Date: {patient.admission_date}, Treatments: {patient.treatment_description}, Severity: {patient.severity_description}",
                                  font=("Arial", 14),
                                  bg="#DB7E0E",
                                  fg="white")
            patient_label.pack()
        
        return Nurse(name, id)

    def add_patient(self, patient):
        self.patient_list.append(patient) #Should I make a list instance variable for a patient that includes name, admission date, treatement list, and severity level?
        for treatment in patient.treatment_needs:
            self.treatment_workload[treatment] += treatment
            self.workload += treatment
        for severity in patient.severity_vector:
            self.severity_workload[severity] += severity

        
