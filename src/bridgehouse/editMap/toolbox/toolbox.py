from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import (QApplication, QStyledItemDelegate,
        QTableView, QWidget, QPushButton, QLineEdit, QStyle, QSpinBox,
    QComboBox)
import uuid

class UUIDLineEdit(QLineEdit):
    def __init__(self, parent=None, btnName=None):
        QLineEdit.__init__(self, parent)

        self.btn = QPushButton(btnName, self)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.setStyleSheet('QLineEdit {{ padding-left: {}px; }} '.format(
            self.btn.sizeHint().width() + frameWidth + 1))
        msz = self.minimumSizeHint()
        self.setMinimumSize(max(msz.width(), self.btn.sizeHint().height() + frameWidth * 2 + 2),
                            max(msz.height(), self.btn.sizeHint().height() + frameWidth * 2 + 2))
        self.setInputMask("HHHHHHHH-HHHH-HHHH-HHHH-HHHHHHHHHHHH; ")
        self.btn.clicked.connect(lambda: self.setText(str(uuid.uuid4())))


class UUIDLineEditDelegate(QStyledItemDelegate):
    def __init__(self, btnName=None):
        super(UUIDLineEditDelegate, self).__init__()
        self.btnName = btnName

    def createEditor(self, parent, option, index):
        editor = UUIDLineEdit(parent, self.btnName)
        return editor

    def setEditorData(self, lineEdit, index):
        value = index.model().data(index, Qt.EditRole)
        lineEdit.setText(str(value))

    def setModelData(self, lineEdit, model, index):
        value = lineEdit.text()
        model.setData(index, value, Qt.EditRole)
        
    def updateEditorGeometry(self, lineEdit, option, index):
        lineEdit.setGeometry(option.rect)
        
        
class SpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, min=False, max=False):
        super(SpinBoxDelegate, self).__init__()
        self.min, self.max = min, max

    def createEditor(self, parent, option, index):
        editor = QSpinBox(parent)
        editor.setFrame(False)
        editor.setMinimum(int(self.min))
        editor.setMaximum(int(self.max))
        editor.setValue(0)

        return editor

    def setEditorData(self, spinBox, index):
        value = index.model().data(index, Qt.EditRole)

        spinBox.setValue(0 if not value else value)

    def setModelData(self, spinBox, model, index):
        spinBox.interpretText()
        value = spinBox.value()

        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
        
class ComboBoxSpinBoxDelegate(QStyledItemDelegate):
    def __init__(self, comboList=None):
        super(ComboBoxSpinBoxDelegate, self).__init__()
        self.comboList = comboList
        
    def createEditor(self, parent, option, index):
        if index.parent().row() != -1:
            editor = QComboBox(parent)
            if self.comboList:
                editor.addItems(self.comboList)
            
            return editor
        else:
            editor = QSpinBox(parent)
            editor.setMaximum(65535)
            editor.setMinimum(0)
            editor.setValue(443)
            return editor

    def setEditorData(self, comboBox, index):
        value = index.model().data(index, Qt.EditRole)
        if index.parent().row() != -1 and value in self.comboList:
            comboBox.setCurrentText(value)
        else:
            try:
                comboBox.setValue(int(value))
            except:
                pass

    def setModelData(self, comboBox, model, index):
        if index.parent().row() != -1:
            value = comboBox.currentText()
        else:
            value = comboBox.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
        
class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, comboList=None):
        super(ComboBoxDelegate, self).__init__()
        self.comboList = comboList
        
    def createEditor(self, parent, option, index):
        editor = QComboBox(parent)
        if self.comboList:
            editor.addItems(self.comboList)
            
        return editor

    def setEditorData(self, comboBox, index):
        value = index.model().data(index, Qt.EditRole)
        if value in self.comboList:
            comboBox.setCurrentText(value)

    def setModelData(self, comboBox, model, index):
        value = comboBox.currentText()

        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)
