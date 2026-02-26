import sys
import csv
import hashlib
from uuid import uuid4
from PyQt5.QtWidgets import QApplication, QSizePolicy, QFrame, QGroupBox, QComboBox, QWidget,QScrollArea, QVBoxLayout # type: ignore
from PyQt5.QtWidgets import QLabel, QMessageBox, QFileDialog, QLineEdit, QGridLayout, QPushButton, QHBoxLayout 
from PyQt5.QtGui import QFont, QPixmap # type: ignore
from PyQt5.QtCore import Qt
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Tuple
from uuid import uuid4

#Object Classes


#Nurse Class
class Nurse:
    def __init__(self, nurse_id, name, hashed_password,
                 assigned_patients=None, last_workload=None,
                 shift=None):
        self.nurse_id = nurse_id
        self.name = name
        self.hashed_password = hashed_password
        self.role = "nurse"   # used by DataManager + WindowManager

        # Lists of Patient objects
        self.assigned_patients = assigned_patients or []
        self.last_workload = last_workload or []

    #Add patient to assigned patients list
    def add_patient(self, patient):
        if patient not in self.assigned_patients:
            self.assigned_patients.append(patient)
    
    #Remove patient from assigned patients list
    def remove_patient(self, patient):
        if patient in self.assigned_patients:
            self.assigned_patients.remove(patient)
    
    #At end of each shift, move current workload to last_workload and clear assigned_patients
    def clear_assignments(self):
        """Move current workload to last_workload and reset."""
        self.last_workload = self.assigned_patients.copy()
        self.assigned_patients = []

    '''This could be useful for csv reading. Should this belong in the datamanager instead?'''
    # def from_dict(self, data):
    #     """Load from a dictionary."""
    #     self.nurse_id = data["nurse_id"]
    #     self.name = data["name"]
    #     self.hashed_password = data["hashed_password"]
    #     self.role = data["role"]
    #     self.shift = data.get("shift", None)
    #     self.skill_level = data.get("skill_level", 0)


    def to_dict(self):
        """Convert to a serializable dictionary for saving."""
        return {
            "nurse_id": self.nurse_id,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "assigned_patients": [p.patient_id for p in self.assigned_patients],
            "last_workload": [p.patient_id for p in self.last_workload],
            "shift": self.shift,
            "skill_level": self.skill_level
        }

    def __repr__(self):
        return f"<Nurse {self.nurse_id}: {self.name}>"

#Admin Class
class Admin:
    def __init__(self, admin_id, name, hashed_password, permissions=None):
        self.admin_id = admin_id
        self.name = name
        self.hashed_password = hashed_password
        self.role = "admin"   # used by DataManager + WindowManager
    
    
    def to_dict(self):
        return {
            "admin_id": self.admin_id,
            "name": self.name,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "permissions": self.permissions
        }

#Patient Class  
@dataclass      
class Patient:
    name: str
    dob: str
    mrn: str
    admission_date: str
    room: str
    treatment_needs: List[int]

    low_threshold: int = 10
    high_threshold: int = 19

    severity_sum: int = field(init=False)
    severity_vector: List[int] = field(init=False)
    
    current_nurse: Optional["Nurse"] = None
    assignment_history: List[Tuple[str, datetime]] = field(default_factory=list)

    def __post_init__(self):
        # Validate treatment needs
        if len(self.treatment_needs) != 9:
            raise ValueError(
                f"Treatment needs must have 9 values, got {len(self.treatment_needs)}"
            )

        if any(t not in (0, 1, 2, 3) for t in self.treatment_needs):
            raise ValueError("Each treatment need must be 0, 1, 2, or 3")

        self.patient_id: str = field(default_factory=lambda: str(uuid4()))

        # Compute severity sum
        self.severity_sum = sum(self.treatment_needs)

        # Compute one-hot severity vector
        if self.severity_sum < self.low_threshold:
            self.severity_vector = [1, 0, 0]   # low
        elif self.severity_sum < self.high_threshold:
            self.severity_vector = [0, 1, 0]   # medium
        else:
            self.severity_vector = [0, 0, 1]   # high

    def assign_nurse(self, nurse: "Nurse"):
        self.current_nurse = nurse
        self.assignment_history.append((nurse.nurse_id, datetime.now()))

    def __repr__(self):
        return f"Patient({self.name}, MRN={self.mrn})"


#Manager Classes


#Window Manager Class
class WindowManager:
    def __init__(self, data_manager):
          self.data_manager = data_manager
          self.current = None
    
    def login_success(self, user):
        print("\n--- LOGIN SUCCESS DEBUG ---")
        print("USER OBJECT:", user)
        print("USER TYPE:", type(user))

        if isinstance(user, Nurse):
            print("ROUTING TO NURSE WINDOW")
            self.switch(MenuWindow, user)

        elif isinstance(user, Admin):
            print("ROUTING TO ADMIN WINDOW")
            self.switch(AdminMenuWindow, user)

    def logout(self):
        self.user = None
        self.switch(LoginWindow)

    def switch(self, new_window, *args):
        if self.current is not None:
          self.current.close()
        self.current = new_window(self, self.data_manager, *args)
        self.current.show()

