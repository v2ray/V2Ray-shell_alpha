#!/usr/bin/env python3

from PyQt5.QtWidgets import (QVBoxLayout,QPushButton, QHBoxLayout, QDialog,
                             QComboBox, QLabel, QLineEdit, QGroupBox, QSpinBox,
                             QRadioButton, QMessageBox, QProgressDialog,
                             QApplication, QCheckBox, QSpacerItem)
from PyQt5.QtCore import (QFile, QFileInfo, QIODevice, QUrl, pyqtSignal, 
                          QObject, QTime, Qt, QDate, QDir, QCoreApplication)
from PyQt5.QtNetwork import (QNetworkProxy, QNetworkRequest, QNetworkAccessManager, 
                             QNetworkReply)
from PyQt5.QtGui import QFont

import json, sys, copy

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-2]))

class updateV2rayQTime(QTime):
    def __init__(self):
        super(updateV2rayQTime, self).__init__()
        """
        Morning   :  05:00 to 12:00 (5, 6, 7, 8, 9, 12)
        Afternoon :  13:00 to 17:00 (13, 14, 15, 16, 17)
        Evening   :  18:00 to 21:00 (18, 19, 20, 21)
        Night     :  22:00 to 04:00 (22, 23, 0, 1, 2, 3, 4)
        """
        self.morning   = (5,   6,  7,  8,  9, 10, 11, 12)
        self.afternoon = (13, 14, 15, 16, 17)
        self.evening   = (18, 19, 20, 21)
        self.night     = (22, 23,  0,  1,  2,  3, 4)

    def isMorning(self):
        if self.currentTime().hour() in self.morning:
            return True
        else: return False
        
    def isAfternoon(self):
        if self.currentTime().hour() in self.afternoon:
            return True
        else: return False
        
    def isEvening(self):
        if self.currentTime().hour() in self.evening:
            return True
        else: return False
        
    def isNight(self):
        if self.currentTime().hour() in self.night:
            return True
        else: return False

class v2rayAPI(QObject):
    checkDownloadInfo = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.v2raycoreAPI= False
        self.version = False
        self.errorString = False
        self.downloadINFO = {}
        
    def setV2raycoreErrorString(self, error):
        self.errorString = copy.deepcopy(error)
        
    def getV2raycoreErrorString(self):
        return self.errorString
        
    def getV2raycoreVersion(self):
        return self.version
    
    def setV2raycoreVersion(self, version):
        self.version = copy.deepcopy(version)
        
    def setv2raycoreAPI(self, api):
        self.v2raycoreAPI = copy.deepcopy(api)
        
    def getv2raycoreAPI(self):
        return self.v2raycoreAPI
    
    def setdownloadINFO(self, fileName, downloadPath):
        self.downloadINFO[str(fileName)] = str(downloadPath)
    
    def getdownloadINFO(self):
        return self.downloadINFO

