#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        DataMgr.py
#
# Purpose:     Data manager module used to control all the other data processing 
#              modules and store the interprocess/result data.
#
# Author:      Yuancheng Liu
#
# Created:     2022/04/16
# Version:     v_0.1
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------
import os 
import time
from fnmatch import fnmatch
import threading

import CASimulatorGlobal as gv

LOOP_T = 0.5 # Thread loop time interval

class Stage(object):
    def __init__(self, name, pos, link, bgImg) -> None:
        self.name = name
        self.pos = pos
        self.link = link
        self.bgImg = bgImg
        self.activeFg = False
        self.stageProgress = 0

    def actStage(self, actFlag):
        self.activeFg = actFlag
        self.stageProgress  = 1 if self.activeFg else 0

    def updateStage(self, pct=2):
        self.stageProgress = min(self.stageProgress+pct, 10)

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataMgr(object):
    """ Manager object used to process and store the data.""" 
    def __init__(self) -> None:
        super().__init__()

        self.rtn_addiontal = False
        parm = gv.gStageDict['report']
        self.report = Stage('report', parm['pos'], parm['link'], parm['bg'])
        self.report.actStage(True)

        parm = gv.gStageDict['analysis']
        self.analysis = Stage('analysis', parm['pos'], parm['link'], parm['bg'])

        parm = gv.gStageDict['artifactDe']
        self.artifactDe = Stage('AartifactDe', parm['pos'], parm['link'], parm['bg'])

        parm = gv.gStageDict['artifactRe']
        self.artifactRe = Stage('artifactRe', parm['pos'], parm['link'], parm['bg'])

        parm = gv.gStageDict['aptEvnts']
        self.aptEvnts = Stage('aptEvnts', parm['pos'], parm['link'], parm['bg'])
        self.aptEvnts.actStage(False)


        parm = gv.gStageDict['mitreTTPs']
        self.mitreTTPs = Stage('mitreTTPs', parm['pos'], parm['link'], parm['bg'])

        parm = gv.gStageDict['components']
        self.components = Stage('components', parm['pos'], parm['link'], parm['bg'])
        
        parm = gv.gStageDict['proDec']
        self.proDec = Stage('proDec', parm['pos'], parm['link'], parm['bg'])

        parm = gv.gStageDict['screenPlay']
        self.screenPlay = Stage('screenPlay', parm['pos'], parm['link'], parm['bg'])

        parm = gv.gStageDict['testBed']
        self.testBed = Stage('testBed', parm['pos'], parm['link'], parm['bg'])
        
        if 'testActionLayerModule' in gv.gStageDict.keys():
            parm = gv.gStageDict['testActionLayerModule']
            self.testModule = Stage('testActionLayerModule', parm['pos'], parm['link'], parm['bg'])
            self.rtn_addiontal = True


    def getStagesList(self):
        if self.rtn_addiontal:
            return [self.report ,self.analysis, self.artifactDe, self.artifactRe,  
                    self.aptEvnts, self.mitreTTPs, self.components,
                    self.proDec, self.screenPlay, self.testBed,  self.testModule]

        return [self.report ,self.analysis, self.artifactDe, self.artifactRe,  
                    self.aptEvnts, self.mitreTTPs, self.components,
                    self.proDec, self.screenPlay, self.testBed]

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataMgr2(object):
    """ Manager object used to process and store the data.""" 
    def __init__(self) -> None:
        super().__init__()
        self.parser = pp.PacketParser()
        self.checker = pc.ProtocoCheker(gv.PRO_SCORE_REF)
        self.proList = {}
        self.proSumDict = {}
        self.soreRst = {}

#-----------------------------------------------------------------------------
    def calCommSumDict(self):
        """ Calculate the protocol summery dictionary."""
        self.proSumDict = {}
        for item in self.proList:
            keyVal =  item[gv.SRC_TAG]+'-'+item[gv.DES_TAG]  
            if not (keyVal in self.proSumDict.keys()):
                self.proSumDict[keyVal] = pp.protcolRcdDict(item[gv.SRC_TAG], item[gv.DES_TAG])
            self.proSumDict[keyVal].addRecord(item)

#-----------------------------------------------------------------------------
    def calQSScore(self):
        """ Calculate the QS score based on the current stored data set."""
        self.soreRst = {}
        for key, item in self.proSumDict.items():
            value = self.checker.matchScore(item.encriptDict)
            self.soreRst[key] = value

#-----------------------------------------------------------------------------
    def loadFile(self, filePath):
        """ Load data from the packet capture file.
            Args:
                filePath ([str]): cap file path.
        """
        typeCheck = fnmatch(filePath, '*.cap') or fnmatch(filePath, '*.pcap') or fnmatch(filePath, '*.pcapng')
        if os.path.exists(filePath) and typeCheck:
            self.parser.loadCapFile(filePath)
            self.proList = self.parser.getProtocalList()
            return True
        print(">> Error: file not exist or type not valid !")
        return False

