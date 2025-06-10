import sys
from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QWidget, 
    QPushButton, 
    QLabel, 
    QMessageBox, 
    QLineEdit, 
    QHBoxLayout, 
    QVBoxLayout, 
    QGridLayout
)
from PyQt6.QtCore import Qt


class WelcomeWindow(QWidget):
    
    # So, self is automatic, so manager is the 'self' passed in main.py, ie, its the instance of AppManager
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.initUI()
    

    def initUI(self):
        self.setWindowTitle("PyQt6 Database App")
        self.resize(400, 300)
        self.setupLayout()

        
    def setupLayout(self):
        layout = QVBoxLayout()
        layout.addStretch()
        
        welcome_label = self.setupLabels()
        layout.addWidget(welcome_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)

        # Alternative way to write this:
        # layout.addWidget(self.setupLabels(), alignment=Qt.AlignmentFlag.AlignCenter)

        enter_button = self.setupButtons()
        enter_button.clicked.connect(self.enterButtonClicked)
        layout.addWidget(enter_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

        self.setLayout(layout)


    def setupLabels(self):
        welcome_label = QLabel("Welcome to my PyQt6/PSQL database app!", self)
        welcome_label.resize(200, 20)
        return welcome_label


    def setupButtons(self):
        enter_button = QPushButton(self)
        enter_button.setText("Enter")
        return enter_button
    
    
    def enterButtonClicked(self):
        self.manager.show_main()
