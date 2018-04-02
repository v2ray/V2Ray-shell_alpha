#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QWidget, QHBoxLayout,
                             QPushButton, QButtonGroup, QLineEdit,
                             QApplication, QGroupBox, QVBoxLayout,
                             QAbstractItemView, QTreeView)

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))

from bridgehouse import logbook


class dnsTab(QWidget):

    def __init__(self):
        super().__init__()
        self.dnsJSONFile = {
                            "hosts": {
                                "example.com": "127.0.0.1"
                                },
                            "servers": [
                                "8.8.8.8",
                                "8.8.4.4",
                                "localhost"
                                ]
                            }
        self.translate = QCoreApplication.translate
        self.headerLabelDNS = (self.translate("dnsTab", "DNS Server"),)
        self.headerLabelHost = (self.translate("dnsTab", "Host Name"), self.translate("dnsTab", "Host IP"))
        
    def createDnsTab(self):
        # DNS servers
        btnDnsAdd = QPushButton(self.translate("dnsTab", "Add"), self)
        btnDnsDelete = QPushButton(self.translate("dnsTab", "Delete"), self)

        labelDNS = QLabel(self.translate("dnsTab", "DNS Server"), self)
        self.lineEditDNS = QLineEdit()
        hboxDNSServer = QHBoxLayout()
        hboxDNSServer.addWidget(labelDNS)
        hboxDNSServer.addWidget(self.lineEditDNS)
        hboxDNSServer.addStretch()
        
        self.groupButtonDns = QButtonGroup()
        self.groupButtonDns.addButton(btnDnsAdd)
        self.groupButtonDns.addButton(btnDnsDelete)
        
        vboxBtnDns = QVBoxLayout()
        vboxBtnDns.addWidget(btnDnsAdd)
        vboxBtnDns.addWidget(btnDnsDelete)
        vboxBtnDns.addStretch()
        
        self.treeViewDNS = treeViewtDNS = QTreeView()
        treeViewtDNS.setSelectionMode(QAbstractItemView.SingleSelection)
        treeViewtDNS.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeViewtDNS.setUniformRowHeights(True)
        treeViewtDNS.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.treeViewDNSMode = QStandardItemModel()
        self.treeViewDNSMode.setHorizontalHeaderLabels(self.headerLabelDNS)
        treeViewtDNS.setModel(self.treeViewDNSMode)
        
        hboxTreeViewDNS = QHBoxLayout()
        hboxTreeViewDNS.addWidget(treeViewtDNS)
        hboxTreeViewDNS.addLayout(vboxBtnDns)
        
        vboxTreViewDNS = QVBoxLayout()
        vboxTreViewDNS.addLayout(hboxDNSServer)
        vboxTreViewDNS.addLayout(hboxTreeViewDNS)
        # DNS Server End
        
        # Host
        labelHostName = QLabel(self.translate("dnsTab", "Host Name: "), self)
        self.lineEditHostName = QLineEdit(self)
        labelHostIP = QLabel(self.translate("dnsTab", "Host IP Address: "), self)
        self.lineEditHostIP = QLineEdit(self)
        
        self.treeViewHOST = treeViewtHOST = QTreeView()
        treeViewtHOST.setSelectionMode(QAbstractItemView.SingleSelection)
        treeViewtHOST.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeViewtHOST.setUniformRowHeights(True)
        treeViewtHOST.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        self.treeViewHOSTMode = QStandardItemModel()
        self.treeViewHOSTMode.setHorizontalHeaderLabels(self.headerLabelHost)
        treeViewtHOST.setModel(self.treeViewHOSTMode)
        
        btnHostAdd = QPushButton(
            self.translate("dnsTab", "Add"), self)
        btnHostDelete = QPushButton(
            self.translate("dnsTab", "Delete"), self)
        btnHostChange = QPushButton(
            self.translate("dnsTab", "Modify"), self)
        
        self.groupButtonHost = QButtonGroup()
        self.groupButtonHost.addButton(btnHostAdd)
        self.groupButtonHost.addButton(btnHostDelete)
        self.groupButtonHost.addButton(btnHostChange)
        
        hboxHostName = QHBoxLayout()
        hboxHostName.addWidget(labelHostName)
        hboxHostName.addWidget(self.lineEditHostName)
        hboxHostName.addStretch()
        
        hboxHostIP = QHBoxLayout()
        hboxHostIP.addWidget(labelHostIP)
        hboxHostIP.addWidget(self.lineEditHostIP)
        hboxHostIP.addStretch()
        
        vboxBtnHost = QVBoxLayout()
        vboxBtnHost.addStretch()
        vboxBtnHost.addWidget(btnHostAdd)
        vboxBtnHost.addWidget(btnHostChange)
        vboxBtnHost.addWidget(btnHostDelete)
        
        hboxTreeViewHOST = QHBoxLayout()
        hboxTreeViewHOST.addWidget(self.treeViewHOST)
        hboxTreeViewHOST.addLayout(vboxBtnHost)
        
        vboxTreeViewHOST = QVBoxLayout()
        vboxTreeViewHOST.addLayout(hboxHostName)
        vboxTreeViewHOST.addLayout(hboxHostIP)
        vboxTreeViewHOST.addLayout(hboxTreeViewHOST)
        # Host End
        
        vboxDnsTab = QVBoxLayout()
        vboxDnsTab.addLayout(vboxTreViewDNS)
        vboxDnsTab.addLayout(vboxTreeViewHOST)
        
        groupBoxDnsTab = QGroupBox("", self)
        groupBoxDnsTab.setLayout(vboxDnsTab)
        
        self.createDnsSignals()
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxDnsTab.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingDnsTabFromJSONFile(self.dnsJSONFile, True)

        return groupBoxDnsTab
    
    def createDnsSignals(self):
        self.groupButtonDns.buttonClicked.connect(self.ongroupButtonDns)
        self.treeViewDNS.clicked.connect(self.ontreeViewDNS)
        self.groupButtonHost.buttonClicked.connect(self.ongroupButtonHost)
        self.treeViewHOST.clicked.connect(self.ontreeViewHost)

    def ontreeViewDNS(self):
        itemSelection = self.treeViewDNS.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        row = rowCurrent.row()
        
        dnsServer = self.treeViewDNSMode.item(row).text()
        self.lineEditDNS.setText(dnsServer)
    
    def ontreeViewHost(self):
        itemSelection = self.treeViewHOST.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        row = rowCurrent.row()
        
        hostName = self.treeViewHOSTMode.item(row, 0).text()
        hostIP = self.treeViewHOSTMode.item(row, 1).text()
        self.lineEditHostName.setText(hostName)
        self.lineEditHostIP.setText(hostIP)
        
    def ongroupButtonHost(self, e):
        hostName = self.lineEditHostName.text()
        hostIP = self.lineEditHostIP.text()
        hostCount = self.treeViewHOSTMode.rowCount()
        if (not hostCount and
            e.text() == self.translate("dnsTab", "Add") and
            hostName and hostIP):
            self.treeViewHOSTMode.appendRow((QStandardItem(hostName), QStandardItem(hostIP)))
            self.treeViewHOST.setCurrentIndex(self.treeViewHOSTMode.index(0, 0))
            self.lineEditHostIP.clear()
            self.lineEditHostName.clear()
            return
        elif (not hostCount and 
              (e.text() == self.translate("dnsTab", "Delete") or 
               e.text() == self.translate("dnsTab", "Modify"))): return
        elif (not hostCount and 
              e.text() == self.translate("dnsTab", "Add") and 
              (not hostName or not hostIP)): return
        
        itemSelection = self.treeViewHOST.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        row = rowCurrent.row()
        
        if (e.text() == self.translate("dnsTab", "Add") and 
            hostName and hostIP):
            self.treeViewHOSTMode.appendRow((QStandardItem(hostName), QStandardItem(hostIP)))
            self.treeViewHOST.setCurrentIndex(self.treeViewHOSTMode.index(hostCount, 0))
            self.lineEditHostIP.clear()
            self.lineEditHostName.clear()
        if (e.text() == self.translate("dnsTab", "Modify") and 
            hostName and hostIP):
            self.treeViewHOSTMode.setItem(row, 0, QStandardItem(hostName))
            self.treeViewHOSTMode.setItem(row, 1, QStandardItem(hostIP))
            self.treeViewHOST.setCurrentIndex(self.treeViewHOSTMode.index(row, 0))
            
        if (e.text() == self.translate("dnsTab", "Delete")):
            self.treeViewHOSTMode.removeRow(row)
            self.lineEditHostIP.clear()
            self.lineEditHostName.clear()

    def ongroupButtonDns(self, e):
        dnsServer = self.lineEditDNS.text()
        dnsServerCount = self.treeViewDNSMode.rowCount()
        if (not dnsServerCount and 
            e.text() == self.translate("dnsTab", "Add") and dnsServer):
            self.treeViewDNSMode.appendRow(QStandardItem(dnsServer))
            self.treeViewDNS.setCurrentIndex(self.treeViewDNSMode.index(0, 0))
            self.lineEditDNS.clear()
            return
        elif (not dnsServerCount and 
              e.text() == self.translate("dnsTab", "Delete")): return
        elif (not dnsServerCount and 
              e.text() == self.translate("dnsTab", "Add") and
               not dnsServer): return
        
        itemSelection = self.treeViewDNS.selectionModel()
        rowCurrent = itemSelection.selectedIndexes()[0]
        row = rowCurrent.row()
        
        dnsServers = []
        for i in range(dnsServerCount):
            dnsServers.append(self.treeViewDNSMode.item(i).text())

        if (e.text() == self.translate("dnsTab", "Add")):
            dnsServer = self.lineEditDNS.text()
            if ((dnsServer in dnsServers) or (not dnsServer)): return
            self.treeViewDNSMode.appendRow(QStandardItem(dnsServer))
            self.treeViewDNS.setCurrentIndex(self.treeViewDNSMode.index(dnsServerCount, 0))
            self.lineEditDNS.clear()
        if (e.text() == self.translate("dnsTab", "Delete")):
            self.treeViewDNSMode.removeRow(row)
            self.lineEditDNS.clear()
    
    def settingDnsTabFromJSONFile(self, dnsJSONFile={}, openFromJSONFile=False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        
        if (not dnsJSONFile): dnsJSONFile = {}

        try:
            dnsJSONFile["hosts"]
        except KeyError as e:
            logbook.writeLog("Dns", "KeyError", e)
            dnsJSONFile["hosts"] = {}
            
        try:
            dnsJSONFile["servers"]
        except KeyError as e:
            logbook.writeLog("Dns", "KeyError", e)
            dnsJSONFile["servers"] = [
                                "8.8.8.8",
                                "8.8.4.4",
                                "localhost"
                                ]
        
        dnsCount = len(dnsJSONFile["servers"])
        hostCount = len(dnsJSONFile["hosts"]) 
        
        if (dnsCount > 0):
            self.treeViewDNSMode.setRowCount(0)
            for i in range(dnsCount):
                dnsServer = QStandardItem(str(dnsJSONFile["servers"][i]))
                self.treeViewDNSMode.appendRow(dnsServer)
            self.treeViewDNS.setCurrentIndex(self.treeViewDNSMode.index(0, 0))
        
        if (hostCount > 0):
            self.treeViewHOSTMode.setRowCount(0)
            for i, j in dnsJSONFile["hosts"].items():
                hostName, hostIP = QStandardItem(str(i)), QStandardItem(str(j)) 
                self.treeViewHOSTMode.appendRow((hostName, hostIP))
            self.treeViewHOST.setCurrentIndex(self.treeViewHOSTMode.index(0, 0))

    def createDnsJSONFile(self):
        dnsCount = self.treeViewDNSMode.rowCount()
        hostCount = self.treeViewHOSTMode.rowCount()
        dnsJSONFile = {}
        if (dnsCount > 0):
            dnsJSONFile["servers"] = []
            for i in range(dnsCount):
                dnsJSONFile["servers"].append(self.treeViewDNSMode.item(i).text())
        if (hostCount > 0):
            dnsJSONFile["hosts"] = {}
            for i in range(hostCount):
                # there have a problem if domain have multiple ip addresses. json can not use Duplicate key
                dnsJSONFile["hosts"][self.treeViewHOSTMode.item(i, 0).text()] = self.treeViewHOSTMode.item(i, 1).text()

        return dnsJSONFile
    
    def __debugTest(self):
        import json
        print(json.dumps(self.createDnsJSONFile(), indent=4, sort_keys=False))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = dnsTab()
    v = QVBoxLayout()
    v.addWidget(ex.createDnsTab())
    ex.setLayout(v)
    ex.setGeometry(200, 100, 800, 768)
    ex.show()
    sys.exit(app.exec_()) 