#-----------------------------------------------------------------------------
    def loadNetLive(self, interfaceName, packetCount=10):
        self.parser.loadNetLive(interfaceName, packetCount=packetCount)
        self.proList = self.parser.getProtocalList()
        return True

#-----------------------------------------------------------------------------
    def getProtocalDict(self):
        return self.proSumDict

    def getScoreDict(self):
        return self.soreRst

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class DataMgrPT(threading.Thread):
    """ A Package class used to run the data manager in a thread parallel with 
        other thread. (PT for parallel threading)
    """
    def __init__(self, threadID, name, debugMD=False):
        threading.Thread.__init__(self)
        self.dataMgr = DataMgr()
        self.debugMD = debugMD
        self.fileNeedLoad = None    # Packet file path
        self.interfaceNeedLoad = None   # network interface name 
        self.interfacePacktNum = 30     # default interface capture loop number.
        self.updateFlag = False
        self.terminate = False
        
    #-----------------------------------------------------------------------------
    def loadFile(self, filePath):
        self.fileNeedLoad = filePath
        self.interfaceNeedLoad = None
        self.updateFlag = True
        return True
    
    #-----------------------------------------------------------------------------
    def loadNetLive(self, interfaceName, packetCount):
        self.interfaceNeedLoad = interfaceName
        self.interfacePacktNum = packetCount
        self.fileNeedLoad = False
        self.updateFlag = True
        return True

    #-----------------------------------------------------------------------------
    def run(self):
        while not self.terminate:
            if self.updateFlag:
                if self.debugMD: print(">> Load the data:")
                if self.fileNeedLoad:
                    print("From File %s" %str(self.fileNeedLoad))
                    self.dataMgr.loadFile(self.fileNeedLoad)
                    self.fileNeedLoad = None
                
                if self.interfaceNeedLoad:
                    print('From Network Interface: %s' %str(self.interfaceNeedLoad))
                    self.dataMgr.loadNetLive(self.interfaceNeedLoad, self.interfacePacktNum)
                    self.interfaceNeedLoad = None

                self.dataMgr.calCommSumDict()
                self.dataMgr.calQSScore()
                self.updateFlag = False
            time.sleep(LOOP_T)
        print("DataMangerPT thread stoped!")

    #-----------------------------------------------------------------------------
    def getProtocalDict(self):
        if self.updateFlag: return None
        return self.dataMgr.getProtocalDict()

    def getScoreDict(self):
        if self.updateFlag: return None
        return self.dataMgr.getScoreDict()
    
    def checkUpdating(self):
        return self.updateFlag 

    #-----------------------------------------------------------------------------
    def stop(self):
        """ Stop the thread."""
        self.terminate = True

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def testCase(mode=0):
    if mode == 0:
        print("> Start test: Init datamanager ")
        dataMgr = DataMgr()
        r1 = dataMgr.loadFile('FILE_NOT_EXIST!')
        r2 = dataMgr.loadFile('capData/test_normal.pcapng')
        result = 'Pass' if (not r1) and r2 else 'Fail'
        print(">> Test load file: %s" %result)

        dataMgr.calCommSumDict()
        print('>> calculate the protocol summery : ')
        print(dataMgr.getProtocalDict())

        dataMgr.calQSScore()
        print('>> calculate the quantum safe score : ')
        print(dataMgr.getScoreDict())
        dataMgr = None 

        print("\n> Test parallel thread data manager.")

        dataMgrMT = DataMgrPT(1, 'Test MultiThread')
        dataMgrMT.start()
        dataMgrMT.loadFile('capData/test_normal.pcapng')

        while dataMgrMT.checkUpdating():
            time.sleep(0.5)
        
        print('>> print the protocol summery : ')
        print(dataMgrMT.getProtocalDict())

        print('>> print the quantum safe score : ')
        print(dataMgrMT.getScoreDict())

        dataMgrMT.stop()
    if mode == 1: 
        print("> Start test: load from Wifi network interface ")
        dataMgrMT = DataMgrPT(1, 'Test MultiThread')
        dataMgrMT.start()
        dataMgrMT.loadNetLive('Wi-Fi', 50)
        while dataMgrMT.checkUpdating():
            time.sleep(0.5)
        
        print('>> print the protocol summery : ')
        print(dataMgrMT.getProtocalDict())

        print('>> print the quantum safe score : ')
        print(dataMgrMT.getScoreDict())
        dataMgrMT.stop()

    else:
        print('>> Put your own test code here:')
        
if __name__ == '__main__':
    #testCase()
    testCase(mode=1)

