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
from math import atan2, sin, cos, pi


from datetime import datetime
import uiGobal as gv

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class PanelImge(wx.Panel):
    """ Panel to display image. """

    def __init__(self, parent, panelSize=(1100, 700)):
        wx.Panel.__init__(self, parent, size=panelSize)
        self.SetBackgroundColour(wx.Colour(200, 200, 200))
        self.panelSize = panelSize
        self.bmp = wx.Bitmap(gv.BGIMG_PATH, wx.BITMAP_TYPE_ANY)


        self.buildStateBts()
        
        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.SetDoubleBuffered(True)

    def buildStateBts(self):
        startPt = (150, 150)
        stateSz = (120, 120)
        dis = 200
        self.button_pointer = wx.BitmapButton(self, -1, 
                                    wx.Bitmap("img/rpt_load_img_120.png", wx.BITMAP_TYPE_ANY), 
                                    pos=(startPt[0]- 60, startPt[1]-60), 
                                    size=(120, 120))
        self.button_pointer.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)

        btlist = []
        for i in range(3):
            vPos = startPt[1] + dis*i
            for j in range(3):
                hPos = startPt[0] + 200*(1+j)
                button = wx.BitmapButton(self, -1, 
                                    wx.Bitmap("img/placeHoderImg.png", wx.BITMAP_TYPE_ANY), 
                                    pos=(hPos- 60, vPos-60), 
                                    size=(120, 120))
                btlist.append(button)





    def mouseDown(self, event):
        pic = wx.Bitmap("img/rpt_load_img_120G.png", wx.BITMAP_TYPE_ANY)
        self.button_pointer.SetBitmap(pic)
        self.button_pointer.Disable()


#--PanelImge--------------------------------------------------------------------
    def onPaint(self, evt):
        """ Draw the map on the panel."""
        dc = wx.PaintDC(self)
        w, h = self.panelSize
        #dc.DrawBitmap(self._scaleBitmap(self.bmp, w, h), 0, 0)
        dc.SetPen(wx.Pen('RED'))
        dc.DrawText('This is a sample image', w//2, h//2)
        dc.SetBrush(wx.Brush(wx.Colour(200, 200, 200)))
        dc.DrawRectangle(0, 0, 1000, 800)

        self.DrawArrowLine(dc , 0, 0 , 50, 50)


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



