#!/usr/bin/env python3
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,
                             QPushButton, QTextEdit, QLabel,
                             QLineEdit, QGridLayout, QFileDialog, QButtonGroup)
from PyQt5.QtCore import (QProcess, QSize, QIODevice, QProcessEnvironment,
                          QObject, pyqtSignal, QCoreApplication, QFileInfo,
                          QFile, qDebug)
from PyQt5.Qt import QTextCursor

import re
import sys
import codecs
import os
import signal

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    # this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.absoluteFilePath().split("/")
    sys.path.append("/".join(srcPath[:-3]))


class runV2raycore(QObject):
    """
    you should emit a signal to start or stop a program.
    """
    start = pyqtSignal()
    stop = pyqtSignal()

    def __init__(self,
                 outputTextEdit,
                 v2rayPath="v2ray",
                 v2rayOption="",
                 bridgetreasureChest=False):
        super().__init__()
        self.outputTextEdit = outputTextEdit
        self.v2rayPath = v2rayPath
        self.v2rayOption = v2rayOption
        self.bridgetreasureChest = bridgetreasureChest
        if not self.bridgetreasureChest:
            from bridgehouse.extension import bridgetreasureChest
            self.bridgetreasureChest = bridgetreasureChest.bridgetreasureChest()

        self.v2rayProcess = QProcess()
        self.v2rayProcess.setProcessChannelMode(QProcess.MergedChannels)
        self.v2rayProcess.setProcessEnvironment(
            QProcessEnvironment.systemEnvironment())

        self.v2rayProcess.readyRead.connect(self.setoutputTextEdit)
        self.v2rayProcess.started.connect(self.oncreatePIDFile)
        self.start.connect(self.onstart)
        self.stop.connect(self.onstop)
        self.translate = QCoreApplication.translate
        self.pidFile = ".v2rayPID"

    def onstart(self):
        if (self.v2rayProcess.state() == QProcess.NotRunning):
            self.outputTextEdit.clear()
            command = self.translate(
                "runV2raycore", "v2ray file path had no seted.")
            if (self.v2rayPath):
                checkSpaces = re.search(" ", self.v2rayPath)
                if checkSpaces:
                    # in fact, you can just keep this line.
                    # do not need check spaces
                    command = '"' + self.v2rayPath + '" ' + self.v2rayOption
                else:
                    command = "{} {}".format(self.v2rayPath, self.v2rayOption)
                self.killOrphanProcess()
                self.v2rayProcess.start(command, QIODevice.ReadWrite)
                self.outputTextEdit.insertPlainText("{}\n\n".format(command))

            if (self.v2rayProcess.state() == QProcess.NotRunning):
                self.outputTextEdit.moveCursor(QTextCursor.End)
                self.outputTextEdit.append("\n")
                self.outputTextEdit.insertPlainText(
                    str("{}\n".format(command)))
                self.outputTextEdit.insertPlainText(
                    str(self.translate(
                        "runV2raycore", "{}   Error Code:{}").format(
                        self.v2rayProcess.errorString(),
                        self.v2rayProcess.error())))
                self.outputTextEdit.moveCursor(QTextCursor.End)

            self.outputTextEdit.textChanged.connect(self.getV2raycoreVersion)

    def killOrphanProcess(self):
        openFile = QFileInfo(self.pidFile)

        fileName = openFile.fileName()
        if QFile.exists(fileName):
            openFile = QFile(fileName)
        else:
            return
        v2rayPID = None

        try:
            openFile.open(QIODevice.ReadOnly | QIODevice.Text)
            v2rayPID = str(openFile.readAll(), "utf-8")
        except Exception:
            pass

        try:
            os.kill(int(v2rayPID), signal.SIGTERM)
        except Exception:
            pass

    def oncreatePIDFile(self):
        if self.v2rayProcess.state() == QProcess.NotRunning:
            return

        outFile = QFileInfo(self.pidFile)
        fileName = outFile.fileName()
        if QFile.exists(fileName):
            QFile.remove(fileName)
        outFile = QFile(fileName)

        v2rayPID = str(self.v2rayProcess.processId())
        qDebug("process ID is: {}".format(v2rayPID))
        try:
            outFile.open(QIODevice.WriteOnly | QIODevice.Text)
            outFile.write(codecs.encode(v2rayPID, "utf-8"))
        except Exception:
            pass
        outFile.close()

    def getV2raycoreVersion(self):
        text = self.outputTextEdit.toPlainText()
        version = re.findall("V2Ray v\d\.\d{1,2}", text)
        failtostart = re.findall("Failed to start App", text)
        if (version):
            version = version[0].split(" ")[1]
            self.bridgetreasureChest.setV2raycoreVersion(version)
        if (failtostart):
            self.outputTextEdit.textChanged.disconnect(
                self.getV2raycoreVersion)
            self.onstop()

    def onstop(self):
        if (self.v2rayProcess.state() == QProcess.Running):
            self.v2rayProcess.close()
            self.v2rayProcess.kill()
            self.outputTextEdit.moveCursor(QTextCursor.End)
            self.outputTextEdit.append("\n\n")
            self.outputTextEdit.insertPlainText(
                str(self.translate(
                    "runV2raycore",
                    "{} is stop now...").format(self.v2rayPath)))
            self.outputTextEdit.insertPlainText(
                str(self.translate(
                    "runV2raycore",
                    "\n{} is ready to run...").format(self.v2rayPath)))
            self.outputTextEdit.moveCursor(QTextCursor.End)

    def setoutputTextEdit(self):
        self.outputTextEdit.moveCursor(QTextCursor.End)
        self.outputTextEdit.insertPlainText(
            str(self.v2rayProcess.readAllStandardOutput(), "utf-8"))
        self.outputTextEdit.insertPlainText(
            str(self.v2rayProcess.readAllStandardError(), "utf-8"))
        self.outputTextEdit.moveCursor(QTextCursor.End)