class updateV2ray(QObject):
    downloadFinish = pyqtSignal()

    def __init__(self, 
                 v2rayapi = False, 
                 url      = False, 
                 checkDownloadInfo   = False, 
                 downloadV2raycore   = False):
        super().__init__()
        self.downloadURL = url
        self.reply    = None
        self.outFile  = None
        self.fileName = None
        self.httpRequestAborted = False
        self.v2rayAPI = v2rayapi
        self.v2raycoreAPIURL = QUrl(r"""https://api.github.com/repos/v2ray/v2ray-core/releases/latest""")
        Qt.Everyday = 8
        self.downloadPath  = False
        self.qnam = QNetworkAccessManager()
        self.startV2ray = False
        self.stopV2ray  = False
        self.translate = QCoreApplication.translate
        self.msgBox = QMessageBox()
        self.fly = QApplication.desktop().screen().rect().center()-self.msgBox.rect().center()
        self.silentInstall = False
        if (self.v2rayAPI and self.downloadURL and checkDownloadInfo): self.getV2raycoreInfoFromGithub()
        elif (self.v2rayAPI and self.downloadURL and downloadV2raycore): self.downloadV2raycore()
        else: pass

    def downloadV2raycore(self, url = False):
        if (url):
            self.downloadURL = url
        fileInfo = QFileInfo(self.downloadURL.path())
        self.fileName = fileName = fileInfo.fileName()
    
        if not fileName:
            fileName = "v2ray.zip"
        
        if QFile.exists(fileName):
            QFile.remove(fileName)
            
        self.outFile = QFile(fileName)
        
        if not self.outFile.open(QIODevice.WriteOnly):
            if (self.silentInstall == False):
                self.msgBox.information(QDialog().move(self.fly), 
                                   self.translate("updateV2ray", "Download {}").format(fileName), 
                                   self.translate("updateV2ray", 
                                                  "Unable to save the file {}: {}.").format(
                                                      fileName, 
                                                      self.outFile.errorString()))
            self.outFile = None
            return

        self.httpRequestAborted = False
        
        if (self.silentInstall == False):
            self.progressDialog = QProgressDialog()
            self.progressDialog.setLabelText(
                self.translate("updateV2ray", "v2ray-core is downloading..."))
            self.progressDialog.canceled.connect(self.cancelDownload)

        self.startRequest(self.downloadURL)
        
    def startRequest(self, url):
        self.reply = self.qnam.get(QNetworkRequest(url))
        self.reply.finished.connect(self.httpFinished)
        self.reply.readyRead.connect(self.httpReadyRead)
        if (self.silentInstall == False):
            self.reply.downloadProgress.connect(self.updateDataReadProgress)

    def httpReadyRead(self):
        if self.outFile is not None:
            self.outFile.write(self.reply.readAll())
            
    def updateDataReadProgress(self, bytesRead, totalBytes):
        if self.httpRequestAborted: return
        
        self.progressDialog.setMaximum(totalBytes)
        self.progressDialog.setValue(bytesRead)    
        
    def cancelDownload(self):
        self.httpRequestAborted = True
        if self.reply is not None:
            self.reply.abort()
            if QFile.exists(self.fileName):
                QFile.remove(self.fileName)
    
    def httpFinished(self):
        if self.httpRequestAborted:
            if self.outFile is not None:
                self.outFile.close()
                self.outFile.remove()
                del self.outFile

            self.reply.deleteLater()
            self.reply = None
            if self.silentInstall == False: self.progressDialog.hide()
            return
        
        if self.silentInstall == False: self.progressDialog.hide()
        self.outFile.flush()
        self.outFile.close()

        redirectionTarget = self.reply.attribute(QNetworkRequest.RedirectionTargetAttribute)

        if self.reply.error():
            self.outFile.remove()
            if self.silentInstall == False:
                self.msgBox.information(QDialog().move(self.fly), 
                                   self.translate("updateV2ray", "Download"), 
                                   self.translate("updateV2ray", "Download failed: {}.").format(self.reply.errorString()))
                self.progressDialog.close()

        elif redirectionTarget is not None:
            newUrl = self.downloadURL.resolved(redirectionTarget)
            self.downloadURL = newUrl
            self.reply.deleteLater()
            self.reply = None
            self.outFile.open(QIODevice.WriteOnly)
            self.outFile.resize(0)
            self.startRequest(self.downloadURL)
            return
        else:
            self.reply.deleteLater()
            self.reply = None
            self.outFile = None
            self.downloadFinish.emit()
            
    def getV2raycoreInfoFromGithub(self, url = False):
        if (url):
            self.downloadURL = url
        self.reqV2raycore = QNetworkRequest(self.downloadURL)
        self.qnam.finished.connect(self.handleResponse)
        self.qnam.get(self.reqV2raycore)
        
    def handleResponse(self, reply):
        """
        Read all API from https://api.github.com/repos/v2ray/v2ray-core/releases/latest
        """
        errorCode = reply.error()
        if (self.v2rayAPI):
            if errorCode == QNetworkReply.NoError:
                self.v2rayAPI.setv2raycoreAPI(str(reply.readAll(), "utf-8"))
                self.createDownloadINFO()
            else:
                self.v2rayAPI.setV2raycoreErrorString(reply.errorString())
                self.v2rayAPI.setv2raycoreAPI(False)
            self.v2rayAPI.checkDownloadInfo.emit()

    def createDownloadINFO(self):
        api = None
        try:
            api = json.loads(self.v2rayAPI.getv2raycoreAPI())
        except Exception:
            api = None
        if (api):
            try:
                ### this code for get Latest release Download Files' path
                for i in api["assets"]:
                    self.v2rayAPI.setdownloadINFO(i["name"], i["browser_download_url"])
                self.v2rayAPI.setV2raycoreVersion(api["tag_name"])
            except Exception:
                pass

    def setautoupdateProxy(self, proxy):        
        self.proxy = QNetworkProxy()
        protocol      = copy.deepcopy(proxy[0])
        proxyhostName = copy.deepcopy(proxy[1])
        proxyPort     = copy.deepcopy(proxy[2])
        
        self.proxy.setType(protocol)
        self.proxy.setHostName(proxyhostName)
        self.proxy.setPort(int(proxyPort))
        self.proxy.setApplicationProxy(self.proxy)
    
    def enableUpdateSchedule(self, bridgetreasureChest, bridgeSingal = False):
        if (bridgeSingal):
            self.startV2ray = bridgeSingal[0]
            self.stopV2ray  = bridgeSingal[1] ### this signals for auto install v2ray-core
        
        self.v2rayAPI = v2rayAPI()
        self.bridgetreasureChest = bridgetreasureChest
        proxy = None
        self.silentInstall = self.bridgetreasureChest.getsilentInstall()

        if v2rayshellDebug == False:
            """
            if in debug mode, use the panel's proxy
            """
            proxy   = self.bridgetreasureChest.getProxy()
            if proxy: self.setautoupdateProxy(proxy)
            else    : return False
        
        correctTime = False
        correctDate = False
        
        self.usingVersion  = self.bridgetreasureChest.getV2raycoreVersion()
        self.latestVersion = False
        
        scheduleDate = self.bridgetreasureChest.getupdateScheduledate()
        currentDate  = QDate().currentDate().dayOfWeek()
        
        scheduleTime = self.bridgetreasureChest.getupdateScheduletime()
        currentTime = False
        if updateV2rayQTime().isMorning():
            currentTime = 1
        elif updateV2rayQTime().isAfternoon():
            currentTime = 2
        elif updateV2rayQTime().isEvening():
            currentTime = 3
        elif updateV2rayQTime().isNight():
            currentTime = 4

        self.downloadFile  = self.bridgetreasureChest.getupdatedownloadFile()
        self.installOption = self.bridgetreasureChest.getupdateinstallOption()
        
        if scheduleDate == currentDate:
            correctDate   = True

        if  scheduleDate  == Qt.Everyday:
            correctDate   = True
            
        if scheduleTime == currentTime:
            correctTime = True
        else:
            correctTime = False
        
        def checkDonwloadinfo():
            self.getV2raycoreInfoFromGithub(self.v2raycoreAPIURL)
            self.v2rayAPI.checkDownloadInfo.connect(lambda:self.getdownloadPath(self.usingVersion))
        
        if (correctTime and correctDate):
            checkDonwloadinfo()
            
        if v2rayshellDebug:
            checkDonwloadinfo()

    def getdownloadPath(self, usingVersion):
        download = False
        if (self.v2rayAPI.getv2raycoreAPI()):
            self.downloadPath  = False
            for file, filePath in self.v2rayAPI.getdownloadINFO().items():
                if self.downloadFile == file:
                    self.downloadPath = copy.deepcopy(filePath)
                    break
            self.latestVersion = copy.deepcopy(self.v2rayAPI.getV2raycoreVersion())
            
            if usingVersion == "":
                download = True
            elif self.checkNewestfileDownload(usingVersion, self.latestVersion):
                download = True 

            if (download and self.downloadPath):
                self.checkdownloadFileExists(self.downloadPath)
                self.downloadV2raycore(QUrl(self.downloadPath))
                self.downloadFinish.connect(
                    lambda: self.installDownloadFile(self.downloadFile, self.latestVersion))

    def installDownloadFile(self, downloadFile, latestVersion):
        if self.installOption == "manual":
            self.msgBox.information(
                QDialog().move(self.fly), 
                self.translate("updateV2ray", "update"), 
                self.translate("updateV2ray", 
                               "The newest v2ray-core: {} .\nversion: {} was downloaded,\nPlease check.").format(
                                   downloadFile, latestVersion))
        elif self.installOption == "auto":
            if self.unzipdownloadFile(downloadFile, latestVersion) and (self.silentInstall == False):
                self.msgBox.information(
                    QDialog().move(self.fly), 
                    self.translate("updateV2ray", "update"), 
                    self.translate("updateV2ray", 
                                   "The newest v2ray-core: {} .\n version: {} was installed. \nPlease restart V2ray-shell").format(
                                       downloadFile, latestVersion))

    def checkdownloadFileExists(self, downloadPath):
        if (downloadPath == False or downloadPath == ""): return False
        filePath = QUrl(downloadPath)
        fileInfo = QFileInfo(filePath.path()) 
        fileName = fileInfo.fileName()
        if QFile.exists(fileName):
            QFile.remove(fileName)
            return True

    def unzipdownloadFile(self, downladFile, latestVersion):
        import zipfile, re
        fileInfo = None
        self.newV2rayPath = None
        if QFile.exists(downladFile):
            fileInfo = QFileInfo(QFile(downladFile))
        else:
            return False
        
        def checkFilesize(file):
            v2rayFile = QFile(file.absoluteFilePath())
            ### check file size need open the file
            v2rayFile.open(QIODevice.ReadOnly | QIODevice.Text)
            if v2rayFile.error() == v2rayFile.NoError:
                if v2rayFile.size() > 600000:
                    v2rayFile.close()
                    return True
            else:
                v2rayFile.close()
                return False
        
        if (fileInfo):
            with zipfile.ZipFile(fileInfo.absoluteFilePath(),"r") as zip_ref:
                for i in zip_ref.namelist():
                    absoluteFilePath = fileInfo.absolutePath()+QDir.separator()+i
                    if re.search("/v2ray.exe$", absoluteFilePath):  ### windows
                        self.newV2rayPath = None
                        self.newV2rayPath = QFileInfo(QFile(absoluteFilePath))
                        if self.newV2rayPath and checkFilesize(self.newV2rayPath):break
                    if re.search("/v2ray$", absoluteFilePath):     ### other
                        self.newV2rayPath = None
                        self.newV2rayPath = QFileInfo(QFile(absoluteFilePath))
                        if self.newV2rayPath and checkFilesize(self.newV2rayPath):break
                if (self.stopV2ray):
                    self.stopV2ray.emit()
                zip_ref.extractall(fileInfo.absolutePath())
            if self.newV2rayPath:
                self.bridgetreasureChest.setV2raycoreFilePath(self.newV2rayPath.absoluteFilePath())
                self.bridgetreasureChest.setV2raycoreVersion(latestVersion)
                self.bridgetreasureChest.save.emit()
                self.startV2ray.emit()
                return True
            else: return False
        
    def checkNewestfileDownload(self, usingVersion, latestVersion):
        import re
        if usingVersion == False: return True
        v = re.search("v", usingVersion)
        if (v):
            usingVersion = usingVersion[1:].split('.')
        else:
            return False
        del v
        v = re.search("v", latestVersion)
        if (v): 
            latestVersion = latestVersion[1:].split('.')
        else:
            return False
        if (latestVersion[0] > usingVersion[0]):
            return True
        elif (latestVersion[0] == usingVersion[0]) and (latestVersion[1] > usingVersion[1]):
            return True
        else: return False
        
    def partsoftheDay(self):
        """
        Morning   :  05:00 to 12:00 (5, 6, 7, 8, 9, 10, 11, 12)
        Afternoon :  13:00 to 17:00 (13, 14, 15, 16, 17)
        Evening   :  18:00 to 21:00 (18, 19, 20, 21)
        Night     :  22:00 to 04:00 (22, 23, 0, 1, 2, 3, 4)
        """
        return (self.translate("updateV2ray", "Morning"),
                self.translate("updateV2ray", "Afternoon"), 
                self.translate("updateV2ray", "Evening"), 
                self.translate("updateV2ray", "Night"))

