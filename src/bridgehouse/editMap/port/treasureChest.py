#!/usr/bin/env python3

from PyQt5.QtCore import QUuid
import copy
from bridgehouse.editMap.port import updateListSignal


class treasureChest():
    """
    Share in/outbound panel's setting, share in/outbound's data.
    Export or store in/outbound(Detour) settings.  export or store in/outbound's data.
    """

    def __init__(self):
        self.__log = {}
        self.__dns = {}
        self.__api = {}
        self.__routing = {}
        self.__policy = {}
        self.__inbound = {}
        self.__outbound = {}
        self.__inboundDetour = {}
        self.__outboundDetour = {}
        self.__transport = {}
        self.__stats = {}
        self.__emails = set()
        self.__levels = set()
        self.updateList = updateListSignal.updateListSignal()
    
    def clear(self):
        self.__log = {}
        self.__dns = {}
        self.__api = {}
        self.__routing = {}
        self.__policy = {}
        self.__inbound = {}
        self.__outbound = {}
        self.__inboundDetour = {}
        self.__outboundDetour = {}
        self.__transport = {}
        self.__stats = {}
        self.__levels.clear()
    
    def __validBoundTags(self, tag):
        if (not tag): return False

        if (tag in self.getAllTags()): return True
        else: return False
        
    def getAllTags(self):
        allTags = set()
        allTags.add("api")  # v2ray 3.7 have new tag
        if (len(self.__outbound) > 0):
            for i in self.__outbound.items():
                allTags.add(i[1]["tag"])
        if (len(self.__inbound) > 0): 
            for i in self.__inbound.items():
                allTags.add(i[1]["tag"])
        if (len(self.__outboundDetour) > 0):
            for i in self.__outboundDetour.items():
                allTags.add(i[1]["tag"])
        if (len(self.__inboundDetour) > 0):
            for i in self.__inboundDetour.items():
                allTags.add(i[1]["tag"])

        return allTags
 
    def getInbound(self):
        if (self.__inbound):
            inbound = {}  # return a copy
            for i in self.__inbound.items():
                inbound = copy.deepcopy(i[1])
            return inbound
        else:
            return False
    
    def getInboundDetour(self, tag):
        if (tag in self.__inboundDetour.keys()):
            inboundDetour = copy.deepcopy(self.__inboundDetour[tag]) 
            return inboundDetour
        else:
            return False
        
    def getRandomHex(self):
        """
        if user conf.json file have no named tags, random a tag name to panel
        if allow in/outbound(Detour) no tags will make this script complicated
        """
        import codecs
        from zlib import crc32  # Use crc32 in order to use the same character length
        # use [2:] remove '0x', i don't like the function hex() header '0x'
        return str(hex(crc32(codecs.encode(QUuid.createUuid().toString(), "utf-8"))))[5:]
 
    def setInbound(self, inboundJSONData, openFromJSONFile=False):
        """
        add new inbound  or modify old inbound
        """
        if (not openFromJSONFile):
            tag = inboundJSONData["tag"]
            self.__inbound.clear()  # make sure this inbound is only one
            if (self.__validBoundTags(tag)): return False
            if not tag: return False
            self.__inbound[tag] = copy.deepcopy(inboundJSONData)
            self.updateList.updateLevelandEmail.emit()
            return tag
        elif(openFromJSONFile):
            try:
                # many example have no named a bound's tag
                inboundJSONData["tag"]
            except KeyError:
                # if there no tag keys (listen, port, protocol), 
                # will a get critical error stop this script 
                tag = inboundJSONData["tag"] = "inbound-{}".format(self.getRandomHex())
                self.__inbound.clear()
                self.__inbound[tag] = copy.deepcopy(inboundJSONData)
                self.updateList.updateLevelandEmail.emit()
                return tag
            else:
                # if there are duplicate names, rename this tag
                tag = inboundJSONData["tag"]
                if (self.__validBoundTags(tag) or not tag): 
                    tag = inboundJSONData["tag"] = "{}-{}".format(tag, self.getRandomHex())
                    self.__inbound.clear()
                    self.__inbound[tag] = copy.deepcopy(inboundJSONData)
                    self.updateList.updateLevelandEmail.emit()
                    return tag
                else:
                    self.__inbound.clear()
                    self.__inbound[tag] = copy.deepcopy(inboundJSONData)
                    self.updateList.updateLevelandEmail.emit()
                    return tag
 
    def removeInboundDetour(self, tag):
        if (tag in self.__inboundDetour.keys()):
            del self.__inboundDetour[tag]
            return True
        else:
            return False
        
    def removeOutboundDetour(self, tag):
        if (tag in self.__outboundDetour.keys()):
            del self.__outboundDetour[tag]
            self.updateList.setInboundTag.emit()
            return True
        else:
            return False
    
    def getInboundTags(self):
        inBoundTags = []
        if (len(self.__inbound) > 0):
            for i in self.__inbound.items():
                inBoundTags.append(copy.deepcopy(i[1]["tag"]))
        if (len(self.__inboundDetour) > 0):
            for i in self.__inboundDetour.items():
                inBoundTags.append(copy.deepcopy(i[1]["tag"]))

        return inBoundTags
       
    def getOutboundTags(self):
        outBoundTags = []
        if (len(self.__outbound) > 0):
            for i in self.__outbound.items():
                outBoundTags.append(copy.deepcopy(i[1]["tag"]))
        if (len(self.__outboundDetour) > 0):
            for i in self.__outboundDetour.items():
                outBoundTags.append(copy.deepcopy(i[1]["tag"]))
        
        return outBoundTags    
    
    def addInboundDetour(self, inboundDetourJSONData, openFromJSONFile=False):
        """
        add a new inboundDetour
        """
        if (not openFromJSONFile):
            tag = inboundDetourJSONData["tag"]
            if (self.__validBoundTags(tag)): return False
            else:
                self.__inboundDetour[tag] = copy.deepcopy(inboundDetourJSONData)
                self.updateList.updateLevelandEmail.emit()
                return tag
        elif(openFromJSONFile):
            try:
                inboundDetourJSONData["tag"]
            except KeyError:
                # TODO if there no keys (listen, port, protocol), will a get critical error stop this script 
                tag = inboundDetourJSONData["tag"] = "inbound-{}".format(self.getRandomHex())
                self.__inboundDetour[tag] = copy.deepcopy(inboundDetourJSONData)
                self.updateList.updateLevelandEmail.emit()
                return tag
            else:
                # if there are duplicate names, rename this tag
                tag = inboundDetourJSONData["tag"]
                if (self.__validBoundTags(tag) or not tag):
                    tag = inboundDetourJSONData["tag"] = "{}-{}".format(tag,
                                                                        self.getRandomHex())
                    self.__inboundDetour[tag] = copy.deepcopy(inboundDetourJSONData)
                    self.updateList.updateLevelandEmail.emit()
                    return tag
                else:
                    self.__inboundDetour[tag] = copy.deepcopy(inboundDetourJSONData)
                    self.updateList.updateLevelandEmail.emit()
                    return tag

    def setInboundDetour(self, oldTag, newinboundDetourJSONData, openFromJSONFile=False):
        """
        modify an old inboundDetour
        """
        if (self.__validBoundTags(oldTag) and not openFromJSONFile):
            self.removeInboundDetour(oldTag)
            self.addInboundDetour(newinboundDetourJSONData, openFromJSONFile)
            return True
        elif (openFromJSONFile):
            if not newinboundDetourJSONData: return False
            for i in newinboundDetourJSONData:
                if not i: break
                self.addInboundDetour(i, openFromJSONFile)
            return True
        else:
            return False
        
    def addLevel(self, level):
        self.__levels.add(str(level))
    
    def getLevels(self):
        if len(self.__levels) > 0: 
            sortLevel = []
            level = copy.deepcopy(self.__levels)
            for i in level:
                try:
                    sortLevel.append(int(i))
                except Exception:
                    pass
            sortLevel.sort()
            return [str(i) for i in sortLevel]
        else: return False

    def addEmail(self, email):
        if email:
            self.__emails.add(copy.deepcopy(email))
        
    def getEmails(self):
        if len(self.__emails) > 0: return self.__emails
        else: return False

    def setLog(self, JSONDataLog):
        self.__log = copy.deepcopy(JSONDataLog)
    
    def setDns(self, JSONDataDns):
        self.__dns = copy.deepcopy(JSONDataDns)
    
    def setTransport(self, JSONDataTransport=False):
        if (JSONDataTransport):
            self.__transport = copy.deepcopy(JSONDataTransport)

    def setRouting(self, JSONDataRouting):
        self.__routing = copy.deepcopy(JSONDataRouting)

    def setApi(self, JSONDataApi):
        try:
            self.__api["tag"] = copy.deepcopy(JSONDataApi["tag"])
            self.__api["services"] = copy.deepcopy(JSONDataApi["services"])
        except Exception: pass
    
    def getApi(self):
        api = copy.deepcopy(self.__api)
        return api
    
    def setStats(self, JSONDataStats):
        self.__stats = copy.deepcopy(JSONDataStats)
    
    def getStats(self):
        return self.__stats

    def setPolicy(self, JSONDataPolicy):
        """
        when the script start, if the JSON has policy. add to policyTAB
        but would not parse in/outbound's policy
        """
        self.__policy = copy.deepcopy(JSONDataPolicy)
        if self.__policy:
            for i in self.__policy.keys():
                try:
                    int(i)
                except Exception:
                    continue
                self.addLevel(str(i))
        self.updateList.updateLevelandEmail.emit()

    def getPolicy(self):
        polciy = copy.deepcopy(self.__policy)
        
        return polciy
    
    def getLog(self):
        log = copy.deepcopy(self.__log)
        
        return log
    
    def getDns(self):
        dns = copy.deepcopy(self.__dns)
        
        return dns
    
    def getTransport(self):
        transport = copy.deepcopy(self.__transport)
        if (not transport):
            return False
        else: return transport 

    def getRouting(self):
        routing = copy.deepcopy(self.__routing)
    
        return routing
    
    def getOutbound(self):
        if (self.__outbound):
            outbound = {}
            for i in self.__outbound.items():
                outbound = copy.deepcopy(i[1])
            return outbound
        else:
            return False
    
    def getOutboundDetour(self, tag):
        if (tag in self.__outboundDetour.keys()):
            outboundDetour = copy.deepcopy(self.__outboundDetour[tag])
            return outboundDetour
        return False
 
    def setOutbound(self, outboundJSONData, openFromJSONFile=False):
        """
        add new outbound or modify old outbound
        """
        if (not openFromJSONFile):
            tag = outboundJSONData["tag"]
            self.__outbound.clear()  # make sure this outbound is only one
            if (self.__validBoundTags(tag)): return False
            if not tag: return False
            self.__outbound[tag] = copy.deepcopy(outboundJSONData)
            self.updateList.setInboundTag.emit()
            self.updateList.updateLevelandEmail.emit()
            return tag
        elif (openFromJSONFile):
            try:
                outboundJSONData["tag"]
            except KeyError:
                tag = outboundJSONData["tag"] = "outbound-{}".format(self.getRandomHex())
                self.__outbound.clear()
                self.__outbound[tag] = copy.deepcopy(outboundJSONData)
                self.updateList.setInboundTag.emit()
                self.updateList.updateLevelandEmail.emit()
                return tag
            else:
                # if there are duplicate names, rename this tag
                tag = outboundJSONData["tag"]
                if (self.__validBoundTags(tag) or not tag): 
                    tag = outboundJSONData["tag"] = "{}-{}".format(tag,
                                                                   self.getRandomHex())
                    self.__outbound.clear()
                    self.__outbound[tag] = copy.deepcopy(outboundJSONData)
                    self.updateList.setInboundTag.emit()
                    self.updateList.updateLevelandEmail.emit()
                    return tag
                else:
                    self.__outbound.clear()
                    self.__outbound[tag] = copy.deepcopy(outboundJSONData)
                    self.updateList.setInboundTag.emit()
                    self.updateList.updateLevelandEmail.emit()
                    return tag

    def setOutboundDetour(self, oldTag, newoutboundDetourJSONData, openFromJSONFile=False):
        """
        modify an old outboundDetour
        """
        if (self.__validBoundTags(oldTag) and not openFromJSONFile):
            self.removeOutboundDetour(oldTag)
            self.addOutboundDetour(newoutboundDetourJSONData, openFromJSONFile)
            self.updateList.setInboundTag.emit()
            return True
        elif (openFromJSONFile):
            for i in newoutboundDetourJSONData:
                if not i: break
                self.addOutboundDetour(i, openFromJSONFile)
                self.updateList.setInboundTag.emit()
            return True
        else:
            return False
            
    def addOutboundDetour(self, outboundDetourJSONData, openFromJSONFile=False):
        """
        add a new outboundDetour
        """
        if (not openFromJSONFile):
            tag = outboundDetourJSONData["tag"]
            if (self.__validBoundTags(tag)):
                return False
            else:
                self.__outboundDetour[tag] = copy.deepcopy(outboundDetourJSONData)
                self.updateList.updateLevelandEmail.emit()
                return tag
        else:
            try:
                outboundDetourJSONData["tag"]
            except KeyError:
                tag = outboundDetourJSONData["tag"] = "outbound-{}".format(self.getRandomHex())
                self.__outboundDetour[tag] = copy.deepcopy(outboundDetourJSONData)
                self.updateList.updateLevelandEmail.emit()
                return tag
            else:
                # if there are duplicate names, rename this outbound's tag
                tag = outboundDetourJSONData["tag"]
                if (self.__validBoundTags(tag) or not tag): 
                    tag = outboundDetourJSONData["tag"] = "{}-{}".format(tag,
                                                                         self.getRandomHex())
                    self.__outboundDetour[tag] = copy.deepcopy(outboundDetourJSONData)
                    self.updateList.updateLevelandEmail.emit()
                    return tag
                else:
                    self.__outboundDetour[tag] = copy.deepcopy(outboundDetourJSONData)
                    self.updateList.updateLevelandEmail.emit()
                    return tag

    def exportInboudJSONFile(self):
        """
        for inbound Panel debug test
        """
        inboundJSONFile = {
            "inbound":{},
            "inboundDetour":[]
            }
        for i in self.__inbound.items():
            inboundJSONFile["inbound"] = copy.deepcopy(i[1])

        if (self.__inboundDetour):
            for i in self.__inboundDetour.items():
                inboundJSONFile["inboundDetour"].append(copy.deepcopy(i[1]))
        else:
            del inboundJSONFile["inboundDetour"]
            
        return inboundJSONFile

    def exportOutBoundJSONFile(self):
        """
        for outbound Panel debug test
        """
        outboundJSONFile = {
            "outbound": {},
            "outboundDetour": []
            }
        for i in self.__outbound.items():
            outboundJSONFile["outbound"] = copy.deepcopy(i[1])
        
        if (self.__outboundDetour):
                for i in self.__outboundDetour.items():
                    outboundJSONFile["outboundDetour"].append(copy.deepcopy(i[1]))
        else:
            del outboundJSONFile["outboundDetour"]

        return outboundJSONFile
    
    def exportV2rayJSONFile(self):
        v2rayJSONFile = {
                            "log": {},
                            "inbound": {},
                            "outbound": {},
                            "inboundDetour": [],
                            "outboundDetour": [],
                            "transport": {},
                            "dns": {},
                            "routing": {},
                            "api": {},
                            "stats": {},
                            "policy": {
                                "levels":{}
                                }
                        }
        
        v2rayJSONFile["log"] = self.getLog()
        v2rayJSONFile["dns"] = self.getDns()
        if (self.__api):
            v2rayJSONFile["api"] = self.getApi()
        else:
            del v2rayJSONFile["api"]
        v2rayJSONFile["routing"] = self.getRouting()
        v2rayJSONFile["policy"]["levels"] = self.getPolicy()
        
        for i in self.__inbound.items():
            v2rayJSONFile["inbound"] = copy.deepcopy(i[1])
            
        for i in self.__outbound.items():
            v2rayJSONFile["outbound"] = copy.deepcopy(i[1])
        
        if (self.__inboundDetour):
            for i in self.__inboundDetour.items():
                v2rayJSONFile["inboundDetour"].append(copy.deepcopy(i[1]))
        else:
            del v2rayJSONFile["inboundDetour"]
        
        if (self.__outboundDetour):
            for i in self.__outboundDetour.items():
                v2rayJSONFile["outboundDetour"].append(copy.deepcopy(i[1]))
        else:
            del v2rayJSONFile["outboundDetour"]
            
        v2rayJSONFile["transport"] = self.getTransport()
        if not v2rayJSONFile["transport"]:
            del v2rayJSONFile["transport"]
        
        v2rayJSONFile["stats"] = self.getStats()
        if not v2rayJSONFile["stats"]:
            del v2rayJSONFile["stats"]

        __v2rayJSONFile = copy.deepcopy(v2rayJSONFile)
        del v2rayJSONFile
        
        return __v2rayJSONFile
