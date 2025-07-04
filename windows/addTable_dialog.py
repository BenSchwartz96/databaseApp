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
    QDialog,
    QComboBox
)
from PyQt6.QtCore import Qt

# NEXT TO-DO
# Debug the 'add table' function (which is currently just trying to show the text saved to the input fields)

dataTypes = ["text", "int", "bool"]


class AddTableDialog(QDialog):

    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.new_field_names = []
        self.new_field_types = []
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Add Table")
        self.resize(500, 600)
        self.setupLayout()
    
    def setupLayout(self):

        self.dataTypeDropdown = self.setupDropdown()
        self.dataTypeDropdown.setCurrentIndex(-1)
        self.dataTypeDropdown.setFixedWidth(75)

        self.vbox_1 = QVBoxLayout()
        table_name_label, field_name_label = self.setupLabels1()
        self.table_name_input = QLineEdit(self)
        first_field_input = QLineEdit(self)
        self.table_name_input.setFixedWidth(150)
        first_field_input.setFixedWidth(150)
        self.vbox_1.addStretch()
        self.vbox_1.addWidget(table_name_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox_1.addWidget(self.table_name_input, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox_1.addWidget(field_name_label, alignment=Qt.AlignmentFlag.AlignCenter)

        field_entry_container = QHBoxLayout()
        field_entry_container.addWidget(first_field_input)
        field_entry_container.addWidget(self.dataTypeDropdown)
        self.new_field_names.append(first_field_input)
        self.new_field_types.append(self.dataTypeDropdown)
        self.vbox_1.addLayout(field_entry_container)
        self.vbox_1.addStretch()

        vbox_2 = QVBoxLayout()
        vb2_label_1 = self.setupLabels2()
        vbox_2.addWidget(vb2_label_1, alignment=Qt.AlignmentFlag.AlignCenter)

        vbox_3 = QVBoxLayout()
        add_field_button, add_table_button = self.setupButtons()
        vbox_3.addStretch()
        vbox_3.addWidget(add_field_button)
        vbox_3.addWidget(add_table_button)
        vbox_3.addStretch()


        dialog_layout = QHBoxLayout()
        dialog_layout.addLayout(self.vbox_1)
        # dialog_layout.addLayout(vbox_2)
        dialog_layout.addLayout(vbox_3)
        self.setLayout(dialog_layout)

    def setupDropdown(self):
        global dataTypes
        self.dataTypeDropdown = QComboBox()
        self.dataTypeDropdown.addItems(dataTypes)
        return self.dataTypeDropdown
        # Now we want to populate the dropdown
        # Which will involve making a dataTypes list
        # then we go self.dropdown.addItems(dataTypes)

    def populateDropdown(self):
        pass
        # I dont think we need this.

    def setupLabels1(self):
        table_name_label = QLabel("Table Name")
        table_name_label.resize(200, 20)
        field_name_label = QLabel("Field Names + Data Types")
        field_name_label.resize(200, 20)
        return table_name_label, field_name_label
    
    def setupLabels2(self):
        label_1 = QLabel("Test")
        label_1.resize(200, 20)
        return label_1
    
    def setupButtons(self):
        add_field_button = QPushButton(self)
        add_field_button.setText("Add Field")
        add_field_button.clicked.connect(self.addField)

        add_table_button = QPushButton(self)
        add_table_button.setText("Add Table")
        add_table_button.setFixedWidth(100) #Seems to apply it to both buttons?
        add_table_button.clicked.connect(self.addTable)
        return add_field_button, add_table_button

    def addTable(self):
        new_table_name = self.table_name_input.text()
        sql_statement = self.buildSQL()
        print(sql_statement)
    # TODO: once we've got the proper SQL statement hooked up, we need to then make
    #       the add_table func in database.py, and call it here, with the statement as an arg.

    def buildSQL(self):
        # Validation
        if not self.new_field_names or not self.new_field_types:
            raise ValueError("There must be at least one field name + type.")
        if len(self.new_field_names) != len(self.new_field_types):
            raise ValueError("There must be the same number of field names and types.")
        # This validation isn't working properly. I think it's because there's always the same number of elements by default.
        # What I need to do is have it check if text is present WITHIN the elements or not. 
        
        fields_sql = []
        for name_input, type_input in zip(self.new_field_names, self.new_field_types):
            name = name_input.text()
            type = type_input.currentText()
            fields_sql.append(f'"{name}" {type}')
        return fields_sql
        # so we're currently returning the list of values.
        # TODO: actually construct the full statement and return that. 
        # TODO: fix the validation

        # Debug code.
        # for name, type in zip(self.new_field_names, self.new_field_types):
        #     print(name.text(), type.currentText())

    def addField(self):
        newField = QHBoxLayout()
        newInput = QLineEdit(self)
        newInput.setFixedWidth(150)
        dataTypeDropdown = self.setupDropdown()
        dataTypeDropdown.setCurrentIndex(-1)
        dataTypeDropdown.setFixedWidth(75)

        newField.addWidget(newInput)
        newField.addWidget(dataTypeDropdown)

        # Add the pair of input fields to a list so we have the data in them for when we click add table.
        self.new_field_names.append(newInput)
        self.new_field_types.append(dataTypeDropdown)

        # This line means the new Hbox gets inserted *before* the addStretch()
        self.vbox_1.insertLayout(self.vbox_1.count() -1, newField)