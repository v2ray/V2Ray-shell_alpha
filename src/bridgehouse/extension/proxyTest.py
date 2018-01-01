#!/usr/bin/env python3

import sys, copy
from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout, QLineEdit,
                             QRadioButton, QSpinBox, QHBoxLayout, QButtonGroup, 
                             QPushButton, QGridLayout,QTextEdit)
from PyQt5.QtCore    import (QElapsedTimer, pyqtSignal, QObject, QUrl, 
                             Qt, QFileInfo, QTimer, QCoreApplication)
from PyQt5.QtNetwork import (QNetworkProxy, QNetworkRequest, QNetworkAccessManager, 
                             QNetworkReply)
from PyQt5.QtGui     import QPalette
from PyQt5.Qt        import QColor, QFont

v2rayshellDebug = False

if __name__ == "__main__":
    v2rayshellDebug = True
    ### this for debug test
    path = QFileInfo(sys.argv[0])
    srcPath = path.path().split("/")
    sys.path.append("/".join(srcPath[:-2]))

class proxyStatus(QObject):
    signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.targetHostReplyMessage = False
        self.targetHostReply = False
        self.proxyisWorking = False
        self.error = False
        self.errorCode = False
        self.errorString = False
        self.elapsedTime = False
        self.elapsedTimer = QElapsedTimer()
        
    def clear(self):
        self.targetHostReplyMessage = False
        self.targetHostReply = False
        self.error = False
        self.errorString = False
        self.elapsedTime = False
        self.proxyisWorking = False
        
    def setProxyisWorking(self, work: bool):
        if not isinstance(work, bool):
            raise TypeError
        self.proxyisWorking = work
    
    def getProxyisWorking(self):
        return self.proxyisWorking
    
    def setProxyErrorCode(self, errorCode):
        self.errorCode = copy.deepcopy(errorCode)
        
    def getProxyErrorCode(self):
        return self.errorCode
    
    def setTargetHostReplyMessage(self, replyMessage):
        self.targetHostReplyMessage = copy.deepcopy(replyMessage)
    
    def getTargetHostReplyMessage(self):
        return self.targetHostReplyMessage
        
    def getElapsedTime(self):
        return self.elapsedTime
    
    def setElapsedTime(self, elapsedTime):
        self.elapsedTime = copy.deepcopy(elapsedTime)
        
    def setTargetHostReply(self, reply = False):
        self.targetHostReply = reply
    
    def getTargetHostReply(self):
        return self.targetHostReply
    
    def setProxyErrorString(self, errorString):
        self.errorString = copy.deepcopy(errorString)
        
    def getProxyErrorString(self):
        return self.errorString
    
    def setProxyError(self, error = False):
        self.error = error
        
    def getProxyError(self):
        return self.error
        
class proxyTest():
    def __init__(self, 
                 proxyprotocol  = QNetworkProxy.Socks5Proxy, 
                 proxyhostname  = "127.0.0.1", 
                 proxyhostport  = 1080, 
                 targethosturl  = "http://www.google.com", 
                 getproxyStatus = False,
                 timeout        = False):
        self.protocol           = proxyprotocol
        self.proxyhostName      = proxyhostname
        self.port               = int(proxyhostport)
        self.url                = targethosturl
        self.proxyStatus        = getproxyStatus
        self.reply              = None
        self.stopCheckProxy     = None
        self.req                = None
        self.qnam               = QNetworkAccessManager()
        if (self.proxyStatus):
            self.req = QNetworkRequest(QUrl(self.url))
            self.proxy = QNetworkProxy()
            self.proxy.setType(self.protocol)
            self.proxy.setHostName(self.proxyhostName)
            self.proxy.setPort(self.port)
            self.proxy.setApplicationProxy(self.proxy)
            
            if timeout == 0:
                self.startRequest()
            else:
                self.stopCheckProxy = QTimer()
                self.stopCheckProxy.timeout.connect(self.timeoutStopCheckProxy)
                self.stopCheckProxy.setSingleShot(True)
                if timeout > 15 or timeout < 0:
                    timeout = 5
                ### after five seconds stop checking the proxy and destroy this class
                self.stopCheckProxy.start(1000*timeout)  
                self.startRequest()

    def startRequest(self):
        self.reply = self.qnam.get(self.req) 
        self.reply.finished.connect(self.handleResponse)
        self.proxyStatus.elapsedTimer.start()      
                
    def timeoutStopCheckProxy(self):
        """
        Frequent detection of proxy server, memory overflow may occur. 
        Therefore, it should be automatically destroyed within the stipulated time. 
        Not sure if GC is working
        """
        self.reply.abort()
        self.reply.close()
        #print(sys.getrefcount(self))
        
        del self.protocol; self.proxyhostName; self.port; self.url; self.reply; self.stopCheckProxy
        del self.req; self.qnam; self.proxy
        del self

    def handleResponse(self):      
        errorCode = self.reply.error()
        if errorCode == QNetworkReply.NoError:
            self.proxyStatus.setTargetHostReplyMessage(
                replyMessage = str(self.reply.readAll(), "utf-8"))
            self.proxyStatus.setTargetHostReply(reply = True)
            self.proxyStatus.setProxyisWorking(True)
        else:
            self.proxyStatus.setProxyErrorString(errorString = self.reply.errorString())
            self.proxyStatus.setProxyError(error = True)     ### proxy connection error
            self.proxyStatus.setProxyErrorCode(errorCode = self.reply.error())
            self.proxyStatus.setProxyisWorking(False)

        self.proxyStatus.setElapsedTime(self.proxyStatus.elapsedTimer.elapsed())
        self.proxyStatus.signal.emit()