#Data Manager Class  
class DataManager:
    def __init__(self):
        self.nurses = {}   # nurse_id → Nurse object
        self.admins = {}   # admin_id → Admin object
        self.patients = {} # patient_id → Patient object

        #More specific Nurse/Patient lists
    
    
    #Patient saver
    def add_patient(self, patient: Patient):
        """Store a new patient in the system."""
        self.patients[patient.patient_id] = patient

    # Password hashing helper
    def hash_password(self, raw_password):
        return hashlib.sha256(raw_password.encode()).hexdigest()

    # Login verification
    def verify_login(self, user_id, raw_password):

        #debugging
        # print("\n--- VERIFY LOGIN DEBUG ---")
        # print("NURSES:", self.nurses.keys())
        # print("ADMINS:", self.admins.keys())
        # print("USER ENTERED:", repr(user_id))


        hashed = self.hash_password(raw_password)
        #print("HASHED INPUT:", hashed)

        # 1. Check nurses
        if user_id in self.nurses:
            nurse = self.nurses[user_id]
            # print("MATCHED NURSE:", nurse)
            # print("STORED HASH:", nurse.hashed_password)

            if nurse.hashed_password == hashed:
                #print("PASSWORD MATCHED (NURSE)")
                return nurse
            #print("PASSWORD MISMATCH (NURSE)")

            
        # 2. Check admins
        if user_id in self.admins:
            admin = self.admins[user_id]
            # print("MATCHED ADMIN:", admin)
            # print("STORED HASH:", admin.hashed_password)

            if admin.hashed_password == hashed:
                #print("PASSWORD MATCHED (ADMIN)")
                return admin
        
        # 3. Invalid login
        # print("NO MATCH FOUND")
        return None


#Window Classes


