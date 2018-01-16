#!/usr/bin/env python3

from PyQt5.QtWidgets import (QVBoxLayout, QScrollArea, QWidget, 
                             QLabel, QComboBox, QHBoxLayout, 
                             QLineEdit, QPushButton, QSplitter, QTableWidget,
                             QAbstractItemView, QGroupBox, QTableWidgetItem,
                             QListView, QButtonGroup)
from PyQt5.QtCore import Qt, QFileInfo, QCoreApplication
import sys, json, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-4]))

from bridgehouse.editMap.outbound import (blackholePanel, freedomPanel, shadowsocksPanel, socksPanel, vmessPanel)
from bridgehouse.editMap.transport import muxPanel, transportPanel
from bridgehouse.editMap.port import treasureChest, logbook
        
class OutboundSettingPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate
    
    def createOutboundSettingPanel(self):
        labelTAG = QLabel(
            self.translate("OutboundSettingPanel", "TAG: "), self)
        self.lineEditOutboundSettingTAG = QLineEdit()
        labelsendThrough = QLabel(
            self.translate("OutboundSettingPanel", "Send Through IP: "), self)
        self.lineEditOutboundSettingSendThrough = QLineEdit()
        labelProxySettings = QLabel(
            self.translate("OutboundSettingPanel", "Proxy Settings: "))
        self.comboBoxOutboundDetour = QComboBox()   ### ProxySettings: tag to another Out bound tag
        self.lineEditOutboundSettingSendThrough.setText("0.0.0.0")
        self.comboBoxOutboundDetour.setView(QListView())
        self.comboBoxOutboundDetour.setStyleSheet("QComboBox {min-width: 256px; }"
                                                  "QComboBox QAbstractItemView::item {min-width: 256px; }")
        
        hboxTAG = QHBoxLayout()
        hboxTAG.addWidget(labelTAG)
        hboxTAG.addWidget(self.lineEditOutboundSettingTAG)
        hboxTAG.addStretch()
        
        hboxsendThrough = QHBoxLayout()
        hboxsendThrough.addWidget(labelsendThrough)
        hboxsendThrough.addWidget(self.lineEditOutboundSettingSendThrough)
        hboxsendThrough.addStretch()
        
        hboxProxySetting = QHBoxLayout()
        hboxProxySetting.addWidget(labelProxySettings)
        hboxProxySetting.addWidget(self.comboBoxOutboundDetour)
        hboxProxySetting.addStretch()
        
        self.vboxOutboundSetting = QVBoxLayout()
        self.vboxOutboundSetting.addLayout(hboxTAG)
        self.vboxOutboundSetting.addLayout(hboxsendThrough)
        self.vboxOutboundSetting.addLayout(hboxProxySetting)
        
        return self.vboxOutboundSetting
    
    def clearOutboundSettingPanel(self):
        self.lineEditOutboundSettingSendThrough.clear()
        self.lineEditOutboundSettingTAG.clear()
        self.comboBoxOutboundDetour.setCurrentIndex(0)