class executeProgramPanel(QWidget):

    def __init__(self):
        super().__init__()

        self.start = QPushButton("Start")
        self.stop = QPushButton("Stop")
        self.outputTextEdit = QTextEdit()
        self.outputTextEdit.isReadOnly()

        self.labelComand = QLabel("Comand: ")
        self.lineEditComand = QLineEdit()
        self.lineEditComand.setText("ping")
        self.buttonOpenComand = QPushButton("Open")

        self.labelOption = QLabel("Option: ")
        self.lineEditOption = QLineEdit()
        self.lineEditOption.setText("127.0.0.1 -t")

        self.buttonGroup = buttonGroup = QButtonGroup()
        buttonGroup.addButton(self.start)
        buttonGroup.addButton(self.stop)
        buttonGroup.addButton(self.buttonOpenComand)

        gridBox = QGridLayout()
        gridBox.addWidget(self.labelComand, 0, 0)
        gridBox.addWidget(self.lineEditComand, 0, 1, 1, 4)
        gridBox.addWidget(self.buttonOpenComand, 0, 5, 1, 1)
        gridBox.addWidget(self.labelOption, 1, 0, 1, 1)
        gridBox.addWidget(self.lineEditOption, 1, 1, 1, 4)
        gridBox.addWidget(self.start, 2, 4)
        gridBox.addWidget(self.stop, 2, 5)

        vbox = QVBoxLayout()
        vbox.addWidget(self.outputTextEdit)
        vbox.addLayout(gridBox)
        self.setFixedSize(QSize(600, 460))

        self.setLayout(vbox)

        self.buttonGroup.buttonClicked.connect(self.onbuttonGroupClicked)

    def onbuttonGroupClicked(self, e):
        if e.text() == "Start":
            exeFile = None
            option = None
            if (self.lineEditComand.text() != ""):
                exeFile = self.lineEditComand.text()
            if (self.lineEditOption.text() != ""):
                option = self.lineEditOption.text()

            self.runV2ray = runV2raycore(outputTextEdit=self.outputTextEdit,
                                         v2rayPath=exeFile,
                                         v2rayOption=option)
            self.runV2ray.start.emit()

        elif e.text() == "Open":
            options = QFileDialog.Options()
            filePath, _ = QFileDialog.getOpenFileName(
                self,
                "Open V2ray execute File",
                "",
                "All File (*)",
                options=options)
            if (filePath):
                self.lineEditOption.clear()
                self.lineEditComand.clear()
                self.lineEditComand.setText(filePath)

        elif e.text() == "Stop":
            self.runV2ray.stop.emit()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ex = executeProgramPanel()
    ex.show()
    sys.exit(app.exec_())
