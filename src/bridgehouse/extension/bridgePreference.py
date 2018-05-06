#!/usr/bin/env python3

from PyQt5.QtWidgets import (QDialog, QApplication, QPushButton, QGridLayout,
                             QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,
                             QFileDialog, QGroupBox, QRadioButton, QSpinBox,
                             QComboBox, QCheckBox, QToolTip)
from PyQt5.QtCore import (QSize, QFileInfo, Qt, QCoreApplication,
                          QIODevice, QDir, QFile)
from PyQt5.QtGui import QCursor

import sys, os, codecs

is_win = sys.platform.startswith('win')
is_darwin = sys.platform == 'darwin'  # Mac OS X

# Unix platforms
is_linux = sys.platform.startswith('linux')
is_solar = sys.platform.startswith('sun')  # Solaris
is_aix = sys.platform.startswith('aix')
is_freebsd = sys.platform.startswith('freebsd')
is_hpux = sys.platform.startswith('hp-ux')

is_unix = is_linux or is_solar or is_aix or is_freebsd or is_hpux

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))


class startUp():

    def __init__(self, striptName=False):
        self.striptName = sys.argv[0]
        if striptName:
            self.striptName = striptName
        self.scriptAbsoluteFilePath = QFileInfo(self.striptName).absoluteFilePath()
        self.autoStartupFilename = "V2Ray-shell"

    def setStartUp(self, enable=False):
        if is_unix:
            if self.createLinXDesktopFileToAutostart(
                self.autoStartupFilename,
                self.scriptAbsoluteFilePath,
                enable=enable):
                return True
            return False

        if is_win:
            if self.createWinShortcutToStartup(
                shortcutName=self.autoStartupFilename,
                execFileTarget=self.scriptAbsoluteFilePath,
                startin=QFileInfo(self.scriptAbsoluteFilePath).absolutePath(),
                enable=enable):
                return True
            return False

        if is_darwin:
            if self.createMacsplitFileToStartup(
                self.autoStartupFilename,
                execFileTarget=self.scriptAbsoluteFilePath,
                enable=enable):
                return True
            return False

    def createWinShortcutToStartup(self,
                                   shortcutName,
                                   execFileTarget,
                                   arguments=None,
                                   startin=None,
                                   iconPath=None,
                                   enable=False):
        from win32com.client import Dispatch

        shell = Dispatch('WScript.Shell')
        startupPath = shell.SpecialFolders("Startup")
        fullPath = os.path.join("{}\{}.lnk".format(startupPath, shortcutName))
        
        if QFile.exists(fullPath):
            QFile.remove(fullPath)
            if not enable: return True

        shortcut = shell.CreateShortCut(fullPath)

        shortcut.Targetpath = execFileTarget
        if not execFileTarget.endswith(".exe"):
            arguments = execFileTarget
            shortcut.Targetpath = os.path.join(
                QFileInfo(sys.executable).absolutePath(), "pythonw.exe")

        if arguments:
            shortcut.Arguments = ''' "{}"'''.format(arguments)
        if startin:
            shortcut.WorkingDirectory = startin
        if iconPath:
            shortcut.IconLocation = iconPath
        try:
            shortcut.save()
        except Exception:
            return False
        if QFile.exists(fullPath):
            return True

    def createLinXDesktopFileToAutostart(self,
                                         shortcutName,
                                         execFileTarget,
                                         iconPath=None,
                                         enable=False):
        autostartPath = os.path.join(QDir.homePath(), ".config/autostart")
        if not QDir(autostartPath).exists():
            return False

        # https://developer.toradex.com/knowledge-base/how-to-autorun-application-at-the-start-up-in-linux#Graphical
        xdesktopFile = """[Desktop Entry]
Type=Application
Version=1.0
Name={name}
Comment={name} startup script
Exec={target}
Path={workdir}
Terminal=false
StartupNotify=false
"""
        xdesktopFile = xdesktopFile.format(
                                        name=shortcutName,
                                        target=execFileTarget,
                                        workdir=QFileInfo(sys.argv[0]).absolutePath())
        shortcutName = "{}.desktop".format(shortcutName)
        
        if not self.createStartupFile(autostartPath, shortcutName, xdesktopFile, enable):
            return False
        return True

    def createMacsplitFileToStartup(self, splitFileName, execFileTarget):
        launchAgentsPath = os.path.join(QDir.homePath(), "/Library/LaunchAgents/")
        if not QDir(launchAgentsPath).exists():
            if not QDir.mkdir(launchAgentsPath): return False

        # https://developer.apple.com/library/content/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html
        macOSSplitFile = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>{name}</string>
        <key>ProgramArguments</key>
        <array>
            <string>{target}</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
    </dict>
