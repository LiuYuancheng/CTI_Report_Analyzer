#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        uiPanel.py
#
# Purpose:     This module is used to create different function panels.
# Author:      Yuancheng Liu
#
# Created:     2020/01/10
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------
import wx
from wx.adv import Animation, AnimationCtrl
from math import atan2, sin, cos, pi


from datetime import datetime
import uiGobal as gv

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
            if stage['name'] == 'report': button.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)
            if stage['name'] == 'analysis': button.Bind(wx.EVT_LEFT_DOWN, self.onAnalyseSelection)


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


    def mouseDown(self, event):
        #pic = wx.Bitmap("img/rpt_load_img_120G.png", wx.BITMAP_TYPE_ANY)
        #self.button_pointer.SetBitmap(pic)
        #self.button_pointer.Disable()
        openFileDialog = wx.FileDialog(self, "Open", gv.dirpath, "", 
                "CTI report Files (*.pdf;*.doc;*.ppt)|*.pdf;*.PDF;*.doc", 
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = str(openFileDialog.GetPath())
        openFileDialog.Destroy()
        #self.scValTC.SetValue(path)
        self.srcType = 'file'

        self.stageProgress['report'] = 2

        #self.btlist['analysis'].Enable()

    def onAnalyseSelection(self, event):
        self.infoWindow = wx.MiniFrame(gv.iMainFrame, -1,
            'Monitoring Camera View', pos=(300, 300), size=(300, 230),
            style=wx.DEFAULT_FRAME_STYLE)
        analysPnel = AnalysisSelection(self.infoWindow, 0)
        self.infoWindow.Bind(wx.EVT_CLOSE, self.infoWinClose)
        self.infoWindow.Show()
        #analysPnel.setPlay(True)


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
        dc.SetBrush(wx.Brush(wx.Colour(150, 150, 150)))
        dc.DrawRectangle(0, 0, 1000, 800)


        for stage in self.stageParm:
            pt = stage['pos']
            #print(stage['link'])
            for i in stage['link']:
                if i == 4:
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
            if 0< value < 10: 
                self.stageProgress[key] += 2
                self.pblist[key].SetValue(self.stageProgress[key])
            
            if self.stageProgress['report'] == 10:
                self.btlist['analysis'].Enable()

            

    def DrawArrowLine( self, dc, x0, y0, x1, y1, arrowFrom=True, arrowTo=True, arrowLength=16, arrowWidth=8 ):
        '''
            Draws a line with arrows in a regular wxPython DC.
            The line is drawn with the dc's wx.Pen.  The arrows are filled with the current Pen's colour.
            Edward Sitarski 2021.
        '''

        # Set up the dc for drawing the arrows.
        penSave, brushSave = dc.GetPen(), dc.GetBrush()
        #dc.SetPen( wx.TRANSPARENT_PEN )
        dc.SetPen(wx.Pen(wx.Colour(0, 0, 0), 2))
        dc.SetBrush( wx.Brush(wx.Colour(0, 0, 0)))

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



#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class AnalysisSelection(wx.Panel):
    """ Panel play a gif image to simulation the camera view when train pass."""
    def __init__(self, parent, idx, size=(280, 200), style=wx.TRANSPARENT_WINDOW):
        """ Panel to simulate the camera view."""
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(
            self, label="CTI report analysis configuration:"), flag=wx.LEFT, border=2)
        self.attackCtrl = wx.ComboBox(
            self, -1, choices=['file_name1.pdf', 'file_name2.pdf'], style=wx.CB_READONLY)
        
        self.attackCtrl.SetSelection(0)
        sizer.AddSpacer(5)
        sizer.Add(self.attackCtrl, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)
        sizer.Add(wx.StaticText(
            self, label="CTI report analysis Algo:"), flag=wx.LEFT, border=2)
        self.simuCb3 = wx.CheckBox(self, -1, 'Natural Language Processing (NLP)')
        sizer.Add(self.simuCb3, flag=wx.LEFT, border=2)
        sizer.AddSpacer(5)

        self.simuCb4 = wx.CheckBox(self, -1, 'domain-specific graph alignment algorithm')
        sizer.Add(self.simuCb4, flag=wx.LEFT, border=2)



        self.animCtrl = AnimationCtrl(self, -1, Animation('img/search_100.gif'))
        self.animCtrl.Stop() # stop the gif play first.
        sizer.Add(self.animCtrl, flag=wx.LEFT, border=2)

        self.button_pointer = wx.Button(self, id = 1, label ="Start",   name ="button")
        sizer.Add(self.button_pointer, flag=wx.LEFT, border=2)
        self.button_pointer.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)
        self.SetSizerAndFit(sizer)
        self.Show()


    def mouseDown(self, event):
        self.setPlay(True)

#--PanelCameraView-------------------------------------------------------------
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



