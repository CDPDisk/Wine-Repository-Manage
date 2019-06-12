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


def loaddata(table, check=False):
    # 生成一个模型，用来给tableview
    model = QStandardItemModel()
    # 打开一个csv文件
    # 取出csv文件的头部，类型为list，赋值给headdata
    headdata = c.keys[table]
    # 从headdata中取出数据，放入到模型中
    # if check is True:
    #    item = QStandardItem(' ')
    #    # 设置模型的水平头部
    #    model.setHorizontalHeaderItem(i, item)
    for i in range(len(headdata)):
        item = QStandardItem(headdata[i])
        # 设置模型的水平头部
        model.setHorizontalHeaderItem(i, item)
    rown = 0
    # 从csv文件中取出数据，放入到模型中
    for data in c.select(table):
        for coln in range(len(data)):

            item = QStandardItem(str(data[coln]))
            if coln == 0 and check is True:
                item.setCheckState(Qt.Unchecked)
                item.setCheckable(True)
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


def make_completer(table, keyname):
    if table == 'base' and keyname == 'store_id':
        completer = QCompleter()
        model = QStringListModel()
        temp = c.select_com("select store_id from store")
        strlist = []
        for i in temp:
            strlist.append(i[0])
        model.setStringList(strlist)
        completer.setModel(model)
        return completer
    if table == 'score' and keyname == 'wine_id':
        completer = QCompleter()
        model = QStringListModel()
        temp = c.select_com("select wine_id from base")
        strlist = []
        for i in temp:
            strlist.append(i[0])
        model.setStringList(strlist)
        completer.setModel(model)
        return completer
    return None


