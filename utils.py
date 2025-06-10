from PyQt6.QtWidgets import (
    QApplication,
)

# Generic function to center a window. 
def centerWindow(self):
    #Variable for the main monitor
    screen = QApplication.primaryScreen()
    #Variable representing the available screen geometry. 
    screen_geometry = screen.availableGeometry()
    # Variable representing the geometry of our window.
    window_geometry = self.frameGeometry()
    # Now we say that the center of the QRect representing the window should move to the center of the screen.
    window_geometry.moveCenter(screen_geometry.center())
    # Then we actually move it - note that windows are positioned by top left corner. 
    self.move(window_geometry.topLeft())