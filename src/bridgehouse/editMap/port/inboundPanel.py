#!/usr/bin/env python3

from PyQt5.QtWidgets import (QLabel, QSpinBox, QComboBox, QCheckBox, QWidget,
                             QGroupBox, QLineEdit, QHBoxLayout, QVBoxLayout, 
                             QScrollArea, QRadioButton, QButtonGroup,
                             QPushButton, QSplitter, QTableWidget, QAbstractItemView,
                             QTableWidgetItem, QTabWidget)
from PyQt5.QtCore import Qt, QFileInfo, QCoreApplication

import sys, json, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.port import treasureChest, logbook, openV2rayJSONFile
from bridgehouse.editMap.inbound import (dokodemodoorPanel, httpPanel, shadowsocksPanel, socksPanel, vmessPanel)
from bridgehouse.editMap.transport import transportPanel

class InboundSettingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate
        
    def createInboundSettingPanel(self): 
        labelTAG                          = QLabel(
            self.translate("InboundSettingPanel", "TAG: "), self)
        self.lineEditInboundSettingTAG    = QLineEdit()
        self.labelListen                  = QLabel(
            self.translate("InboundSettingPanel", "Listen: "), self)
        self.lineEditInboundSettingListen = QLineEdit()
        self.labelPort                    = QLabel(
            self.translate("InboundSettingPanel", "Port: "), self)
        self.spinBoxInboundSettingPort    = QSpinBox()
        self.spinBoxMultiplePort          = QSpinBox()
        self.labelDomainOverride          = QLabel(
            self.translate("InboundSettingPanel", "Domain Override: "), self)
        self.checkBoxDomainOverrideHTTP   = QCheckBox(
            self.translate("InboundSettingPanel", "HTTP"), self)
        self.checkBoxDomainOverrideTLS    = QCheckBox(
            self.translate("InboundSettingPanel", "TLS"), self)

        labelMutiplePortStrategy = QLabel(
            self.translate("InboundSettingPanel", "Strategy: "), self)
        self.radioBoxInboundSettingStrategyAlways = QRadioButton(
            self.translate("InboundSettingPanel", "Always"), self)
        self.radioBoxInboundSettingStrategyRandom = QRadioButton(
            self.translate("InboundSettingPanel", "Random"), self)
        labelRefresh     = QLabel(
            self.translate("InboundSettingPanel", "Refresh: "), self)
        self.spinBoxInboundSettingRefresh      = QSpinBox()
        labelConcurrency = QLabel(
            self.translate("InboundSettingPanel", "Concurrency: "), self)
        self.spinBoxInboundSettingConcurrency  = QSpinBox()

        self.spinBoxInboundSettingPort.setRange(0, 65535)
        self.spinBoxInboundSettingPort.setValue(1080)
        self.spinBoxMultiplePort.setRange(0, 65535)
        self.spinBoxMultiplePort.setValue(1180)
        self.spinBoxMultiplePort.setEnabled(False)
        self.checkBoxDomainOverrideHTTP.setCheckable(True)
        self.checkBoxDomainOverrideHTTP.setChecked(False)
        self.checkBoxDomainOverrideTLS.setCheckable(True)
        self.checkBoxDomainOverrideTLS.setChecked(False)
        self.spinBoxInboundSettingRefresh.setRange(2, 60)
        self.spinBoxInboundSettingRefresh.setEnabled(False)
        self.radioBoxInboundSettingStrategyAlways.setChecked(True)
        self.spinBoxInboundSettingConcurrency.setValue(3)
        
        hboxTag = QHBoxLayout()
        hboxTag.addWidget(labelTAG)
        hboxTag.addWidget(self.lineEditInboundSettingTAG)
        hboxTag.addStretch()
        
        hboxListen = QHBoxLayout()
        hboxListen.addWidget(self.labelListen)
        hboxListen.addWidget(self.lineEditInboundSettingListen)
        hboxListen.addWidget(self.labelPort)
        hboxListen.addWidget(self.spinBoxInboundSettingPort)
        hboxListen.addWidget(self.spinBoxMultiplePort)
        hboxListen.addStretch()
        
        self.hboxDomainOverride = hboxDomainOverride = QHBoxLayout()
        hboxDomainOverride.addWidget(self.labelDomainOverride)
        hboxDomainOverride.addWidget(self.checkBoxDomainOverrideHTTP)
        hboxDomainOverride.addWidget(self.checkBoxDomainOverrideTLS)
        hboxDomainOverride.addStretch()
        
        self.btnGroupStrategy = QButtonGroup()
        self.btnGroupStrategy.addButton(self.radioBoxInboundSettingStrategyAlways)
        self.btnGroupStrategy.addButton(self.radioBoxInboundSettingStrategyRandom)
        
        hboxAllocateStrategy = QHBoxLayout()
        hboxAllocateStrategy.addWidget(labelMutiplePortStrategy)
        hboxAllocateStrategy.addWidget(self.radioBoxInboundSettingStrategyAlways)
        hboxAllocateStrategy.addWidget(self.radioBoxInboundSettingStrategyRandom)
        hboxAllocateStrategy.addStretch()
        
        hboxRefresh = QHBoxLayout()
        hboxRefresh.addWidget(labelRefresh)
        hboxRefresh.addWidget(self.spinBoxInboundSettingRefresh)
        hboxRefresh.addStretch()
        
        hboxConcurrency = QHBoxLayout()
        hboxConcurrency.addWidget(labelConcurrency)
        hboxConcurrency.addWidget(self.spinBoxInboundSettingConcurrency)
        hboxConcurrency.addStretch()
        
        vboxAllocate = QVBoxLayout()
        vboxAllocate.addLayout(hboxAllocateStrategy)
        vboxAllocate.addLayout(hboxRefresh)
        vboxAllocate.addLayout(hboxConcurrency)
        
        self.groupBoxAllocate = QGroupBox(
            self.translate("InboundSettingPanel", "Multiple Port Allocate"), self)
        self.groupBoxAllocate.setLayout(vboxAllocate)
        self.groupBoxAllocate.setCheckable(True)
        self.groupBoxAllocate.setChecked(False)
        
        self.vboxInboundSettingPanel = vboxInboundSettingPanel = QVBoxLayout()
        vboxInboundSettingPanel.addLayout(hboxTag)
        vboxInboundSettingPanel.addLayout(hboxListen)
        vboxInboundSettingPanel.addLayout(hboxDomainOverride)
        vboxInboundSettingPanel.addWidget(self.groupBoxAllocate)
        
        self.createInboundSettingPanelSignalls()
        
        return self.vboxInboundSettingPanel
        
    def createInboundSettingPanelSignalls(self):
        self.groupBoxAllocate.clicked.connect(self.ongroupBoxAllocate)
        self.btnGroupStrategy.buttonClicked.connect(self.onradioBoxStrategyRandom)
        self.spinBoxMultiplePort.valueChanged.connect(self.onspinBoxMultiplePort)
      
    def onspinBoxMultiplePort(self, e):
        tmp = e, self.spinBoxInboundSettingPort.value()
        tmpconcurrency = int((max(tmp)-min(tmp))/2)
        self.spinBoxInboundSettingConcurrency.setRange(1, (lambda x: x if x > 0 else 1)(tmpconcurrency))

    def onradioBoxStrategyRandom(self, e):
        if (e.text() == self.translate("InboundSettingPanel", "Always")):
            self.spinBoxInboundSettingRefresh.setEnabled(False)
        elif (e.text() == self.translate("InboundSettingPanel", "Random")):
            self.spinBoxInboundSettingRefresh.setEnabled(True)
    
    def ongroupBoxAllocate(self, e):
        if (e):
            self.spinBoxMultiplePort.setEnabled(True)
            if (self.radioBoxInboundSettingStrategyRandom.isChecked()):
                self.spinBoxInboundSettingRefresh.setEnabled(True)
        else:
            self.spinBoxMultiplePort.setEnabled(False)
            
    def clearInboundSettingPanel(self):
        self.lineEditInboundSettingListen.clear()
        self.lineEditInboundSettingTAG.clear()
        self.spinBoxInboundSettingPort.setValue(1080)
        self.spinBoxMultiplePort.setValue(1180)
        self.checkBoxDomainOverrideHTTP.setChecked(False)
        self.checkBoxDomainOverrideTLS.setChecked(False)
        self.groupBoxAllocate.setChecked(False)
        self.spinBoxInboundSettingConcurrency.setValue(3)
        self.spinBoxInboundSettingRefresh.setValue(2)
        self.spinBoxInboundSettingRefresh.setEnabled(False)
        self.radioBoxInboundSettingStrategyAlways.setChecked(True)
        self.radioBoxInboundSettingStrategyRandom.setChecked(False)