class Stack1(QDialog):
    def __init__(self, table):
        super(Stack1, self).__init__()
        self.table = table
        self.keys = c.keys[self.table]
        self.keys_CH = c.keys_CH[self.table]
        self.keysnum = len(self.keys)
        self.setFixedSize(150 * min(self.keysnum, 4),
                          200 + 10 * self.keysnum // 4)
        self.textbox = []
        self.label = []
        leftLayout = QGridLayout()
        self.default_value = adj.make_record(self.table).data
        for i in range(self.keysnum):
            self.label.append(QLabel(self.keys_CH[i]))
            self.label[i].setAlignment(Qt.AlignCenter)
            self.label[i].setBaseSize(150, 10)

            self.textbox.append(
                QLineEdit(str(self.default_value[self.keys[i]])))
            self.textbox[i].setBaseSize(100, 10)
            completer = make_completer(self.table, self.keys[i])
            if completer is not None:
                self.textbox[i].setCompleter(completer)

            leftLayout.addWidget(self.label[i], i // 4 * 2, i % 4)
            leftLayout.addWidget(self.textbox[i], i // 4 * 2 + 1, i % 4)
        self.button = QPushButton("提交")
        self.button.setFixedSize(200, 50)
        self.button.clicked.connect(self.push)
        leftLayout.addWidget(self.button, 2 + self.keysnum //
                             4 * 2, 0, 1, self.keysnum, Qt.AlignCenter)
        self.setLayout(leftLayout)

    def push(self):
        record = adj.make_record(self.table)
        for i in range(self.keysnum):
            if self.textbox[i].text() == 'None' or self.textbox[i].text() == '':
                record.data[self.keys[i]] = None
            else:
                record.data[self.keys[i]] = self.textbox[i].text()
            # print(self.keys[i], ':', self.textbox[i].text())
        # print(record.data)
        # try:
        c.add(record)
        # except:
        # print("Add data happen error")
        for index in range(3):
            for i in range(form1.stack.widget(index).keysnum):
                form1.stack.widget(index).textbox[i].setText(
                    str(form1.stack.widget(index).default_value[form1.stack.widget(index).keys[i]]))
                completer = make_completer(form1.stack.widget(
                    index).table, form1.stack.widget(index).keys[i])
                if completer is not None:
                    form1.stack.widget(
                        index).textbox[i].setCompleter(completer)
        index = form1.table_label.currentIndex()
        form.stack.widget(index).brush()


class AddMenu(QDialog):
    def __init__(self):
        super(AddMenu, self).__init__()

        self.table_list = ['base', 'score', 'store']
        self.table_list_CH = ['酒基础信息表', '酒评分表', '仓库表']
        self.table_label = QComboBox()
        self.table_label.setFixedSize(120, 20)
        self.table_label.addItems(self.table_list_CH)
        self.table_label.currentIndexChanged.connect(self.change_table)

        self.stack = QStackedWidget()
        self.stack.addWidget(Stack1('base'))
        self.stack.addWidget(Stack1('score'))
        self.stack.addWidget(Stack1('store'))
        leftLayout = QGridLayout()
        leftLayout.addWidget(self.table_label, 0, 2)
        leftLayout.addWidget(self.stack, 1, 0, 1, 3)
        self.setLayout(leftLayout)
        self.stack.setCurrentIndex(0)
        h = self.stack.widget(0).height() + 70
        w = self.stack.widget(0).width() + 20
        self.setFixedSize(w, h)

    def change_table(self, index):
        self.stack.setCurrentIndex(index)
        h = self.stack.widget(index).height() + 70
        w = self.stack.widget(index).width() + 20
        self.setFixedSize(w, h)

    def run(self):
        self.show()


class stack2(QDialog):
    def __init__(self, table):
        super(stack2, self).__init__()
        self.table = table
        self.tableview = QTableView()
        self.checkable = False
        self.model = loaddata(self.table, check=self.checkable)
        self.backmodel = backupdata(self.model)
        self.tableview.setModel(self.model)
        leftLayout = QGridLayout()
        leftLayout.addWidget(self.tableview)
        self.setLayout(leftLayout)

        self.model.itemChanged.connect(self.push)

    def push(self, item):
        if self.checkable is True:
            return
        colnum = self.model.columnCount()
        up_record = adj.make_record(self.table)
        for i in range(colnum):
            up_record.data[self.model.horizontalHeaderItem(
                i).text()] = self.model.item(item.row(), i).text()
        try:
            c.update(up_record)
            self.backmodel = backupdata(self.model)
        except:
            self.model = backupdata(self.backmodel)
            self.tableview.setModel(self.model)
            self.model.itemChanged.connect(self.push)
            print("数据更改错误")

    def push_all(self):
        rownum = self.model.rowCount()
        for row in range(rownum):
            print(row)
            colnum = self.model.columnCount()
            up_record = adj.make_record(self.table)
            for col in range(colnum):
                up_record.data[self.model.horizontalHeaderItem(
                    col).text()] = self.model.item(row, col).text()
            try:
                c.update(up_record)
                self.backmodel = backupdata(self.model)
            except:
                self.model = backupdata(self.backmodel)
                self.tableview.setModel(self.model)
                self.model.itemChanged.connect(self.push)
                print("数据更改错误")
                return

    def brush(self):
        self.model = loaddata(self.table, check=self.checkable)
        self.backmodel = backupdata(self.model)
        self.tableview.setModel(self.model)
        self.model.itemChanged.connect(self.push)

    def rm(self):
        if self.checkable is False:
            return
        self.model.itemChanged.disconnect()

        rownum = self.model.rowCount()
        row = 0
        while(row < rownum):
            if row >= rownum:
                break
            if self.model.item(row, 0).checkState() is Qt.Checked:
                colnum = self.model.columnCount()
                rm_record = adj.make_record(self.table)
                for col in range(colnum):
                    rm_record.data[self.model.horizontalHeaderItem(
                        col).text()] = self.model.item(row, col).text()
                c.delete(rm_record)

                self.model.removeRow(row)
                rownum -= 1
                row -= 1
            row += 1

        self.push_all()

        self.model.itemChanged.connect(self.push)


class MainMenu(QDialog):

    def __init__(self, parent=None):
        # super(MainMenu, self).__init__(parent)
        super(MainMenu, self).__init__()
        # Create widgets
        # self.resize(700, 500)

        self.setMinimumSize(600, 500)
        self.checkable = False

        self.add_button = QPushButton('进口')
        self.add_button.setFixedSize(200, 70)
        self.add_button.clicked.connect(form1.run)

        self.del_button = QPushButton('出口')
        self.del_button.setFixedSize(200, 70)

        self.upd_button = QPushButton('更改')
        self.upd_button.setFixedSize(200, 70)

        self.bus_button = QPushButton('刷新')
        self.bus_button.setFixedSize(120, 50)

        self.table_list = ['base', 'score', 'store']
        self.table_list_CH = ['酒基础信息表', '酒评分表', '仓库表']
        self.table_label = QComboBox()
        self.table_label.setFixedSize(120, 20)
        self.table_label.addItems(self.table_list_CH)
        self.table_label.currentIndexChanged.connect(self.change_table)

        self.stack = QStackedWidget()
        self.stack.addWidget(stack2('base'))
        self.stack.addWidget(stack2('score'))
        self.stack.addWidget(stack2('store'))

        self.check_button = QPushButton('选择')
        self.check_button.setFixedSize(90, 70)
        self.check_button.clicked.connect(self.EnCheck)

        self.rm_button = QPushButton('删除')
        self.rm_button.setFixedSize(90, 70)
        self.rm_button.setEnabled(False)
        # self.rm_button.clicked.connect(self.delf)

        leftLayout = QGridLayout()
        leftLayout.addWidget(self.add_button, 0, 0, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.del_button, 0, 1, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.upd_button, 0, 2, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.check_button, 0, 3, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.rm_button, 0, 4, 2, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.bus_button, 0, 5, 1, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.table_label, 1, 5, 1, 1, Qt.AlignCenter)
        leftLayout.addWidget(self.stack, 2, 0, 1, 6)
        self.setLayout(leftLayout)

        self.index = self.table_label.currentIndex()
        self.bus_button.clicked.connect(self.stack.widget(self.index).brush)
        self.rm_button.clicked.connect(self.rm)

    def change_table(self, index):
        self.stack.setCurrentIndex(index)
        self.index = index
        self.table = self.table_list[index]
        self.bus_button.clicked.disconnect()
        self.bus_button.clicked.connect(self.stack.widget(self.index).brush)

    def EnCheck(self):
        self.checkable = not self.checkable
        self.stack.widget(self.index).checkable = self.checkable
        self.stack.widget(self.index).brush()
        self.rm_button.setEnabled(self.checkable)

    def add(self):
        pass

    def rm(self):
        self.stack.widget(self.index).rm()
        self.checkable = not self.checkable
        self.stack.widget(self.index).checkable = self.checkable
        self.stack.widget(self.index).brush()
        self.rm_button.setEnabled(self.checkable)


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
