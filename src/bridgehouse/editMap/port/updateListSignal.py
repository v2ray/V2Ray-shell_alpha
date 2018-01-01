#!/usr/bin/env python3

from PyQt5.QtCore import pyqtSignal, QObject

class updateListSignal(QObject):
    """
    when the outbound tag had added or changed. 
    will emit a signal to outbound->(Proxy Setting) and inbound->vmess->(Detour To outboundDetuour) update the outbound tags 
    
    when have new level or email will emit to they panel. fresh the list.
    """
    setOutboundTag      = pyqtSignal()
    updateLevelandEmail = pyqtSignal()