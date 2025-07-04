import sys
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
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

from windows.welcome_window import WelcomeWindow
from windows.main_window import MainWindow
from utils import centerWindow

class AppManager():
    
    def __init__(self):
        self.app = QApplication(sys.argv)

    def show_welcome(self):
        self.window = WelcomeWindow(self)
        centerWindow(self.window)
        self.window.show()

    def show_main(self):
        # The clause below is necessary for any window that we expect to replace another window.
        # Because the welcome window will never replace anything, we can skip this for that.
        if self.window:
            self.window.close()
        self.window = MainWindow(self)
        centerWindow(self.window)
        self.window.show()

    def run(self):
        self.show_welcome()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    AppManager().run()