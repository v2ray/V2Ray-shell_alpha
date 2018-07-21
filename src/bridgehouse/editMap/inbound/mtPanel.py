#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QTableView,
                             QHBoxLayout, QGroupBox, QPushButton,
                             QTableWidget, QAbstractItemView, QButtonGroup,
                             QVBoxLayout, QTableWidgetItem)
                             
from PyQt5.QtCore import QFileInfo, QCoreApplication
from PyQt5.Qt import QStandardItemModel, QModelIndex

import sys, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.toolbox import toolbox  
    
class InboundMtPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.mtJSONFile = {
                          "users": [{
                            "email": "love@v2ray.com",
                            "level": 0,
                            "secret": "b0cbcef5a486d9636472ac27f8e11a9d"
                          }]
                        }
        self.translate = QCoreApplication.translate
        
        self.labelUsermtPanel = (self.translate("InboundMtPanel", "Email"),
                                 self.translate("InboundMtPanel", "Level"),
                                 self.translate("InboundMtPanel", "Password"))
        
    def createmtSettingPanel(self):
        UUIDdelegate = toolbox.UUIDLineEditDelegate(
            self.translate("InboundMtPanel", "Gerate UUID"))

        self.model = QStandardItemModel(0, 3)
        self.tableViewInMtUser = tableViewUser = QTableView(self)
        tableViewUser.setModel(self.model)
        self.model.setHorizontalHeaderLabels(self.labelUsermtPanel)
        tableViewUser.setSelectionMode(QAbstractItemView.SingleSelection)
        tableViewUser.setSelectionBehavior(QAbstractItemView.SelectRows)

        tableViewUser.setItemDelegateForColumn(2, UUIDdelegate)

        self.btnInMtNew = QPushButton(
            self.translate("InboundMtPanel", "New"), self)
        self.btnInMtDelete = QPushButton(
            self.translate("InboundMtPanel", "Delete"), self)
        
        self.btnGroup = QButtonGroup()
        self.btnGroup.addButton(self.btnInMtNew)
        self.btnGroup.addButton(self.btnInMtDelete)
        
        vboxBtn = QVBoxLayout()
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(QLabel())
        vboxBtn.addWidget(self.btnInMtNew)
        vboxBtn.addWidget(self.btnInMtDelete)
        
        hbox = QHBoxLayout()
        hbox.addWidget(tableViewUser)
        hbox.addLayout(vboxBtn)
        
        self.groupInboudnMtPanel = QGroupBox(
            self.translate("InboundMtPanel", "MTProto"), self)
        self.groupInboudnMtPanel.setLayout(hbox)
        
        self.createInboundMtPanelSignals()

        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxBtn.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingInboundMtPanelFromJSONFile(self.mtJSONFile, True)
        
        return self.groupInboudnMtPanel
    
    def createInboundMtPanelSignals(self):
        self.btnGroup.buttonClicked.connect(self.onInboundMtbtnGroup)
    
    def onInboundMtbtnGroup(self, e):
        if e.text() == self.translate("InboundMtPanel", "New"):
            self.onbtnInboundMtNew()
        if e.text() == self.translate("InboundMtPanel", "Delete"):
            self.onbtnInboundMtDelete()
            
    def onbtnInboundMtNew(self):
        row = self.model.rowCount()
        if not row:
            self.model.setRowCount(row+1)
            self.setRowData(row)
        else:
            if (self.model.index(row-1, 2, QModelIndex()).data()):
                self.model.setRowCount(row+1)
                self.setRowData(row)
    
    def setRowData(self, row, email=None, level=None, secret=None):
        indexEmail = self.model.index(row, 0, QModelIndex())
        indexLevel = self.model.index(row, 1, QModelIndex())
        indexSecret = self.model.index(row, 2, QModelIndex())
        
        self.model.setData(indexEmail, "" if not email else email)
        self.model.setData(indexLevel, 0 if not level else level)
        self.model.setData(indexSecret, 0 if not secret else secret)
        
        try:
            if level: self.treasureChest.addLevel(int(level))
            if email: self.treasureChest.addEmail(str(email))
        except Exception: pass
    
    def onbtnInboundMtDelete(self):
        row = self.tableViewInMtUser.selectedIndexes()
        if row:
            self.model.removeRow(row[0].row())
            
    def settingInboundMtPanelFromJSONFile(self, inboundMtJSONFile=None, openFromJSONFile=False):
        if not inboundMtJSONFile:
            inboundMtJSONFile = {}
            
        try:
            inboundMtJSONFile['users']
        except KeyError:
            inboundMtJSONFile['users'] = list()
            
        if inboundMtJSONFile['users']:
            for row, user in enumerate(inboundMtJSONFile['users']):
                email = level = secret = None
                try:
                    email = user['email']
                except KeyError:
                    pass
                try:
                    level = user['level']
                except KeyError:
                    pass
                try:
                    secret = user['secret']
                except KeyError:
                    pass
                self.model.setRowCount(row+1)
                self.setRowData(row, email, level, secret)

    def createInboundMtJSONFile(self):
        inboundMtJSONFile = {}
        inboundMtJSONFile['users'] = list()
        
        usersNumber = self.model.rowCount()
        for row in range(usersNumber):
            userData = {}
            userData['email'] = self.model.index(row, 0, QModelIndex()).data()
            userData['level'] = self.model.index(row, 1, QModelIndex()).data()
            userData['secret'] = ''.join(str(self.model.index(row, 2, QModelIndex()).data()).split('-'))
            inboundMtJSONFile['users'].append(copy.deepcopy(userData))
            
        return inboundMtJSONFile
    
    def clearinboundMtPanel(self):
        self.model.setRowCount(0)

    def __debugTest(self):
        import json
        print(json.dumps(self.createInboundMtJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = InboundMtPanel()
    ex.createmtSettingPanel()
    ex.setGeometry(300, 300, 600, 420)
    ex.show()
    sys.exit(app.exec_())