class InboundPortocolPanel(dokodemodoorPanel.DokodemodoorPanel,
                           httpPanel.HttpPanel,
                           shadowsocksPanel.InboundShadowsocksPanel,
                           socksPanel.InboundSocksPanel,
                           vmessPanel.InboundVmessPanel):
    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate

    def createInboundPortocolPanel(self):
        listComboxProtocol = "socks", "vmess", "shadowsocks", "http", "dokodemo-door" 
        labelProtocol      = QLabel(
            self.translate("InboundPortocolPanel", "Protocol: "), self)
        self.comboBoxInboundProtocol = QComboBox()
        self.comboBoxInboundProtocol.addItems(listComboxProtocol)
        
        self.dokodemodoor  = self.createDokodemodoorSettingPanel()
        self.http          = self.createHttpSettingPanel()
        self.inshadowsocks = self.createShadowsocksSettingPanel()
        self.invmess       = self.createVmessSettingPanel()
        self.insocks       = self.createSocksSettingPanel()
        
        self.insocks.show()
        self.http.hide()
        self.invmess.hide()
        self.inshadowsocks.hide()
        self.dokodemodoor.hide()
        
        hboxInboundProtocol = QHBoxLayout()
        hboxInboundProtocol.addWidget(labelProtocol)
        hboxInboundProtocol.addWidget(self.comboBoxInboundProtocol)
        hboxInboundProtocol.addStretch()
        
        self.vboxInboundProtocol = vboxInboundProtocol = QVBoxLayout()
        vboxInboundProtocol.addLayout(hboxInboundProtocol)
        vboxInboundProtocol.addWidget(self.dokodemodoor)
        vboxInboundProtocol.addWidget(self.http)
        vboxInboundProtocol.addWidget(self.inshadowsocks)
        vboxInboundProtocol.addWidget(self.invmess)
        vboxInboundProtocol.addWidget(self.insocks)
        #vboxInboundProtocol.addStretch()
        
        self.createInboundPortocolPanelSignals()

        return self.vboxInboundProtocol
        
    def createInboundPortocolPanelSignals(self):
        self.comboBoxInboundProtocol.currentTextChanged.connect(self.oncomboBoxInboundProtocol)
        
    def oncomboBoxInboundProtocol(self, e):
        def showProtocol(protocol = e):
            self.insocks.hide()
            self.http.hide()
            self.invmess.hide()
            self.inshadowsocks.hide()
            self.dokodemodoor.hide()
            if (protocol == "socks"):
                self.insocks.show()
            elif (protocol == "vmess"):
                self.invmess.show()
            elif (protocol == "shadowsocks"):
                self.inshadowsocks.show()
            elif (protocol == "http"):
                self.http.show()
            elif (protocol == "dokodemo-door"):
                self.dokodemodoor.show()
        
        showProtocol(e)
        
    def ScrollLayout(self, layout):
        box = QVBoxLayout(self)
        scroll = QScrollArea(self)
        box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        
        scrollLayout.addLayout(layout)
        scroll.setWidget(scrollContent)
        
    def ScrollWidget(self, widget):
        box = QVBoxLayout(self)
        scroll = QScrollArea(self)
        box.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        
        scrollLayout = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        
        scrollLayout.addWidget(widget)
        scroll.setWidget(scrollContent)
        scrollLayout.addWidget(widget)
        
    def clearInboundPortocolPanel(self):
        self.cleardokodemodoorPanel()
        self.clearinboundHttpPanel()
        self.clearinboundShadowsocksPanel()
        self.clearinboundsocksPanel()
        self.clearinboundVmessPanel()
 