class OutboundPortocolPanel(blackholePanel.BlackholePanel,
                            freedomPanel.FreedomPanel,
                            shadowsocksPanel.OutboundShadowsocksPanel,
                            socksPanel.OutboundSocksPanel,
                            vmessPanel.OutboundVmessSettingPanel):
    def __init__(self):
        super().__init__()
        self.translate = QCoreApplication.translate
        self.listComboxProtocol = "vmess", "socks", "shadowsocks", "blackhole", "freedom" 
        
    def createOutboundPortocolPanel(self):
        
        labelProtocol = QLabel(
            self.translate("OutboundPortocolPanel", "Protocol: "), self)
        self.comboBoxoutboundProtocol = QComboBox()
        self.comboBoxoutboundProtocol.addItems(self.listComboxProtocol)
       
        self.outvmess  = self.createOutboundVmessPanel()
        self.freedom   = self.createFreedomSettingPanel()
        self.blackhole = self.createBlackholeSettingPanel()
        self.outsocks  = self.createOutboundSocksSettingPanel()
        self.outshadowsocks = self.createShadowsocksSettingPanel()
        
        self.outvmess.show()
        self.freedom.hide()
        self.outshadowsocks.hide()
        self.blackhole.hide()
        self.outsocks.hide()
        
        hboxoutboundProtocol = QHBoxLayout()
        hboxoutboundProtocol.addWidget(labelProtocol)
        hboxoutboundProtocol.addWidget(self.comboBoxoutboundProtocol)
        hboxoutboundProtocol.addStretch()
        
        self.vboxoutboundProtocol = QVBoxLayout()
        self.vboxoutboundProtocol.addLayout(hboxoutboundProtocol)
        self.vboxoutboundProtocol.addWidget(self.blackhole)
        self.vboxoutboundProtocol.addWidget(self.outvmess)
        self.vboxoutboundProtocol.addWidget(self.freedom)
        self.vboxoutboundProtocol.addWidget(self.outshadowsocks)
        self.vboxoutboundProtocol.addWidget(self.outsocks)
        
        self.createInboundPortocolPanelSignals()
        
        return self.vboxoutboundProtocol
        
    def createInboundPortocolPanelSignals(self):
        self.comboBoxoutboundProtocol.currentTextChanged.connect(self.oncomboBoxoutboundProtocol)
        
    def oncomboBoxoutboundProtocol(self, e):
        def showProtocol(protocol = e):
            self.outvmess.hide()
            self.freedom.hide()
            self.outshadowsocks.hide()
            self.blackhole.hide()
            self.outsocks.hide()
            if (protocol == "vmess"):
                self.outvmess.show()
            elif (protocol == "socks"):
                self.outsocks.show()
            elif (protocol == "shadowsocks"):
                self.outshadowsocks.show()
            elif (protocol == "blackhole"):
                self.blackhole.show()
            elif (protocol == "freedom"):
                self.freedom.show()

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
        
    def clearOutboundPortocolPanel(self):
        self.clearblackholePanel()
        self.clearfreedomPanel()
        self.clearoutboundShadowsocksPanel()
        self.clearoutboundSocksPanel()
        self.clearoutboundVmessPanel()
 
