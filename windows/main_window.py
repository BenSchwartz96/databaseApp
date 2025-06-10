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
from database import fetch_table_data, fetch_table_names

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

        # tableNames = fetch_table_names()

        # QComboBox = Dropdown menu
        self.dropdown = QComboBox()
        self.populateDropdown()
        self.dropdown.setCurrentIndex(-1)

        # SET DROPDOWN TO DEFAULT TO NOT HAVING AN OPTION, RATHER THAN BE DEFAULT SET TO 'games'



        # currentTextChanged auto passes selected text to our function. Don't really get how though.
        self.dropdown.currentTextChanged.connect(self.dropdownOptionSelected)   

        grid_layout = QGridLayout()
        # grid_layout.addWidget(QLabel("Row 1"), 0, 0)
        # grid_layout.addWidget(QLabel("Row 2"), 1, 0)
        # grid_layout.addWidget(QLabel(""), 0, 0)
        # grid_layout.addWidget(QLabel(""), 1, 0)

        vbox1 = QVBoxLayout()
        vbox1.addSpacing(50)
        vbox1.addWidget(welcome_label)
        vbox1.addWidget(add_table_button)
        vbox1.addSpacing(70)

        # Should this even be here? Shouldn't I put it somewhere else like the setup buttons function?
        add_table_button.clicked.connect(self.addTableButtonClicked)

        # hbox1 = QHBoxLayout()
        # hbox1.addWidget(welcome_label)
        # hbox1.addWidget(add_table)
        hbox1_container = QWidget()
        hbox1_container.setLayout(vbox1)

        vbox2 = QVBoxLayout()
        vbox2_label = QLabel("Choose table:")
        vbox2.addSpacing(100)
        vbox2.addWidget(vbox2_label)
        vbox2.addWidget(self.dropdown)
        vbox2.addSpacing(100)

        # hbox2 = QHBoxLayout()
        # hbox2.addWidget(self.dropdown)
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
        # This doesn't work. I've ballsed it up. Lets try again tomorrow. 
    



    # Ok ive ballsed this up and this is definitely not how I should do this.
    # Like, I've done this here, but I should be doing it from Main, right? Idk. 
    def show_add_table(self):
        dialog = QDialog()
        dialog.setWindowTitle("Add Table")

        dialog_layout = QHBoxLayout()
        dialog.setLayout(dialog_layout)

        dialog.resize(1000, 200)
        dialog.exec()





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



# # Dummy widgets to define the 3x3 grid.
# grid_layout.addWidget(QLabel(), 0, 0)
# grid_layout.addWidget(QLabel(), 0, 2)
# grid_layout.addWidget(QLabel(), 2, 0)
# grid_layout.addWidget(QLabel(), 2, 2)