class proxyTestPanel(QDialog):
    """
    This is the normal time spent browsing the web milliseconds, 
    not the server response time
    """
    def __init__(self, 
                 proxyprotocol  = QNetworkProxy.Socks5Proxy, 
                 proxyhostname  = "127.0.0.1", 
                 proxyhostport  = 1080, 
                 targethosturl  = "http://www.google.com", 
                 getproxyStatus = False):
        super().__init__()
        self.protocol           = proxyprotocol
        self.proxyhostName      = proxyhostname
        self.port               = int(proxyhostport)
        self.url                = targethosturl
        
        if (getproxyStatus == False):
            self.proxyStatus = proxyStatus()
        else:
            self.proxyStatus = getproxyStatus
        self.translate = QCoreApplication.translate
        
    def createproxyTestPanel(self):
        self.buttonCheckProxy = QPushButton(self.translate("proxyTestPanel", "Check..."), self)
        labelproxyhostName    = QLabel(self.translate("proxyTestPanel", "Proxy Host Name: "), self)
        self.lineEditproxyHostName = QLineEdit(self.proxyhostName)
        labelPort = QLabel(self.translate("proxyTestPanel", "Port: "), self)
        self.spinBoxPort = QSpinBox(self)
        self.spinBoxPort.setRange(0, 65535)
        self.spinBoxPort.setValue(1080)
        
        hboxPort = QHBoxLayout()
        hboxPort.addWidget(labelPort)
        hboxPort.addWidget(self.spinBoxPort)
        hboxPort.addStretch()
        
        labelTargethostUrl = QLabel(
            self.translate("proxyTestPanel", "Target Host Url: "), self)
        self.lineEdittargethostUrl = QLineEdit(self.url, self)
        
        labelProxyProtocol = QLabel(
            self.translate("proxyTestPanel", "Proxy Protocol: "), self)
        radioButtonSocks5 = QRadioButton("Socks5", self)
        radioButtonSocks5.setChecked(True)
        radioButtonHttp   = QRadioButton("Http", self)
        
        self.groupRadioButton = QButtonGroup()
        self.groupRadioButton.addButton(radioButtonSocks5)
        self.groupRadioButton.addButton(radioButtonHttp)
        
        hboxRadioButtonProxyProtocol = QHBoxLayout()
        hboxRadioButtonProxyProtocol.addWidget(radioButtonSocks5)
        hboxRadioButtonProxyProtocol.addWidget(radioButtonHttp)
        hboxRadioButtonProxyProtocol.addStretch()
        
        labelProxyStatus = QLabel(self.translate("proxyTestPanel", "Proxy Status: "), self)
        labelProxyTimeLag = QLabel(self.translate("proxyTestPanel", "Proxy Time Lag: "), self)
        
        self.labelproxyStatus = QLabel()
        self.labelproxyTimeLag = QLabel()
        labelFont = QFont()
        labelFont.setPointSize(16)
        labelFont.setBold(True)
        self.labelproxyStatus.setFont(labelFont)
        self.labelproxyTimeLag.setFont(labelFont)
        
        self.palettelabelProxyStatusOK    = QPalette()
        self.palettelabelProxyStatusOK.setColor(QPalette.WindowText, QColor(34, 139, 34)) ###ForestGreen
        self.palettelabelProxyStatusFalse = QPalette()
        self.palettelabelProxyStatusFalse.setColor(QPalette.WindowText, Qt.red)
        
        self.palettelabelProxyTimeLagForestGreen = QPalette()
        self.palettelabelProxyTimeLagForestGreen.setColor(QPalette.WindowText, QColor(34, 139, 34))
        self.palettelabelProxyTimeLagDarkOrange = QPalette()
        self.palettelabelProxyTimeLagDarkOrange.setColor(QPalette.WindowText, QColor(255, 140, 0))
        self.palettelabelProxyTimeLagRed = QPalette()
        self.palettelabelProxyTimeLagRed.setColor(QPalette.WindowText, Qt.red)
        
        self.textEditProxy = QTextEdit()
        self.textEditProxy.setReadOnly(True)

        gridBoxProxy = QGridLayout()
        gridBoxProxy.addWidget(labelproxyhostName, 0, 0)
        gridBoxProxy.addWidget(self.lineEditproxyHostName, 0, 1)
        gridBoxProxy.addLayout(hboxPort, 0, 2)
        gridBoxProxy.addWidget(labelTargethostUrl, 1, 0)
        gridBoxProxy.addWidget(self.lineEdittargethostUrl, 1, 1)
        gridBoxProxy.addWidget(labelProxyProtocol, 2, 0)
        gridBoxProxy.addLayout(hboxRadioButtonProxyProtocol, 2, 1)
        gridBoxProxy.addWidget(labelProxyStatus, 3, 0)
        gridBoxProxy.addWidget(self.labelproxyStatus, 3, 1)
        gridBoxProxy.addWidget(labelProxyTimeLag, 4, 0)
        gridBoxProxy.addWidget(self.labelproxyTimeLag, 4, 1)
        
        hboxButtonCheckProxy = QHBoxLayout()
        hboxButtonCheckProxy.addStretch()
        hboxButtonCheckProxy.addWidget(self.buttonCheckProxy)
        
        vboxProxy = QVBoxLayout()
        vboxProxy.addLayout(gridBoxProxy)
        vboxProxy.addWidget(self.textEditProxy)
        #vboxProxy.addStretch()
        vboxProxy.addLayout(hboxButtonCheckProxy)
        
        self.buttonCheckProxy.clicked.connect(self.onButtonCheckProxy)
        self.settingProxyPanel()
        self.setLayout(vboxProxy)
        
    def settingProxyPanel(self):
        self.lineEditproxyHostName.setText(self.proxyhostName)
        self.lineEdittargethostUrl.setText(self.url)
        self.spinBoxPort.setValue(self.port)
        protocol = False
        if (self.protocol == QNetworkProxy.Socks5Proxy):
            protocol = "Socks5"
        elif (self.protocol == QNetworkProxy.HttpProxy):
            protocol = "Http"
            
        for i in self.groupRadioButton.buttons():
            if i.text() == protocol:
                i.setChecked(True)
  
    def onButtonCheckProxy(self):
        self.proxyProtocol = QNetworkProxy.Socks5Proxy ### default
        if (self.groupRadioButton.checkedButton().text() == "Socks5"):
            self.proxyProtocol = QNetworkProxy.Socks5Proxy
        elif (self.groupRadioButton.checkedButton().text() == "Http"):
            self.proxyProtocol = QNetworkProxy.HttpProxy
            
        self.url  = self.lineEdittargethostUrl.text()
        self.port = self.spinBoxPort.value()
        self.proxyhostName = self.lineEditproxyHostName.text()
        
        self.setProxyStatuslabelChecking()
        self.proxyStatus.clear()
        self.proxyStatus.signal.connect(self.setProxyStatuslabelColor)
        self.proxy = proxyTest(getproxyStatus = self.proxyStatus, 
                               proxyprotocol  = self.proxyProtocol,
                               targethosturl  = self.url,
                               proxyhostport  = int(self.port),
                               proxyhostname  = self.proxyhostName,
                               timeout        = False)

    def setProxyStatuslabelChecking(self):
        self.labelproxyStatus.setText(self.translate("proxyTestPanel", "Proxy Checking..."))
        palettelabelColorDark = QPalette()
        palettelabelColorDark.setColor(QPalette.WindowText, Qt.black)
        self.labelproxyStatus.setPalette(palettelabelColorDark)
        self.labelproxyTimeLag.clear()
    
    def setProxyStatuslabelColor(self):
        self.textEditProxy.clear()
        if (self.proxyStatus.getProxyError() == False):
            """
            Proxy running OK
            """
            self.labelproxyStatus.setText(
                str(self.translate("proxyTestPanel","Proxy running OK.")))
            self.labelproxyStatus.setPalette(self.palettelabelProxyStatusOK)
            self.labelproxyTimeLag.setText(str(self.proxyStatus.getElapsedTime()) + " ms")
            if (self.proxyStatus.getElapsedTime() < 260):
                self.labelproxyTimeLag.setPalette(self.palettelabelProxyTimeLagForestGreen)
            elif (self.proxyStatus.getElapsedTime() > 420):
                self.labelproxyTimeLag.setPalette(self.palettelabelProxyTimeLagRed)
            else:
                self.labelproxyTimeLag.setPalette(self.palettelabelProxyTimeLagDarkOrange)
            self.textEditProxy.setHtml(self.proxyStatus.getTargetHostReplyMessage())
        else:
            """
            Proxy running False
            """
            self.labelproxyStatus.setText(
                self.translate("proxyTestPanel", "Error Code: {}. Error Message: {}").format(
                    str(self.proxyStatus.getProxyError()), 
                    str(self.proxyStatus.getProxyErrorString())))
            self.labelproxyStatus.setPalette(self.palettelabelProxyStatusFalse)
            self.labelproxyTimeLag.setText(str(self.proxyStatus.getElapsedTime()) + " ms")
            self.labelproxyTimeLag.setPalette(self.palettelabelProxyTimeLagRed)

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    status = proxyStatus()
    proxyPanel = proxyTestPanel(getproxyStatus=status)
    proxyPanel.createproxyTestPanel()
    proxyPanel.setGeometry(500, 300, 600, 320)
    proxyPanel.show()
    sys.exit(app.exec_())