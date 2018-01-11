#!/usr/bin/env python3

from PyQt5.QtWidgets import (QTableWidget, QAbstractItemView, QTableWidgetItem,
                             QMainWindow, QTextEdit, QSplitter, QAction,
                             QFileDialog, QRadioButton, QButtonGroup, QInputDialog,
                             QMenu, QLabel, QToolBar, QStyle, QDialog, QVBoxLayout,
                             QApplication, QSystemTrayIcon)
from PyQt5.QtCore import (Qt, QFileInfo, QTimer, QEvent, QObject,
                          pyqtSignal, QCoreApplication, QTranslator)
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.Qt import QSize, QCursor
from PyQt5.QtNetwork import QNetworkProxy

import sys, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-1]))

filePath = sys.path[0]
# Detect if running in a bundle
if getattr(sys, 'frozen', False):
    filePath = sys._MEIPASS

from bridgehouse.extension import (proxyTest, bridgePreference, updatePanel, 
                                   runV2raycore, bridgetreasureChest, bugReport)
from bridgehouse.editMap import nauticalChartPanel
      
class clickedRow:
    rightClickedRow = False
    mousePos = False

class proxyTryconnect(QObject):
    reconnectproxy = pyqtSignal()
    
    def __init__(self):
        super(proxyTryconnect, self).__init__()
        self.trytimes = 0
        self.keeptrytimes = False
        self.resetTime = False
        self.reset = QTimer()

    def setresetTime(self, time):
        self.resetTime = copy.deepcopy(int(time)) + 30
        self.reset.timeout.connect(lambda: self.setTrytimes(self.keeptrytimes))
        self.reset.start(1000 * self.resetTime)
    
    def setTrytimes(self, times):
        self.trytimes = times
        ### keep the times for timeout reset times
        self.keeptrytimes = copy.deepcopy(times)
        
    def trytimesDecrease(self):
        if self.trytimes == 0:
            self.reconnectproxy.emit()
            return True
        self.trytimes -= 1