#Login Window
class LoginWindow(QWidget):
    def __init__(self, manager, data_manager):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager

        self.setWindowTitle("Sample PyQt Window")
        self.setGeometry(600, 400, 1800, 1000)
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #D3D3D3;")
        
        #Text Labels

        self.title_text = QLabel("UT Health Patient Assignment Portal", self)
        layout.addWidget(self.title_text, alignment=Qt.AlignCenter)

        #Frame Setup
        
        self.login_frame = QFrame()
        self.login_frame.setFrameShape(QFrame.Box)
        self.login_frame.setFrameShadow(QFrame.Raised)
        self.login_frame.setLineWidth(3)
        self.login_frame.setStyleSheet("""
QFrame {
    background-color: #f77f00;
    border-radius: 20px;                                                                                                         
    }
""")
        self.frame_layout = QVBoxLayout()
        self.frame_layout
        layout.addWidget(self.login_frame)
        self.login_frame.setLayout(self.frame_layout)
        

        #Logo Setup

        UT_logo = QLabel()
        pixmap = QPixmap("C:\\Users\\ptbjr\\Pictures\\UTK_logo.png")
        UT_logo.setPixmap(pixmap)
        UT_logo.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        pixmap = pixmap.scaled(500,500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        UT_logo.setPixmap(pixmap)
        layout.addWidget(UT_logo)
        
        #Entry Setup

        self.user_entry = QLineEdit()
        self.user_entry.setPlaceholderText("Nurse ID")
        self.user_entry.setFixedSize(800,50)
        self.frame_layout.addWidget(self.user_entry, alignment=Qt.AlignCenter)

        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Password")
        self.password_entry.setFixedSize(800,50)
        self.frame_layout.addWidget(self.password_entry, alignment=Qt.AlignCenter)

        #Button Setup

        self.button = QPushButton("Login")
        self.button.clicked.connect(lambda: self.attempt_login())
        self.frame_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.button.setFixedSize(200,100)

        self.setLayout(layout)

        self.title_text.setStyleSheet("""
    color: black;
    font-size: 90px;
    font-family: Verdana;
""")


    
    def attempt_login(self):
        user_id = self.user_entry.text()
        password = self.password_entry.text()

        print("\n--- LOGIN BUTTON DEBUG ---")
        print("USER ENTERED ID:", repr(user_id))
        print("USER ENTERED PW:", repr(password))

        user = self.data_manager.verify_login(user_id, password)

        print("VERIFY_LOGIN RETURNED:", user, type(user))

        if user is None:
            self.error_label.setText("Invalid credentials")
            print("Login failed for user:", user_id)
            return

        # Pass the user object to the next window
        self.manager.login_success(user)  

#Menu Window Class
class MenuWindow(QWidget):
    def __init__(self, manager, data_manager, nurse_user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.nurse_user = nurse_user

        #Window Setup
        self.setWindowTitle("Main Menu")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")

        #Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)

        top_bar = QHBoxLayout()
        layout.addLayout(top_bar)

        #Title Label
        title = QLabel("Main Menu")
        title.setFont(QFont("Verdana", 28))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        #Welcome Label
        welcome = QLabel(f"Welcome, Nurse {nurse_user.name}!")
        welcome.setFont(QFont("Verdana", 20))
        welcome.setStyleSheet("color: black;")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        

        #Buttons
        
        #Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFixedSize(250, 120)
        logout_button.setFont(QFont("Verdana", 20))
        logout_button.clicked.connect(lambda: self.manager.logout())
        top_bar.addWidget(logout_button, alignment=Qt.AlignLeft)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
            }
        """)
        frame.setFixedSize(1200, 600)

        grid_layout = QGridLayout()
        frame.setLayout(grid_layout)

        # Add 4 buttons in a 2x2 layout
        self.btn1 = QPushButton("My Profile")
        self.btn1.setFont(QFont("Verdana", 20))
        self.btn1.clicked.connect(lambda : self.manager.switch(ProfileWindow, self.nurse_user))
        self.btn2 = QPushButton("New Patient")
        self.btn2.setFont(QFont("Verdana", 20))
        self.btn2.clicked.connect(lambda : self.manager.switch(NewPatientWindow, self.nurse_user))
        self.btn3 = QPushButton("Import Patient \n Data")
        self.btn3.setFont(QFont("Verdana", 20))
        self.btn4 = QPushButton("Patient Directory")
        self.btn4.clicked.connect(lambda : self.manager.switch(PatientDirectoryWindow, self.nurse_user))
        self.btn4.setFont(QFont("Verdana", 20))


        grid_layout.addWidget(self.btn1, 0, 0)
        grid_layout.addWidget(self.btn2, 0, 1)
        grid_layout.addWidget(self.btn3, 1, 0)
        grid_layout.addWidget(self.btn4, 1, 1)

        for btn in self.btn1, self.btn2, self.btn3, self.btn4:
            btn.setFixedSize(500,200)
        
        layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(layout)

#New Patient Window Class
class NewPatientWindow(QWidget):
    def __init__(self, manager, data_manager, nurse_user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.nurse_user = nurse_user
        
        #Window Setup
        #Frame is VBox with two QHBoxLayouts inside, top_frame for text & return button
        #  and bottom_frame for selection frame and entry frame
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
            #Window Organization

        top_frame = QFrame()
        top_frame_layout = QHBoxLayout()
        top_frame.setLayout(top_frame_layout)
        layout.addWidget(top_frame)
        top_frame_layout.setAlignment(Qt.AlignTop)

        bottom_frame = QFrame()
        bottom_frame_layout = QHBoxLayout()
        bottom_frame.setLayout(bottom_frame_layout)
        layout.addWidget(bottom_frame)
        bottom_frame_layout.setAlignment(Qt.AlignBottom)

        entry_frame = QFrame()
        entry_frame_layout = QVBoxLayout()
        bottom_frame_layout.addWidget(entry_frame)
        entry_frame.setLayout(entry_frame_layout)
        entry_frame_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        entry_frame_layout.setSpacing(20)

        selection_frame = QFrame()
        selection_layout = QGridLayout()
        bottom_frame_layout.addWidget(selection_frame, alignment=Qt.AlignRight)
        selection_frame.setLayout(selection_layout)

        self.setLayout(layout)

        #Top Frame Widgets

        self.setWindowTitle("New Patient")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")
        
        self.return_button = QPushButton("Return to Menu")
        self.return_button.setFixedSize(200,100)
        self.return_button.clicked.connect(lambda : self.manager.switch(MenuWindow, self.nurse_user))
        top_frame_layout.addWidget(self.return_button, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        
        #Text Labels
        self.title_text = QLabel("Add New Patient", self)
        self.title_text.setFont(QFont("Verdana", 28))
        top_frame_layout.addWidget(self.title_text, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.title_text.setStyleSheet("""
    color: black;
    font-size: 90px; #Fix this to be css style
    font-family: Verdana;
""")

        #Entry Frame Setup
        
        
        #Entry Setup
        self.patient_name_entry = QLineEdit()
        self.patient_name_entry.setPlaceholderText("Patient Name")
        self.patient_name_entry.setFixedSize(400,80)
        entry_frame_layout.addWidget(self.patient_name_entry)

        self.mrn_entry = QLineEdit()
        self.mrn_entry.setPlaceholderText("Medical Record Number (MRN)")
        self.mrn_entry.setFixedSize(400,80)
        entry_frame_layout.addWidget(self.mrn_entry)

        self.dob_entry = QLineEdit()
        self.dob_entry.setPlaceholderText("Date of Birth (MM/DD/YYYY)")
        self.dob_entry.setFixedSize(400,80)
        entry_frame_layout.addWidget(self.dob_entry)

        self.admission_entry = QLineEdit()
        self.admission_entry.setPlaceholderText("Admission Date (MM/DD/YYYY)")
        self.admission_entry.setFixedSize(400,80)
        entry_frame_layout.addWidget(self.admission_entry)

        self.room_num_entry = QLineEdit()
        self.room_num_entry.setPlaceholderText("Room Number")
        self.room_num_entry.setFixedSize(400,80)
        entry_frame_layout.addWidget(self.room_num_entry)

        entry_font = QFont("Verdana", 20)

        self.patient_name_entry.setFont(entry_font)
        self.mrn_entry.setFont(entry_font)
        self.dob_entry.setFont(entry_font)
        self.admission_entry.setFont(entry_font)
        self.room_num_entry.setFont(entry_font)

        entry_style = """
            QLineEdit {
                background-color: white;
                font-size: 30px;
                font-family: Verdana;
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 6px;
                }"""
        self.patient_name_entry.setStyleSheet(entry_style)
        self.mrn_entry.setStyleSheet(entry_style)
        self.dob_entry.setStyleSheet(entry_style)
        self.admission_entry.setStyleSheet(entry_style)
        self.room_num_entry.setStyleSheet(entry_style)

        self.save_patient_button = QPushButton("Save Patient")
        self.save_patient_button.setFont(QFont("Verdana", 16))
        self.save_patient_button.setFixedSize(350, 100)
        entry_frame_layout.addWidget(self.save_patient_button, alignment=Qt.AlignCenter)
        self.save_patient_button.clicked.connect(lambda : self.save_patient())
        #Selection Frame
        
        selection_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 15px;
                border: 2px solid #cccccc;
                }""")
        selection_frame.setFixedSize(1200, 900)
        treatment_title = QLabel("Select Treatment needs:")
        treatment_title.setFont(QFont("Verdana", 15))
        treatment_title.setStyleSheet("""
                    QLabel{
                        background-color: #D3D3D3;
                        font-family: Verdana;
                        }""")
        treatment_title.setFixedSize(750,80)

        selection_layout.addWidget(treatment_title, 0, 0, alignment=Qt.AlignCenter)
        
        treatment_types = ["Neurological:", "Psychosocial:", "Safety:", "Hemodynamic \nStability:", "Drains:", "ADLs:", "Meds:", "Wound Care:", "Discharge:"]
        
        self.treatment_dropdowns = []

        for i in range(len(treatment_types)):
            
            treatment_label = QLabel(treatment_types[i])
            treatment_label.setFont(QFont("Verdana", 15 ))
            treatment_label.setAlignment(Qt.AlignTop)
            treatment_label.setStyleSheet("""
                    QLabel{
                        background-color: #D3D3D3;
                        font-family: Verdana;
                        }""")
            selection_layout.addWidget(treatment_label, (1+2*(i//3)), i%3, alignment=Qt.AlignBottom)
            dropdown = QComboBox()
            dropdown.setFont(QFont("Verdana", 10))
            dropdown.addItems(["None", "Low", "Medium", "High"])
            dropdown.setStyleSheet("""
                    QComboBox{
                        background-color: white;
                        font-family: Verdana;
                        }
                    QComboBox QAbstractItemView {
                        background-color: white;
                        selection-background-color: #f77f00;
                        }""")
            selection_layout.addWidget(dropdown, (2+2*(i//3)), i%3, alignment=Qt.AlignTop)
            self.treatment_dropdowns.append(dropdown)

            severity_map = {
            "None": 0,
            "Low": 1,
            "Moderate": 2,
            "High": 3
            }


    
    def save_patient(self):
        name = self.patient_name_entry.text()
        dob = self.dob_entry.text()
        mrn = self.mrn_entry.text()
        admission = self.admission_entry.text()
        room = self.room_num_entry.text()

        severity_map = {
        "None": 0,
        "Low": 1,
        "Medium": 2,
        "High": 3
        }

        treatment_needs = [
            severity_map[dropdown.currentText()]
            for dropdown in self.treatment_dropdowns
            ]

        patient = Patient(
            name=name,
            dob=dob,
            mrn=mrn,
            admission_date=admission,
            room=room,
            treatment_needs=treatment_needs
        )

        self.data_manager.add_patient(patient)

        #Clear entries and dropdowns
        self.patient_name_entry.clear()
        self.dob_entry.clear()
        self.mrn_entry.clear()
        self.admission_entry.clear()
        self.room_num_entry.clear()

        for dropdown in self.treatment_dropdowns:
            dropdown.setCurrentIndex(0)

        QMessageBox.information(self, "Saved", "Patient saved successfully.")
        self.manager.switch(MenuWindow, self.nurse_user)

#Profile Window Class
class ProfileWindow(QWidget):
    def __init__(self, manager, data_manager, nurse_user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.nurse_user = nurse_user

        self.setWindowTitle("My Profile") 
        self.setGeometry(600, 400, 1800, 1000)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: #D3D3D3;")

        top_frame = QFrame()
        top_frame_layout = QHBoxLayout()
        top_frame.setLayout(top_frame_layout)

        self.return_button = QPushButton("Return to Menu")
        self.return_button.setFixedSize(200,100)
        self.return_button.clicked.connect(lambda : self.manager.switch(MenuWindow, self.nurse_user))
        top_frame_layout.addWidget(self.return_button, alignment=Qt.AlignTop | Qt.AlignLeft)


        profile_label = QLabel("Profile for: Nurse [Name]")
        profile_label.setFont(QFont("Verdana", 28))
        profile_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        profile_label.setStyleSheet("color: black;")
        top_frame_layout.addWidget(profile_label)

        layout.addWidget(top_frame)

        workload_frame = QFrame()
        workload_layout = QGridLayout()
        workload_frame.setFixedSize(1500, 800)
        workload_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
                }""")
        workload_frame.setLayout(workload_layout)
        layout.addWidget(workload_frame, alignment=Qt.AlignCenter)
        
        #Workload Frame Widgets

        # ---------- TOP ROW: LABELS ----------
        label1 = QLabel("Last Workload")
        label1.setAlignment(Qt.AlignCenter)
        label1.setFixedSize(600,50)
        label1.setFont(QFont("Verdana", 15))
        label1.setStyleSheet("""background-color: #D3D3D3""")
        label2 = QLabel("Today's Workload")
        label2.setAlignment(Qt.AlignCenter)
        label2.setFixedSize(600,50)
        label2.setFont(QFont("Verdana", 15))
        label2.setStyleSheet("""background-color: #D3D3D3""")

        workload_layout.addWidget(label1, 0, 0)
        workload_layout.addWidget(label2, 0, 1)

        #For patient in today's list of patients, add widget
        #For patient in yesterday's list of patients, add widget
        #At end of each day save today's list to yesterday's list and clear today's list
        # Left VBox
        left_box = QVBoxLayout()
        left_box.addWidget(QLabel("Left VBox Item 1"))
        left_box.addWidget(QLabel("Left VBox Item 2"))

        # Right VBox
        right_box = QVBoxLayout()
        right_box.addWidget(QLabel("Right VBox Item 1"))
        right_box.addWidget(QLabel("Right VBox Item 2"))

        # Add the VBoxes to the grid using QWidget containers
        left_container = QWidget()
        left_container.setLayout(left_box)

        right_container = QWidget()
        right_container.setLayout(right_box)

        workload_layout.addWidget(left_container, 1, 0)
        workload_layout.addWidget(right_container, 1, 1)

#Patient Directory Window Class
class PatientDirectoryWindow(QWidget):
    def __init__(self, manager, data_manager, nurse_user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.nurse_user = nurse_user

        self.setWindowTitle("Patient Directory") 
        self.setGeometry(600, 400, 1800, 1000)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("background-color: #D3D3D3;")

        top_frame = QFrame()
        top_frame_layout = QHBoxLayout()
        top_frame.setLayout(top_frame_layout)
        layout.addWidget(top_frame)
        top_frame_layout.setAlignment(Qt.AlignTop)

        bottom_frame = QFrame()
        bottom_frame_layout = QVBoxLayout()
        bottom_frame.setLayout(bottom_frame_layout)
        layout.addWidget(bottom_frame)
        bottom_frame_layout.setAlignment(Qt.AlignBottom)

        bottom_frame.setStyleSheet("""
            QFrame {
                background-color: #D3D3D3;
                border-radius: 20px;
                border: none;
                }""")
        

        self.return_button = QPushButton("Return to Menu")
        self.return_button.setFixedSize(200,100)
        self.return_button.clicked.connect(lambda : self.manager.switch(MenuWindow, self.nurse_user))
        top_frame_layout.addWidget(self.return_button, alignment=Qt.AlignTop | Qt.AlignLeft)


        profile_label = QLabel("Patient Directory")
        profile_label.setFont(QFont("Verdana", 28))
        profile_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        profile_label.setStyleSheet("color: black;")
        top_frame_layout.addWidget(profile_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        bottom_frame_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)
        content.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        content.setStyleSheet("""
            QWidget {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
                }""")

        header = QFrame()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        header.setStyleSheet("""
        QFrame {
        background-color: #D3D3D3;
        border: none;
        }""")
        header.setFixedHeight(80)
        labels = ["Patient Name", "MRN", "DOB", "Room Number", "View Patient"]
        for text in labels:
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight: bold; font-size: 30px;")
            header_layout.addWidget(lbl, stretch=1)
            lbl.setAlignment(Qt.AlignCenter)
        header_layout.addStretch()
        
     

        content_layout.addWidget(header)

        for i, patient in enumerate(self.data_manager.patients.values()):
            row = QFrame()
            row_layout = QHBoxLayout()
            row.setLayout(row_layout)

        #Placeholder patient data, replace with loop through patient list
            row_layout.setContentsMargins(4, 2, 4, 2)
            row_layout.setSpacing(4)

            name = QLabel(patient.name)
            mrn = QLabel(patient.mrn)
            dob = QLabel(patient.dob)
            room = QLabel(patient.room)
            for lbl in (name, mrn, dob, room):
                lbl.setStyleSheet("font-size: 26px; padding: 0px; border: none; color: black; background-color: #D3D3D3;")

            row.setStyleSheet("""
                QFrame {
                    background-color: #D3D3D3;
                    border-radius: 10px;
                    border: none;
                    }""")

            row_layout.addWidget(name, stretch=2, alignment=Qt.AlignCenter)
            row_layout.addWidget(mrn, stretch=1, alignment=Qt.AlignCenter)
            row_layout.addWidget(dob, stretch=2, alignment=Qt.AlignCenter)
            row_layout.addWidget(room, stretch=2)

            row.setFixedHeight(80)
            
            row_layout.addStretch()

            view_btn = QPushButton("View Patient")
            view_btn.setFixedSize(180, 50)
            view_btn.setFont(QFont("Verdana", 10))
            view_btn.setStyleSheet("""
                QPushButton {
                    border-radius: 15px;
                    }""")
            row_layout.addWidget(view_btn, alignment=Qt.AlignCenter)

            content_layout.addWidget(row)

#Admin Menu Window Class
class AdminMenuWindow(QWidget):
    def __init__(self, manager, data_manager, admin_user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.admin_user = admin_user
        

        #Window Setup
        self.setWindowTitle("Admin Menu")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")

        #Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)

        #Logout Button
        logout_button = QPushButton("Logout")
        logout_button.setFixedSize(250, 120)
        logout_button.setFont(QFont("Verdana", 20))
        logout_button.clicked.connect(lambda: self.manager.logout())
        layout.addWidget(logout_button, alignment=Qt.AlignLeft)

        #Title Label
        title = QLabel("Admin Menu")
        title.setFont(QFont("Verdana", 28))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        #Welcome Label
        welcome = QLabel(f"Welcome, Nurse {admin_user.name}!")
        welcome.setFont(QFont("Verdana", 20))
        welcome.setStyleSheet("color: black;")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)

        top_bar = QHBoxLayout()

        #Buttons
        top_button = QPushButton("Top Left")
        top_button.setFixedSize(120, 40)
        top_bar.addWidget(top_button, alignment=Qt.AlignLeft)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
            }
        """)
        frame.setFixedSize(1200, 600)

        grid_layout = QGridLayout()
        frame.setLayout(grid_layout)

        # Add 6 buttons in a 2x3 layout

        self.btn1 = QPushButton("New \n Nurse")
        self.btn1.clicked.connect(lambda: self.manager.switch(NewNurseWindow, self.admin_user))
        self.btn1.setFont(QFont("Verdana", 15))

        self.btn2 = QPushButton("Import \n Nurses")
        self.btn2.clicked.connect(lambda: self.manager.switch(ImportNursesWindow))
        self.btn2.setFont(QFont("Verdana", 15))
        
        self.btn3 = QPushButton("Nurse \n Directory")
        self.btn3.clicked.connect(lambda: self.manager.switch(NurseDirectoryWindow, self.admin_user))
        self.btn3.setFont(QFont("Verdana", 15))

        self.btn4 = QPushButton("Patient \n Directory")
        self.btn4.clicked.connect(lambda: self.manager.switch(PatientDirectoryWindow, self.admin_user))
        self.btn4.setFont(QFont("Verdana", 15))

        self.btn5 = QPushButton("Assign \n Patients")
        self.btn5.setFont(QFont("Verdana", 15))
        
        self.btn6 = QPushButton("Import \n Patients")
        self.btn6.setFont(QFont("Verdana", 15))

        grid_layout.addWidget(self.btn1, 0, 0)
        grid_layout.addWidget(self.btn2, 0, 1)
        grid_layout.addWidget(self.btn3, 0, 2)
        grid_layout.addWidget(self.btn4, 1, 0)
        grid_layout.addWidget(self.btn5, 1, 1)
        grid_layout.addWidget(self.btn6, 1, 2)

        for btn in self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6:
            btn.setFixedSize(300,200)
        
        layout.addWidget(frame, alignment=Qt.AlignCenter)
        self.setLayout(layout)

#New Nurse Window Class
class NewNurseWindow(QWidget):
    def __init__(self, manager , data_manager, admin_user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.admin_user = admin_user

        # Window Setup
        self.setWindowTitle("New Nurse")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")

        # Main Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Title + Return Button Layout 
        top_bar = QHBoxLayout()
        top_bar.setSpacing(20)

        return_button = QPushButton("Return to \n Menu")
        return_button.setFont(QFont("Verdana", 10))
        return_button.setFixedSize(200, 100)
        return_button.clicked.connect(lambda : self.manager.switch(AdminMenuWindow, self.admin_user))

        title = QLabel("Add New Nurse")
        title.setFont(QFont("Verdana", 28))
        title.setAlignment(Qt.AlignCenter)

        # Add title and return button to top bar
        top_bar.addWidget(return_button, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=1)
        top_bar.addWidget(title, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=2)

        main_layout.addLayout(top_bar)
        main_layout.addStretch(1)

        # Form Frame (orange card)
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
            }
        """)
        form_frame.setFixedSize(1000, 600)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_frame.setLayout(form_layout)

        main_layout.addWidget(form_frame, alignment=Qt.AlignCenter)
        main_layout.addStretch(2)

        # Input Fields
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Nurse Name")
        self.name_field.setFixedSize(650, 100)

        self.id_field = QLineEdit()
        self.id_field.setPlaceholderText("Nurse ID")
        self.id_field.setFixedSize(650, 100)

        self.unit_field = QLineEdit()
        self.unit_field.setPlaceholderText("Assigned Unit")
        self.unit_field.setFixedSize(650, 100)

        # Style for all fields
        field_style = """
            QLineEdit {
                background-color: white;
                font-size: 28px;
                font-family: Verdana;
                padding: 8px;
                border: 1px solid #aaa;
                border-radius: 6px;
            }
        """

        for field in (self.name_field, self.id_field, self.unit_field):
            field.setStyleSheet(field_style)
            form_layout.addWidget(field, alignment=Qt.AlignCenter)

        # Save Button
        save_button = QPushButton("Save Nurse")
        save_button.setFont(QFont("Verdana", 16))
        save_button.setFixedSize(350, 100)
        form_layout.addWidget(save_button, alignment=Qt.AlignCenter)
        save_button.clicked.connect(self.save_nurse)

    def save_nurse(self):
        name = self.name_field.text().strip()
        nurse_id = self.id_field.text().strip()
        unit = self.unit_field.text().strip()

        if not name or not nurse_id or not unit:
            print("All fields required")
            return
        
        #add_nurse(name, nurse_id, unit, working=True)
        print("Nurse saved!")

#Nurse Directory
class NurseDirectoryWindow(QWidget):
    def __init__(self, manager, data_manager):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager


        self.setWindowTitle("Nurse Directory")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")

        # MAIN LAYOUT
        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- TOP FRAME ---
        top_frame = QFrame()
        top_frame_layout = QHBoxLayout()
        top_frame.setLayout(top_frame_layout)
        layout.addWidget(top_frame)
        top_frame_layout.setAlignment(Qt.AlignTop)

        # Return Button
        return_button = QPushButton("Return to Menu")
        return_button.setFixedSize(200, 100)
        return_button.clicked.connect(self.return_to_admin)
        top_frame_layout.addWidget(return_button, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=1)

        # Title
        title = QLabel("Nurse Directory")
        title.setFont(QFont("Verdana", 28))
        title.setAlignment(Qt.AlignCenter)
        top_frame_layout.addWidget(title, alignment=Qt.AlignTop | Qt.AlignLeft, stretch=2)

        # --- BOTTOM ORANGE FRAME ---
        bottom_frame = QFrame()
        bottom_frame_layout = QVBoxLayout()
        bottom_frame.setLayout(bottom_frame_layout)
        layout.addWidget(bottom_frame)

        bottom_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
            }
        """)

        # --- SCROLL AREA ---
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        bottom_frame_layout.addWidget(scroll)

        content = QWidget()
        scroll.setWidget(content)
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)

        # --- HEADER ROW ---
        header = QFrame()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        header.setStyleSheet("""
            QFrame {
                background-color: #e0e0e0;
                border-radius: 8px;
            }
        """)

        labels = ["Nurse Name", "ID", "Unit", "Status", "Patients"]
        for text in labels:
            lbl = QLabel(text)
            lbl.setStyleSheet("font-weight: bold; font-size: 30px;")
            lbl.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(lbl, stretch=1)

        content_layout.addWidget(header)

        # --- LOAD NURSES ---
        nurses = load_nurses()
        if not nurses:
            nurses = [
                {"name": "Alice Brown", "id": "N001", "unit": "ICU", "working": True},
                {"name": "David Smith", "id": "N002", "unit": "ER", "working": False},
                {"name": "Maria Lopez", "id": "N003", "unit": "Pediatrics", "working": True},
            ]

        nurses = sorted(nurses, key=lambda x: x["name"])

        # --- NURSE ROWS ---
        for nurse in nurses:
            row = QFrame()
            row_layout = QHBoxLayout()
            row.setLayout(row_layout)

            # Row background color
            if nurse["working"]:
                row.setStyleSheet("background-color: lightgreen; border-radius: 8px;")
            else:
                row.setStyleSheet("background-color: lightgray; border-radius: 8px;")

            # Labels
            name = QLabel(nurse["name"])
            nurse_id = QLabel(nurse["id"])
            unit = QLabel(nurse["unit"])
            status = QLabel("Working" if nurse["working"] else "Not Working")

            for lbl in (name, nurse_id, unit, status):
                lbl.setStyleSheet("font-size: 26px; padding: 0px; border: none;")
                lbl.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(lbl, stretch=1)

            # Patients Button
            view_btn = QPushButton("View Patients")
            view_btn.setFixedSize(180, 50)
            view_btn.setFont(QFont("Verdana", 10))
            row_layout.addWidget(view_btn, alignment=Qt.AlignCenter)

            content_layout.addWidget(row)

    def return_to_admin(self):
        self.manager.switch(AdminWindow)

#Import Nurse
class ImportNursesWindow(QWidget):
    def __init__(self, manager, data_manager):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager


        self.setWindowTitle("Import Nurses")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")

        #Main Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #Top Bar
        top_bar = QHBoxLayout()
        top_bar.setSpacing(20)

        return_button = QPushButton("Return to \n Menu")
        return_button.setFont(QFont("Verdana", 10))
        return_button.setFixedSize(200, 100)
        return_button.clicked.connect(self.return_to_admin)

        title = QLabel("Import Nurses")
        title.setFont(QFont("Verdana", 28))
        title.setAlignment(Qt.AlignCenter)

        top_bar.addWidget(return_button, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=1)
        top_bar.addWidget(title, alignment=Qt.AlignLeft | Qt.AlignTop, stretch=2)

        layout.addLayout(top_bar)
        layout.addStretch(1)

        # Form Frame (orange card)
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
            }
        """)
        form_frame.setFixedSize(1000, 600)

        form_layout = QVBoxLayout()
        form_layout.setAlignment(Qt.AlignCenter)
        form_frame.setLayout(form_layout)

        layout.addWidget(form_frame, alignment=Qt.AlignCenter)
        layout.addStretch(2)

        import_button = QPushButton("Choose \n CSV File")
        import_button.setFont(QFont("Verdana", 15))
        import_button.setFixedSize(600, 200)
        import_button.clicked.connect(self.import_csv)
        form_layout.addWidget(import_button)

        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Verdana", 16))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("background-color: transparent;")
        form_layout.addWidget(self.status_label)

    def import_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")

        if not file_path:
            self.status_label.setText("No file selected.")
            return

        try:
            with open(file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    name = row.get("name", "").strip()
                    nurse_id = row.get("id", "").strip()
                    unit = row.get("unit", "").strip()
                    working = row.get("working", "1").strip() == "1"

                    if name and nurse_id and unit:
                        add_nurse(name, nurse_id, unit, working)

            self.status_label.setText("Import successful!")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")

#Patient View Window Class
class PatientProfileWindow(QWidget):
    def __init__(self, manager, data_manager, patient, user):
        super().__init__()
        self.manager = manager
        self.data_manager = data_manager
        self.patient = patient
        self.user = user

    def init_ui(self):
        layout = QVBoxLayout()

        # -------------------------
        # HEADER SECTION
        # -------------------------
        header = QLabel(f"{self.patient.name}")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(header)

        layout.addWidget(QLabel(f"MRN: {self.patient.patient_id}"))
        layout.addWidget(QLabel(f"DOB: {self.patient.dob}"))
        layout.addWidget(QLabel(f"Room: {self.patient.room}"))

        # -------------------------
        # CLINICAL INFO SECTION
        # -------------------------
        clinical_group = QGroupBox("Clinical Information")
        clinical_layout = QVBoxLayout()

        clinical_layout.addWidget(QLabel(f"Acuity: {self.patient.acuity}"))
        clinical_layout.addWidget(QLabel(f"Mobility: {self.patient.mobility}"))
        clinical_layout.addWidget(QLabel(f"Isolation: {self.patient.isolation}"))
        clinical_layout.addWidget(QLabel(f"Special Needs: {self.patient.special_needs}"))

        clinical_group.setLayout(clinical_layout)
        layout.addWidget(clinical_group)

        # -------------------------
        # ASSIGNMENT SECTION
        # -------------------------
        assignment_group = QGroupBox("Assignment")
        assignment_layout = QVBoxLayout()

        nurse_name = (
            self.patient.current_nurse.name
            if self.patient.current_nurse else "None"
        )
        assignment_layout.addWidget(QLabel(f"Current Nurse: {nurse_name}"))

        if isinstance(self.user, Nurse):
            assign_btn = QPushButton("Assign to Me")
            assign_btn.clicked.connect(self.assign_to_self)
            assignment_layout.addWidget(assign_btn)

            send_admin_btn = QPushButton("Send to Admin")
            send_admin_btn.clicked.connect(self.send_to_admin)
            assignment_layout.addWidget(send_admin_btn)

        assignment_group.setLayout(assignment_layout)
        layout.addWidget(assignment_group)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def assign_to_self(self):
    # Update patient + nurse objects
        self.patient.assign_nurse(self.user)
        self.user.add_patient(self.patient)

        QMessageBox.information(self, "Assigned", "Patient assigned to you.")

    # Refresh window
        self.manager.switch(PatientProfileWindow, self.patient, self.user)

    def send_to_admin(self):
        QMessageBox.information(self, "Sent", "Patient sent to admin.")

    def go_back(self):
        if isinstance(self.user, Nurse):
            self.manager.switch(MenuWindow, self.user)
        else:
            self.manager.switch(AdminMenuWindow, self.user)



#Program initiation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    data_manager = DataManager()
    manager = WindowManager(data_manager)

        # TEST ADMIN
    admin = Admin(
        admin_id="A001",
        name="Kerry Cao",
        hashed_password=data_manager.hash_password("adminpass"),
        permissions=["all"]
    )
    data_manager.admins[admin.admin_id] = admin

    nurse = Nurse(
        nurse_id="N001",
        name="Patrick Burke",
        hashed_password=data_manager.hash_password("nursepass"),
        assigned_patients=[],
        last_workload=[],
        shift="day"
    )
    data_manager.nurses[nurse.nurse_id] = nurse

    manager.switch(LoginWindow)

    sys.exit(app.exec_()) 

