#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiPanel.py
#
# Purpose:     This module is used to create different function panels.
# Author:      Yuancheng Liu
#
# Created:     2022/03/12
# Copyright:   2022 @ National Cybersecurity R&D Laboratories (https://ncl.sg/)
# License:     
#-----------------------------------------------------------------------------
import wx
from wx.adv import Animation, AnimationCtrl
from math import atan2, sin, cos, pi


from datetime import datetime
import CASimulatorGlobal as gv

class stage(object):

    def __init__(self, name, pos) -> None:
        pass 
        


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelImge(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, panelSize=(1100, 700)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)
        self.fileState = 0

        self.stageParm = [
            {'name': 'report', 'pos': (150, 150), 'link':(0,4), 'Act': True, 'bg': 'img/rpt_load_img_120.png'}, 
            {'name': 'analysis', 'pos': (350, 150), 'link':(4,6), 'Act': False, 'bg': 'img/analys_120.png'},
            {'name': 'ArtifDe', 'pos': (550, 150), 'link':(0,4), 'Act': True, 'bg': 'img/artifectDe.png'},
            {'name': 'ArtifRe', 'pos': (750, 150), 'link':(0,6), 'Act': True, 'bg': 'img/artiFecRe.png'},

            {'name': 'AptEvnt', 'pos': (350, 350), 'link':(0, 6), 'Act': True, 'bg': 'img/aptEvent.png'},
            {'name': 'Mitre', 'pos': (550, 350), 'link':(1, 3), 'Act': True, 'bg': 'img/mitreTtps.png'},
            {'name': 'Components', 'pos': (750, 350), 'link':(0, 6), 'Act': True, 'bg': 'img/components.png'},
            
            {'name': 'ProDec', 'pos': (350, 550), 'link':(0, 4), 'Act': False, 'bg': 'img/ProDec.png'},
            {'name': 'ScreenPlay', 'pos': (550, 550), 'link':(0, 4), 'Act': True, 'bg': 'img/screenplay.png'},
            {'name': 'Testbed', 'pos': (750, 550), 'link':(0, ), 'Act': False, 'bg': 'img/testBed.png'},
        ]
        self.stageProgress = {
            'report': 0,
            'analysis': 0, 
            'ArtifDe': 0,
            'ArtifRe': 0,
            'AptEvnt': 0, 
            'Mitre': 0,
            'Components': 0, 
            'ProDec': 0, 
            'ScreenPlay': 0, 
            'Testbed':0,
        }

        self.btlist = {}
        self.pblist = {}
        self.progress = [0]*10
        self.buildStateBts()
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def buildStateBts(self):
        startPt = (150, 150)
        stateSz = (120, 120)
        dis = 200
        self.btlist = {}
        for stage in self.stageParm:
            pt = stage['pos']
            button = wx.BitmapButton(self, -1, 
                                wx.Bitmap(stage['bg'], wx.BITMAP_TYPE_ANY), 
                                pos=(pt[0] - 60, pt[1] -60),
                                size=(120, 120))
            if not stage['Act']:button.Disable()
            if stage['name'] == 'report': button.Bind(wx.EVT_LEFT_DOWN, self.onFileSelect)
            if stage['name'] == 'analysis': button.Bind(wx.EVT_LEFT_DOWN, self.onAnalyseSelection)
            if stage['name'] == 'AptEvnt': button.Bind(wx.EVT_LEFT_DOWN, self.aptEventSelection)

            gauge = wx.Gauge(self, range = 10, pos=(pt[0] - 70, pt[1] + 62), size = (140, 10), style = wx.GA_HORIZONTAL)
            gauge.SetValue(1)
            if self.stageProgress[stage['name']] == 0:
                gauge.Hide()

            self.btlist[stage['name']] = button
            self.pblist[stage['name']] = gauge
            #btlist.append(button)
        
    
        # self.button_pointer = wx.BitmapButton(self, -1, 
        #                             wx.Bitmap("img/rpt_load_img_120.png", wx.BITMAP_TYPE_ANY), 
        #                             pos=(self.centerPtList[0][0] -60, self.centerPtList[0][1] -60), 
        #                             size=(120, 120))
        # self.button_pointer.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)

               # create wx.Bitmap object 
        #bmp = wx.Bitmap('img/rpt_load_img_120.png')
  
        # create button at point (20, 20)
        #self.button_pointer = wx.Button(self, id = 1, label ="Button", pos=(startPt[0]- 60, startPt[1]-60), 
        #                                size=(120, 120),  name ="button")
          
        # set bmp as bitmap for button
        #self.button_pointer.SetBitmap(bmp)

        # btlist = []
        # for pt in self.centerPtList:
        #     if pt[0] == 150: continue
        #     button = wx.BitmapButton(self, -1, 
        #                         wx.Bitmap("img/placeHoderImg.png", wx.BITMAP_TYPE_ANY), 
        #                         pos=(pt[0] - 60, pt[1] -60),
        #                         size=(120, 120))
        #     btlist.append(button)


    def onFileSelect(self, event):
        openFileDialog = wx.FileDialog(self, "Open", gv.dirpath, "", 
                "CTI report Files (*.pdf;*.doc;*.ppt)|*.pdf;*.PDF;*.doc", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = str(openFileDialog.GetPath())
        name = str(openFileDialog.GetName())
        print('file name: %s' %str(name))
        gv.iRptFnameList.append(path)

        openFileDialog.Destroy()
        self.stageProgress['report'] = 2


    def onAnalyseSelection(self, event):
        self.infoWindow = wx.MiniFrame(gv.iMainFrame, -1,
            'CTI report analysis config', pos=(300, 300), size=(480, 600),
            style=wx.DEFAULT_FRAME_STYLE)
        analysPnel = CTIAnalysisConfiPnl(self.infoWindow, 0)
        self.infoWindow.Bind(wx.EVT_CLOSE, self.infoWinClose)
        self.infoWindow.Show()
        #analysPnel.setPlay(True)

    def aptEventSelection(self,event):
        self.infoWindow = wx.MiniFrame(gv.iMainFrame, -1,
            'APT event dashboard', pos=(300, 300), size=(1060, 470),
            style=wx.DEFAULT_FRAME_STYLE)
        analysPnel = CTIAnalysisConfiPnl2(self.infoWindow, 0)
        self.infoWindow.Bind(wx.EVT_CLOSE, self.infoWinClose)
        self.infoWindow.Show()

#--PanelMap--------------------------------------------------------------------
    def infoWinClose(self, event):
        """ Close/Destroy the pop-up detail information window."""
        if self.infoWindow:
            self.infoWindow.Destroy()

#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        #dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        dc.SetPen(wx.Pen('RED'))
        dc.DrawText('This is a sample image', w//2, h//2)
        dc.SetBrush(wx.Brush(wx.Colour(60, 60, 60)))
        dc.DrawRectangle(0, 0, 1000, 800)


        for stage in self.stageParm:
            pt = stage['pos']
            #print(stage['link'])
            for i in stage['link']:
                if i == 4:
                    if stage['name']== 'report' and self.fileState == 2:
                        self.DrawArrowLine(dc, pt[0], pt[1], pt[0]+130, pt[1], color=wx.Colour('Green'))
                    else:
                        self.DrawArrowLine(dc, pt[0], pt[1], pt[0]+130, pt[1])

                if i == 6:
                    self.DrawArrowLine(dc, pt[0], pt[1], pt[0], pt[1]+130)

                if i == 1:
                    self.DrawArrowLine(dc, pt[0], pt[1], pt[0]-130, pt[1]-130)

                if i == 3:
                    self.DrawArrowLine(dc, pt[0], pt[1], pt[0]+130, pt[1]-130)
            
            dc.SetPen(wx.Pen('Gray'))
            dc.SetBrush(wx.Brush(wx.Colour(200, 210, 200)))
            dc.DrawRectangle(pt[0] - 70, pt[1] - 70, 140, 140)

        if self.fileState == 1:
            dc.SetPen(wx.Pen('Green'))
            dc.SetTextForeground(wx.Colour('Green'))
            dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            #pos = self.stageParm['report']['pos']
            dc.DrawText('Verifying CTI file ...', 80, 60)
        elif self.fileState == 2:
            dc.SetPen(wx.Pen('White'))
            dc.SetTextForeground(wx.Colour('White'))
            dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            #pos = self.stageParm['report']['pos']
            dc.DrawText('CTI report file ready.', 80, 60)
        else:
            dc.SetTextForeground(wx.Colour('White'))
            dc.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            #pos = self.stageParm['report']['pos']
            dc.DrawText('Click this button to load CTI report file', 80, 60)

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        #image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = bitmap.ConvertToImage()
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        #result = wx.BitmapFromImage(image) # used below 2.7
        result = wx.Bitmap(image, depth=wx.BITMAP_SCREEN_DEPTH)
        return result

#--PanelImge--------------------------------------------------------------------
    def _scaleBitmap2(self, bitmap, width, height):
        """ Resize a input bitmap.(bitmap-> image -> resize image -> bitmap)"""
        image = wx.ImageFromBitmap(bitmap) # used below 2.7
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image) # used below 2.7
        return result

#--PanelImge--------------------------------------------------------------------
    def updateBitmap(self, bitMap):
        """ Update the panel bitmap image."""
        if not bitMap: return
        self.bmp = bitMap

#--PanelMap--------------------------------------------------------------------
    def updateDisplay(self, updateFlag=None):
        """ Set/Update the display: if called as updateDisplay() the function will 
            update the panel, if called as updateDisplay(updateFlag=?) the function
            will set the self update flag.
        """
        self.Refresh(False)
        self.Update()

    def updateStage(self):
        for key, value in self.stageProgress.items():
            if value == 2:
                self.pblist[key].Show()
                self.fileState = 1
                self.updateDisplay()
            if 0< value < 10: 
                self.stageProgress[key] += 2
                self.pblist[key].SetValue(self.stageProgress[key])
            
            if self.stageProgress['report'] == 10:
                self.btlist['analysis'].Enable()
                self.fileState = 2
                self.updateDisplay()

            

    def DrawArrowLine( self, dc, x0, y0, x1, y1, arrowFrom=True, arrowTo=True, arrowLength=16, arrowWidth=8, color= wx.Colour(0, 0, 0)):
        '''
            Draws a line with arrows in a regular wxPython DC.
            The line is drawn with the dc's wx.Pen.  The arrows are filled with the current Pen's colour.
            Edward Sitarski 2021.
        '''

        # Set up the dc for drawing the arrows.
        penSave, brushSave = dc.GetPen(), dc.GetBrush()
        #dc.SetPen( wx.TRANSPARENT_PEN )
        dc.SetPen(wx.Pen(color, 2))
        dc.SetBrush( wx.Brush(color))

        dc.DrawLine( x0, y0, x1, y1 )
        if x0 == x1 and y0 == y1:
            return
        

        
        # Compute the "to" arrow polygon.
        angle = atan2( y1 - y0, x1 - x0 )
        toCosAngle, toSinAngle = -cos(angle), -sin(angle)
        toArrowPoly = [
            (int(xp*toCosAngle - yp*toSinAngle), int(yp*toCosAngle + xp*toSinAngle)) for xp, yp in (
                (0,0),
                (arrowLength, arrowWidth/2),
                (arrowLength, -arrowWidth/2),
            )
        ]
        
        # Draw the arrows.
        if arrowTo:
            dc.DrawPolygon( toArrowPoly, x1, y1 )
        #if arrowFrom:
        #    dc.DrawPolygon( [(-x,-y) for x,y in toArrowPoly], x0, y0 )
        
        # Restore the dc.
        dc.SetPen( penSave )
        dc.SetBrush( brushSave )

class CTIAnalysisConfiPnl2(wx.Panel):
    def __init__(self, parent, idx, size=(280, 200), style=wx.TRANSPARENT_WINDOW):
        """ Panel to simulate the camera view."""
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        flagL = wx.LEFT
        self.bitmap1 = wx.StaticBitmap(
            self, -1, wx.Image("img/event.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        sizer.Add(self.bitmap1, flag=flagL, border=2)
        self.SetSizerAndFit(sizer)
        self.Show()


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class CTIAnalysisConfiPnl(wx.Panel):
    """ CTI report analysis config setting panel"""
    def __init__(self, parent, idx, size=(280, 200), style=wx.TRANSPARENT_WINDOW):
        """ Panel to simulate the camera view."""
        wx.Panel.__init__(self, parent)
        self.SetSizerAndFit(self._buildUISizer())
        self.Show()

    def _buildUISizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        flagL = wx.LEFT
        self.bitmap1 = wx.StaticBitmap(
            self, -1, wx.Image(gv.ANA_TITLE_PATH, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        sizer.Add(self.bitmap1, flag=flagL, border=2)
        sizer.AddSpacer(5)

        sizer.Add(wx.StaticText(
            self, label="CTI Report Analysis Configuration"), flag=flagL, border=2)
        sizer.AddSpacer(10)

        sizer.Add(wx.StaticText(
            self, label="CTI Report File Selection: "), flag=flagL, border=2)
        sizer.AddSpacer(2)
        self.fileSelectCB = wx.ComboBox(
            self, -1, choices=gv.iRptFnameList, style=wx.CB_READONLY, size=(400, 25))
        self.fileSelectCB.SetSelection(0)
        sizer.Add(self.fileSelectCB, flag=flagL, border=2)
        sizer.AddSpacer(10)

        sizer.Add(wx.StaticText(
            self, label="CTI Report Analysis Algo:"), flag=flagL, border=2)
        sizer.AddSpacer(2)
        self.algoCB1 = wx.CheckBox(self, -1, 'Natural Language Processing (NLP)')
        sizer.Add(self.algoCB1, flag=flagL, border=2)
        self.algoCB1.SetValue(True)
        sizer.AddSpacer(2)
        self.algoCB2 = wx.CheckBox(self, -1, 'Domain-specific graph alignment algorithm')
        sizer.Add(self.algoCB2, flag=flagL, border=2)
        self.algoCB2.SetValue(True)
        sizer.AddSpacer(2)
        self.algoCB3 = wx.CheckBox(self, -1, '[ Placeholder for other algorithm ] ')
        sizer.Add(self.algoCB3, flag=flagL, border=2)
        sizer.AddSpacer(10)

        sizer.Add(wx.StaticText(
            self, label="CTI Report Analysis Output result:"), flag=flagL, border=2)
        sizer.AddSpacer(2)
        self.rstCB1 = wx.CheckBox(self, -1, 'Artifact Description')
        self.rstCB1.SetValue(True)
        sizer.Add(self.rstCB1, flag=flagL, border=2)
        sizer.AddSpacer(2)
        self.rstCB2 = wx.CheckBox(self, -1, 'APT Event')
        self.rstCB2.SetValue(True)
        sizer.Add(self.rstCB2, flag=flagL, border=2)
        sizer.AddSpacer(10)

        self.animCtrl = AnimationCtrl(self, -1, Animation(gv.ANA_PROCE_PATH))
        self.animCtrl.Stop() # stop the gif play first.
        sizer.Add(self.animCtrl, flag=wx.LEFT, border=2)
        self.button_pointer = wx.Button(self, id = 1, label ="Start",   name ="button")
        sizer.Add(self.button_pointer, flag=wx.LEFT, border=2)
        self.button_pointer.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)

        sizer.Add(wx.StaticText(
            self, label="Progress Log:"), flag=flagL, border=2)
        sizer.AddSpacer(10)
        self.detailTC = wx.TextCtrl(
            self, size=(500, 300), style=wx.TE_MULTILINE)
        sizer.Add(self.detailTC, flag=flagL, border=2)
    
        return sizer

#-----------------------------------------------------------------------------
    def mouseDown(self, event):
        self.setPlay(True)
        self.detailTC.AppendText("Starting analysis the report .... \n")
        self.detailTC.AppendText("Parsing the report .... \n")
        self.detailTC.AppendText("Pass the report in algo module: \n [Natural Language Processing (NLP)].... \n")

#-----------------------------------------------------------------------------
    def setPlay(self, plagFlag):
        """ Set the gif play or stop"""
        if plagFlag:
            self.animCtrl.Play()
        else:
            self.animCtrl.Stop()

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelCtrl(wx.Panel):
    """ Function control panel."""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.gpsPos = None
        self.SetSizer(self._buidUISizer())

#--PanelCtrl-------------------------------------------------------------------
    def _buidUISizer(self):
        """ build the control panel sizer. """
        flagsR = wx.CENTER
        ctSizer = wx.BoxSizer(wx.VERTICAL)
        hbox0 = wx.BoxSizer(wx.HORIZONTAL)
        ctSizer.AddSpacer(5)
        # Row idx 0: show the search key and map zoom in level.
        hbox0.Add(wx.StaticText(self, label="Control panel".ljust(15)),
                  flag=flagsR, border=2)
        ctSizer.Add(hbox0, flag=flagsR, border=2)
        return ctSizer

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    """ Main function used for local test debug panel. """

    print('Test Case start: type in the panel you want to check:')
    print('0 - PanelImge')
    print('1 - PanelCtrl')
    #pyin = str(input()).rstrip('\n')
    #testPanelIdx = int(pyin)
    testPanelIdx = 1    # change this parameter for you to test.
    print("[%s]" %str(testPanelIdx))
    app = wx.App()
    mainFrame = wx.Frame(gv.iMainFrame, -1, 'Debug Panel',
                         pos=(300, 300), size=(640, 480), style=wx.DEFAULT_FRAME_STYLE)
    if testPanelIdx == 0:
        testPanel = PanelImge(mainFrame)
    elif testPanelIdx == 1:
        testPanel = PanelCtrl(mainFrame)
    mainFrame.Show()
    app.MainLoop()

if __name__ == "__main__":
    main()