class InboundPanel(InboundSettingPanel, InboundPortocolPanel, transportPanel.TransportPanel):
    def __init__(self, CaptainstreasureChest = False):
        super().__init__()
        ### don not delete this self.inboundJSONFile setting, debug will use it
        self.inboundJSONFile = {
                                "protocol": "socks",
                                "port": "1080",
                                "tag": "Inbound",
                                "listen": "127.0.0.1",
                                "allocate": {
                                    "strategy": "random",
                                    "refresh": 5,
                                    "concurrency": 3
                                    },
                                "settings": {},
                                "streamSettings": {},
                                "domainOverride": [""]
                               }
        self.tableWidgetInboundVerticalHeaderLabels = ["Inbound"]
        if (CaptainstreasureChest):
            self.treasureChest = CaptainstreasureChest
        else:
            self.treasureChest = treasureChest.treasureChest()  ### a empty treasure chest
        self.updateList = self.treasureChest.updateList
        
        self.translate = QCoreApplication.translate
        
        self.labelHeaderInbound = (self.translate("InboundPanel", "Tag name"), 
                                   self.translate("InboundPanel", "Listen: port"), 
                                   self.translate("InboundPanel", "Protocol"))

    def createInboundPanel(self):
        super(InboundPanel, self).createTransportPanel()
        super(InboundPanel, self).createInboundSettingPanel()
        super(InboundPanel, self).createInboundPortocolPanel()
        
        vboxInboundPanel = QVBoxLayout()
        vboxInboundPanel.addLayout(self.vboxInboundSettingPanel)
        vboxInboundPanel.addLayout(self.vboxInboundProtocol)
        vboxInboundPanel.addLayout(self.vboxcheckBoxStreamSetting)
        vboxInboundPanel.addStretch()
        
        groupBoxInboundPanel = QGroupBox("", self)
        groupBoxInboundPanel.setLayout(vboxInboundPanel)
        
        self.tableWidgetInbound = tableWidgetInbound = QTableWidget()
        tableWidgetInbound.setColumnCount(3)
        tableWidgetInbound.setHorizontalHeaderLabels(self.labelHeaderInbound)
        tableWidgetInbound.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidgetInbound.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidgetInbound.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidgetInbound.horizontalHeader().setStretchLastSection(True)
        
        splitterInbound = QSplitter(Qt.Horizontal)
        splitterInbound.addWidget(tableWidgetInbound)
        splitterInbound.addWidget(groupBoxInboundPanel)
        
        btnInboundApply  = QPushButton(
            self.translate("InboundPanel", "Add"), self)
        btnInboundDelete = QPushButton(
            self.translate("InboundPanel", "Delete"), self)
        btnInboundChange = QPushButton(
            self.translate("InboundPanel", "Apply"), self)
        
        self.btnGroupInbound = btnGroupInbound = QButtonGroup()
        btnGroupInbound.addButton(btnInboundApply)
        btnGroupInbound.addButton(btnInboundChange)
        btnGroupInbound.addButton(btnInboundDelete)
        
        hboxBtnInbound   = QHBoxLayout()
        hboxBtnInbound.addStretch()
        hboxBtnInbound.addWidget(btnInboundApply)
        hboxBtnInbound.addWidget(btnInboundChange)
        hboxBtnInbound.addWidget(btnInboundDelete)
        
        vboxSpliterInbound = QVBoxLayout()
        vboxSpliterInbound.addWidget(splitterInbound)
        vboxSpliterInbound.addLayout(hboxBtnInbound)
        
        groupBoxSpliterInbound = QGroupBox("", self)
        groupBoxSpliterInbound.setLayout(vboxSpliterInbound)
        
        self.createInboundPanelSignals()
        
        if (v2rayshellDebug):
            self.__debugBtn     = QPushButton("__debugTest", self)
            self.__debugRefresh = QPushButton("__debugRefresh", self)
            
            hbox = QHBoxLayout(self)
            hbox.addWidget(self.__debugBtn)
            hbox.addWidget(self.__debugRefresh)
            groupBoxdebugBtn = QGroupBox("", self)
            groupBoxdebugBtn.setLayout(hbox)
            vboxSpliterInbound.addWidget(groupBoxdebugBtn)
            self.editV2rayJSONFile = openV2rayJSONFile.editV2rayJSONFile(
                CaptainstreasureChest = self.treasureChest)

            tabWidget = QTabWidget()
            tabWidget.addTab(groupBoxSpliterInbound, "Inbound")
            tabWidget.addTab(self.editV2rayJSONFile.createPanel(), "open V2ray File")
            
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.__debugRefresh.clicked.connect(self.refreshInboundPaneltableWidget)
            self.settingInboundPanelFromJSONFile(self.inboundJSONFile, True)
            return tabWidget

        return groupBoxSpliterInbound
    
    def createInboundPanelSignals(self):
        self.btnGroupInbound.buttonClicked.connect(self.onbtnGroupInbound)
        self.tableWidgetInbound.itemSelectionChanged.connect(self.ontableWidgetInboundItemSelection)
        self.tableWidgetInbound.itemClicked.connect(self.ontableWidgetInboundItemSelection)
        self.updateList.setInboundTag.connect(self.onupdateInVmessPanelcomboBox)
        
    def onupdateInVmessPanelcomboBox(self):
        allIntboundTags = self.treasureChest.getInboundTags()
        if (self.comboBoxInboundProtocol.currentText() == "vmess"):
            currentTag = self.comboBoxInVmessInboundTags.currentText()
            self.comboBoxInVmessInboundTags.clear()
            self.comboBoxInVmessInboundTags.addItem("")
            self.comboBoxInVmessInboundTags.addItems(allIntboundTags)
            self.comboBoxInVmessInboundTags.setCurrentText(currentTag)
        else:
            self.comboBoxInVmessInboundTags.clear()
            self.comboBoxInVmessInboundTags.addItem("")
            self.comboBoxInVmessInboundTags.addItems(allIntboundTags)

    def setcomboBoxInVmessInboundTags(self, tag = None, currentRow = None):
        """
        update the self.comboBoxInVmessOutboudTags real time, 
        when outbound had added, deleted, changed
        """
        allIntboundTags = self.treasureChest.getInboundTags()
        if (tag != None and currentRow != None):
            if (currentRow == 0):
                currentBound = self.treasureChest.getInbound()
            else:
                currentBound = self.treasureChest.getInboundDetour(tag)
            if (currentBound["protocol"] == "vmess"):
                try:
                    currentDetourtoTag = currentBound["settings"]["detour"]["to"]
                except Exception:### KeyError
                    currentDetourtoTag = ""
                self.comboBoxInVmessInboundTags.clear()
                if (tag in allIntboundTags): allIntboundTags.remove(tag)
                self.comboBoxInVmessInboundTags.addItem("")
                self.comboBoxInVmessInboundTags.addItems(allIntboundTags)
                self.comboBoxInVmessInboundTags.setCurrentText(currentDetourtoTag)
        else:
            self.comboBoxInVmessInboundTags.clear()
            self.comboBoxInVmessInboundTags.addItem("")
            self.comboBoxInVmessInboundTags.addItems(allIntboundTags)

    def onbtnGroupInbound(self, e):
        if (e.text() == self.translate("InboundPanel", "Add")):
            self.tableWidgetInboundAdd()    
        if (e.text() == self.translate("InboundPanel", "Delete")):
            self.tableWidgetInboundDelete()
        if (e.text() == self.translate("InboundPanel", "Apply")):
            self.tableWidgetInboundChange()
    
    def settingInboundPanalDefault(self):
        self.settingdokodemodoorPanelFromJSONFile()
        self.settinghttpPanelFromJSONFile()
        self.settingInboundShadowsocksPanelFromJSONFile()
        self.settingInboundSocksPanelFromJSONFile()
        self.settingInboundVmessPanelFromJSONFile()
        self.settingtransportPanelFromJSONFile()

    def tableWidgetInboundAdd(self):
        rowCount = self.tableWidgetInbound.rowCount()
        inboundJSONData = copy.deepcopy(self.createInboundJSONFile())
        if (inboundJSONData):
            tag       = str(inboundJSONData["tag"])
            ipAddress = str(inboundJSONData["listen"]) + ":" + str(inboundJSONData["port"])
            protocol  = str(inboundJSONData["protocol"])
        else:
            return False

        def settableWidgetInbound(tag, ipAddress, protocol):
            self.tableWidgetInbound.setRowCount(rowCount + 1)
            self.tableWidgetInbound.setItem(rowCount, 0, QTableWidgetItem(tag))
            self.tableWidgetInbound.setItem(rowCount, 1, QTableWidgetItem(ipAddress))
            self.tableWidgetInbound.setItem(rowCount, 2, QTableWidgetItem(protocol))
            self.tableWidgetInbound.resizeColumnsToContents()

        if (rowCount == 0):
            tag = self.treasureChest.setInbound(inboundJSONData)
            settableWidgetInbound(tag, ipAddress, protocol)
            self.setcomboBoxInVmessInboundTags(tag, rowCount)
            self.settingInboundPanalDefault()
        else:
            tag = self.treasureChest.addInboundDetour(inboundJSONData)
            if (tag):
                settableWidgetInbound(tag, ipAddress, protocol)
                self.setcomboBoxInVmessInboundTags(tag, rowCount)
                self.settingInboundPanalDefault()
            else:
                ### TODO
                pass
        self.clearInboundPanel()
        
    def tableWidgetInboundDelete(self):
        currentRow = self.tableWidgetInbound.currentRow()
        tag = self.tableWidgetInbound.item(currentRow, 0)
        
        if (tag and currentRow > 0):
            if (self.treasureChest.removeInboundDetour(tag.text()) == False):
                ### TODO
                pass
            self.tableWidgetInbound.removeRow(currentRow)
            self.clearInboundPanel()
        elif (tag and currentRow == 0):  ### delete inbound
            ### inbound should not be deleted
            pass
    
    def tableWidgetInboundChange(self):
        currentRow = self.tableWidgetInbound.currentRow()
        tag = self.tableWidgetInbound.item(currentRow, 0)
        inboundJSONData = copy.deepcopy(self.createInboundJSONFile())
        
        if (tag and inboundJSONData):
            def settableWidgetInbound(tag, ipAddress, protocol):
                self.tableWidgetInbound.setItem(currentRow, 0, QTableWidgetItem(tag))
                self.tableWidgetInbound.setItem(currentRow, 1, QTableWidgetItem(ipAddress))
                self.tableWidgetInbound.setItem(currentRow, 2, QTableWidgetItem(protocol))
                self.tableWidgetInbound.resizeColumnsToContents()
            if (currentRow == 0):
                if (self.treasureChest.setInbound(inboundJSONData) == False):
                    ### TODO
                    pass
                else:
                    self.setcomboBoxInVmessInboundTags(inboundJSONData["tag"], currentRow)
                    settableWidgetInbound(str(inboundJSONData["tag"]), 
                                          str(inboundJSONData["listen"]) + ":" + str(inboundJSONData["port"]), 
                                          str(inboundJSONData["protocol"]))
            else:
                if (self.treasureChest.setInboundDetour(tag.text(), inboundJSONData) == False):
                    ### TODO
                    pass
                else:
                    self.setcomboBoxInVmessInboundTags(inboundJSONData["tag"], currentRow)
                    settableWidgetInbound(str(inboundJSONData["tag"]), 
                                          str(inboundJSONData["listen"]) + ":" + str(inboundJSONData["port"]), 
                                          str(inboundJSONData["protocol"]))
        else:
            pass

    def ontableWidgetInboundItemSelection(self):
        currentRow = self.tableWidgetInbound.currentRow()
        tag = self.tableWidgetInbound.item(currentRow, 0)
        
        if (tag):
            if (currentRow == 0):
                inboundJSONData = copy.deepcopy(self.treasureChest.getInbound())
                if (inboundJSONData):
                    self.settingInboundPanelFromJSONFile(inboundJSONData)
                    self.setcomboBoxInVmessInboundTags(inboundJSONData["tag"], currentRow)
                else:
                    ### TODO
                    pass
            else:
                inboundJSONData = copy.deepcopy(self.treasureChest.getInboundDetour(tag.text()))
                if (inboundJSONData):
                    self.settingInboundPanelFromJSONFile(inboundJSONData)
                    self.setcomboBoxInVmessInboundTags(inboundJSONData["tag"], currentRow)
                else:
                    ### TODO
                    pass

    def settingInboundPanelFromJSONFile(self, inboundJSONFile = {}, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        allocate = True; tranport = True; domainOveride = True; tag = True
        
        if (inboundJSONFile == None): inboundJSONFile = {} 

        try:
            inboundJSONFile["protocol"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)            
            inboundJSONFile["protocol"] = "socks"
            
        try:
            inboundJSONFile["port"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["port"] = 1080
            
        try:
            inboundJSONFile["listen"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["listen"] = "127.0.0.1"
            
        try:
            inboundJSONFile["settings"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["settings"] = {}
        
        try:
            inboundJSONFile["tag"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["tag"] = ""
            tag = False

        try:
            inboundJSONFile["domainOverride"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["domainOverride"] = [""]
            domainOveride = False

        try:
            inboundJSONFile["streamSettings"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["streamSettings"] = {}
            tranport = False

        try:
            inboundJSONFile["allocate"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["allocate"] = {}
            allocate = False

        try:
            inboundJSONFile["allocate"]["concurrency"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["allocate"]["concurrency"] = 3
        
        try:
            inboundJSONFile["allocate"]["refresh"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["allocate"]["refresh"] = 5

        try:
            inboundJSONFile["allocate"]["strategy"]
        except KeyError as e:
            logbook.writeLog("Inbound", "KeyError", e)
            inboundJSONFile["allocate"]["strategy"] = "random"

        self.comboBoxInboundProtocol.setCurrentText(str(inboundJSONFile["protocol"]))
        
        ### checking Multiple Ports
        port = str(inboundJSONFile["port"])
        if ("-" in port):
            self.groupBoxAllocate.setChecked(True)
            self.spinBoxInboundSettingPort.setValue(int(min(port.split("-"))))
            self.spinBoxMultiplePort.setValue(int(max(port.split("-"))))
            self.spinBoxMultiplePort.setEnabled(True)
            if (allocate):
                try:
                    self.spinBoxInboundSettingConcurrency.setValue(
                        int(inboundJSONFile["allocate"]["concurrency"]))
                except KeyError as e:
                    logbook.writeLog("Inbound", "KeyError", e)
                except (TypeError, ValueError) as e:
                    logbook.writeLog("Inbound", "TypeError or ValueError", e)

                try:
                    self.spinBoxInboundSettingRefresh.setValue(
                        int(inboundJSONFile["allocate"]["refresh"]))
                except KeyError as e:
                    logbook.writeLog("Inbound", "KeyError", e)
                except (TypeError, ValueError) as e:
                    logbook.writeLog("Inbound", "TypeError or ValueError", e)
                    
                strategy = inboundJSONFile["allocate"]["strategy"]
                if (strategy == "always"):
                    self.radioBoxInboundSettingStrategyAlways.setChecked(True)
                if (strategy == "random"):
                    self.radioBoxInboundSettingStrategyRandom.setChecked(True)
                    if(self.groupBoxAllocate.isChecked()):
                        self.spinBoxInboundSettingRefresh.setEnabled(True)
                else:
                    ### strategy may be some wrong with value, pass it
                    pass
        else:
            self.spinBoxInboundSettingPort.setValue(int(port))
            self.groupBoxAllocate.setChecked(False)
            self.spinBoxMultiplePort.setDisabled(True)
        
        if (tag):
            self.lineEditInboundSettingTAG.setText(str(inboundJSONFile["tag"]))
        
        self.lineEditInboundSettingListen.setText(str(inboundJSONFile["listen"]))

        protocol = str(inboundJSONFile["protocol"])
        if (inboundJSONFile["settings"] != {} or inboundJSONFile["settings"] != None):
            settings = copy.deepcopy(inboundJSONFile["settings"])
            if (protocol =="vmess"):
                self.settingInboundVmessPanelFromJSONFile(settings, openFromJSONFile)
                self.comboBoxInboundProtocol.setCurrentText("vmess")
            if (protocol == "socks"):
                self.settingInboundSocksPanelFromJSONFile(settings, openFromJSONFile)
                self.comboBoxInboundProtocol.setCurrentText("socks")
            if (protocol == "shadowsocks"):
                self.settingInboundShadowsocksPanelFromJSONFile(settings, openFromJSONFile)
                self.comboBoxInboundProtocol.setCurrentText("shadowsocks")
            if (protocol == "http"):
                self.settinghttpPanelFromJSONFile(settings, openFromJSONFile)
                self.comboBoxInboundProtocol.setCurrentText("http")
            if (protocol == "dokodemo-door"):
                self.settingdokodemodoorPanelFromJSONFile(settings, openFromJSONFile)
                self.comboBoxInboundProtocol.setCurrentText("dokodemo-door")

        if (tranport == False or 
            (inboundJSONFile["streamSettings"] == {} or 
             inboundJSONFile["streamSettings"] == None)):
            self.checkBoxTransportSetting.setChecked(False)
            self.groupTransportPanel.hide()
        else:
            self.settingtransportPanelFromJSONFile(
                copy.deepcopy(inboundJSONFile["streamSettings"]), openFromJSONFile)
            self.checkBoxTransportSetting.setChecked(True)
            self.groupTransportPanel.show()

        if (domainOveride and ("http" in inboundJSONFile["domainOverride"])):
            self.checkBoxDomainOverrideHTTP.setChecked(True)
        
        if(domainOveride and ("tls" in inboundJSONFile["domainOverride"])):
            self.checkBoxDomainOverrideTLS.setChecked(True)
 
    def createInboundJSONFile(self):
        inboundJSONFile = {}
        inboundJSONFile["tag"]    = self.lineEditInboundSettingTAG.text()
        inboundJSONFile["listen"] = self.lineEditInboundSettingListen.text()
        
        if (inboundJSONFile["tag"] == "" or inboundJSONFile["listen"] == ""):
            return False
        
        inboundJSONFile["protocol"] = self.comboBoxInboundProtocol.currentText()
        inboundJSONFile["allocate"] = {}
        def setAllocate(strategy = "always"):
            inboundJSONFile["allocate"]["strategy"]    = strategy
            inboundJSONFile["allocate"]["refresh"]     = self.spinBoxInboundSettingRefresh.value() 
            inboundJSONFile["allocate"]["concurrency"] = self.spinBoxInboundSettingConcurrency.value()
            
        if (self.groupBoxAllocate.isChecked()):
            inboundJSONFile["port"] = str(self.spinBoxInboundSettingPort.value()) + "-" + str(self.spinBoxMultiplePort.value())
            if (self.radioBoxInboundSettingStrategyAlways.isChecked()):
                setAllocate("always")
            else:
                setAllocate("random")
        else:
            inboundJSONFile["port"] = self.spinBoxInboundSettingPort.value()
            del inboundJSONFile["allocate"]
                
        protocol = self.comboBoxInboundProtocol.currentText()
        if (protocol == "vmess"):
            inboundJSONFile["settings"] = copy.deepcopy(self.createInboundVmessJSONFile())
        if (protocol == "socks"):
            inboundJSONFile["settings"] = copy.deepcopy(self.createInboundSocksJSONFile())
        if (protocol == "http"):
            inboundJSONFile["settings"] = copy.deepcopy(self.createHttpJSONFile())
        if (protocol == "dokodemo-door"):
            inboundJSONFile["settings"] = copy.deepcopy(self.createDokodemodorrJSONFile())
        if (protocol == "shadowsocks"):
            inboundJSONFile["settings"] = copy.deepcopy(self.createInboundShadowsocksJSONFile())
        else:
            pass
            
        inboundJSONFile["streamSettings"] = {}
        if (self.checkBoxTransportSetting.isChecked()):                 
            inboundJSONFile["streamSettings"] = copy.deepcopy(self.createtransportSettingJSONFile())
        else:
            del inboundJSONFile["streamSettings"]
            
        inboundJSONFile["domainOverride"] = []
        if (self.checkBoxDomainOverrideHTTP.isChecked()):
            inboundJSONFile["domainOverride"].append("http")
        if (self.checkBoxDomainOverrideTLS.isChecked()):
            inboundJSONFile["domainOverride"].append("tls")
            
        if (inboundJSONFile["domainOverride"] == []):
            del inboundJSONFile["domainOverride"]

        return inboundJSONFile
    
    def clearInboundPanel(self):
        self.clearTransportPanel()
        self.clearInboundPortocolPanel()
        self.clearInboundSettingPanel()
    
    def refreshInboundPaneltableWidget(self):
        self.tableWidgetInbound.setRowCount(0)
        def settableWidgetInbound(tag, ipAddress, protocol, row):
            self.tableWidgetInbound.setRowCount(row+1)
            self.tableWidgetInbound.setItem(row, 0, QTableWidgetItem(tag))
            self.tableWidgetInbound.setItem(row, 1, QTableWidgetItem(ipAddress))
            self.tableWidgetInbound.setItem(row, 2, QTableWidgetItem(protocol))
            self.tableWidgetInbound.resizeColumnsToContents()

        inbound = {}
        inboundJSONData = self.treasureChest.getInbound()
        
        try:            
            inbound["tag"]       = str(inboundJSONData["tag"])
            inbound["ipAddress"] = str(inboundJSONData["listen"]) + ":" + str(inboundJSONData["port"])
            inbound["protocol"]  = str(inboundJSONData["protocol"])
        except Exception: return

        inboundDetourTags = self.treasureChest.getInboundTags()
        inboundDetour = []
        if (len(inboundDetourTags) > 1):
            for i in inboundDetourTags[1:]:
                inboundDetourJSONData = self.treasureChest.getInboundDetour(i)
                inboundDetour.append(dict(tag       = inboundDetourJSONData["tag"], 
                                          ipAddress = str(inboundDetourJSONData["listen"]) + ":" + str(inboundDetourJSONData["port"]),
                                          protocol  = str(inboundDetourJSONData["protocol"])))
                del inboundDetourJSONData
        inboundDetour.insert(0, inbound)

        for i in range(0, len(inboundDetour)):
            settableWidgetInbound(inboundDetour[i]["tag"], 
                                  inboundDetour[i]["ipAddress"], 
                                  inboundDetour[i]["protocol"], 
                                  i)
        self.clearInboundPanel()

    def __debugTest(self):
        boundJSONFile = self.treasureChest.exportInboudJSONFile()
        print(json.dumps(boundJSONFile, indent = 4, sort_keys = False))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = InboundPanel()
    ex.ScrollWidget(ex.createInboundPanel())
    ex.setGeometry(300, 100, 1024, 768)
    ex.show()
    sys.exit(app.exec_())
