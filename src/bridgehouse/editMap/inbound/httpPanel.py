#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QLabel, QSpinBox,
                             QHBoxLayout, QGroupBox, QPushButton,
                             QTableWidget, QAbstractItemView, QButtonGroup,
                             QVBoxLayout, QLineEdit, QGridLayout, QTableWidgetItem,
                             QCheckBox)
from PyQt5.QtCore import QFileInfo, QCoreApplication

import sys, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.inbound import logbook


class HttpPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.httpJSONFile = {
                            "timeout": 300,
                              "accounts": [
                                    {
                                        "user": "my-username",
                                        "pass": "my-password"
                                    }
                                ],
                            "allowTransparent": False,
                            "userLevel": 0
                            }
        self.translate = QCoreApplication.translate
        
        self.labelUserHttpPanel = (self.translate("HttpPanel", "User"),
                          self.translate("HttpPanel", "Password"))

    def createHttpSettingPanel(self):
        labelTimeout = QLabel(self.translate("HttpPanel", "Timeout: "), self)
        self.spinBoxHttpTimeout = QSpinBox()
        
        self.spinBoxHttpTimeout.setRange(0, 999)
        self.spinBoxHttpTimeout.setValue(300)
        
        self.checkBoxallowTransparent = QCheckBox(
            self.translate("HttpPanel", "Allow Transparent"), self)
        self.checkBoxallowTransparent.setChecked(False)

        hboxTimeout = QHBoxLayout()
        hboxTimeout.addWidget(labelTimeout)
        hboxTimeout.addWidget(self.spinBoxHttpTimeout)
        hboxTimeout.addStretch()
        
        labeluserLevel = QLabel(self.translate("HttpPanel", "User Level: "))
        self.spinBoxHttpuserLevel = QSpinBox()
        self.spinBoxHttpuserLevel.setRange(0, 65535)
        self.spinBoxHttpuserLevel.setValue(0)
        
        hboxuserLevel = QHBoxLayout()
        hboxuserLevel.addWidget(labeluserLevel)
        hboxuserLevel.addWidget(self.spinBoxHttpuserLevel)
        hboxuserLevel.addStretch()

        btnHttpNew = QPushButton(
            self.translate("HttpPanel", "New"), self)
        btnHttpDelete = QPushButton(
            self.translate("HttpPanel", "Delete"), self)
        
        self.groupButtonHttp = QButtonGroup()
        self.groupButtonHttp.addButton(btnHttpNew)
        self.groupButtonHttp.addButton(btnHttpDelete)
        
        vboxButtonHttp = QVBoxLayout()
        vboxButtonHttp.addStretch()
        vboxButtonHttp.addWidget(btnHttpNew)
        vboxButtonHttp.addWidget(btnHttpDelete)
        
        self.tableWidgetHttp = QTableWidget()
        self.tableWidgetHttp.setColumnCount(2)
        self.tableWidgetHttp.adjustSize()
        self.tableWidgetHttp.setHorizontalHeaderLabels(self.labelUserHttpPanel)
        self.tableWidgetHttp.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetHttp.setSelectionBehavior(QAbstractItemView.SelectRows)
        #self.tableWidgetHttp.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidgetHttp.horizontalHeader().setStretchLastSection(True)
        
        hboxHttpTableWidget = QHBoxLayout()
        hboxHttpTableWidget.addWidget(self.tableWidgetHttp)
        hboxHttpTableWidget.addLayout(vboxButtonHttp)
        
        vboxHttpTableWidget = QVBoxLayout()
        vboxHttpTableWidget.addLayout(hboxHttpTableWidget)
        
        self.groupBoxHttpAuth = QGroupBox(
            self.translate("HttpPanel", "Requires Authentication: "), self)
        self.groupBoxHttpAuth.setCheckable(True)
        self.groupBoxHttpAuth.setChecked(False)
        self.groupBoxHttpAuth.setLayout(vboxHttpTableWidget)
        
        vboxHttp = QVBoxLayout()
        vboxHttp.addLayout(hboxTimeout)
        vboxHttp.addLayout(hboxuserLevel)
        vboxHttp.addWidget(self.checkBoxallowTransparent)
        vboxHttp.addWidget(self.groupBoxHttpAuth)

        self.createHttpPanelSignals()
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            self.__debugBtn.clicked.connect(self.__debugTest)
            vboxHttp.addWidget(self.__debugBtn)
            self.settinghttpPanelFromJSONFile(self.httpJSONFile, True)

        groupBoxHttp = QGroupBox(self.translate("HttpPanel", "Http"), self)
        groupBoxHttp.setLayout(vboxHttp)

        return groupBoxHttp
    
    def createHttpPanelSignals(self):
        self.groupButtonHttp.buttonClicked.connect(self.ongroupButtonHttp)
        
    def ongroupButtonHttp(self, e):
        if (e.text() == self.translate("HttpPanel", "Delete")):
            self.onbtnHttpDelete()
        if (e.text() == self.translate("HttpPanel", "New")):
            self.onbtnHttpNew()

    def onbtnHttpNew(self):
        row = self.tableWidgetHttp.rowCount()
        if (not row):
            self.tableWidgetHttp.setRowCount(row + 1)
        else:
            user = self.tableWidgetHttp.item(row-1, 0)
            password = self.tableWidgetHttp.item(row-1, 1)
            if (user and password):
                self.tableWidgetHttp.setRowCount(row + 1)

    def onbtnHttpDelete(self):
        self.onbtnHttpClear()
        if (not self.tableWidgetHttp.rowCount()): return
        row = self.tableWidgetHttp.currentRow()
        self.tableWidgetHttp.removeRow(row)
    
    def settinghttpPanelFromJSONFile(self, httpJSONFile={}, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        self.tableWidgetHttp.setRowCount(0)
        
        if (not httpJSONFile): httpJSONFile = {}

        try:
            httpJSONFile["timeout"]
        except KeyError as e:
            logbook.writeLog("http", "KeyError", e)
            httpJSONFile["timeout"] = 300
            
        try:
            httpJSONFile["allowTransparent"]
        except KeyError as e:
            logbook.writeLog("http", "KeyError", e)
            httpJSONFile["allowTransparent"] = False
            
        try:
            httpJSONFile["accounts"]
        except KeyError as e:
            logbook.writeLog("http", "KeyError", e)
            httpJSONFile["accounts"] = {}
            
        try:
            httpJSONFile["userLevel"]
        except KeyError as e:
            logbook.writeLog("http", "KeyError", e)
            httpJSONFile["userLevel"] = 0
    
        try:
            self.spinBoxHttpTimeout.setValue(int(self.httpJSONFile["timeout"]))
        except (ValueError, TypeError) as e:
            logbook.writeLog("http", "ValueError or TypeError", e)
            self.spinBoxHttpTimeout.setValue(300)
            
        try:
            self.checkBoxallowTransparent.setChecked(bool(httpJSONFile["allowTransparent"]))
        except (ValueError, TypeError) as e:
            logbook.writeLog("http", "ValueError or TypeError", e)
            self.checkBoxallowTransparent.setChecked(False)
            
        try:
            self.spinBoxHttpuserLevel.setValue(int(httpJSONFile["userLevel"]))
        except (ValueError, TypeError) as e:
            logbook.writeLog("http", "ValueError or TypeError", e)
            self.spinBoxHttpuserLevel.setValue(0)
        try:
            self.treasureChest.addLevel(self.spinBoxHttpuserLevel.value())
        except Exception:pass

        accountsNumber = len(httpJSONFile["accounts"])
        if (accountsNumber):
            accounts = httpJSONFile["accounts"]
            self.tableWidgetHttp.setRowCount(accountsNumber)
            self.groupBoxHttpAuth.setChecked(True)
            for i in range(accountsNumber):
                try:user = accounts[i]["user"]
                except Exception: user = ""
                try:password = accounts[i]["pass"]
                except Exception: password = ""

                self.tableWidgetHttp.setItem(i, 0, QTableWidgetItem(str(user)))
                self.tableWidgetHttp.setItem(i, 1, QTableWidgetItem(str(password)))
                self.tableWidgetHttp.resizeColumnsToContents()
        else:self.groupBoxHttpAuth.setChecked(False)

    def createHttpJSONFile(self):
        httpJSONFile = {}
        httpJSONFile["timeout"] = self.spinBoxHttpTimeout.value()

        if (self.groupBoxHttpAuth.isChecked()):
            httpJSONFile["accounts"] = []
            accountsNumber = self.tableWidgetHttp.rowCount()
            if (accountsNumber):
                account = {}
                for i in range(accountsNumber):
                    account["user"] = self.tableWidgetHttp.item(i, 0).text()
                    account["pass"] = self.tableWidgetHttp.item(i, 1).text()
                    httpJSONFile["accounts"].append(copy.deepcopy(account))
            else:del httpJSONFile["accounts"]
                
        httpJSONFile["allowTransparent"] = self.checkBoxallowTransparent.isChecked()
        httpJSONFile["userLevel"] = self.spinBoxHttpuserLevel.value()
        
        try:self.treasureChest.addLevel(self.spinBoxHttpuserLevel.value())
        except Exception:pass

        return httpJSONFile
    
    def clearinboundHttpPanel(self):
        self.tableWidgetHttp.setRowCount(0)
        self.spinBoxHttpTimeout.setValue(300)
        self.spinBoxHttpuserLevel.setValue(0)
        self.checkBoxallowTransparent.setChecked(False)
        self.groupBoxHttpAuth.setChecked(False)
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createHttpJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = HttpPanel()
    ex.createHttpSettingPanel()
    ex.setGeometry(300, 300, 600, 420)
    ex.show()
    sys.exit(app.exec_())
