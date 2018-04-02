#!/usr/bin/env python3

from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
                             QGridLayout, QRadioButton, QGroupBox, QButtonGroup,
                             QDialog, QSpacerItem)
from PyQt5.QtCore import (QFile, QFileInfo, QUrl, QIODevice, QTimer,
                          QCoreApplication, QSysInfo)
from PyQt5.QtGui import QDesktopServices
from PyQt5.Qt import QTextCursor, PYQT_VERSION_STR, QT_VERSION_STR
import sys, copy, codecs

                             
class bugReport(QDialog):

    def __init__(self):
        super(bugReport, self).__init__()
        self.translate = QCoreApplication.translate
        self.readedHowReportBug = False
        self.timerAutoSave = QTimer()
        self.timerAutoSave.timeout.connect(self.onautoSave)
        self.timerAutoSave.start(1000 * 60 * 3)
        
    def createPanel(self):
        labelReportTitle = QLabel(self.translate("bugReport", "Bug Report Title: "))
        self.lineEditReportTitle = QLineEdit()
        
        labelTestedEnvironment = QLabel(self.translate("bugReport", "Tested Environment: "))
        self.lineEditTestedEnvironment = QLineEdit(
            self.translate("bugReport",
                           """System Platform:{}_{}   Python Version:{}.{}.{}-{}   PyQt Version:{}    QT Version:{}""").format(
                               QSysInfo.prettyProductName() if QSysInfo.prettyProductName() == "unknown" else "{}-{}".format(QSysInfo.kernelType(), QSysInfo.kernelVersion()),
                               QSysInfo.currentCpuArchitecture(),
                               sys.version_info.major,
                               sys.version_info.minor,
                               sys.version_info.micro,
                               sys.version_info.releaselevel,
                               PYQT_VERSION_STR,
                               QT_VERSION_STR))
        
        radioBtnQuickReport = QRadioButton(self.translate("bugReport", "Quick Report"))
        radioBtnKnowHowFix = QRadioButton(self.translate("bugReport", "Know How Fix"))
        radioBtnKnowHowFix.setChecked(True)
        radioBtnFeatureRequest = QRadioButton(self.translate("bugReport", "Feature Request"))
        buttonOpenHowReportBugURL = QPushButton(
            self.translate("bugReport", """Click Me! Read "HOW REPORT A BUG" before report a bug."""))

        self.buttonGroupBugReport = QButtonGroup()
        self.buttonGroupBugReport.addButton(radioBtnQuickReport)
        self.buttonGroupBugReport.addButton(radioBtnKnowHowFix)
        self.buttonGroupBugReport.addButton(radioBtnFeatureRequest)
        self.buttonGroupBugReport.addButton(buttonOpenHowReportBugURL)
        
        hboxRadiobutton = QHBoxLayout()
        hboxRadiobutton.addWidget(radioBtnKnowHowFix)
        hboxRadiobutton.addWidget(radioBtnQuickReport)
        hboxRadiobutton.addWidget(radioBtnFeatureRequest)
        hboxRadiobutton.addWidget(buttonOpenHowReportBugURL)
        hboxRadiobutton.addStretch()
        
        labelStepsToReproduce = QLabel(self.translate("bugReport", "Steps To Reproduce: "))
        self.textEditStepsToReproduce = QTextEdit()
        
        labelActualresults = QLabel(self.translate("bugReport", "Actual results: "))
        self.textEditActualresults = QTextEdit()
        self.textEditActualresults.insertPlainText(
            self.translate("bugReport", "if have Python's Traceback, Please Paste.\nif is V2Ray-core JSON Editor issue, please Paste the JSON File without server information."))
        self.textEditActualresults.setAcceptDrops(True)

        labelExpectedresults = QLabel(self.translate("bugReport", "Expected results: "))
        self.textEditExpectedresults = QTextEdit()

        labelFeatureRequest = QLabel(self.translate("bugReport", "Feature Request: "))
        self.textEditFeatureRequest = QTextEdit()
        
        labelQuickReport = QLabel(self.translate("bugReport", "Quick Report: "))
        self.textEditQuickReport = QTextEdit()
        
        labelHowFix = QLabel(self.translate("bugReport", "How Fix: "))
        self.textEditHowFix = QTextEdit()
        
        gridBoxReport = QGridLayout()
        gridBoxReport.addWidget(labelReportTitle, 0, 0)
        gridBoxReport.addWidget(self.lineEditReportTitle, 0, 1)
        gridBoxReport.addWidget(labelTestedEnvironment, 1, 0)
        gridBoxReport.addWidget(self.lineEditTestedEnvironment, 1, 1)
        gridBoxReport.addLayout(hboxRadiobutton, 2, 0, 1, 2)

        gridBoxQuickReport = QGridLayout()
        gridBoxQuickReport.addWidget(labelQuickReport, 0, 0)
        gridBoxQuickReport.addWidget(self.textEditQuickReport, 0, 1)

        self.groupBoxQuickReport = QGroupBox("", self)
        self.groupBoxQuickReport.setLayout(gridBoxQuickReport)
        self.groupBoxQuickReport.hide()
        
        gridBoxKnowHowFix = QGridLayout()
        gridBoxKnowHowFix.addWidget(labelStepsToReproduce, 0, 0)
        gridBoxKnowHowFix.addWidget(self.textEditStepsToReproduce, 0, 1)
        gridBoxKnowHowFix.addWidget(labelActualresults, 1, 0)
        gridBoxKnowHowFix.addWidget(self.textEditActualresults, 1, 1)
        self.buttonInsertPiture = QPushButton(self.translate("bugReport", "Insert Picture From URL:"))
        self.lineEditInserPiture = QLineEdit()
        gridBoxKnowHowFix.addWidget(self.lineEditInserPiture, 2, 1)
        gridBoxKnowHowFix.addWidget(self.buttonInsertPiture, 2, 0)
        gridBoxKnowHowFix.addItem(QSpacerItem(50, 50), 3, 0, 1, 4)
        gridBoxKnowHowFix.addWidget(labelExpectedresults, 4, 0)
        gridBoxKnowHowFix.addWidget(self.textEditExpectedresults, 4, 1)
        gridBoxKnowHowFix.addWidget(labelHowFix, 5, 0)
        gridBoxKnowHowFix.addWidget(self.textEditHowFix, 5, 1)
        
        self.groupBoxKnowHowFix = QGroupBox()
        self.groupBoxKnowHowFix.setLayout(gridBoxKnowHowFix)

        gridBoxFeatureRequest = QGridLayout()
        gridBoxFeatureRequest.addWidget(labelFeatureRequest, 0, 0)
        gridBoxFeatureRequest.addWidget(self.textEditFeatureRequest, 0, 1)
        
        self.groupBoxFeatureRequest = QGroupBox("", self)
        self.groupBoxFeatureRequest.setLayout(gridBoxFeatureRequest)
        self.groupBoxFeatureRequest.hide()
        
        hboxButton = QHBoxLayout()
        self.buttonExportBugReportText = QPushButton(self.translate("bugReport", "Export Bug Report Text"))
        self.buttonExitButReport = QPushButton(self.translate("bugReport", "Exit"))
        hboxButton.addStretch()
        hboxButton.addWidget(self.buttonExportBugReportText)
        hboxButton.addWidget(self.buttonExitButReport)
        
        vboxBugReport = QVBoxLayout(self)
        vboxBugReport.addLayout(gridBoxReport)
        vboxBugReport.addWidget(self.groupBoxQuickReport)
        vboxBugReport.addWidget(self.groupBoxKnowHowFix)
        vboxBugReport.addWidget(self.groupBoxFeatureRequest)
        vboxBugReport.addLayout(hboxButton)
        vboxBugReport.addStretch()
        
        self.settextEidtReadonly(result=True)
        self.createSignals()
        
    def createSignals(self):
        self.buttonGroupBugReport.buttonClicked.connect(self.onbuttonGroupBugReport)
        self.buttonExitButReport.clicked.connect(self.close)
        self.buttonExportBugReportText.clicked.connect(self.onautoSave)
        self.buttonInsertPiture.clicked.connect(self.onbuttonInsertPiture)
        
    def onbuttonInsertPiture(self):
        url = self.lineEditInserPiture.text()
        if url != "":
            url = QUrl(url)
            self.textEditActualresults.moveCursor(QTextCursor.End)
            self.textEditActualresults.insertPlainText("""\n<img src="{}"/>""".format(url.path()))
            self.textEditActualresults.moveCursor(QTextCursor.End)
            self.lineEditInserPiture.clear()
        
    def settextEidtReadonly(self, result=True):
        self.lineEditInserPiture.setReadOnly(result)
        self.textEditActualresults.setReadOnly(result)
        self.textEditExpectedresults.setReadOnly(result)
        self.textEditFeatureRequest.setReadOnly(result)
        self.textEditHowFix.setReadOnly(result)
        self.textEditQuickReport.setReadOnly(result)
        self.textEditStepsToReproduce.setReadOnly(result)

    def onautoSave(self):
        currentButton = self.buttonGroupBugReport.buttons()
        for i in currentButton:
            if i.isChecked():
                button = i.text()
                if button == self.translate("bugReport", "Quick Report"):
                    self.savebugReportText(save=copy.deepcopy(self.saveQuickReport()))
                if button == self.translate("bugReport", "Know How Fix"):
                    self.savebugReportText(save=copy.deepcopy(self.saveKnowHowFix()))
                if button == self.translate("bugReport", "Feature Request"):
                    self.savebugReportText(save=copy.deepcopy(self.saveFeatureRequest()))
    
    def savebugReportText(self, save=False):
        if save:
            outFile = QFileInfo(self.translate("bugReport", "bugReport.txt"))
            fileName = outFile.fileName()
            if QFile.exists(fileName):
                QFile.remove(fileName)
                    
            outFile = QFile(fileName)
            outFile.open(QIODevice.WriteOnly | QIODevice.Text)
            outFile.write(codecs.encode(save, "utf-8"))
    
    def saveQuickReport(self):
        bugReportText = self.translate("bugReport", "Bug Report Title: \n{}\nTested Environment: \n{}\n\nQuick Report:\n{}\n").format(
            self.lineEditReportTitle.text(),
            self.lineEditTestedEnvironment.text(),
            self.textEditQuickReport.toPlainText())

        return  bugReportText
    
    def saveKnowHowFix(self):
        bugReportText = self.translate("bugReport", """Bug Report Title: {}
\nTested Environment: \n{}
\nSteps To Reproduce: \n{}
\nActual Results: \n{}
\nExpected Results: \n{}
\nHow Fix: \n{}\n""").format(
            self.lineEditReportTitle.text(),
            self.lineEditTestedEnvironment.text(),
            self.textEditStepsToReproduce.toPlainText(),
            self.textEditActualresults.toPlainText(),
            self.textEditExpectedresults.toPlainText(),
            self.textEditHowFix.toPlainText())

        return bugReportText
    
    def saveFeatureRequest(self):
        bugReportText = self.translate("bugReport", """Feature Request Title: \n{}
Tested Environment: \n{}
Feature Request Details:\n{}\n""").format(
            self.lineEditReportTitle.text(),
            self.lineEditTestedEnvironment.text(),
            self.textEditFeatureRequest.toPlainText())
        
        return bugReportText
        
    def onbuttonGroupBugReport(self, button):

        def hideAllWidget():
            self.groupBoxFeatureRequest.hide()
            self.groupBoxKnowHowFix.hide()
            self.groupBoxQuickReport.hide()
        
        buttonText = button.text()
        if buttonText == self.translate("bugReport", "Quick Report"):
            hideAllWidget()
            self.groupBoxQuickReport.show()
        elif buttonText == self.translate("bugReport", "Know How Fix"):
            hideAllWidget()
            self.groupBoxKnowHowFix.show()
        elif buttonText == self.translate("bugReport", "Feature Request"):
            hideAllWidget()
            self.groupBoxFeatureRequest.show()
        elif buttonText == self.translate("bugReport", """Click Me! Read "HOW REPORT A BUG" before report a bug."""):
            QDesktopServices.openUrl(QUrl("https://www.chiark.greenend.org.uk/~sgtatham/bugs.html"))
            self.settextEidtReadonly(result=False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = bugReport()
    ex.createPanel()
    ex.setGeometry(250, 150, 1024, 768)
    ex.show()
    sys.exit(app.exec_())
