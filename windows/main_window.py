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
    QGridLayout,
    QMenuBar,
    QTableView,
    QComboBox,
    QDialog
)
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem
from windows.addTable_dialog import AddTableDialog
from database import fetch_table_data, fetch_table_names
from utils import centerWindow

# Finish the new-table dialogue
# Insert a way to add/remove/edit data.


class MainWindow(QMainWindow):
    
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.initUI()
    

    def initUI(self):
        self.setWindowTitle("PyQt6 Database App")
        self.resize(1000, 600)
        self.setupLayout()
        self.createMenuBars()

        
    def setupLayout(self):
        # We cannot set a layout on QMainWindow, so we need to render a central widget to get our layout.
        # This will also serve to specify the 'main area' part of the window, excluding toolbars/menu bars.
        central_widget = QWidget()
        welcome_label = self.setupLabels()
        add_table_button = self.setupButtons()
        self.table = QTableView()

        # QComboBox means Dropdown menu
        self.dropdown = QComboBox()
        self.populateDropdown()
        self.dropdown.setCurrentIndex(-1)

        # currentTextChanged auto passes selected text to our function. Don't really get how though.
        self.dropdown.currentTextChanged.connect(self.dropdownOptionSelected)   

        grid_layout = QGridLayout()

        vbox1 = QVBoxLayout()
        vbox1.addSpacing(50)
        vbox1.addWidget(welcome_label)
        vbox1.addWidget(add_table_button)
        vbox1.addSpacing(70)

        hbox1_container = QWidget()
        hbox1_container.setLayout(vbox1)

        vbox2 = QVBoxLayout()
        vbox2_label = QLabel("Choose table:")
        vbox2.addSpacing(100)
        vbox2.addWidget(vbox2_label)
        vbox2.addWidget(self.dropdown)
        vbox2.addSpacing(100)

        hbox2_container = QWidget()
        hbox2_container.setLayout(vbox2)

        table_hbox = QHBoxLayout()
        table_hbox.addWidget(self.table)
        table_container = QWidget()
        table_container.setLayout(table_hbox)

        grid_layout.addWidget(hbox1_container, 1, 0)
        grid_layout.addWidget(hbox2_container, 1, 1)
        grid_layout.addWidget(table_container, 2, 0, 2, 3)      # Row 2, Col 0, Spans 2 rows and 3 columns.

        
        # self.fetchData()

        # The line below would be okay if this was a QWidget instead of a QMainWindow.
        # self.setLayout(layout)
        central_widget.setLayout(grid_layout)
        # Now setting this as the central widget.
        self.setCentralWidget(central_widget)

        # Shows some text in the bottom left.
        # self.statusBar().showMessage("Ready")

    def setupLabels(self):
        label_1 = QLabel("Welcome! Things are a bit sparse here at the moment, but we're working on it.")
        label_1.resize(200, 20)
        return label_1


    def setupButtons(self):
        button_add_table = QPushButton(self)
        button_add_table.setText("Add Table")
        button_add_table.clicked.connect(self.addTableButtonClicked)
        return button_add_table


    def dropdownOptionSelected(self, text):
        self.fetchTableData(text)
        # I used to call populateDropdown here, but that caused an issue.
        # Instead I should call it after adding or removing a table.

    def populateDropdown(self):
        tableNames = fetch_table_names()
        self.dropdown.clear()
        self.dropdown.addItems(tableNames)

    def addTableButtonClicked(self):
        self.show_add_table()
    

    def show_add_table(self):
        self.window = AddTableDialog(self)
        centerWindow(self.window)
        # The two lines below forbid interaction with main window while dialog is open.
        self.window.setModal(True)
        self.window.exec()
        # Once we have the ability to add a table, we're gonna need to call populateDropdown


    def createMenuBars(self):
        # Initialising menubar and adding menus to it
        # menu_bar = self.menuBar()
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)
        main_menu = menu_bar.addMenu("Menu")
        menu_2 = menu_bar.addMenu("Test")
        settings_menu = menu_bar.addMenu("Settings")

        # Actions
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        # Adding actions to the menus
        main_menu.addAction(exit_action)
        menu_2.addAction(exit_action)


    # This function is what presents the table with the game data.
    def fetchTableData(self, tableName):
        # Our imported function returns all column names, and all rows.
        columns, data = fetch_table_data(tableName)
        # We need a data model to connect to our table.
        model = QStandardItemModel()
        model.setColumnCount(len(columns))
        model.setHorizontalHeaderLabels(columns)
        for row in data:
            items = [QStandardItem(str(field)) for field in row]
            model.appendRow(items)
        # Line below assigns the new model to the table, which was made outside of this function. 
        self.table.setModel(model)