class v2rayUpdatePanel(QDialog):
    def __init__(self,
                 protocol      = False, 
                 proxyhostName = False, 
                 port          = False,
                 v2rayapi      = False,
                 bridgetreasureChest = False):
        super().__init__()
        self.translate = QCoreApplication.translate
        
        self.update = {
                  "enable": True,
                        "schedule": {
                            "date": 8,
                            "time": 4
                        },
                    "install": "auto",    ### auto install/ manual install 
                    "downloadFile": False,
                    "silentInstall": True
            }
        self.daysoftheweek = (self.translate("v2rayUpdatePanel", "Select a Day for update"),
                              self.translate("v2rayUpdatePanel", "Every Monday"), 
                              self.translate("v2rayUpdatePanel", "Every Tuesday"), 
                              self.translate("v2rayUpdatePanel", "Every Wednesday"), 
                              self.translate("v2rayUpdatePanel", "Every Thursday"), 
                              self.translate("v2rayUpdatePanel", "Every Friday"), 
                              self.translate("v2rayUpdatePanel", "Every Saturday"),
                              self.translate("v2rayUpdatePanel", "Every Sunday"),
                              self.translate("v2rayUpdatePanel", "Every Day"))
        
        self.downloadFiles = (
            "v2ray-windows-64.zip",
            "v2ray-macos.zip",
            "v2ray-linux-64.zip",
            "v2ray-windows-32.zip",
            "v2ray-linux-32.zip",
            "v2ray-freebsd-32.zip",
            "v2ray-freebsd-64.zip",
            "v2ray-linux-arm.zip",
            "v2ray-linux-arm64.zip",
            "v2ray-linux-mips.zip",
            "v2ray-linux-mips64.zip",
            "v2ray-linux-mips64le.zip",
            "v2ray-linux-mipsle.zip",
            "v2ray-openbsd-32.zip",
            "v2ray-openbsd-64.zip")
        
        self.protocol      = protocol
        self.proxyhostName = proxyhostName
        self.port          = port
        if (v2rayapi):
            self.v2rayAPI  = v2rayapi
        else:
            self.v2rayAPI  = v2rayAPI()
            
        self.bridgetreasureChest = bridgetreasureChest
        if self.bridgetreasureChest == False:
            from bridgehouse.extension import bridgetreasureChest
            self.bridgetreasureChest = bridgetreasureChest.bridgetreasureChest()
            
        self.v2raycoreAPIURL   = QUrl(r"""https://api.github.com/repos/v2ray/v2ray-core/releases/latest""")
        self.spinBoxPort       = QSpinBox()   
        self.lineEditProxy     = QLineEdit()
        self.radioButtonSocks5 = QRadioButton("Socks")
        self.radioButtonHttp   = QRadioButton("Http")
        self.groupBoxViaProxy  = QGroupBox(self.translate("v2rayUpdatePanel", "Via Proxy"))
        self.groupBoxViaProxy.setCheckable(True)
        self.proxy = QNetworkProxy()
        
        if (self.protocol and self.proxyhostName and self.port and v2rayapi):
            self.settingProxyhost(protocol, proxyhostName, port)
            self.groupBoxViaProxy.setChecked(True)
        else:
            self.groupBoxViaProxy.setChecked(False)

    def createPanel(self):
        labelProxy = QLabel(self.translate("v2rayUpdatePanel", "Proxy: "))
        self.lineEditProxy.setFixedWidth(256)
        self.spinBoxPort.setRange(0, 65535)
        self.spinBoxPort.setValue(1080)

        self.buttonCheck      = QPushButton(
            self.translate("v2rayUpdatePanel", "Check"))
        self.labelCheckResult = QLabel(
            self.translate("v2rayUpdatePanel", " Check the latest V2Ray-core version"))
        labelcurrentV2raycoreVersion = QLabel(
            self.translate("v2rayUpdatePanel", "Can't get V2Ray-core's version"))
        version = self.bridgetreasureChest.getV2raycoreVersion()
        if (version):
            labelFont = QFont()
            labelFont.setPointSize(12)
            labelFont.setBold(True)
            labelcurrentV2raycoreVersion.setFont(labelFont)
            labelcurrentV2raycoreVersion.setText(
                self.translate("v2rayUpdatePanel", "The current version of V2Ray is: {}").format(version))
        
        labelDownloadPath = QLabel(
            self.translate("v2rayUpdatePanel", "V2Ray-core Download Path: "))
        self.lineEditDownloadPath = QLineEdit()
        self.lineEditDownloadPath.setFixedWidth(512)
        self.lineEditDownloadPath.setReadOnly(True)
        self.comboBoxv2raycoreVersion = QComboBox()
        self.buttonDownload = QPushButton(self.translate("v2rayUpdatePanel", "Download"))

        hboxProxyAddress = QHBoxLayout()
        hboxProxyAddress.addWidget(labelProxy)
        hboxProxyAddress.addWidget(self.lineEditProxy)
        hboxProxyAddress.addWidget(self.spinBoxPort)
        hboxProxyAddress.addStretch()
        
        hboxRadioButton = QHBoxLayout()
        hboxRadioButton.addWidget(self.radioButtonSocks5)
        hboxRadioButton.addWidget(self.radioButtonHttp)
        hboxRadioButton.addStretch()

        vboxViaProxy = QVBoxLayout()
        vboxViaProxy.addLayout(hboxProxyAddress)
        vboxViaProxy.addLayout(hboxRadioButton)
        
        self.groupBoxViaProxy.setLayout(vboxViaProxy)
        
        hboxCheckStatus = QHBoxLayout()
        hboxCheckStatus.addWidget(self.buttonCheck)
        hboxCheckStatus.addWidget(self.labelCheckResult)
        hboxCheckStatus.addWidget(self.comboBoxv2raycoreVersion)
        hboxCheckStatus.addStretch()
        
        hboxDownloadPath = QHBoxLayout()
        hboxDownloadPath.addWidget(labelDownloadPath)
        hboxDownloadPath.addWidget(self.lineEditDownloadPath)
        hboxDownloadPath.addWidget(self.buttonDownload)
        hboxDownloadPath.addStretch()
        
        self.groupBoxupdateSchedule = QGroupBox(
            self.translate("v2rayUpdatePanel", "Automatic Updates"))
        self.groupBoxupdateSchedule.setCheckable(True)
        self.groupBoxupdateSchedule.setChecked(False)

        self.comboBoxScheduledate = QComboBox()
        self.comboBoxScheduledate.addItems(self.daysoftheweek)
        labelAt = QLabel(
            self.translate("v2rayUpdatePanel", "at"))
        self.comboBoxScheduletime = QComboBox()
        self.comboBoxScheduletime.addItems(self.partsoftheDay())
        
        labelDownloadFile = QLabel(
            self.translate("v2rayUpdatePanel", " Download: "))
        self.comboBoxDownloadFile = QComboBox()
        self.comboBoxDownloadFile.addItems(self.downloadFiles)
        
        hboxSchedule = QHBoxLayout()
        hboxSchedule.addWidget(self.comboBoxScheduledate)
        hboxSchedule.addWidget(labelAt)
        hboxSchedule.addWidget(self.comboBoxScheduletime)
        hboxSchedule.addWidget(labelDownloadFile)
        hboxSchedule.addWidget(self.comboBoxDownloadFile)
        hboxSchedule.addStretch()

        labelThen = QLabel(
            self.translate("v2rayUpdatePanel", "Then "))
        self.radioButtonAuto   = QRadioButton(
            self.translate("v2rayUpdatePanel", "Auto"))
        self.radioButtonManual = QRadioButton(
            self.translate("v2rayUpdatePanel", "Manual"))
        self.radioButtonManual.setChecked(True) 
        
        self.checkBoxsilentInstall = QCheckBox(
            self.translate("v2rayUpdatePanel","Silently"))
        labelInstallV2raycore  = QLabel(
            self.translate("v2rayUpdatePanel", "Install V2Ray-core"))
        
        hboxRadioButtonAutoManual = QHBoxLayout()
        hboxRadioButtonAutoManual.addWidget(labelThen)
        hboxRadioButtonAutoManual.addWidget(self.radioButtonAuto)
        hboxRadioButtonAutoManual.addWidget(self.radioButtonManual)
        hboxRadioButtonAutoManual.addSpacerItem(QSpacerItem(25, 5))
        hboxRadioButtonAutoManual.addWidget(self.checkBoxsilentInstall)
        hboxRadioButtonAutoManual.addWidget(labelInstallV2raycore)
        hboxRadioButtonAutoManual.addStretch()
        
        self.buttonApplyandClose = QPushButton(
            self.translate("v2rayUpdatePanel", "Apply and Close"))
        self.buttonCancel        = QPushButton(
            self.translate("v2rayUpdatePanel", "Cancel"))
        
        hboxbuttonApplyCloseCancel = QHBoxLayout()
        hboxbuttonApplyCloseCancel.addStretch()
        hboxbuttonApplyCloseCancel.addWidget(self.buttonApplyandClose)
        hboxbuttonApplyCloseCancel.addWidget(self.buttonCancel)
        
        vboxSchedule = QVBoxLayout()
        vboxSchedule.addLayout(hboxSchedule)
        vboxSchedule.addLayout(hboxRadioButtonAutoManual)
        self.groupBoxupdateSchedule.setLayout(vboxSchedule)
        
        vboxUpdatPanel = QVBoxLayout()
        vboxUpdatPanel.addWidget(self.groupBoxViaProxy)
        vboxUpdatPanel.addWidget(labelcurrentV2raycoreVersion)
        vboxUpdatPanel.addLayout(hboxCheckStatus)
        vboxUpdatPanel.addLayout(hboxDownloadPath)
        vboxUpdatPanel.addWidget(self.groupBoxupdateSchedule)
        vboxUpdatPanel.addLayout(hboxbuttonApplyCloseCancel)
        vboxUpdatPanel.addStretch()
        
        if v2rayshellDebug:
            self.updatev2ray = updateV2ray()
            self.__testBtn = QPushButton("__Test")
            vboxUpdatPanel.addWidget(self.__testBtn)
            #self.__testBtn.clicked.connect(lambda: self.updatev2ray.unzipdownloadFile("v2ray-linux-mips64le.zip"))
            self.__testBtn.clicked.connect(lambda:self.updatev2ray.enableUpdateSchedule(self.bridgetreasureChest))
            
        self.settingupdateSchedule()
        
        self.setLayout(vboxUpdatPanel)
        
        self.createUpadtePanelSignals()
        
    def createUpadtePanelSignals(self):
        self.comboBoxv2raycoreVersion.currentTextChanged.connect(self.ondownloadVersionSelect)
        self.buttonCheck.clicked.connect(self.onbuttonCheckV2raycoreversion)
        self.buttonDownload.clicked.connect(self.ondownloadV2raycore)
        self.groupBoxViaProxy.clicked.connect(self.ongroupBoxViaProxy)
        self.buttonCancel.clicked.connect(self.close)
        self.buttonApplyandClose.clicked.connect(self.onupdatebuttonApplyandClose)
        
    def onupdatebuttonApplyandClose(self):
        self.bridgetreasureChest.clearUpdate()
        update = {}
        update["enable"] = True if self.groupBoxupdateSchedule.isChecked() else False
        update["schedule"] = {}
        update["schedule"]["date"] = int(self.comboBoxScheduledate.currentIndex())
        update["schedule"]["time"] = int(self.comboBoxScheduletime.currentIndex())
        update["install"] = "auto" if self.radioButtonAuto.isChecked() else "manual"
        update["downloadFile"]  = self.comboBoxDownloadFile.currentText()
        update["silentInstall"] = True if self.checkBoxsilentInstall.isChecked() else False

        self.bridgetreasureChest.setUpdateSchedule(update)
        self.bridgetreasureChest.save.emit()
        self.close()
        
    def settingupdateSchedule(self):
        if self.bridgetreasureChest.updateisEnable():
            self.groupBoxupdateSchedule.setChecked(True)
        else:
            self.groupBoxupdateSchedule.setChecked(False)
            
        downloadFile = self.bridgetreasureChest.getupdatedownloadFile()
        if downloadFile in self.downloadFiles:
            self.comboBoxDownloadFile.setCurrentText(downloadFile)
            
        try:
            self.comboBoxScheduledate.setCurrentIndex(
                self.bridgetreasureChest.getupdateScheduledate())
        except Exception:
            ### a new panel will get a false value from config.v2rayshell 
            pass

        try:
            self.comboBoxScheduletime.setCurrentIndex(
                self.bridgetreasureChest.getupdateScheduletime())
        except Exception:
            pass

        installOption = self.bridgetreasureChest.getupdateinstallOption()
        if installOption == "auto":
            self.radioButtonAuto.setChecked(True)
            self.radioButtonManual.setChecked(False)
        else:
            self.radioButtonManual.setChecked(True)
            self.radioButtonAuto.setChecked(False)
        
        self.checkBoxsilentInstall.setChecked(
            True if self.bridgetreasureChest.getsilentInstall() else False)
    
    def partsoftheDay(self):
        """
        Morning   :  05:00 to 12:00 (5, 6, 7, 8, 9, 10, 11, 12)
        Afternoon :  13:00 to 17:00 (13, 14, 15, 16, 17)
        Evening   :  18:00 to 21:00 (18, 19, 20, 21)
        Night     :  22:00 to 04:00 (22, 23, 0, 1, 2, 3, 4)
        """
        return (self.translate("v2rayUpdatePanel", "Select a time for update"),
                self.translate("v2rayUpdatePanel", "Morning"), 
                self.translate("v2rayUpdatePanel", "Afternoon"), 
                self.translate("v2rayUpdatePanel", "Evening"), 
                self.translate("v2rayUpdatePanel", "Night"))

    def settingProxyhost(self, protocol, proxyhostName, port):
        """
        update v2ray need via proxy
        """
        self.proxy.setType(protocol)
        self.proxy.setHostName(proxyhostName)
        self.proxy.setPort(int(port))
        self.proxy.setApplicationProxy(self.proxy)
        
        if (protocol == QNetworkProxy.Socks5Proxy):
            self.radioButtonSocks5.setChecked(True)
            self.radioButtonHttp.setChecked(False)
        if (protocol == QNetworkProxy.HttpProxy):
            self.radioButtonHttp.setChecked(True)
            self.radioButtonSocks5.setChecked(False)
                
        self.lineEditProxy.setText(proxyhostName)
        self.spinBoxPort.setValue(int(port))
        
    def checkisViaProxy(self):
        if self.groupBoxViaProxy.isChecked(): 
            if self.lineEditProxy.text() == "" or self.spinBoxPort.value() == 0:
                self.lineEditDownloadPath.clear()
                self.comboBoxv2raycoreVersion.clear()
                return
            else:
                if (self.radioButtonSocks5.isChecked()):
                    protocol = QNetworkProxy.Socks5Proxy
                elif (self.radioButtonHttp.isChecked()):
                    protocol = QNetworkProxy.HttpProxy
                self.proxy.setType(protocol)
                self.proxy.setHostName(self.lineEditProxy.text())
                self.proxy.setPort(self.spinBoxPort.value())
                self.proxy.setApplicationProxy(self.proxy)
        else:
            self.proxy.setType(QNetworkProxy.NoProxy)
            self.proxy.setApplicationProxy(self.proxy)
        
    def ongroupBoxViaProxy(self):
        self.checkisViaProxy()

    def onbuttonCheckV2raycoreversion(self):
        self.checkisViaProxy()
        labelFont = QFont()
        labelFont.setPointSize(12)
        labelFont.setBold(True)
        self.labelCheckResult.setFont(labelFont)
        self.labelCheckResult.setText(
            self.translate("v2rayUpdatePanel", "Checking..."))
        self.updateV2ray = updateV2ray(self.v2rayAPI, 
                                       self.v2raycoreAPIURL, 
                                       checkDownloadInfo = True, 
                                       downloadV2raycore = False)
        self.v2rayAPI.checkDownloadInfo.connect(self.settingUpdateDownloadFiles)
    
    def ondownloadVersionSelect(self):
        currentv2raycoreVersion = self.comboBoxv2raycoreVersion.currentText()
        if currentv2raycoreVersion != "":
            downloadINFO = self.v2rayAPI.getdownloadINFO()
            downloadPath = downloadINFO[currentv2raycoreVersion]
            self.lineEditDownloadPath.setText(downloadPath)
        else:
            self.lineEditDownloadPath.clear()
        
    def settingUpdateDownloadFiles(self):
        if (self.v2rayAPI.getv2raycoreAPI() == False):
            self.labelCheckResult.setText(self.v2rayAPI.getV2raycoreErrorString())
            self.lineEditDownloadPath.clear()
            self.comboBoxv2raycoreVersion.clear()
            return
        
        downloadINFO = copy.deepcopy(self.v2rayAPI.getdownloadINFO())
        try:
            downloadINFO["metadata.txt"]
            metadata = True
        except Exception:
            metadata = False
            
        if (metadata): del downloadINFO["metadata.txt"]  ### metadata.txt should not in the download list
        
        if (downloadINFO):
            k = 1
            self.comboBoxv2raycoreVersion.clear()
            self.comboBoxv2raycoreVersion.insertItem(0, "")
            for i in downloadINFO.keys():
                self.comboBoxv2raycoreVersion.insertItem(++k, str(i))
            self.comboBoxv2raycoreVersion.setSizeAdjustPolicy(QComboBox.AdjustToContents)
            self.labelCheckResult.setText(
                self.translate("v2rayUpdatePanel", "The latest version is: {}").format(
                    self.v2rayAPI.getV2raycoreVersion()))

    def ondownloadV2raycore(self):
        self.checkisViaProxy()
        filePath = self.lineEditDownloadPath.text()
        if (filePath != ""):
            self.updateV2ray = updateV2ray(self.v2rayAPI, 
                                           QUrl(filePath), 
                                           checkDownloadInfo = False, 
                                           downloadV2raycore = True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    v2rayapi = v2rayAPI()
    ex = v2rayUpdatePanel(QNetworkProxy.Socks5Proxy, "127.0.0.1", 1080, v2rayapi)
    ex.createPanel()
    ex.setGeometry(420, 320, 1024, 320)
    ex.show()
    sys.exit(app.exec_())