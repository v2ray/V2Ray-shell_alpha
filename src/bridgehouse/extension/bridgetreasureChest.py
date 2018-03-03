#!/usr/bin/env python3
from PyQt5.QtCore import (QObject, pyqtSignal, QFile, QFileInfo, 
                          QIODevice, Qt, QCoreApplication, QDir,
                          qDebug)
from PyQt5.QtWidgets import QDialog, QMessageBox, QApplication
from PyQt5.QtNetwork import QNetworkProxy

import copy, sys, json, codecs

class bridgetreasureChest(QObject):
    save = pyqtSignal()

    def __init__(self):
        super().__init__()
        """{
            "preferences": {
                    "v2ray-core": "3.10",
                    "v2ray-coreFilePath": "D:/Program Files/v2ray/v2ray.exe"
                    "connection":{
                            "enable": True,
                            "connect": "switch", ### reconnect/switch
                            "interval": 60       ### seconds
                            "timeout" : 0,
                            "trytimes": 3
                        },
                    "language":"en_US",
                    "startup": True
            },
            "update":{
                  "enable": True,
                        "schedule": {
                            "date": 8,
                            "time": 3
                        },
                    "install": "auto",          ### auto install/ manual install 
                    "downloadFile": False,
                    "silentInstall": True
            },
            "configFiles": [{
                            "enable": true,
                            "hostName": "v2ray.cool",
                            "configFileName": "config.json"
                    }
            ]
        }
        """
        self.translate = QCoreApplication.translate

        self.v2rayshellConfigFileName = QFileInfo(sys.argv[0]).absolutePath() + "/" + "config.v2rayshell"
        qDebug(self.v2rayshellConfigFileName)
        qDebug(QFileInfo(sys.argv[0]).absolutePath())

        self.preferences = {
            "v2ray-core": False,
            "v2ray-coreFilePath": False,
            "connection": {
                    "enable": False,
                    "connect": False,
                    "interval": False,
                    "timeout" : False,
                    "trytimes": False
                },
            "language": False,
            "startup": False
            }
        self.update = {
            "enable" : False,
            "schedule": {
                "date": False,
                "time": False
                },
            "install": False,
            "downloadFile": False,
            "silentInstall": True
            }

        Qt.Everyday    = 8
        self.daysoftheweek = (None, 
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

        self.configFiles = []
        self.openFile = None
        self.fileName = None
        self.init     = False
        self.connectionCheckenable   = False
        self.connectionCheckinterval = False
        self.connectionChecktimeout  = False
        self.connectionTrytimes      = False
        self.connectionConnect       = False
        self.updateEnable            = False
        self.updateScheduledate      = False
        self.updateScheduletime      = False
        self.updateinstallOption     = False
        self.updatedownloadFile      = False
        self.updatesilentInstall     = False
        self.proxyProtocol           = False
        self.proxyAddres             = False
        self.proxyPort               = False
        self.allLanguages            = {}
        self.latestReleaseV2rayCore  = False
        self.latestReleaseV2rayCoreDownloadPath = False

        self.morning   = (5, 6, 7, 8, 9, 10, 11, 12)
        self.afternoon = (13, 14, 15, 16, 17)
        self.evening   = (18, 19, 20, 21)
        self.night     = (22, 23, 24, 0, 1, 2, 3, 4)

        self.msgBox = QMessageBox()
        self.fly = QApplication.desktop().screen().rect().center()-self.msgBox.rect().center()

        self.initbridgeJSONData(False)
        self.save.connect(self.saveV2raycoreJSONFile)

    def clear(self):
        self.preferences = {
            "v2ray-core": False,
            "v2ray-coreFilePath": False,
            "connection": {
                    "enable": False,
                    "connect": False,
                    "interval": False,
                    "timeout" : False,
                    "trytimes": False
                },
            "language": False,
            "startup": False
            }

        self.update = {
            "enable" : False,
            "schedule": {
                "date": False,
                "time": False
                },
            "install": False,
            "downloadFile": False,
            "silentInstall": False
            }

        self.configFiles = []
        self.init = False

    def clearUpdate(self):
        self.update = {
            "enable" : False,
            "schedule": {
                "date": False,
                "time": False
                },
            "install": False,
            "downloadFile": False,
            "silentInstall": False
            }

    def clearPreferences(self):
        self.preferences = {
            "v2ray-core": False,
            "v2ray-coreFilePath": False,
            "connection": {
                    "enable": False,
                    "connect": False,
                    "interval": False,
                    "timeout" : False,
                    "trytimes": False
                },
            "language": False,
            "startup": False
            }

    def setLanguage(self, language):
        self.preferences["language"] = copy.deepcopy(language)

    def getLanguage(self):
        return self.preferences["language"]
    
    def setStartup(self, startup=False):
        if not isinstance(startup, int):
            self.preferences["startup"] = False
        self.preferences["startup"] = startup

    def getStartup(self):
        return self.startup

    def getAllLanguage(self):
        return self.allLanguages

    def setProxyAddress(self, address):
        self.proxyAddres = copy.deepcopy(address)

    def setProxyProtocol(self, protocol: (QNetworkProxy.HttpProxy, QNetworkProxy.Socks5Proxy)):
        if not isinstance(protocol, int):
            self.proxyProtocol = QNetworkProxy.Socks5Proxy
        self.proxyProtocol = copy.deepcopy(protocol)
        
    def setProxyPort(self, port:"0~65535"):
        if port < 0 or port > 65535:
            self.proxyPort = 1080
        self.proxyPort = copy.deepcopy(int(port))
        
    def getProxyPort(self):
        return self.proxyPort
    
    def getProxyProtocol(self):
        return self.proxyProtocol
    
    def getProxyAddress(self):
        return self.proxyAddres
    
    def setProxy(self, proxy: ("protocol", "address", "port")):
        if len(proxy) == 3:
            self.setProxyProtocol(proxy[0])
            self.setProxyAddress(proxy[1])
            self.setProxyPort(int(proxy[2]))
            return True
        else: return False
    
    def getProxy(self):
        proxy = self.getProxyProtocol(), self.getProxyAddress(), self.getProxyPort()
        if (not proxy[0] or not proxy[1] or not proxy[2]):
            return False
        else: return proxy
        
    def setUpdateSchedule(self, update):
        self.update = {}
        self.update = copy.deepcopy(update)
        self.updateEnable        = self.update["enable"]
        self.updateScheduledate  = self.update["schedule"]["date"]
        self.updateScheduletime  = self.update["schedule"]["time"]
        self.updateinstallOption = self.update["install"]
        self.updatedownloadFile  = self.update["downloadFile"]
        self.updatesilentInstall = self.update["silentInstall"]

    def updateisEnable(self):
        if self.updateEnable:
            return True
        else:
            return False

    def setupdateEnable(self, enable: bool):
        if not isinstance(enable, bool):
            raise TypeError
        if enable:
            self.updateEnable = True
            self.update["enable"] = True
        elif not enable:
            self.updateEnable = False
            self.update["enable"] = False

    def getupdateinstallOption(self):
        return self.updateinstallOption
    
    def setsilentInstall(self, enable):
        if not isinstance(enable, bool):
            self.updatesilentInstall = False
        else:
            self.updatesilentInstall = enable

    def getsilentInstall(self):
        return self.updatesilentInstall
    
    def setupdateinstallOption(self, option: "option should be auto or manual"):
        if option == "auto":
            self.updateinstallOption = "auto"
            self.update["install"] = self.updateinstallOption
            return True
        elif option == "manual":
            self.updateinstallOption = "manual"
            self.update["install"] = self.updateinstallOption
            return True
        else: return False
    
    def setupdateScheduledate(self, date):
        if date in range(8):
            self.updateScheduledate = copy.deepcopy(date)
            self.update["schedule"]["date"] = self.updateScheduledate
            return True
        else: return False
        
    def setupdateScheduletime(self, time):
        if time in self.partsoftheDay():
            self.updateScheduletime = copy.deepcopy(time)
            return True
        else: return False
    
    def updateinstallOptionisauto(self):
        if self.updateinstallOption == "auto":
            return True
        else:
            return False
        
    def updateinstallOptionismanual(self):
        if self.updateinstallOption == "manual":
            return True
        else:
            return False
        
    def setupdatedownloadFile(self, downloadFile):
        if downloadFile in self.downloadFiles:
            self.updatedownloadFile = copy.deepcopy(downloadFile)
            return True
        else: return False
    
    def getupdatedownloadFile(self):
        return self.updatedownloadFile
        
    def getupdateScheduledate(self):
        """
        Returns the weekday (1 = Monday to 7 = Sunday) for this date
        Qt.Monday    1
        Qt.Tuesday   2
        Qt.Wednesday 3
        Qt.Thursday  4
        Qt.Friday    5
        Qt.Saturday  6
        Qt.Sunday    7
        Qt.Everyday  8
        """
        if   self.updateScheduledate == 1:
            return Qt.Monday
        elif self.updateScheduledate == 2:
            return Qt.Tuesday
        elif self.updateScheduledate == 3:
            return Qt.Wednesday
        elif self.updateScheduledate == 4:
            return Qt.Thursday
        elif self.updateScheduledate == 5:
            return Qt.Friday 
        elif self.updateScheduledate == 6:
            return Qt.Saturday
        elif self.updateScheduledate == 7:
            return Qt.Saturday
        elif self.updateScheduledate == 8:
            return Qt.Everyday

    def getupdateScheduletime(self):
        return self.updateScheduletime
    
    def setLatestReleaseV2rayCore(self, version):
        self.latestReleaseV2rayCore = version
    
    def getLatestReleaseV2rayCore(self):
        return self.latestReleaseV2rayCore

    def setLatestReleaseV2rayCoreDownloadPath(self, path):
        self.latestReleaseV2rayCoreDownloadPath = copy.deepcopy(path)
        
    def getLatestReleaseV2rayCoreDownloadPath(self):
        return self.latestReleaseV2rayCoreDownloadPath
                                    
    def setConnection(self, connection):
        self.preferences["connection"] = {}
        self.preferences["connection"] = copy.deepcopy(connection)
        self.connectionCheckenable   = self.preferences["connection"]["enable"]
        self.connectionCheckinterval = self.preferences["connection"]["interval"]
        self.connectionChecktimeout  = self.preferences["connection"]["timeout"]
        self.connectionTrytimes      = self.preferences["connection"]["trytimes"]
        self.connectionConnect       = self.preferences["connection"]["connect"]
    
    def connectionisSwitch(self):
        if self.connectionConnect == "switch":
            return True
        else:
            return False

    def connectionisReconnect(self):
        if self.connectionConnect == "reconnect":
            return True
        else:
            return False
    
    def getConnectionEnable(self):
        return self.connectionCheckenable
    
    def getConnectioninterval(self):
        if self.connectionCheckinterval < 60:
            return 60
        elif self.connectionCheckinterval > 360:
            return 360
        else:
            return self.connectionCheckinterval
    
    def getConnectiontimeout(self):
        return self.connectionChecktimeout
    
    def getConnectiontrytimes(self):
        return self.connectionTrytimes
    
    def getConnection(self):
        return self.preferences["connection"]

    def clearconfigFiles(self):
        self.configFiles = []
    
    def initDataFinished(self):
        self.init = True
    
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
    
    def initbridgeJSONData(self, v2rayshellConfigFileName = False):
        """
        open v2rayshell config JSON File. save it to memory.
        """
        if (v2rayshellConfigFileName):
            self.v2rayshellConfigFileName = v2rayshellConfigFileName
        
        self.clear()

        fileInfo = QFileInfo(self.v2rayshellConfigFileName)
        self.fileName = fileInfo.fileName()
        self.openFile = QFile(self.v2rayshellConfigFileName)
        
        self.openFile.open(QIODevice.ReadOnly | QIODevice.Text)
        if self.openFile.error() != self.openFile.NoError:
            self.msgBox.information(QDialog().move(self.fly), 
                               "{}".format(self.fileName),
                               self.translate("bridgetreasureChest", "Unable to open the file {}:  {}.").format(
                                   self.v2rayshellConfigFileName,
                                   self.openFile.errorString()))
            self.msgBox.move(
                QApplication.desktop().screen().rect().center()-self.msgBox.rect().center())
            self.openFile = None
            return
        JSONData = str(self.openFile.readAll(), "utf-8")
        try:
            JSONData = json.loads(JSONData)
        except ValueError as e:
            self.msgBox.information(QDialog().move(self.fly), 
                               self.translate("bridgetreasureChest", "Parse JSON Data Error"),
                               self.translate("bridgetreasureChest", "Unable to parse {}:  error:{}.").format(self.fileName, e))
            self.msgBox.move(
                QApplication.desktop().screen().rect().center()-self.msgBox.rect().center())
            self.openFile = None
            JSONData = None
            return
        
        try:
            JSONData["preferences"]
        except Exception:
            JSONData["preferences"] = {}
        
        try:
            JSONData["configFiles"]
        except Exception:
            JSONData["configFiles"] = []
        
        if (len(JSONData["preferences"]) > 0):
            try:
                JSONData["preferences"]["v2ray-core"]
            except Exception:
                JSONData["preferences"]["v2ray-core"] = False
            else:
                self.setV2raycoreVersion(JSONData["preferences"]["v2ray-core"])
                
            try:
                JSONData["preferences"]["v2ray-coreFilePath"]
            except Exception:
                JSONData["preferences"]["v2ray-coreFilePath"] = False
            else:
                self.setV2raycoreFilePath(JSONData["preferences"]["v2ray-coreFilePath"])
                
            try:
                JSONData["preferences"]["language"]
            except Exception:
                JSONData["preferences"]["language"] = "en_US"
            else:
                self.setLanguage(JSONData["preferences"]["language"])
                
            try:
                JSONData["preferences"]["startup"]
            except Exception:
                JSONData["preferences"]["startup"] = False
            else:
                self.setStartup(JSONData["preferences"]["startup"])
                
            try:
                JSONData["preferences"]["connection"]
            except Exception:
                JSONData["preferences"]["connection"] = {}
                
            if not JSONData["preferences"]["connection"]:
                JSONData["preferences"]["connection"] = {}
                
            try:
                JSONData["preferences"]["connection"]["enable"]
            except Exception:
                JSONData["preferences"]["connection"]["enable"] = False
                
                
            try:
                JSONData["preferences"]["connection"]["connect"]
            except Exception: 
                JSONData["preferences"]["connection"]["connect"] = "switch"
                
            try:
                JSONData["preferences"]["connection"]["interval"]
            except Exception:
                JSONData["preferences"]["connection"]["interval"] = 60
                
            try:
                JSONData["preferences"]["connection"]["timeout"]
            except Exception:
                JSONData["preferences"]["connection"]["timeout"] = 5
                
            try:
                JSONData["preferences"]["connection"]["trytimes"]
            except Exception:
                JSONData["preferences"]["connection"]["trytimes"] = 3
            
            self.setConnection(JSONData["preferences"]["connection"])
            
            try:
                JSONData["update"]
            except Exception:
                JSONData["update"] = {}
                
            try:
                JSONData["update"]["enable"]
            except Exception:
                JSONData["update"]["enable"] = False
                
            try:
                JSONData["update"]["schedule"]
            except Exception:
                JSONData["update"]["schedule"] = {}
                
            try:
                JSONData["update"]["schedule"]["date"]
            except Exception:
                JSONData["update"]["schedule"]["date"] = 8
                
            try:
                JSONData["update"]["schedule"]["time"]
            except Exception:
                JSONData["update"]["schedule"]["time"] = 3
                
            try:
                JSONData["update"]["install"]
            except Exception:
                JSONData["update"]["install"] = "manual"
                
            try:
                JSONData["update"]["downloadFile"]
            except Exception:
                JSONData["update"]["downloadFile"] = "v2ray-windows-64.zip"

            try:
                JSONData["update"]["silentInstall"]
            except Exception:
                JSONData["update"]["silentInstall"] = True

            self.setUpdateSchedule(JSONData["update"])

        if (len(JSONData["configFiles"]) > 0):
            for i in JSONData["configFiles"]:
                try:
                    self.setV2raycoreconfigFiles(i["enable"], i["hostName"], i["configFileName"])
                except Exception:
                    continue
        
        self.allLanguages = copy.deepcopy(self.findQmFiles())
        
        self.openFile.close()

    def saveV2raycoreJSONFile(self):
        JSONData = {}
        JSONData["preferences"] = copy.deepcopy(self.preferences)
        JSONData["update"]      = copy.deepcopy(self.update)
        JSONData["configFiles"] = copy.deepcopy(self.configFiles)
        
        outFile = QFileInfo(self.v2rayshellConfigFileName)
        
        fileName = outFile.fileName()
        if QFile.exists(fileName):
            QFile.remove(fileName)
            
        outFile = QFile(fileName)
        
        outFile.open(QIODevice.WriteOnly | QIODevice.Text)
        if outFile.error() != outFile.NoError:
            self.msgBox.information(QDialog().move(self.fly), 
                               "{}".format(fileName), 
                               self.translate("bridgetreasureChest", "Unable to open the file {}:  {}.").format(fileName, 
                                                                         outFile.errorString()))
            outFile = None
            return False
        
        outFile.write(codecs.encode(json.dumps(JSONData, indent = 4, sort_keys = False), "utf-8"))
        
        if outFile.error() != outFile.NoError:
            self.msgBox.information(QDialog().move(self.fly), 
                               "{}".format(fileName), 
                               self.translate("bridgetreasureChest", "Unable to save the file {}:  {}.").format(fileName, 
                                                                         outFile.errorString()))
            outFile = None
            return False
        
        outFile.close()
        
    def findQmFiles(self):
        trans_dir = QDir('./translations/')
        
        fileNames = trans_dir.entryList(['*.qm'], QDir.Files, QDir.Name)
        trans = {}
        for i in fileNames:
            trans[QFileInfo(i).baseName()] = trans_dir.absoluteFilePath(i)
        return trans

    def setV2raycoreFilePath(self, path):
        self.preferences["v2ray-coreFilePath"] = copy.deepcopy(path) 
        
    def getV2raycoreFilePath(self):
        return self.preferences["v2ray-coreFilePath"]
    
    def setV2raycoreVersion(self, version):
        self.preferences["v2ray-core"] = copy.deepcopy(version)
    
    def getV2raycoreVersion(self):
        return self.preferences["v2ray-core"]
    
    def setV2raycoreconfigFiles(self, enable, hostName, configFileName):
        config = {}
        config["enable"]         = enable
        config["hostName"]       = hostName
        config["configFileName"] = configFileName
        self.configFiles.append(copy.deepcopy(config))
    
    def getV2raycoreconfigFiles(self):
        if len(self.configFiles) > 0:
            return self.configFiles
        else: 
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = bridgetreasureChest()
    sys.exit(app.exec_())
