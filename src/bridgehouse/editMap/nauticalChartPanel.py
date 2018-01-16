#!/usr/bin/env python3

from PyQt5.QtWidgets import (QWidget, QButtonGroup, QVBoxLayout, QApplication,
                            QTabWidget, QScrollArea, QHBoxLayout, QPushButton,
                            QDialog, QFileDialog)                         
from PyQt5.QtCore import QFileInfo, QCoreApplication
import sys, json

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))
    
from bridgehouse.editMap.port import (inboundPanel, outboundPanel, logbook, openV2rayJSONFile, treasureChest)
from bridgehouse.editMap import (logTAB, dnsTAB, transportTAB, routingTAB, policyTAB)

class nauticalChartPanel(QDialog):
    def __init__(self, filePath = False):
        super().__init__()
        self.configJSONFile = {
                            "log": {},
                            "dns": {},
                            "routing": {},
                            "policy":  {},
                            "inbound": {},
                            "outbound": {},
                            "inboundDetour": [],
                            "outboundDetour": [],
                            "transport": {}
                        }
        self.filePath = filePath
        self.treasureChest = treasureChest.treasureChest()
        self.translate = QCoreApplication.translate

    def createPanel(self):
        hboxButton = QHBoxLayout()
        btnSave = QPushButton(self.translate("nauticalChartPanel", "Save"))
        btnExit = QPushButton(self.translate("nauticalChartPanel", "Exit")) 
        self.groupButtonConfigure = QButtonGroup()
        self.groupButtonConfigure.addButton(btnSave)
        self.groupButtonConfigure.addButton(btnExit)
        
        hboxButton.addStretch()
        hboxButton.addWidget(btnSave)
        hboxButton.addWidget(btnExit)

        self.inbound  = inboundPanel.InboundPanel(self.treasureChest)
        self.outbound = outboundPanel.OutboundPanel(self.treasureChest)

        tabWidgetConfigurePanel = QTabWidget()
        tabWidgetConfigurePanel.addTab(
            self.inbound.createInboundPanel(), 
            self.translate("nauticalChartPanel", "Inbound"))
        tabWidgetConfigurePanel.addTab(
            self.outbound.createOutboundPanel(), 
            self.translate("nauticalChartPanel", "Outbound"))
        
        self.transportTAB = transportTAB.transportTab()
        tabWidgetConfigurePanel.addTab(
            self.transportTAB.createTransportPanel(), 
            self.translate("nauticalChartPanel", "Transport Setting"))
        
        self.dnsTAB = dnsTAB.dnsTab()
        tabWidgetConfigurePanel.addTab(
            self.dnsTAB.createDnsTab(), 
            self.translate("nauticalChartPanel", "DNS Server"))
        
        self.routingTAB = routingTAB.routingTab()
        tabWidgetConfigurePanel.addTab(
            self.routingTAB.createRoutingTab(), 
            self.translate("nauticalChartPanel", "Router Setting"))
        
        self.policyTAB = policyTAB.policyTab(self.treasureChest)
        tabWidgetConfigurePanel.addTab(
            self.policyTAB.createPolicyTab(), 
            self.translate("nauticalChartPanel", "Policy"))
        
        self.logTAB = logTAB.logTab()
        tabWidgetConfigurePanel.addTab(
            self.logTAB.createLogTab(), 
            self.translate("nauticalChartPanel", "Log Files"))
        
        vboxConfigure = QVBoxLayout()
        vboxConfigure.addWidget(tabWidgetConfigurePanel)
        vboxConfigure.addLayout(hboxButton)
        self.ScrollLayout(vboxConfigure)
        
        if (v2rayshellDebug):
            self.__debugBtn     = QPushButton("__debugTest", self)
            self.__debugRefresh = QPushButton("__RefreshTest", self)
            self.__printTags    = QPushButton("__PrintTags", self)
            self.__printAllLevels = QPushButton("__PrintAllLevels", self)
            self.__printAllEmails = QPushButton("__PrintAllEmails", self)
            
            hboxBtn = QHBoxLayout(self)
            hboxBtn.addWidget(self.__debugBtn)
            hboxBtn.addWidget(self.__printTags)
            hboxBtn.addWidget(self.__printAllLevels)
            hboxBtn.addWidget(self.__printAllEmails)
            hboxBtn.addWidget(self.__debugRefresh)
            vboxConfigure.addLayout(hboxBtn)
            
            self.__debugBtn.clicked.connect(self.__debugTest)
            self.__debugRefresh.clicked.connect(self.__debugRefreshTest)
            self.__printTags.clicked.connect(lambda: print(self.treasureChest.getAllTags()))
            self.__printAllLevels.clicked.connect(lambda: print(self.treasureChest.getLevels()))
            self.__printAllEmails.clicked.connect(lambda: print(self.treasureChest.getEmails()))
            
            self.editV2rayJSONFile = openV2rayJSONFile.editV2rayJSONFile(self.treasureChest)
            tabWidgetConfigurePanel.addTab(self.editV2rayJSONFile.createPanel(), "open V2ray File")
            self.settingv2rayshellPanelFromJSONFile(True)

        if (self.filePath):
            openV2rayJSONFile.openV2rayJSONFile(self.filePath, self.treasureChest).initboundJSONData()
            self.settingv2rayshellPanelFromJSONFile(openFromJSONFile = True)
        
        self.createPanelSignals()

    def createPanelSignals(self):
        self.groupButtonConfigure.buttonClicked.connect(self.ongroupButtonConfigureclicked)
        
    def ongroupButtonConfigureclicked(self, e):
        print(e.text())
        if e.text() == self.translate("nauticalChartPanel", "Exit"):
            self.close()
        elif e.text() == self.translate("nauticalChartPanel", "Save"):
            self.savenauticalChart(self.createv2rayJSONFile())
    
    def savenauticalChart(self, JSONData):
        JSONData = json.dumps(JSONData, indent = 4, sort_keys = False)
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getSaveFileName(self,
                                                  self.translate("nauticalChartPanel", "Save V2Ray config.json File"),
                                                  "config.json",
                                                  """
                                                  V2Ray config.json (config.json);;
                                                  json file (*.json);;
                                                  All Files (*)
                                                  """,
                                                  options = options)
        if (filePath):
            openV2rayJSONFile.openV2rayJSONFile().saveTextdata(filePath = filePath, 
                                                               data     = JSONData)
    
    def settingv2rayshellPanelFromJSONFile(self, openFromJSONFile = False):
        logbook.setisOpenJSONFile(openFromJSONFile)
        if (openFromJSONFile):
            self.inbound.refreshInboundPaneltableWidget()
            self.outbound.refreshOutboundPaneltableWidget()
            self.routingTAB.settingRoutingTABFromJSONFile(
                routingJSONFile = self.treasureChest.getRouting(), openFromJSONFile = True)
            self.logTAB.settingLogTabFromJSONFile(
                logJSONFile = self.treasureChest.getLog(), openFromJSONFile = True)
            tansportJSONData = self.treasureChest.getTransport()
            if (tansportJSONData):
                self.transportTAB.settingtransportPanelFromJSONFile(
                    transportJSONFile = tansportJSONData, openFromJSONFile = True)
                self.transportTAB.groupTransportPanel.setChecked(True)
            else:
                pass
            self.dnsTAB.settingDnsTabFromJSONFile(
                dnsJSONFile = self.treasureChest.getDns(), openFromJSONFile = True)
            self.policyTAB.settingPolicyTabFromJSONFile(
                policyJSONFile = self.treasureChest.getPolicy())

    def createv2rayJSONFile(self):
        self.treasureChest.setDns(self.dnsTAB.createDnsJSONFile())
        self.treasureChest.setLog(self.logTAB.createLogJSONFile())
        self.treasureChest.setRouting(self.routingTAB.createRoutingJSONFile())
        self.treasureChest.setPolicy(JSONDataPolicy = self.policyTAB.createPolicyJSONFile())
        if (self.transportTAB.groupTransportPanel.isChecked()):
            self.treasureChest.setTransport(self.transportTAB.createtransportSettingJSONFile())
        else:
            self.treasureChest.setTransport(JSONDataTransport = False)
        
        v2rayJSONFile = self.treasureChest.exportV2rayJSONFile()
    
        return v2rayJSONFile
        
    def __debugTest(self):
        print(json.dumps(self.createv2rayJSONFile(), indent = 4, sort_keys = False))
        
    def __debugRefreshTest(self):
        self.inbound.refreshInboundPaneltableWidget()
        self.outbound.refreshOutboundPaneltableWidget()
        self.routingTAB.settingRoutingTABFromJSONFile(
            routingJSONFile = self.treasureChest.getRouting(), openFromJSONFile = True)
        self.logTAB.settingLogTabFromJSONFile(
            logJSONFile = self.treasureChest.getLog(), openFromJSONFile = True)
        tansportJSONData = self.treasureChest.getTransport()
        if (tansportJSONData):
            self.transportTAB.settingtransportPanelFromJSONFile(
                transportJSONFile = tansportJSONData, openFromJSONFile = True)
            self.transportTAB.groupBoxStreamSetting.setChecked(True)
        else:
            pass
        self.dnsTAB.settingDnsTabFromJSONFile(
            dnsJSONFile = self.treasureChest.getDns(), openFromJSONFile = True)
        self.policyTAB.settingPolicyTabFromJSONFile(
            policyJSONFile = self.treasureChest.getPolicy())
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = nauticalChartPanel()
    ex.createPanel()
    ex.setGeometry(500, 40, 1024, 950)
    ex.show()
    sys.exit(app.exec_())