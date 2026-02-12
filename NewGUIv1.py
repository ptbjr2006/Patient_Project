import sys
from PyQt5.QtWidgets import QApplication, QFrame, QComboBox, QWidget, QLabel, QLineEdit, QGridLayout, QPushButton, QHBoxLayout, QVBoxLayout # type: ignore
from PyQt5.QtGui import QFont, QPixmap # type: ignore
from PyQt5.QtCore import Qt

#Window Classes

    #Login Window

class LoginWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

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
        self.button.clicked.connect(lambda: self.manager.switch(MenuWindow))
        self.frame_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.button.setFixedSize(200,100)

        self.setLayout(layout)

        self.title_text.setStyleSheet("""
    color: black;
    font-size: 90px;
    font-family: Verdana;
""")


    def login_click(self):
        #run for loop of usernames and for loop of passwords
        #send to Admin version or nurse version
        self.label.setText("Button clicked!")

#Menu Window Class

class MenuWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        #Window Setup
        self.setWindowTitle("Main Menu")
        self.setGeometry(600, 400, 1800, 1000)
        self.setStyleSheet("background-color: #D3D3D3;")

        #Layout
        layout = QVBoxLayout()
        layout.setSpacing(20)

        #Title Label
        title = QLabel("Main Menu")
        title.setFont(QFont("Verdana", 28))
        title.setStyleSheet("color: black;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
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

        # Add 4 buttons in a 2x2 layout
        self.btn1 = QPushButton("My Profile")
        self.btn1.setFont(QFont("Verdana", 20))

        self.btn2 = QPushButton("New Patient")
        self.btn2.setFont(QFont("Verdana", 20))
        self.btn2.clicked.connect(lambda : self.manager.switch(NewPatientWindow))
        self.btn3 = QPushButton("Import Patient \n Data")
        self.btn3.setFont(QFont("Verdana", 20))

        self.btn4 = QPushButton("Patient Directory")
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
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        
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
        self.return_button.clicked.connect(lambda : self.manager.switch(MenuWindow))
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

        #Selection Frame
        
        selection_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
                }""")
        selection_frame.setFixedSize(1200, 900)
        treatment_title = QLabel("Select Treatment needs:")
        treatment_title.setFont(QFont("Verdana", 20))
        treatment_title.setStyleSheet("""
                    QLabel{
                        background-color: #D3D3D3;
                        font-family: Verdana;
                        }""")
        treatment_title.setFixedSize(750,80)

        selection_layout.addWidget(treatment_title, 0, 0, alignment=Qt.AlignCenter)
        
        treatment_types = ["Neurological:", "Psychosocial:", "Safety:", "Hemodynamic \nStability:", "Drains:", "ADLs:", "Meds:", "Wound Care:", "Discharge:"]
        
        for i in range(len(treatment_types)):
            print(i)
            treatment_label = QLabel(treatment_types[i])
            treatment_label.setFont(QFont("Verdana", 20))
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
'''
# Profile Window Class
class ProfileWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager

        self.setWindowTitle("My Profile") 
        self.setGeometry(600, 400, 1800, 1000)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.return_button = QPushButton("Return to Menu")
        self.return_button.setFixedSize(200,100)
        self.return_button.clicked.connect(lambda : self.manager.switch(MenuWindow))
        layout.addWidget(self.return_button, alignment=Qt.AlignTop | Qt.AlignLeft)

        profile_label = QLabel("Profile for: Nurse [Name]")
        profile_label.setFont(QFont("Verdana", 28))
        profile_label.setStyleSheet("color: black;")
        profile_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(profile_label)

        

        workload_frame = QFrame()
        workload_layout = QGridLayout()
        workload_frame.setStyleSheet("""
            QFrame {
                background-color: #f77f00;
                border-radius: 20px;
                border: 2px solid #cccccc;
                }""")
        workload_frame.setLayout(workload_layout)
        layout.addWidget(workload_frame, alignment=Qt.AlignCenter)

        #Workload Frame Widgets
'''

#Window Manager Class

class WindowManager:
    def __init__(self):
          self.current = None

    def switch(self, new_window):
        if self.current is not None:
          self.current.close()
        self.current = new_window(self)
        self.current.show()
     
        

        


# Global Functions

    #Button function to change windows

def open_new_window(current_window, new_window_class):
        new_window = new_window_class()
        new_window.show()
        current_window.close()
        return new_window


#Program initiation

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    manager = WindowManager()
    manager.switch(LoginWindow)

    sys.exit(app.exec_()) 
