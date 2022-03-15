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

#------<IMAGES PATH>-------------------------------------------------------------
IMG_FD = 'img'
ICO_PATH = os.path.join(dirpath, IMG_FD, "geoIcon.ico")
BGIMG_PATH = os.path.join(dirpath, IMG_FD, "SampleImg.png")

#-------<GLOBAL VARIABLES (start with "g")>------------------------------------
# VARIABLES are the built in data type.
gTranspPct = 100     # Windows transparent percentage.
gUpdateRate = 1     # main frame update rate 1 sec.


#-------<GLOBAL PARAMTERS>-----------------------------------------------------
iMainFrame = None   # MainFrame.
iImagePanel = None  # Image panel.
iCtrlPanel = None   # control panel
iRptFnameList = ['CTI_test_file.pdf' ]  # CTI file name list
