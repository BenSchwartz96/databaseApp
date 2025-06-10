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

class AddTableWindow(QWidget):

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Add Table")
        self.resize(800, 200)
        self.setupLayout()
    
    def setupLayout(self):
        pass
