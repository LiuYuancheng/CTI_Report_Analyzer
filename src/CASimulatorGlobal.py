#-----------------------------------------------------------------------------
# Name:        uiGlobal.py
#
# Purpose:     This module is used as a local config file to set constants, 
#              global parameters which will be used in the other modules.
#              
# Author:      Yuancheng Liu
#
# Created:     2022/03/14
# Copyright:   2022 @ National Cybersecurity R&D Laboratories (https://ncl.sg/)
# License:     
#-----------------------------------------------------------------------------
import os

print("Current working directory is : %s" % os.getcwd())
dirpath = os.path.dirname(__file__)
print("Current source code location : %s" % dirpath)
APP_NAME = 'CTI_Report_Analyzer_SimulaterUI [Ver:0.1]'
APP_WIN_SIZE = (1050, 750)

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico")
BGIMG_PATH = os.path.join(dirpath, IMG_FD, "SampleImg.png")

ANA_TITLE_PATH = os.path.join(dirpath, IMG_FD, 'analysis', 'analysisBg3.jpg')
ANA_PROCE_PATH = os.path.join(dirpath, IMG_FD, 'analysis', 'search_100.gif')



#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gTranspPct = 100     # Windows transparent percentage.
gUpdateRate = 1     # main frame update rate 1 sec.
gStageDict = {
    'report': {
        'pos': (150, 150), 'link': (0, 4),
        'bg': os.path.join(dirpath, IMG_FD, 'report', "rpt_load_img_120.png")
    },  # CTI report load.
    'analysis': {
        'pos': (350, 150), 'link': (4, 6),
        'bg': os.path.join(dirpath, IMG_FD, 'analysis', "analysis_img_120.png")
    },  # CTI analysis
    'artifactDe': {
        'pos': (550, 150), 'link': (0, 4),
        'bg': os.path.join(dirpath, IMG_FD, 'artifactDe', "artifactDe_img_120.png")
    },  # Artifact description
    'artifactRe': {
        'pos': (750, 150), 'link': (0, 6),
        'bg': os.path.join(dirpath, IMG_FD, 'artifactRe', "artifactRe_img_120.png")
    },  # Artifact reconstruction

    'aptEvnts': {
        'pos': (350, 350), 'link': (0, 6),
        'bg': os.path.join(dirpath, IMG_FD, 'aptEvnts', "aptEvnts_img_120.png")
    },  # Apt events.

    'mitreTTPs': {
        'pos': (550, 350), 'link': (1, 3),
        'bg': os.path.join(dirpath, IMG_FD, 'mitreTTPs', "mitreTTPs_img_120.png")
    },  # MitreTTPs control.

    'components': {
        'pos': (750, 350), 'link': (0, 6),
        'bg': os.path.join(dirpath, IMG_FD, 'components', "components_img_120.png")
    },  # Components.

    'proDec': {
        'pos': (350, 550), 'link': (0, 4),
        'bg': os.path.join(dirpath, IMG_FD, 'proDec', "proDec_img_120.png")
    },  # Procedure description.

    'screenPlay': {
        'pos': (550, 550), 'link': (0, 4),
        'bg': os.path.join(dirpath, IMG_FD, 'screenPlay', "screenPlay_img_120.png")
    },  # Screen play.
    'testBed': {
        'pos': (750, 550), 'link': (0, ),
        'bg': os.path.join(dirpath, IMG_FD, 'testBed', "testBed_img_120.png")
    },  # Test bed automation 

    # 'testActionLayerModule': {
    #     'pos': (50, 550), 'link': (0, ),
    #     'bg': os.path.join(dirpath, IMG_FD , "placeHoderImg.png")
    # },  # Test add new action module in the action handling layer


}


#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # MainFrame.
iImagePanel = None  # Image panel.
iCtrlPanel = None   # control panel
idataMgr = None     # dataMgr
iRptFnameList = ['CTI_test_file.pdf' ]  # CTI file name list