</plist>"""
        macOSSplitFile = macOSSplitFile.format(name=splitFileName, target=execFileTarget)
        splitFileName = "{}.split".format(splitFileName)
        if not self.createStartupFile(launchAgentsPath, splitFileName, macOSSplitFile):
            return False
        return True
        
    def createStartupFile(self, autostartupPath, scriptName, script, enable=False):
        fileName = os.path.join(autostartupPath, scriptName)
        outFile = QFileInfo(fileName)
        if QFile.exists(fileName):
            QFile.remove(fileName)
            if not enable: return True

        outFile = QFile(fileName)

        outFile.open(QIODevice.WriteOnly | QIODevice.Text)
        if outFile.error() != outFile.NoError:
            outFile = None
            return False
        outFile.write(codecs.encode(script, "utf-8"))
        if outFile.error() != outFile.NoError:
            outFile = None
            return False
        outFile.close()

        return True

    
class bridgepreferencesPanel(QDialog):

    def __init__(self, bridgetreasureChest=False):
        super().__init__()

        self.__preferencesJSONFile = {
    				                "v2ray-core": "x.xx",
    				                "v2ray-coreFilePath": "v2ray",
                                    "connection":{
                                        "enable": True,
                                        "connect": "switch",  # reconnect/switch
                                        "interval": 60,  # seconds
                                        "timeout" : 3,
                                        "trytimes": 3
                                    },
                                    "language": "en_US",
                                    "startup": True
                                }
        self.bridgetreasureChest = bridgetreasureChest
        if not bridgetreasureChest:
            from bridgehouse.extension import bridgetreasureChest
            self.bridgetreasureChest = bridgetreasureChest.bridgetreasureChest()
        self.translate = QCoreApplication.translate
        self.AllLanguage = self.bridgetreasureChest.getAllLanguage()
        self.starup = startUp()
        
    def createpreferencesPanel(self):
        self.labelV2raycoreVersion = QLabel(
            self.translate("bridgepreferencesPanel", "v2ray core version is: "))
        self.labelv2raycorecurrentVersion = QLabel() 
        self.labelV2raycoreFilePath = QLabel(
            self.translate("bridgepreferencesPanel", "v2ray core File Path: "))
        self.lineEditFilePath = QLineEdit()
        self.buttonOpenV2raycoreFile = QPushButton(
            self.translate("bridgepreferencesPanel", "Open"))
        
        self.buttonpreferenceApply = QPushButton(
            self.translate("bridgepreferencesPanel", "Apply and Close"))
        self.buttonpreferenceCancel = QPushButton(
            self.translate("bridgepreferencesPanel", "Cancel"))
        hboxbutton = QHBoxLayout()
        hboxbutton.addStretch()
        hboxbutton.addWidget(self.buttonpreferenceApply)
        hboxbutton.addWidget(self.buttonpreferenceCancel)
        
        gridBox = QGridLayout()
        gridBox.addWidget(self.labelV2raycoreVersion, 0, 0, 1, 1)
        gridBox.addWidget(self.labelv2raycorecurrentVersion, 0, 1, 1, 1)
        gridBox.addWidget(self.labelV2raycoreFilePath, 1, 0, 1, 1)
        gridBox.addWidget(self.lineEditFilePath, 2, 0, 1, 5)
        gridBox.addWidget(self.buttonOpenV2raycoreFile, 2, 5, 1, 1)
        
        self.grouBoxConnection = QGroupBox(
            self.translate("bridgepreferencesPanel", "Configure Connection settings."), self)
        self.grouBoxConnection.setCheckable(True)
        self.grouBoxConnection.setChecked(False)

        self.radioButtonSwitch = QRadioButton(
            self.translate("bridgepreferencesPanel", "Switch to the next server"))
        self.radioButtonSwitch.setChecked(True)
        self.radioButtonReconnect = QRadioButton(
            self.translate("bridgepreferencesPanel", "Reconnect the server"))
        hboxRadioButton = QHBoxLayout()
        hboxRadioButton.addWidget(self.radioButtonSwitch)
        hboxRadioButton.addWidget(self.radioButtonReconnect)
        hboxRadioButton.addStretch()
        
        labelInterval = QLabel(
            self.translate("bridgepreferencesPanel", "Check the Interval: "))
        self.spinBoxInterval = QSpinBox()
        self.spinBoxInterval.setRange(60, 360)
        self.spinBoxInterval.setValue(60)
        labelMinandMaxInterval = QLabel(
            self.translate("bridgepreferencesPanel", "Interval time value is 60 to 360"))

        labelCheckProxyTimeout = QLabel(
            self.translate("bridgepreferencesPanel", "Check Proxy Timeout: "))
        self.spinBoxCheckProxyTimeout = QSpinBox()
        self.spinBoxCheckProxyTimeout.setRange(0, 15)
        self.spinBoxCheckProxyTimeout.setValue(3)
        labelCheckProxyTimeoutWarning = QLabel(
            self.translate("bridgepreferencesPanel", "Set 0 to disable timeout."))
    
        labeltrytimes = QLabel(
            self.translate("bridgepreferencesPanel", "Try Times: "))
        self.spinboxTrytimes = QSpinBox()
        self.spinboxTrytimes.setRange(0, 12)
        self.spinboxTrytimes.setValue(3)
        labelMaxtrytimes = QLabel(
            self.translate(
                "bridgepreferencesPanel",
                "0 means immediately connect, \nthe maximum value of try times is 12"))
        
        gridBoxConnection = QGridLayout()
        gridBoxConnection.addWidget(labelInterval, 0, 0, Qt.AlignLeft)
        gridBoxConnection.addWidget(self.spinBoxInterval, 0, 1, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelMinandMaxInterval, 0, 2, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelCheckProxyTimeout, 1, 0, Qt.AlignLeft)
        gridBoxConnection.addWidget(self.spinBoxCheckProxyTimeout, 1, 1, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelCheckProxyTimeoutWarning, 1, 2, Qt.AlignLeft)
        gridBoxConnection.addWidget(labeltrytimes, 2, 0, Qt.AlignLeft)
        gridBoxConnection.addWidget(self.spinboxTrytimes, 2, 1, Qt.AlignLeft)
        gridBoxConnection.addWidget(labelMaxtrytimes, 2, 2, Qt.AlignLeft)

        hboxConnection = QHBoxLayout()
        hboxConnection.addLayout(gridBoxConnection)
        hboxConnection.addStretch()
        
        vboxConnection = QVBoxLayout()
        vboxConnection.addLayout(hboxRadioButton)
        vboxConnection.addLayout(hboxConnection)

        self.grouBoxConnection.setLayout(vboxConnection)
        
        labelLanguageSetting = QLabel(
            self.translate("bridgepreferencesPanel", "Language: "))
        self.comboBoxLanguage = QComboBox()
        hboxLanguage = QHBoxLayout()
        hboxLanguage.addWidget(labelLanguageSetting)
        hboxLanguage.addWidget(self.comboBoxLanguage)
        hboxLanguage.addStretch()
        
        self.comboxStarup = QCheckBox(
            self.translate("bridgepreferencesPanel", "Starting Script Automatically on System Boot"))
        self.comboxStarup.setChecked(False)

        vboxpreferences = QVBoxLayout()
        vboxpreferences.addLayout(gridBox)
        vboxpreferences.addWidget(self.grouBoxConnection)
        vboxpreferences.addLayout(hboxLanguage)
        vboxpreferences.addWidget(self.comboxStarup)
        vboxpreferences.addStretch()
        vboxpreferences.addLayout(hboxbutton)
        
        self.setLayout(vboxpreferences)
        self.setWindowTitle(
            self.translate("bridgepreferencesPanel", "Preferences"))
        self.resize(QSize(680, 320))
        
        self.createpreferencePanelSignals()
        
        self.settingv2rayshellpreferencesPanel()
        
        if v2rayshellDebug:
            self.starupTest = startUp()
            hbox = QHBoxLayout()
            self.__testBtn = QPushButton("__testBtn")
            hbox.addWidget(self.__testBtn)
            vboxpreferences.addLayout(hbox)
            self.__testBtn.clicked.connect(lambda: self.starupTest.setStartUp(True))
        
    def createpreferencePanelSignals(self):
        self.buttonpreferenceCancel.clicked.connect(self.onbuttonpreferenceCancel)
        self.buttonOpenV2raycoreFile.clicked.connect(self.onbuttonOpenV2raycoreFile)
        self.buttonpreferenceApply.clicked.connect(self.onbuttonpreferenceApply)
        self.comboxStarup.clicked.connect(self.onsetStartUp)
        
    def onsetStartUp(self):
        if not self.starup.setStartUp(True if self.comboxStarup.isChecked() else False):
            self.comboxStarup.setChecked(False)
            QToolTip.showText(QCursor.pos(),
                              self.translate("bridgepreferencesPanel", "Setting startup failed..."),
                              self.comboxStarup)

    def onbuttonpreferenceApply(self):

        self.bridgetreasureChest.setV2raycoreFilePath(self.lineEditFilePath.text())

        connection = {}
        connection["enable"] = True if self.grouBoxConnection.isChecked() else False

        if self.radioButtonReconnect.isChecked():
            connection["connect"] = "reconnect"
        elif self.radioButtonSwitch.isChecked():
            connection["connect"] = "switch"

        self.bridgetreasureChest.setStartup(True if self.comboxStarup.isChecked() else False)

        connection["interval"] = self.spinBoxInterval.value()
        connection["timeout"] = self.spinBoxCheckProxyTimeout.value()
        connection["trytimes"] = self.spinboxTrytimes.value()

        self.bridgetreasureChest.setLanguage(self.comboBoxLanguage.currentText())
        self.bridgetreasureChest.setConnection(connection)
        self.bridgetreasureChest.save.emit()
        self.close()

    def onbuttonOpenV2raycoreFile(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self,
                                                      self.translate("bridgepreferencesPanel", "Open V2ray execute File"),
                                                      "",
                                                      "All File (*)",
                                                      options=options)
        if (filePath):
            self.lineEditFilePath.setText(filePath)

    def onbuttonpreferenceCancel(self):
        self.close()

    def settingv2rayshellpreferencesPanel(self):
        version = self.bridgetreasureChest.getV2raycoreVersion()
        filePath = self.bridgetreasureChest.getV2raycoreFilePath()
        allLanguages = self.bridgetreasureChest.getAllLanguage()
        language = self.bridgetreasureChest.getLanguage()
        startup = self.bridgetreasureChest.getStartup()

        if version:
            self.labelv2raycorecurrentVersion.setText(version)
        if filePath:
            self.lineEditFilePath.setText(filePath)
        if allLanguages:
            self.comboBoxLanguage.clear()
            allLangs = []
            for i in allLanguages.keys():
                allLangs.append(i)
            self.comboBoxLanguage.addItems(allLangs)
            if language in allLangs:
                self.comboBoxLanguage.setCurrentText(language)
            else:
                self.comboBoxLanguage.setCurrentText("en_US")
        else:
            self.comboBoxLanguage.setCurrentText("en_US")
            
        self.comboxStarup.setChecked(True if startup else False)
        
        connection = self.bridgetreasureChest.getConnection()
        if connection:
            try:
                connection["enable"]
            except Exception:
                connection["enable"] = False
    
            self.grouBoxConnection.setChecked(connection["enable"])
            
            try:
                connection["connect"]
            except Exception:
                connection["connect"] = "switch"
            
            if connection["connect"] == "switch":
                self.radioButtonSwitch.setChecked(True)
                self.radioButtonSwitch.setChecked(False)
            elif connection["connect"] == "reconnect":
                self.radioButtonReconnect.setChecked(True)
                self.radioButtonSwitch.setChecked(False)

            try:
                connection["interval"]
            except Exception:
                connection["interval"] = 10
            
            try:
                self.spinBoxInterval.setValue(connection["interval"])
            except Exception:
                self.spinBoxInterval.setValue(10)
                
            try:
                self.spinBoxCheckProxyTimeout.setValue(connection["timeout"])
            except Exception:
                self.spinBoxCheckProxyTimeout.setValue(3)
                
            try:
                self.spinboxTrytimes.setValue(connection["trytimes"])
            except Exception:
                self.spinboxTrytimes.setValue(3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = bridgepreferencesPanel()
    ex.createpreferencesPanel()
    ex.show()
    sys.exit(app.exec_())
