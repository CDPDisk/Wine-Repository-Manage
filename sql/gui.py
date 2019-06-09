#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import adj
# import sqlite3
# import PyQt5


# Create an instance of the application window and run it


def loaddata(table):
    # 生成一个模型，用来给tableview
    model = QStandardItemModel()
    # 打开一个csv文件
    # 取出csv文件的头部，类型为list，赋值给headdata
    headdata = c.keys[table]
    # 从headdata中取出数据，放入到模型中
    for i in range(len(headdata)):
        item = QStandardItem(headdata[i])
        # 设置模型的水平头部
        model.setHorizontalHeaderItem(i, item)
    rown = 0
    # 从csv文件中取出数据，放入到模型中
    for data in c.select(table):
        for coln in range(len(data)):
            item = QStandardItem(data[coln])
            # 在模型的指定位置添加数据(item)
            model.setItem(rown, coln, item)
        rown += 1
    return model


def backupdata(rawmodel):
    model = QStandardItemModel()
    for i in range(rawmodel.columnCount()):
        item = QStandardItem(rawmodel.horizontalHeaderItem(i))
        model.setHorizontalHeaderItem(i, item)

    for i in range(rawmodel.rowCount()):
        for j in range(rawmodel.columnCount()):
            item = QStandardItem(rawmodel.item(i, j).text())
            model.setItem(i, j, item)
    return model


class Stack1(QDialog):
    def __init__(self, table):
        super(Stack1, self).__init__()
        self.table = table
        self.keys = c.keys[self.table]
        self.keysnum = len(self.keys)
        self.setFixedSize(150 * self.keysnum, 200)
        self.textbox = []
        self.label = []
        leftLayout = QGridLayout()
        self.default_value = adj.make_record(self.table).data
        for i in range(self.keysnum):
            self.label.append(QLabel(self.keys[i]))
            self.label[i].setAlignment(Qt.AlignCenter)
            self.label[i].setBaseSize(150, 20)

            self.textbox.append(
                QLineEdit(str(self.default_value[self.keys[i]])))
            self.textbox[i].setBaseSize(100, 20)

            leftLayout.addWidget(self.label[i], 0, i)
            leftLayout.addWidget(self.textbox[i], 1, i)
        self.button = QPushButton("提交")
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(self.push)
        leftLayout.addWidget(self.button, 2, 0, 1, len(
            self.keys) // 2, Qt.AlignCenter)
        self.setLayout(leftLayout)

    def push(self):
        record = adj.make_record(self.table)
        for i in range(self.keysnum):
            if self.textbox[i].text() == 'None':
                record.data[self.keys[i]] = None
            else:
                record.data[self.keys[i]] = self.textbox[i].text()
            # print(self.keys[i], ':', self.textbox[i].text())
        # print(record.data)
        # try:
        c.add(record)
        # except:
        # print("Add data happen error")
        for i in range(self.keysnum):
            self.textbox[i].setText(self.default_value[self.keys[i]])


class AddMenu(QDialog):
    def __init__(self):
        super(AddMenu, self).__init__()

        self.table_list = ['base', 'score', 'store']
        self.table_label = QComboBox()
        self.table_label.setFixedSize(100, 20)
        self.table_label.addItems(self.table_list)
        self.table_label.currentIndexChanged.connect(self.change)

        self.stack = QStackedWidget()
        self.stack.addWidget(Stack1('base'))
        self.stack.addWidget(Stack1('score'))
        self.stack.addWidget(Stack1('store'))
        leftLayout = QGridLayout()
        leftLayout.addWidget(self.table_label, 0, 2)
        leftLayout.addWidget(self.stack, 1, 0, 1, 3)
        self.setLayout(leftLayout)

    def change(self, index):
        self.stack.setCurrentIndex(index)
        h = self.stack.widget(index).height() + 20
        w = self.stack.widget(index).width() + 20
        self.setFixedSize(w, h)

    def run(self):
        self.show()


class stack2(QDialog):
    def __init__(self, table):
        super(stack2, self).__init__()
        self.tableview = QTableView()
        self.table = table
        self.model = loaddata(self.table)
        self.backmodel = backupdata(self.model)
        self.tableview.setModel(self.model)
        leftLayout = QGridLayout()
        leftLayout.addWidget(self.tableview)
        self.setLayout(leftLayout)
        self.model.itemChanged.connect(self.update)

    def update(self, item):
        col = self.model.columnCount()
        up_record = adj.make_record(self.table)
        for i in range(col):
            up_record.data[self.model.horizontalHeaderItem(
                i).text()] = self.model.item(item.row(), i).text()
        # try:
        c.update(up_record)
        self.backmodel = backupdata(self.model)
        # except:
        #     self.model = backupdata(self.backmodel)
        #     self.tableview.setModel(self.model)
        #     self.model.itemChanged.connect(self.update)
        #     print("数据更改错误")

    def brush(self):
        self.model = loaddata(self.table)
        self.backmodel = backupdata(self.model)
        self.tableview.setModel(self.model)
        self.model.itemChanged.disconnect()
        self.model.itemChanged.connect(self.update)


class MainMenu(QDialog):

    def __init__(self, parent=None):
        # super(MainMenu, self).__init__(parent)
        super(MainMenu, self).__init__()
        # Create widgets
        # self.resize(700, 500)

        self.setMinimumSize(600, 500)
        self.add_button = QPushButton('进口')
        self.add_button.setFixedSize(200, 70)
        self.add_button.clicked.connect(form1.run)

        self.del_button = QPushButton('出口')
        self.del_button.setFixedSize(200, 70)

        self.upd_button = QPushButton('更改')
        self.upd_button.setFixedSize(200, 70)

        self.bus_button = QPushButton('刷新')
        self.bus_button.setFixedSize(70, 50)

        self.table_list = ['base', 'score', 'store']
        self.table_label = QComboBox()
        self.table_label.setFixedSize(70, 20)
        self.table_label.addItems(self.table_list)
        self.table_label.currentIndexChanged.connect(self.change_table)

        self.stack = QStackedWidget()
        self.stack.addWidget(stack2('base'))
        self.stack.addWidget(stack2('score'))
        self.stack.addWidget(stack2('store'))

        leftLayout = QGridLayout()
        leftLayout.addWidget(self.add_button, 0, 0, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.del_button, 0, 1, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.upd_button, 0, 2, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.bus_button, 0, 3, 1, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.table_label, 1, 3, 1, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.stack, 2, 0, 1, 4)
        self.setLayout(leftLayout)

        self.index = self.table_label.currentIndex()
        self.bus_button.clicked.connect(self.stack.widget(self.index).brush)

    def change_table(self, index):
        self.stack.setCurrentIndex(index)
        self.index = index
        self.table = self.table_list[index]
        self.bus_button.clicked.disconnect()
        self.bus_button.clicked.connect(self.stack.widget(self.index).brush)
# Greets the user

    def add(self):
        pass

    def rm(self):
        pass


# app = QApplication.instance()
# Create the Qt Application
# if app is None:
c = adj.wine()
app = QApplication(sys.argv)
# Create and show the form
form1 = AddMenu()
form = MainMenu(form1)
form.show()

# Run the main Qt loop

app.exec_()
c.close()