class bridgePanel(QMainWindow, QObject):
    start = pyqtSignal()
    stop  = pyqtSignal()

    def __init__(self, app):
        super().__init__()
        self.__v2rayshellConfigFile = {
                                        "preferences": {        
                                            "v2ray-core": "",
                                            "v2ray-coreFilePath": "",
                                            "connection": {
                                                "connect": "switch",
                                                "interval": 45,
                                                "timeout": 3,
                                                "enable": True,
                                                "trytimes": 3
                                                }
                                            },
                                        "configFiles": [
                                            {
                                                "enable": True,
                                                "hostName": "",
                                                "configFileName": ""
                                            }
                                         ]
                                   }
        self.bridgetreasureChest = bridgetreasureChest.bridgetreasureChest()
        self.app = app
        self.translate = QCoreApplication.translate
        self.__v2rayshellVersion = "20171119"
        self.__windowTitile = "V2Ray-shell"
        self.runv2raycore = False
        self.iconStart = QIcon()
        self.iconStop  = QIcon()
        self.__iconSize = QSize(32, 32)
        self.iconStart.addPixmap(QPixmap(filePath + "/icons/start.png"), QIcon.Normal, QIcon.On)
        self.iconStop.addPixmap(QPixmap(filePath + "/icons/stop.png"), QIcon.Disabled, QIcon.On)
        self.currentRowRightClicked = False
        self.v2rayshellTrayIcon = QSystemTrayIcon()
        self.v2rayshellTrayIcon.setIcon(self.iconStart)
        self.v2rayshellTrayIcon.show()
        
        self.radioButtonGroup = QButtonGroup()
        
        self.setV2RayshellLanguage()
        self.trytimes = self.bridgetreasureChest.getConnectiontrytimes()
        self.interval = self.bridgetreasureChest.getConnectioninterval() 
        self.proxyTryConnect = proxyTryconnect()
        self.proxyTryConnect.setTrytimes(self.trytimes)
        self.proxyTryConnect.setresetTime(self.trytimes * self.interval)
        self.labelBridge = (self.translate("bridgePanel", "Start/Stop"), 
                            self.translate("bridgePanel", "Host Name"), 
                            self.translate("bridgePanel", "Config Name"), 
                            self.translate("bridgePanel", "Proxy"), 
                            self.translate("bridgePanel", "Time Lag"))

        self.createBridgePanel()

    def createBridgePanel(self):
        self.setWindowTitle(self.__windowTitile)
        self.setWindowIcon(self.iconStart)
        menubar = self.menuBar()
        self.statusBar()

        self.actionNewV2rayConfigFile = QAction(
            self.translate("bridgePanel", "Add V2Ray-core Config File"), self)
        self.actionNewV2rayConfigFile.setShortcut("Ctrl+n")
        self.actionNewV2rayConfigFile.setStatusTip(
            self.translate("bridgePanel", "Add V2Ray-core Config File"))
        
        self.actionSaveV2rayshellConfigFile = QAction(
            self.translate("bridgePanel", "Save V2Ray-shell Config File"), self)
        self.actionSaveV2rayshellConfigFile.setShortcut("Ctrl+s")
        self.actionSaveV2rayshellConfigFile.setStatusTip(
            self.translate("bridgePanel", "Save V2Ray-shell Config File"))
        
        self.actionReloadV2rayshellConfigFile = QAction(
            self.translate("bridgePanel", "Open V2Ray-shell Config File"), self)
        self.actionReloadV2rayshellConfigFile.setShortcut("Ctrl+o")
        self.actionReloadV2rayshellConfigFile.setStatusTip(
            self.translate("bridgePanel", "Open V2Ray-shell Config File"))
        
        self.actionQuitV2rayshellPanel = QAction(
            self.translate("bridgePanel", "Quit"), self)
        self.actionQuitV2rayshellPanel.setShortcut("Ctrl+Shift+q")
        self.actionQuitV2rayshellPanel.setStatusTip(
            self.translate("bridgePanel", "Quit V2Ray-shell"))

        fileMenu = menubar.addMenu(
            self.translate("bridgePanel", "&File"))
        fileMenu.addAction(self.actionNewV2rayConfigFile)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actionReloadV2rayshellConfigFile)
        fileMenu.addAction(self.actionSaveV2rayshellConfigFile)
        fileMenu.addSeparator()
        fileMenu.addAction(self.actionQuitV2rayshellPanel)
        
        self.texteditBridge = QTextEdit(self)
        self.texteditBridge.setReadOnly(True)
        
        self.tableWidgetBridge = QTableWidget()
        self.tableWidgetBridge.setRowCount(0)
        self.tableWidgetBridge.setColumnCount(5)
        self.tableWidgetBridge.setHorizontalHeaderLabels(self.labelBridge)
        self.tableWidgetBridge.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidgetBridge.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidgetBridge.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tableWidgetBridge.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetBridge.setContextMenuPolicy(Qt.CustomContextMenu)
        
        self.popMenu = popMenu = QMenu(self.tableWidgetBridge)
        self.actionpopMenuAddV2rayConfigFile  = QAction(
            self.translate("bridgePanel", "Add V2Ray Config File"), self)
        self.actionpopMenuAddV2rayConfigFile.setShortcut("Ctrl+n")
        self.actionpopMenuEditV2rayConfigFile = QAction(
            self.translate("bridgePanel", "Edit V2Ray Config File"), self)
        self.actionpopMenuProxyCheckTimeLag   = QAction(
            self.translate("bridgePanel", "Proxy Time Lag Check..."), self)
        self.actionpopMenuDeleteRow           = QAction(
            self.translate("bridgePanel", "Delete"), self)
        
        popMenu.addAction(self.actionpopMenuAddV2rayConfigFile)
        popMenu.addAction(self.actionpopMenuEditV2rayConfigFile)
        popMenu.addAction(self.actionpopMenuProxyCheckTimeLag)
        popMenu.addAction(self.actionpopMenuDeleteRow)
        
        self.actionopenV2rayshellPreferencesPanel = QAction(
            self.translate("bridgePanel", "preferences"), self)
        self.actionopenV2rayshellPreferencesPanel.setStatusTip(
            self.translate("bridgePanel", "Setting V2Ray-shell"))
        
        optionMenu = menubar.addMenu(self.translate("bridgePanel", "&options"))
        optionMenu.addAction(self.actionpopMenuProxyCheckTimeLag)
        optionMenu.addAction(self.actionopenV2rayshellPreferencesPanel)
        
        helpMenu = menubar.addMenu(self.translate("bridgePanel", "&help"))
        self.actioncheckv2raycoreupdate  = QAction(
            self.translate("bridgePanel", "check V2Ray-core update"), self)
        self.actionv2rayshellBugreport   = QAction(self.translate("bridgePanel", "Bug Report"), self)
        self.actionaboutv2rayshell  = QAction(self.translate("bridgePanel", "About"), self)
        
        helpMenu.addAction(self.actioncheckv2raycoreupdate)
        helpMenu.addAction(self.actionv2rayshellBugreport)
        helpMenu.addAction(self.actionaboutv2rayshell)
        
        toolBar = QToolBar()
        self.actionV2rayStart = QAction(self.translate("bridgePanel", "Start"))
        self.actionV2rayStart.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MediaPlay")))
        self.actionV2rayStop  = QAction(self.translate("bridgePanel", "Stop"))
        self.actionV2rayStop.setIcon(self.style().standardIcon(getattr(QStyle, "SP_MediaStop")))
        toolBar.addAction(self.actionV2rayStart)
        toolBar.addAction(self.actionV2rayStop)
        self.addToolBar(toolBar)
        
        self.trayIconMenu = QMenu()
        self.v2rayshellTrayIcon.setContextMenu(self.trayIconMenu)
        
        self.trayIconMenushowhidePanel = QAction(self.translate("bridgePanel", "Show/Hide"))
        self.trayIconMenuclosePanel    = QAction(self.translate("bridgePanel", "Quit"))
        
        self.trayIconMenu.addAction(self.trayIconMenushowhidePanel)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.trayIconMenuclosePanel)
        
        self.splitterBridge = QSplitter(Qt.Vertical)
        self.splitterBridge.addWidget(self.tableWidgetBridge)
        self.splitterBridge.addWidget(self.texteditBridge)
        
        self.setCentralWidget(self.splitterBridge)
        
        self.createBridgePanelSignals()
        
        self.onloadV2rayshellConfigFile(init = True)
        
        self.onv2raycoreStart()
        
        self.autocheckv2raycoreUpdate()
  
    def createBridgePanelSignals(self):
        self.actionNewV2rayConfigFile.triggered.connect(self.tableWidgetBridgeAddNewV2rayConfigFile)
        self.actionReloadV2rayshellConfigFile.triggered.connect(self.onloadV2rayshellConfigFile)
        self.actionSaveV2rayshellConfigFile.triggered.connect(self.onsaveV2rayshellConfigFile)
        self.actionopenV2rayshellPreferencesPanel.triggered.connect(self.createBridgepreferencesPanel)
        self.actionpopMenuAddV2rayConfigFile.triggered.connect(self.tableWidgetBridgeAddNewV2rayConfigFile)
        self.actionpopMenuEditV2rayConfigFile.triggered.connect(self.oncreatenauticalChartPanel)
        self.actionpopMenuDeleteRow.triggered.connect(self.tableWidgetBridgeDelete)
        self.actionpopMenuProxyCheckTimeLag.triggered.connect(self.onproxyserverTimeLagTest)
        self.actioncheckv2raycoreupdate.triggered.connect(self.onopenv2rayupdatePanel)
        self.actionv2rayshellBugreport.triggered.connect(self.bugReportPanel)
        self.actionQuitV2rayshellPanel.triggered.connect(self.close)
        self.actionV2rayStart.triggered.connect(self.onv2raycoreStart)
        self.actionV2rayStop.triggered.connect(self.onv2raycoreStop)
        self.actionaboutv2rayshell.triggered.connect(self.about)
        self.radioButtonGroup.buttonClicked.connect(self.onradioButtonClicked)
        self.tableWidgetBridge.cellDoubleClicked.connect(self.ontableWidgetBridgecellDoubleClicked)
        self.tableWidgetBridge.customContextMenuRequested.connect(self.ontableWidgetBridgeRightClicked)
        self.v2rayshellTrayIcon.activated.connect(self.restorebridgePanel)
        self.trayIconMenushowhidePanel.triggered.connect(self.onsystemTrayIconMenushowhidebridgePanel)
        self.trayIconMenuclosePanel.triggered.connect(self.close)
        self.proxyTryConnect.reconnectproxy.connect(self.swapNextConfigFile)
        self.start.connect(self.onupdateinstallFinishedstartNewV2raycore)
        self.stop.connect(self.onv2raycoreStop)
        
    def setV2RayshellLanguage(self):
        self.trans = QTranslator()
        language     = self.bridgetreasureChest.getLanguage()
        allLanguages = self.bridgetreasureChest.getAllLanguage()
        if language and allLanguages:
            if language in allLanguages:
                self.trans.load(allLanguages[language])
                self.app.installTranslator(self.trans)
        
    def autocheckv2raycoreUpdate(self):
        self.v2rayshellautoUpdate = updatePanel.updateV2ray()
        self.bridgeSingal = (self.start, self.stop)
        self.trycheckUpdate = QTimer()
        self.trycheckUpdate.timeout.connect(
            lambda: self.v2rayshellautoUpdate.enableUpdateSchedule(
                self.bridgetreasureChest, self.bridgeSingal))
        
        self.trycheckUpdate.start(1000 * 60 * 60 * 4) ### Check every four hours
        self.trycheckUpdate.singleShot(               ### Check when the script is started
            1000 * 15,  ### fifty seconds
            lambda: self.v2rayshellautoUpdate.enableUpdateSchedule(
                self.bridgetreasureChest, self.bridgeSingal))
        
    def event(self, event):
        if (event.type() == QEvent.WindowStateChange and self.isMinimized()):
            self.setWindowFlags(self.windowFlags() & ~Qt.Tool)
            self.v2rayshellTrayIcon.show()
            return True
        else:
            return super(bridgePanel, self).event(event)
        
    def onsystemTrayIconMenushowhidebridgePanel(self):
        if self.isHidden():
            self.showNormal()
        elif self.isVisible():
            self.hide()

    def restorebridgePanel(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            elif self.isHidden():
                self.showNormal()

    def close(self):
        super(bridgePanel, self).close()
        self.v2rayshellTrayIcon.hide()
        self.onv2raycoreStop()

    def closeEvent(self, event):
        self.close()
        event.accept()
        sys.exit(self.app.exec_())
        
    def onv2raycoreStop(self):
        if (self.runv2raycore):
            self.runv2raycore.stop.emit()
        try:
            ### force stop checking proxy time lag
            del self.autoCheckTimer
        except Exception:
            pass
        
    def onupdateinstallFinishedstartNewV2raycore(self):
        self.onloadV2rayshellConfigFile(init = True)
        self.onv2raycoreStart()

    def onv2raycoreStart(self):
        currentActiveRow = False
        rowCount = self.tableWidgetBridge.rowCount()
        for i in range(rowCount):
            currentActiveRow = self.tableWidgetBridge.cellWidget(i, 0)
            if currentActiveRow.isChecked():
                self.texteditBridge.clear()
                option = self.tableWidgetBridge.item(i, 2)
                if option:
                    option = '-config="{}" -format=json'.format(option.text())
                else:
                    option = ""
                filePath = self.bridgetreasureChest.getV2raycoreFilePath()
                if (filePath == False or filePath == ""):
                    filePath = "v2ray"
                self.runv2raycore = runV2raycore.runV2raycore(
                    outputTextEdit      = self.texteditBridge, 
                    v2rayPath           = filePath, 
                    v2rayOption         = option,
                    bridgetreasureChest = self.bridgetreasureChest)
                
                self.runv2raycore.start.emit()
                self.autocheckProxy(i)
                break
            else:
                del currentActiveRow
                
    def autocheckProxy(self, row):
        ### TODO
        """
        Frequent access to the server may cause suspicion of DDOS attacks, 
        which may put the VPS server at risk.
        """
        enableAutoCheck = self.bridgetreasureChest.getConnectionEnable()
        
        if (enableAutoCheck):
            self.proxyStatus = proxyTest.proxyStatus()
            self.autoCheckTimer = QTimer()
            invervalTime = self.bridgetreasureChest.getConnectioninterval()
            timeout      = self.bridgetreasureChest.getConnectiontimeout()
            proxyAddress = self.getProxyAddressFromTableWidget(row)
            
            if proxyAddress:
                self.autoCheckTimer.timeout.connect(lambda: self.startCheckProxy(
                    timeout      = timeout,
                    proxyAddress = proxyAddress,
                    row          = row,
                    proxyStatus  = self.proxyStatus))
                
                self.bridgetreasureChest.setProxy(proxyAddress)
                
                self.autoCheckTimer.start(1000 * invervalTime)
                
                self.autoCheckTimer.singleShot(100, lambda:  self.startCheckProxy(
                    timeout      = timeout, 
                    proxyAddress = proxyAddress,
                    row          = row,
                    proxyStatus  = self.proxyStatus))
            
    def setTableWidgetTimelag(self, row, proxyStatus):    
        newlabelTimelag = self.setlabelTimeLagColor(proxyStatus)
        oldlabelTimelag = self.tableWidgetBridge.cellWidget(row, 4)
        del oldlabelTimelag
        self.tableWidgetBridge.setCellWidget(row, 4, newlabelTimelag)
        self.tableWidgetBridge.resizeColumnsToContents()

    def startCheckProxy(self, timeout, proxyAddress, row, proxyStatus):
        if (proxyAddress):
            proxyStatus.clear()
            proxyStatus.signal.connect(
                lambda: self.setTableWidgetTimelag(row, proxyStatus))
                    
            self.proxy = proxyTest.proxyTest(proxyprotocol  = proxyAddress[0],
                                             proxyhostname  = proxyAddress[1],
                                             proxyhostport  = int(proxyAddress[2]),
                                             getproxyStatus = proxyStatus,
                                             timeout        = int(timeout))
            
    def setlabelTimeLagColor(self, proxyStatus = False):
        labelTimeLag = QLabel()
        if (proxyStatus and proxyStatus.getProxyError() == False):
            labelFont = QFont()
            labelFont.setPointSize(12)
            labelFont.setBold(True)
            labelTimeLag.setFont(labelFont)
            forestGreen = "QLabel {color: rgb(34, 139, 34)}"
            darkOrange  = "QLabel {color: rgb(255, 140, 0)}"
            red         = "QLabel {color: rgb(194,24,7)}"
            
            if (proxyStatus.getElapsedTime() < 260):
                labelTimeLag.setStyleSheet(forestGreen)
            elif (proxyStatus.getElapsedTime() > 420):
                labelTimeLag.setStyleSheet(red)
            else:
                labelTimeLag.setStyleSheet(darkOrange)
            labelTimeLag.setText("{} ms".format(str(proxyStatus.getElapsedTime())))

            return labelTimeLag
        
        elif (proxyStatus and proxyStatus.getProxyError()):
            labelTimeLag.setText("{}:{}".format(proxyStatus.getProxyErrorString(), 
                                                proxyStatus.getProxyErrorCode()))
            
            self.proxyTryConnect.trytimesDecrease()                       
            return labelTimeLag
    
    def swapNextConfigFile(self):
        self.onv2raycoreStop()
        try:
            self.proxyTryConnect.setTrytimes(self.bridgetreasureChest.getConnectiontrytimes())
        except Exception:
            self.proxyTryConnect.setTrytimes(3)
        
        if (self.bridgetreasureChest.connectionisSwitch()):
            ### swap next row's configFile
            buttons = self.radioButtonGroup.buttons()
            buttonsNumber = len(buttons)
            activeRow = False
            for i in range(buttonsNumber):
                if buttons[i].isChecked():
                    buttons[i].setChecked(False)
                    if i == buttonsNumber-1:
                        buttons[0].setChecked(True)
                        activeRow = 0
                        break
                    else:
                        buttons[i + 1].setChecked(True)
                        activeRow = i + 1
                    break
    
            ### change the row icons
            for i in range(buttonsNumber):
                widget = self.tableWidgetBridge.cellWidget(i, 0)
                if (widget):
                    widget.setIcon(self.iconStop)
                    widget.setIconSize(self.__iconSize)
                    if (widget.isChecked()):
                        pass
            widget = self.tableWidgetBridge.cellWidget(activeRow, 0)
            if widget:
                widget.setIcon(self.iconStart)
                widget.setIconSize(self.__iconSize)
        
        self.onv2raycoreStart()
    
    def onopenv2rayupdatePanel(self):
        currentActiveRow = False
        rowCount = self.tableWidgetBridge.rowCount()
        currentRow = False
        for i in range(rowCount):
            currentActiveRow = self.tableWidgetBridge.cellWidget(i, 0)
            if currentActiveRow.isChecked():
                currentRow = i 
                break

        if (currentActiveRow and currentActiveRow.isChecked()):
            proxy = self.tableWidgetBridge.item(currentRow, 3)
            proxy = proxy.text().split(":")
            protocol = QNetworkProxy.Socks5Proxy
            if (proxy[0] == "socks"):
                protocol = QNetworkProxy.Socks5Proxy
            elif (proxy[0] == "http"):
                protocol = QNetworkProxy.HttpProxy
            hostName = proxy[1]
            hostPort = int(proxy[2])
            
            v2rayAPI = updatePanel.v2rayAPI()
            self.createupdatePanel = updatePanel.v2rayUpdatePanel(v2rayapi            = v2rayAPI,
                                                                  protocol            = protocol,
                                                                  proxyhostName       = hostName,
                                                                  port                = hostPort,
                                                                  bridgetreasureChest = self.bridgetreasureChest)
            self.createupdatePanel.createPanel()
            self.createupdatePanel.setWindowIcon(self.iconStart)
            self.createupdatePanel.setWindowTitle(
                self.translate("bridgePanel", "Check V2Ray-core update"))
            self.createupdatePanel.resize(QSize(1024, 320))
            self.createupdatePanel.move(
                QApplication.desktop().screen().rect().center()-self.createupdatePanel.rect().center())
            self.createupdatePanel.show()
            self.createupdatePanel.exec_()
        else:
            self.noPoxyServerRunning()

    def ontableWidgetBridgeRightClicked(self, pos):
        index = self.tableWidgetBridge.indexAt(pos)
        clickedRow.rightClickedRow = index.row()
        clickedRow.mousePos = QCursor().pos()
        self.popMenu.move(QCursor().pos())
        self.popMenu.show()

    def ontableWidgetBridgecellDoubleClicked(self, row, column):
        if(column == 1):
            hostName, ok = QInputDialog.getText(self, 
                                                self.translate("bridgePanel", 'Host Name'), 
                                                self.translate("bridgePanel", 'Enter Host Name:'))
            if(ok):
                self.tableWidgetBridge.setItem(row, column, QTableWidgetItem(str(hostName)))
                self.tableWidgetBridge.resizeColumnsToContents()
        elif(column == 2):
            fileNames = self.onopenV2rayConfigJSONFile()
            if (fileNames):
                for fileName in fileNames:
                    self.tableWidgetBridge.setItem(row, column, QTableWidgetItem(str(fileName)))
                    self.tableWidgetBridge.resizeColumnsToContents()
        elif(column == 3):
            self.onproxyserverTimeLagTest()
        elif(column == 4):
            self.onproxyserverTimeLagTest()

    def getProxyAddressFromTableWidget(self, row):
        proxy = self.tableWidgetBridge.item(row, 3)
        try:
            proxy = proxy.text().split(":")
        except Exception:
            return False

        if (proxy[0] == "socks"):
            proxy[0] = QNetworkProxy.Socks5Proxy
        elif (proxy[0] == "http"):
            proxy[0] = QNetworkProxy.HttpProxy
        
        if len(proxy) < 3: return False
        else: return proxy

    def onproxyserverTimeLagTest(self):
        proxyStatus = proxyTest.proxyStatus()
        """
        right clicked mouse button pop a menu check proxy
        """
        currentActiveRow = False
        rowCount = self.tableWidgetBridge.rowCount()
        currentRow = False
        for i in range(rowCount):
            currentActiveRow = self.tableWidgetBridge.cellWidget(i, 0)
            if currentActiveRow.isChecked():
                currentRow = i 
                break
        if (currentActiveRow and currentActiveRow.isChecked()):
            proxy = self.getProxyAddressFromTableWidget(currentRow)
            protocol = proxy[0]
            hostName = proxy[1]
            hostPort = int(proxy[2])
                
            proxy = proxyTest.proxyTestPanel(proxyhostname  = hostName, 
                                             proxyhostport  = hostPort, 
                                             proxyprotocol  = protocol, 
                                             getproxyStatus = proxyStatus)
            proxy.createproxyTestPanel()
            proxy.setWindowTitle(self.translate("bridgePanel", "Proxy Time Lag Check"))
            proxy.setWindowIcon(self.iconStart)
            proxy.resize(QSize(600, 480))
            proxy.move(QApplication.desktop().screen().rect().center()-proxy.rect().center())
            proxy.show()
            proxy.exec_()
        else:
            self.noPoxyServerRunning()
            
    def noPoxyServerRunning(self):
        warningPanel = QDialog()
        warningPanel.setWindowTitle(self.translate("bridgePanel", "Warnnig..."))
        warningPanel.setWindowIcon(self.iconStop)
        labelMsg = QLabel(
            self.translate("bridgePanel", "There no any server is running, \n[File]->[Add V2Ray-core Config File] (Ctrl+n) add a config.json."))
        vbox = QVBoxLayout()
        vbox.addWidget(labelMsg)
        warningPanel.setLayout(vbox)
        warningPanel.move(QApplication.desktop().screen().rect().center()-warningPanel.rect().center())
        warningPanel.show()
        warningPanel.exec_()

    def getProxyAddressFromJSONFile(self, filePath):
        from bridgehouse.editMap.port import treasureChest, openV2rayJSONFile
        tempTreasureChest = treasureChest.treasureChest()
        openV2rayJSONFile.openV2rayJSONFile(filePath, tempTreasureChest, disableLog = True).initboundJSONData()
        inbound   = tempTreasureChest.getInbound()
        if (inbound):
            protocol  = inbound["protocol"]
            ipAddress = inbound["listen"]
            port      = inbound["port"]
            if (protocol == "socks" or protocol == "http"):
                return "{}:{}:{}".format(protocol, ipAddress, port)
            else:
                return False
        else:
            return False

    def onradioButtonClicked(self, e):
        rowCount = self.tableWidgetBridge.rowCount()
        #radioButtonClickedRow = 0
        for i in range(rowCount):
            widget = self.tableWidgetBridge.cellWidget(i, 0)
            if (widget):
                widget.setIcon(self.iconStop)
                widget.setIconSize(self.__iconSize)
                if (widget.isChecked()):
                    #radioButtonClickedRow = i
                    pass
        e.setIcon(self.iconStart)
        e.setIconSize(self.__iconSize)
    
    def onloadV2rayshellConfigFile(self, init = False):
        """
        when the script first start, and auto load v2ray-shell config file.
        """
        if init:
            self.settingv2rayshelltableWidget()
        else:
            def openV2rayshellConfigFile():
                options = QFileDialog.Options()
                filePath, _ = QFileDialog.getOpenFileName(self,
                                                          self.translate("bridgePanel", "Open V2Ray-sehll Config File"),
                                                          "",
                                                          "V2Ray-shell config file (*.v2rayshell)",
                                                          options = options)
                if (filePath):
                    self.bridgetreasureChest.clear()
                    self.tableWidgetBridge.setRowCount(0)
                    self.bridgetreasureChest.inibridgeJSONData(v2rayshellConfigFileName = filePath)
                    self.settingv2rayshelltableWidget()
            openV2rayshellConfigFile()
    
    def onopenV2rayConfigJSONFile(self):
        """
        open a new v2ray config file to tabelWidget
        """
        options = QFileDialog.Options()
        filePaths, _ = QFileDialog.getOpenFileNames(self,
                                                  self.translate("bridgePanel", "Open V2Ray-core Config File"),
                                                  "",
                                                  """
                                                  V2Ray config file (*.json);;
                                                  """,
                                                  options = options)
        
        if (filePaths):
            return filePaths
        else:
            return False 

    def createBridgepreferencesPanel(self):
        self.createpreferencesPanel = bridgePreference.bridgepreferencesPanel(self.bridgetreasureChest)
        self.createpreferencesPanel.createpreferencesPanel()
        self.createpreferencesPanel.setWindowIcon(self.iconStart)
        self.createpreferencesPanel.move(
            QApplication.desktop().screen().rect().center()-self.createpreferencesPanel.rect().center())
        self.createpreferencesPanel.show()
        self.createpreferencesPanel.exec_()
    
    def settingv2rayshelltableWidget(self):
        v2rayConfigFiles = self.bridgetreasureChest.getV2raycoreconfigFiles()
        if v2rayConfigFiles == False:return
        v2rayConfigFilesNumber = len(v2rayConfigFiles)
        if (v2rayConfigFilesNumber > 0):
            self.tableWidgetBridge.setRowCount(0)
            for i in range(v2rayConfigFilesNumber):
                try:
                    enable = bool(v2rayConfigFiles[i]["enable"])
                    hostName = str(v2rayConfigFiles[i]["hostName"])
                    configFileName = str(v2rayConfigFiles[i]["configFileName"])
                except Exception: pass
                
                radioButtonStopStart = QRadioButton(self)
                radioButtonStopStart.setIcon(self.iconStop if not enable else self.iconStart)
                radioButtonStopStart.setChecked(True if enable else False)
                radioButtonStopStart.setIconSize(self.__iconSize)
                self.radioButtonGroup.addButton(radioButtonStopStart)
                self.tableWidgetBridge.setRowCount(i+1)
                self.tableWidgetBridge.setCellWidget(i, 0, radioButtonStopStart)
                self.tableWidgetBridge.setItem(i, 1, QTableWidgetItem(hostName))
                self.tableWidgetBridge.setItem(i, 2, QTableWidgetItem(configFileName))
                self.tableWidgetBridge.setItem(i, 3, QTableWidgetItem(self.getProxyAddressFromJSONFile(configFileName)))
                self.tableWidgetBridge.resizeColumnsToContents()
                #self.tableWidgetBridge.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def onsaveV2rayshellConfigFile(self):
        self.bridgetreasureChest.clearconfigFiles()
        rowCount = self.tableWidgetBridge.rowCount()
        for i in range(rowCount):
            enable = self.tableWidgetBridge.cellWidget(i, 0)
            if enable and enable.isChecked():
                enable = True
            else:
                enable = False
            
            hostName = self.tableWidgetBridge.item(i, 1)
            if hostName:
                hostName = hostName.text()
            else:
                hostName = ""
                
            config = self.tableWidgetBridge.item(i, 2)
            if config:
                config = config.text()
            else:
                config = ""
            self.bridgetreasureChest.setV2raycoreconfigFiles(enable, hostName, configFileName = config)
        self.bridgetreasureChest.save.emit()
    
    def oncreatenauticalChartPanel(self):
        v2rayConfigFileName = self.tableWidgetBridge.item(clickedRow.rightClickedRow, 2)
        if (v2rayConfigFileName):
            nc = nauticalChartPanel.nauticalChartPanel(v2rayConfigFileName.text())
            nc.createPanel()
            nc.setWindowTitle(
                self.translate("bridgePanel", "V2Ray config file edit"))
            nc.setWindowIcon(self.iconStart)
            nc.setGeometry(0, 0, 1024, 768)
            ### move widget to center
            nc.move(QApplication.desktop().screen().rect().center()-nc.rect().center())
            nc.show()
            nc.exec_()

    def tableWidgetBridgeAddNewV2rayConfigFile(self):
        configFileNames = self.onopenV2rayConfigJSONFile()
        if (configFileNames):
            for configFileName in configFileNames:
                rowCount = self.tableWidgetBridge.rowCount()
                radioButtonStopStart = QRadioButton(self)
                radioButtonStopStart.setIcon(self.iconStop)
                radioButtonStopStart.setIconSize(self.__iconSize)
                self.radioButtonGroup.addButton(radioButtonStopStart)

                self.tableWidgetBridge.setRowCount(rowCount+1)
                self.tableWidgetBridge.setCellWidget(rowCount, 0, radioButtonStopStart)
                self.tableWidgetBridge.setItem(rowCount, 1, QTableWidgetItem(""))
                self.tableWidgetBridge.setItem(rowCount, 2, QTableWidgetItem(configFileName))
                self.tableWidgetBridge.setItem(rowCount, 3, QTableWidgetItem(self.getProxyAddressFromJSONFile(configFileName)))
                self.tableWidgetBridge.resizeColumnsToContents()
        else:
            pass
    
    def tableWidgetBridgeDelete(self):
        self.tableWidgetBridge.removeRow(clickedRow.rightClickedRow)

    def validateV2rayJSONFile(self, JSONData):
        """
        simply validate a V2Ray json file.
        """
        try:
            JSONData["inbound"]
            JSONData["outbound"]
        except KeyError:
            return False
        else:
            return True
        
    def about(self):
        NineteenEightySeven = QLabel(
            self.translate("bridgePanel", """Across the Great Wall, we can reach every corner in the world.""")) ### Crossing the Great Wall to Join the World
        Timeless            = QLabel(
            self.translate("bridgePanel", """You weren't thinking about that when you were creating it.\nBecause if you did? You never would have gone through with it."""))
        DwayneRichardHipp   = QLabel(
            self.translate("bridgePanel", """May you do good and not evil.\nMay you find forgiveness for yourself and forgive others.\nMay you share freely, never taking more than you give."""))
        vbox = QVBoxLayout()
        vbox.addWidget(NineteenEightySeven)
        vbox.addWidget(Timeless)
        vbox.addWidget(DwayneRichardHipp)
        
        dialogAbout = QDialog()
        dialogAbout.setWindowTitle(self.translate("bridgePanel", "About V2Ray-shell"))
        dialogAbout.setWindowIcon(self.iconStart)
        dialogAbout.move(
            QApplication.desktop().screen().rect().center()-dialogAbout.rect().center())
        dialogAbout.setLayout(vbox)
        dialogAbout.show()
        dialogAbout.exec_()
        
    def bugReportPanel(self):
        self.bugReport = bugReport.bugReport()
        self.bugReport.setWindowTitle(self.translate("bridgePanel", "Bug Report"))
        self.bugReport.setWindowIcon(self.iconStart)
        self.bugReport.createPanel()
        self.bugReport.show()
        self.bugReport.setGeometry(250, 150, 1024, 768)
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    if hasattr(Qt, "AA_EnableHighDpiScaling"):  #### hope it's working. i don't have hight dpi monitor
        app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "AA_UseHighDpiPixmpas"):
        app.setAttribute(Qt.AA_UseHighDpiPixmpas)
        
    app.setQuitOnLastWindowClosed(False)
    ex = bridgePanel(app)
    ex.setGeometry(300, 120, 1200, 768)
    #ex.show()
    sys.exit(app.exec_())