class OutboundPanel(OutboundPortocolPanel, 
                    OutboundSettingPanel, 
                    muxPanel.muxPanel,
                    transportPanel.TransportPanel):
    def __init__(self, CaptainstreasureChest = False):
        super().__init__()
        self.outboundJSONFile = {
                                    "sendThrough": "0.0.0.0",
                                    "protocol": "vmess",
                                    "settings": {},
                                    "tag": "Outbound",
                                    "streamSettings": {},
                                    "proxySettings": {
                                        "tag": "another-outbound-tag"
                                    },
                                    "mux": {}
                                }
        self.tableWidgetOutboundVerticalHeaderLabels = ["Outbound"]
        
        if (CaptainstreasureChest):
            self.treasureChest = CaptainstreasureChest
        else:
            self.treasureChest = treasureChest.treasureChest()  ### a empty treasure chest

        self.updateList = self.treasureChest.updateList
        self.translate = QCoreApplication.translate
        
        self.labelHeaderOutbound = (self.translate("OutboundPanel", "Tag name"), 
                                    self.translate("OutboundPanel", "Protocol"))
        
    def createOutboundPanel(self):
        super(OutboundPanel, self).createmuxSettingPanel()
        super(OutboundPanel, self).createOutboundSettingPanel()
        super(OutboundPanel, self).createOutboundPortocolPanel()
        super(OutboundPanel, self).createTransportPanel()
        
        vboxOutboundPanel = QVBoxLayout()
        vboxOutboundPanel.addLayout(self.vboxOutboundSetting)
        vboxOutboundPanel.addLayout(self.vboxoutboundProtocol)
        vboxOutboundPanel.addWidget(self.groupBoxmuxSetting)
        vboxOutboundPanel.addLayout(self.vboxcheckBoxStreamSetting)
        vboxOutboundPanel.addStretch()
        
        groupBoxOutbound = QGroupBox("", self)
        groupBoxOutbound.setLayout(vboxOutboundPanel)
    
        self.tableWidgetOutbound = tableWidgetOutbound = QTableWidget()
        tableWidgetOutbound.setColumnCount(2)
        tableWidgetOutbound.setHorizontalHeaderLabels(self.labelHeaderOutbound)
        tableWidgetOutbound.setSelectionMode(QAbstractItemView.SingleSelection)
        tableWidgetOutbound.setSelectionBehavior(QAbstractItemView.SelectRows)
        tableWidgetOutbound.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tableWidgetOutbound.horizontalHeader().setStretchLastSection(True)
        
        splitterOutbound = QSplitter(Qt.Horizontal)
        splitterOutbound.addWidget(tableWidgetOutbound)
        splitterOutbound.addWidget(groupBoxOutbound)
        
        btnOutboundApply  = QPushButton(
            self.translate("OutboundPanel", "Add"), self)
        btnOutboundDelete = QPushButton(
            self.translate("OutboundPanel", "Delete"), self)
        btnOutboundChange = QPushButton(
            self.translate("OutboundPanel", "Apply"), self)
        
        self.btnGroupOutbound = btnGroupOutbound = QButtonGroup()
        btnGroupOutbound.addButton(btnOutboundApply)
        btnGroupOutbound.addButton(btnOutboundChange)
        btnGroupOutbound.addButton(btnOutboundDelete)
        
        hboxbtnOutbound = QHBoxLayout()
        hboxbtnOutbound.addStretch()
        hboxbtnOutbound.addWidget(btnOutboundApply)
        hboxbtnOutbound.addWidget(btnOutboundChange)
        hboxbtnOutbound.addWidget(btnOutboundDelete)
        
        vboxSpliterOutbound = QVBoxLayout()
        vboxSpliterOutbound.addWidget(splitterOutbound)
        vboxSpliterOutbound.addLayout(hboxbtnOutbound)
        
        groupBoxSpliterOutbound = QGroupBox("", self)
        groupBoxSpliterOutbound.setLayout(vboxSpliterOutbound)
        
        if (v2rayshellDebug):
            self.__debugBtn = QPushButton("__debugTest", self)
            vboxSpliterOutbound.addWidget(self.__debugBtn)
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.settingOutboundPanelFromJSONFile(self.outboundJSONFile, True)

        self.createOutboundPanelSignals()
        
        return groupBoxSpliterOutbound
    
    def createOutboundPanelSignals(self):
        self.btnGroupOutbound.buttonClicked.connect(self.onbtnGroupOutbound)
        self.tableWidgetOutbound.clicked.connect(self.ontableWidgetOutboundItemSelection)
        self.tableWidgetOutbound.itemSelectionChanged.connect(self.ontableWidgetOutboundItemSelection)
        
    def onbtnGroupOutbound(self, e):
        if (e.text() == self.translate("OutboundPanel", "Add")):
            self.tableWidgetOutboundAdd()
        if (e.text() == self.translate("OutboundPanel", "Delete")):
            self.tableWidgetOutboundDelete()
        if (e.text() == self.translate("OutboundPanel", "Apply")):
            self.tableWidgetOutboundChange()
            
    def setcomboBoxOutboundDetour(self, tag, currentRow):
        """
        update the self.comboBoxOutboundDetour real time, 
        when outbound had added, deleted, changed
        """
        allOutboundTags = self.treasureChest.getOutboundTags()
        if (currentRow == 0):
            currentBound = self.treasureChest.getOutbound()
        else:
            currentBound = self.treasureChest.getOutboundDetour(tag)
        if (currentBound):
            try:
                currentDetourtoTag = currentBound["proxySettings"]["tag"]
            except:
                currentDetourtoTag =  ""
            self.comboBoxOutboundDetour.clear()
            if (tag in allOutboundTags):
                allOutboundTags.remove(tag)
            self.comboBoxOutboundDetour.addItem("")
            self.comboBoxOutboundDetour.addItems(allOutboundTags)
            self.comboBoxOutboundDetour.setCurrentText(currentDetourtoTag)

    def tableWidgetOutboundAdd(self):
        rowCount = self.tableWidgetOutbound.rowCount()
        outboundJSONData = copy.deepcopy(self.createOutboundJSONFile())
        if (outboundJSONData):
            tag       = str(outboundJSONData["tag"])
            protocol  = str(outboundJSONData["protocol"])
        else:
            return False

        def settableWidgetOutbound(tag, protocol):
            self.tableWidgetOutbound.setRowCount(rowCount + 1)
            self.tableWidgetOutbound.setItem(rowCount, 0, QTableWidgetItem(tag))
            self.tableWidgetOutbound.setItem(rowCount, 1, QTableWidgetItem(protocol))
            self.tableWidgetOutbound.resizeColumnsToContents()
            
        if (rowCount == 0):
            tag = self.treasureChest.setOutbound(outboundJSONData)
            if (tag):
                settableWidgetOutbound(tag, protocol)
                self.setcomboBoxOutboundDetour(tag, rowCount)
            else:
                ### TODO
                pass
        else:
            tag = self.treasureChest.addOutboundDetour(outboundJSONData)
            if (tag):
                settableWidgetOutbound(tag, protocol)
                self.setcomboBoxOutboundDetour(tag, rowCount)
            else:
                ### TODO
                pass
        self.clearOutboundPanel()
        
    def tableWidgetOutboundDelete(self):
        currentRow = self.tableWidgetOutbound.currentRow()
        tag = self.tableWidgetOutbound.item(currentRow, 0)
        
        if (tag and currentRow > 0):  ### delete outboundDetour
            if (self.treasureChest.removeOutboundDetour(tag.text()) == False):
                ### TODO
                pass
            self.tableWidgetOutbound.removeRow(currentRow)
            self.clearOutboundPanel()

        elif (tag and currentRow == 0):  ### delete outbound
            ### outbound should not be deleted
            pass

    def tableWidgetOutboundChange(self):
        currentRow = self.tableWidgetOutbound.currentRow()
        tag = self.tableWidgetOutbound.item(currentRow, 0)
        newOutboundJSONData = copy.deepcopy(self.createOutboundJSONFile())
        
        if (tag and newOutboundJSONData):
            newtag    = str(newOutboundJSONData["tag"])
            protocol  = str(newOutboundJSONData["protocol"])
            def settableWidgetOutbound():
                self.tableWidgetOutbound.setItem(currentRow, 0, QTableWidgetItem(newtag))
                self.tableWidgetOutbound.setItem(currentRow, 1, QTableWidgetItem(protocol))
                self.tableWidgetOutbound.resizeColumnsToContents()
            
            if (currentRow == 0):
                if (self.treasureChest.setOutbound(newOutboundJSONData)):
                    settableWidgetOutbound()
                    self.setcomboBoxOutboundDetour(newtag, currentRow)
                else:
                    ### TODO
                    pass
            if (currentRow > 0):
                if (self.treasureChest.setOutboundDetour(tag.text(), newOutboundJSONData)):
                    settableWidgetOutbound()
                    self.setcomboBoxOutboundDetour(newtag, currentRow)
                else:
                    ### TODO
                    pass
        else:
            return False
                
    def ontableWidgetOutboundItemSelection(self):
        currentRow = self.tableWidgetOutbound.currentRow()
        tag        = self.tableWidgetOutbound.item(currentRow, 0)
        if (tag):
            if (currentRow == 0):
                outboundJSONFile = self.treasureChest.getOutbound()
                if (outboundJSONFile):
                    self.settingOutboundPanelFromJSONFile(outboundJSONFile)
                    self.setcomboBoxOutboundDetour(outboundJSONFile["tag"], currentRow)
                    del outboundJSONFile
                else:
                    ### TODO
                    pass
            if (currentRow > 0):
                outboundJSONFile = self.treasureChest.getOutboundDetour(tag.text())
                if (outboundJSONFile):
                    self.settingOutboundPanelFromJSONFile(outboundJSONFile)
                    self.setcomboBoxOutboundDetour(outboundJSONFile["tag"], currentRow)
                    del outboundJSONFile
                else:
                    ### TODO
                    pass

    def settingOutboundPanelFromJSONFile(self, outboundJSONFile, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        transport = True; mux = True; detourPorxy = True; tag = True
        
        if (outboundJSONFile == None): outboundJSONFile = {}
        
        try:
            outboundJSONFile["sendThrough"]
        except KeyError as e:
            logbook.writeLog("Outbound", "KeyError", e)
            outboundJSONFile["sendThrough"] = ""
     
        try:
            outboundJSONFile["protocol"]
        except KeyError as e:
            logbook.writeLog("Outbound", "KeyError", e)
            outboundJSONFile["protocol"] = "vmess"
     
        try:
            outboundJSONFile["tag"]
        except KeyError as e:
            logbook.writeLog("Outbound", "KeyError", e)
            outboundJSONFile["tag"] = ""
            tag = False 
        
        try:
            outboundJSONFile["settings"]
        except KeyError as e:
            logbook.writeLog("Outbound", "KeyError", e)
            outboundJSONFile["settings"] = {}     
        
        try:    
            outboundJSONFile["streamSettings"]
        except KeyError as e:
            outboundJSONFile["streamSettings"] = {}
            logbook.writeLog("Outbound", "KeyError", e)     
            transport = False
            
        try:
            outboundJSONFile["proxySettings"]
        except KeyError as e:
            logbook.writeLog("Outbound", "KeyError", e)
            outboundJSONFile["proxySettings"] = {}

        try:
            outboundJSONFile["proxySettings"]["tag"]
        except KeyError as e:
            outboundJSONFile["proxySettings"]["tag"] = ""
            logbook.writeLog("Outbound", "KeyError", e)
            detourPorxy = False

        try:
            outboundJSONFile["mux"]
        except KeyError as e:
            outboundJSONFile["mux"] = {}
            mux = False
        
        if (tag):
            self.lineEditOutboundSettingTAG.setText(str(outboundJSONFile["tag"]))

        self.lineEditOutboundSettingSendThrough.setText(str(outboundJSONFile["sendThrough"]))
                
        if (detourPorxy and outboundJSONFile["proxySettings"]["tag"] != ""):
            ### TODO if JSONFile open from user conf, need get all outbound tags
            self.comboBoxOutboundDetour.addItem(outboundJSONFile["proxySettings"]["tag"])
            self.comboBoxOutboundDetour.setCurrentText(outboundJSONFile["proxySettings"]["tag"])
        else:
            self.comboBoxOutboundDetour.addItem("")
            self.comboBoxOutboundDetour.setCurrentText("")
        
        outboundProtocol = outboundJSONFile["protocol"]
        if (outboundJSONFile["settings"] != {} or outboundJSONFile["settings"] != None):
            settings = copy.deepcopy(outboundJSONFile["settings"])
            if (outboundProtocol == "vmess"):
                self.settingOutboundVmessPanelFromJSONFile(settings, openFromJSONFile)
            if (outboundProtocol == "socks"):
                self.settingOutboundSocksPanelFromJSONFile(settings, openFromJSONFile)
            if (outboundProtocol == "shadowsocks"):
                self.settingOutboundShadowsocksPanelFromJSONFile(settings, openFromJSONFile)
            if (outboundProtocol == "blackhole"):
                self.settingblackholePanelFromJSONFile(settings, openFromJSONFile)
            if (outboundProtocol == "freedom"):
                self.settingfreedomPanelFromJSONFile(settings, openFromJSONFile)
    
        if (outboundProtocol in self.listComboxProtocol):
            self.comboBoxoutboundProtocol.setCurrentText(outboundProtocol)

        if (transport == False or 
            (outboundJSONFile["streamSettings"] == {}) or
            (outboundJSONFile["streamSettings"] == None)):
            self.checkBoxTransportSetting.setChecked(False)
            self.groupTransportPanel.hide()
        else:
            self.settingtransportPanelFromJSONFile(
                copy.deepcopy(outboundJSONFile["streamSettings"]), openFromJSONFile)
            self.checkBoxTransportSetting.setChecked(True)
            self.groupTransportPanel.show()
                
        if (mux == False and 
            (outboundJSONFile["mux"] == {}) or 
            outboundJSONFile["mux"] == None):
            self.groupBoxmuxSetting.setChecked(False) 
        else:
            self.settingmuxPanelFromJSONFile(
                copy.deepcopy(outboundJSONFile["mux"]), openFromJSONFile)
            self.groupBoxmuxSetting.setChecked(True)

    def createOutboundJSONFile(self):
        outboundJSONFile = {}
        outboundJSONFile["tag"]         = self.lineEditOutboundSettingTAG.text()
        outboundJSONFile["sendThrough"] = self.lineEditOutboundSettingSendThrough.text()
        if (outboundJSONFile["tag"] == ""):
            return False
        
        if outboundJSONFile["sendThrough"] == "":
            del outboundJSONFile["sendThrough"]

        outboundProtocol = self.comboBoxoutboundProtocol.currentText()
        outboundJSONFile["protocol"] = copy.deepcopy(outboundProtocol)
        outboundJSONFile["settings"] = {}
        if (outboundProtocol == "vmess"):
            outboundJSONFile["settings"] = copy.deepcopy(self.createOutboundVmessJSONFile())
        if (outboundProtocol == "socks"):
            outboundJSONFile["settings"] = copy.deepcopy(self.createOutboundSocksJSONFile())
        if (outboundProtocol == "shadowsocks"):
            outboundJSONFile["settings"] = copy.deepcopy(self.createOutboundShadowsocksJSONFile())
        if (outboundProtocol == "blackhole"):
            outboundJSONFile["settings"] = copy.deepcopy(self.createblackholeJSONFile())
        if (outboundProtocol == "freedom"):
            outboundJSONFile["settings"] = copy.deepcopy(self.createFreedomJSONFile())
        del outboundProtocol
        
        outboundJSONFile["streamSettings"] = {}
        if (self.checkBoxTransportSetting.isChecked()):
            outboundJSONFile["streamSettings"] = copy.deepcopy(self.createtransportSettingJSONFile())
        else:
            del outboundJSONFile["streamSettings"]

        outboundJSONFile["proxySettings"] = {}
        outboundJSONFile["proxySettings"]["tag"] = self.comboBoxOutboundDetour.currentText()
        if (outboundJSONFile["proxySettings"]["tag"] == ""):
            del outboundJSONFile["proxySettings"]

        outboundJSONFile["mux"] = {}
        if (self.groupBoxmuxSetting.isChecked()):
            outboundJSONFile["mux"] = copy.deepcopy(self.createmuxSettingJSONFile())
        else:
            del outboundJSONFile["mux"]

        return outboundJSONFile
    
    def clearOutboundPanel(self):
        self.clearOutboundPortocolPanel()
        self.clearOutboundSettingPanel()
        self.clearmuxPanel()
        self.clearTransportPanel()
    
    def refreshOutboundPaneltableWidget(self):
        self.tableWidgetOutbound.setRowCount(0)
        def settableWidgetOutbound(tag, protocol, row):
            self.tableWidgetOutbound.setRowCount(row+1)
            self.tableWidgetOutbound.setItem(row, 0, QTableWidgetItem(tag))
            self.tableWidgetOutbound.setItem(row, 1, QTableWidgetItem(protocol))
            self.tableWidgetOutbound.resizeColumnsToContents()
        
        outbound = {}
        outboundJSONData = self.treasureChest.getOutbound()
        try:
            outbound["tag"]       = str(outboundJSONData["tag"])
            outbound["protocol"]  = str(outboundJSONData["protocol"])
        except Exception: return
        
        outboundDetourTags = self.treasureChest.getOutboundTags()
        outboundDetour = []
        if (len(outboundDetourTags) > 1):
            for i in outboundDetourTags[1:]:
                outboundDetourJSONData = self.treasureChest.getOutboundDetour(i)
                outboundDetour.append(dict(tag       = outboundDetourJSONData["tag"],
                                           protocol  = outboundDetourJSONData["protocol"]))
                del outboundDetourJSONData
        outboundDetour.insert(0, outbound)
        
        for i in range(0, len(outboundDetour)):
            settableWidgetOutbound(outboundDetour[i]["tag"],
                                   outboundDetour[i]["protocol"], 
                                   i)

    def __debugTest(self):
        boundJSONFile = self.treasureChest.exportOutBoundJSONFile()
        print(json.dumps(boundJSONFile, indent = 4, sort_keys = False))

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = OutboundPanel()
    ex.ScrollWidget(ex.createOutboundPanel())
    ex.setGeometry(300, 100, 1024, 768)
    ex.show()
    sys.exit(app.exec_())
