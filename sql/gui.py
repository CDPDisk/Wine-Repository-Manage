#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import sqlite3
import PyQt5


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.pro_label = QComboBox()
        self.pro_label.setEditable(True)
        self.pro_label.addItems(['pro1', 'pro2', 'pro3', 'pro4', 'NULL'])
        # completer=QCompleter()
        # self.pro_label.setCompleter(completer)
        # model=QStringListModel()
        # model.setStringList(['pro1', 'pro2', 'pro3', 'pro4', 'other'])
        # completer.setModel(model)

        leftLayout = QGridLayout()
        leftLayout.addWidget(self.pro_label)
        self.setLayout(leftLayout)

    # Greets the user
    def greetings(self):
        print("Hello %s" % self.edit.text())


if __name__ == '__main__':
    print("My word")
    print(value, ..., sep, end, file, flush)
    print()
    print()
    #app = QApplication.instance()
    # Create the Qt Application
    #if app is None:
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
