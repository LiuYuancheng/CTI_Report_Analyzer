# -----------------------------------------------------------------------------
# Name:        CascadeSlider.py
# Purpose:  This function is used to create the horizontal slider for the rudder
#           control and the vertical slider for the throttle control
#
# Author:   Liu Yuancheng
#
# Created:     2016/01/12
# Copyright:   
# License:    
# -----------------------------------------------------------------------------
"""Copyright 2016-2018 ZycraftUSV Pte. Ltd."""
import wx
import numpy as np

OFFSET_OVER_ADJ = 12        # offset this much more than the adjusting button size
OFFSET_OVER_ADJ_DOUBLE = OFFSET_OVER_ADJ * 2
HORIZ_Y_OFFSET = 6          # offset for drawing thumbs on horiz ctl
VERT_X_OFFSET = 2           # offset for drawing thumbs on vert ctl

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Control_Slider_edit(wx.Panel):
    """ Create a slider with the control thumb and feed back indicator for the rudder
    and throttle control.

        Inport: (parent, idStr, minValue, maxValue) are same parameters as <wx.Slider>
                idStr: identification string: 'rudder', 'throttle1', etc.
                value: A list of the init value of thumb&indicators.
                size: (Size of the whole slider, Size of the thumb)
                direction(str): Same as the type in <wx.Slider>
                valInverse: True - Descending sort of the scale, False- ascending
                    sort of the scale
                label: (label_of_the_tool_tips, (label_of_the_forward_button,
                    label_of_the_backward_button))
                thumbDisplay: True - Show text on the thumb, False - Don't show
                    anything on the thumb
                tickCnt: # of ticks in each half-axis
        Init_example:
                self.test_slider = Control_Slider_edit(self, -1, (0,0), -100,
                    100, size=((36, 770), (30, 20)),\
                    direction = 'vertical',valInverse = True,
                    label=('test',('+', '-')), thumbDisplay=True)
    """
    def __init__(self, parent, idStr, value, minValue, maxValue, size, direction,
            valInverse, label, thumbDisplay, tickCnt):
        wx.Panel.__init__(self, parent, id=-1, size=size[0], style=wx.TRANSPARENT_WINDOW)
        self.direction = direction
        self.idStr = idStr          # ID for this control, passed to setValueCallback
        self.label = label[0]       # The label shown in the Tool tip
        self.bt_label = label[1]    # default button label is "+/-"
        self.maxLim = maxValue
        self.maxValue = maxValue
        self.minLim = minValue
        self.minValue = minValue
        self.parent = parent
        self.sizeOfButton = size[1]
        self.thumbDisplay = thumbDisplay  # Tag to show text on the slider thumb.
        self.tickCnt = tickCnt
        if valInverse:
            self.valInverse = -1
        else:
            self.valInverse = 1

        # size[0]: control size, size[1]: button size
        # adjusted size, not counting +/- at end
        if direction == wx.SL_HORIZONTAL:
            self.sizeAdj = (size[0][0] - size[1][0] * 2 - OFFSET_OVER_ADJ_DOUBLE -
                (self.sizeOfButton[0] // 2), size[0][1])
            self.midPt = (self.sizeAdj[0] // 2 + size[1][0] + OFFSET_OVER_ADJ,
                self.sizeAdj[1] // 2)
            self.sizeDrawLimits = (size[1][0] + OFFSET_OVER_ADJ, size[1][0] +
                OFFSET_OVER_ADJ + self.sizeAdj[0])    # left/right drawing area
            Log.info('UI   horz size:%s, mid:%s, lims:%s', self.sizeAdj,
                self.midPt, self.sizeDrawLimits)
        else:
            self.sizeAdj = (size[0][0], size[0][1] - size[1][1] * 2 -
                OFFSET_OVER_ADJ_DOUBLE - (self.sizeOfButton[1] // 2))
            self.midPt = (self.sizeAdj[0] // 2, self.sizeAdj[1] // 2 +
                size[1][1] + OFFSET_OVER_ADJ)
            self.sizeDrawLimits = (size[1][1] + OFFSET_OVER_ADJ, size[1][1] +
                OFFSET_OVER_ADJ + self.sizeAdj[1])    # top/bottom drawing area
        # midpoint of control
        self.indicator_val = [None, None]
        self.setValueCallback = None
        self.stepSize = (self.maxValue - self.minValue) // (self.tickCnt * 2)
        self.values = []                # The value of the thumb and indicators
        self.previousValues = []        # The value of the thumb and indicators
        for i in value:
            self.values.append(i)
        # Add the control thumb
        self.SetBackgroundColour(wx.Colour(120, 120, 120))
        thumbLabel = ' '
        if self.thumbDisplay:
            thumbLabel = str(value[0])
        #Log.debug('UI   BUTTON_POINTER1 %s -> %s', self.label, bt_position)
        self.button_pointer = wx.Button(self, id=-1, label=thumbLabel,
            pos=(0, 0), size=self.sizeOfButton)
        self.updateButtonPos(0)     # draw it in correct pos
        #self.button_pointer.SetFont(wx.Font(8, wx.SWISS, wx.NORMAL, wx.NORMAL))
        #self.button_pointer.SetForegroundColour(wx.Colour(255, 255, 255, 80))
        self.button_pointer.Bind(wx.EVT_LEFT_DOWN, self.mouseDown)

        # Set the forward/backward adjustment buttons.
        if self.direction == wx.SL_HORIZONTAL:
            bt_position1 = (0, HORIZ_Y_OFFSET)
            #bt_position2 = (self.sizeDrawLimits[1] + OFFSET_OVER_ADJ -
            #    self.sizeOfButton[0] // 2, HORIZ_Y_OFFSET)
            bt_position2 = (self.sizeDrawLimits[1] + OFFSET_OVER_ADJ, HORIZ_Y_OFFSET)
        else:
            bt_position1 = (VERT_X_OFFSET, 0)
            #bt_position2 = (VERT_X_OFFSET, self.sizeDrawLimits[1] + OFFSET_OVER_ADJ -
            #    self.sizeOfButton[1] // 2)
            bt_position2 = (VERT_X_OFFSET, self.sizeDrawLimits[1] + OFFSET_OVER_ADJ)
        self.Fw_bt = wx.Button(self, id=-1, label=self.bt_label[0],
            pos=bt_position1, size=self.sizeOfButton)
        self.Fw_bt.Bind(wx.EVT_BUTTON, self.onAdjust)
        self.Bw_bt = wx.Button(self, id=-1, label=self.bt_label[1],
            pos=bt_position2, size=self.sizeOfButton)
        self.Bw_bt.Bind(wx.EVT_BUTTON, self.onAdjust)

        # Bind events to the panel.
        self.Bind(wx.EVT_LEFT_UP, self.mouseUp)
        self.Bind(wx.EVT_MOTION, self.mouseMove)
        self.Bind(wx.EVT_PAINT, self.onPaint)

# ------Control_Slider---------------------------------------------------------
    def drawBG(self, PaintDC):
        """ Draw the background and the scale of the rudder/throttle slider.
        (User can overwrite this class to create their own background and draw
        the scale according to the requirement)
        :param PaintDC: wx.PaintDC
        :return: None
        """
        dc = PaintDC
        drawColor = wx.Colour(220, 234, 234)
        #dc.SetBrush(wx.Brush(wx.Colour(120, 120, 120)))
        # Draw the scale for the RPM, Port side only draw the scale and Stbd side draw
        # the numbers
        dc.SetFont(gv.gSmallerFont)
        dc.SetPen(wx.Pen(drawColor, 1))
        divBy = self.tickCnt * 2
        for i in range(self.tickCnt + 1):
            if self.label == 'Rudder':
                off = (i * self.sizeAdj[0]) / divBy
                #off = (i * self.tickCnt * 7) / self.sizeAdj[0]    # 7 steps in 0, 3500, 500
                #Log.info('UI   Rudder mid:%s, i:%s, off:%s, sz:%s', self.midPt[0],
                #    i, off, self.sizeAdj)
                x = self.midPt[0] - off
                if i == 0:
                    dc.DrawLine(x, 0, x, 10)
                    continue
                dc.DrawLine(x, 2, x, 7)
                x = self.midPt[0] + off
                dc.DrawLine(x, 2, x, 7)
            elif self.label == 'Port':
                off = (i * self.sizeAdj[1]) / divBy
                #off = (i * self.tickCnt * 7) / self.sizeAdj[1]    # 7 steps in 0, 3500, 500
                y = self.midPt[1] - off
                #Log.info('UI   Port mid:%s, i:%s, off:%s, sz:%s, y:%s', self.midPt[1],
                #    i, off, self.sizeAdj, y)
                if i == 0:
                    dc.DrawLine(0, y, 9, y)
                    continue
                dc.DrawLine(2, y, 7, y)
                y = self.midPt[1] + off
                dc.DrawLine(2, y, 7, y)
            elif self.label == 'Stbd':
                off = (i * self.sizeAdj[1]) / divBy
                try:
                    rpm = int(round(np.interp(i * self.stepSize * 0.01,
                        gv.vThrottleValsSampled.get(), gv.vThrottleToRPM.get()), 0))
                except Exception:
                    rpm = '-'       # globals probably not initialized yet (on base)
                #Log.info('UI   Stbd mid:%s, i:%s, off:%s, sz:%s, rpm:%s',
                #    self.midPt[1], i, off, self.sizeAdj, rpm)
                dc.DrawText(str(rpm), 0, self.midPt[1] - off - 3)
                if i == 0: continue
                dc.DrawText(str(rpm), 0, self.midPt[1] + off - 3)

        # Draw the middle line
        dc.SetPen(wx.Pen(drawColor, 2))
        if self.label == 'Rudder':
            dc.DrawLine(self.sizeDrawLimits[0], self.midPt[1],
                self.sizeDrawLimits[1], self.midPt[1])
        elif self.label == 'Port':
            dc.DrawLine(10, self.sizeDrawLimits[0], 10, self.sizeDrawLimits[1])
        elif self.label == 'Stbd':
            dc.DrawLine(25, self.sizeDrawLimits[0], 25, self.sizeDrawLimits[1])

# ------Control_Slider---------------------------------------------------------
    def drawIndicator(self, dc, indicator_val, index):
        """ Draw a indicator according to the indicator parameters.
        :param dc: device context for drawing
        :param indicator_val:
        :return: None
        """
        shape, size, colour, lineWid, offset = indicator_val
        dc.SetPen(wx.Pen(colour[0], lineWid))
        dc.SetBrush(wx.Brush(colour[1]))
        # dc.DrawRectangle(0, int(self.size[1] // 2), 8, int(abs(self.fb_value)) * 7 - 2)
        if self.direction == wx.SL_HORIZONTAL:
            posX = self.sizeDrawLimits[0] + int(
                float(self.values[index] - self.minValue) / float(self.maxValue -
                self.minValue) * self.sizeAdj[0])
            #Log.info('UI   DrawIndX:%s, posX:%s, offset:%s', self.label, posX, offset)
            if shape == 'circle':
                dc.DrawCircle(posX, offset, size)
            elif shape == 'box':
                dc.DrawRectangle(posX - size[0] // 2, offset - size[1] // 2,
                    size[0], size[1])
            elif shape == 'line':
                dc.DrawLine(posX, offset, posX, offset + size)
            else:
                # other shape will be treated as 'text'
                dc.DrawText(str(shape), posX, offset)
                pass
        else:
            posY = self.sizeDrawLimits[0] + int(
                float(self.values[index] - self.minValue) / float(self.maxValue -
                self.minValue) * self.sizeAdj[1])
            #Log.info('UI   DrawIndV:%s, posY:%s, offset:%s', self.label, posY, offset)
            if shape == 'circle':
                dc.DrawCircle(offset, posY, size)
            elif shape == 'box':
                dc.DrawRectangle(offset - size[0] // 2, posY - size[1] // 2,
                    size[0], size[1])
            elif shape == 'line':
                dc.DrawLine(offset, posY, offset + size, posY)
            else:
                dc.DrawText(str(shape), offset, posY)
                pass

# ------Control_Slider---------------------------------------------------------
#     def enableThumbDisplay(self, tag):
#         """ Enable/Disable label shown on the slider thumb.
#         :param bool tag: T: Show text on thumb, F: Don't show text on thumb
#         :return: None
#         """
#         self.thumbDisplay = tag
#         if not self.thumbDisplay:
#             # Clear the label on the thumb after it is disabled.
#             self.updateIndicatorValue(' ')

# ------Control_Slider---------------------------------------------------------
    def getValue(self, idx):
        """ Return the slider value.
        """
        return self.values[idx] * self.valInverse

# ------Control_Slider---------------------------------------------------------
    def mouseDown(self, event):
        """ Update the position record and the active tag when the user press
        the slider's thumb.
        :param event: Mouse left down event
        :return: None
        """
        self.CaptureMouse()
        self.previousValues = copy(self.values)
        #Log.debug('UI   mouseDown prev:%s', self.previousValues)

# ------Control_Slider---------------------------------------------------------
    def mouseMove(self, event):
        """ Record the drag position and update the value.
        :param event: Mouse movement event
        :return: None
        """
        if event.Dragging():
            x, y = event.GetPosition()
            if self.direction == wx.SL_HORIZONTAL:
                pos = x
                mid = self.midPt[0]
            else:
                pos = y
                mid = self.midPt[1]
            # Update the setting value according the current thumb position.
            if abs(mid - pos) <= 5:     # gravity on the mid point
                pos = mid
            dist = pos - mid
            drawSz = self.sizeDrawLimits[1] - self.sizeDrawLimits[0]
            val = int((dist * abs(self.maxValue - self.minValue)) /
                drawSz) * self.valInverse
            self.setValue(val, idx=0)
            #Log.info('UI   Control_Slider:%s MouseMove xy:%s, pos:%s, dist:%s,
            #    mid:%s, val:%s',
            #    self.label, (x, y), pos, dist, self.midPt, val)
        else:
            event.Skip()

# ------Control_Slider---------------------------------------------------------
    def mouseUp(self, event):
        """Called when mouse up on control"""
        if self.HasCapture():
            #Log.debug('UI   mouseUp')
            self.ReleaseMouse()
            self.tellNewValue()

# ------Control_Slider---------------------------------------------------------
    def onAdjust(self, event):
        """ Handle the event of the adjustment button.
        """
        btn = event.GetEventObject().GetLabelText()
        value = 0
        if btn == self.bt_label[0]:
            # Forward the throttle
            value = (self.values[0] - self.stepSize) * self.valInverse
            if value < self.minValue: value = self.minValue
        elif btn == self.bt_label[1]:
            # Backward the throttle
            value = (self.values[0] + self.stepSize) * self.valInverse
            if value > self.maxValue: value = self.maxValue

        #Log.debug('UI  Control_Slider %s onAdjust btn:%s, values:%s->%s',
        #    self.label, btn, self.values, value)
        self.previousValues = self.values
        #Log.debug('UI   onAdjust prev:%s', self.previousValues)
        self.setValue(value, idx=0)
        self.tellNewValue()

# ------Control_Slider---------------------------------------------------------
    def onPaint(self, event):
        """ The draw function used to draw the scale and the feed back indicators
        :param event: wx.EVT_PAINT
        :return: None
        """
        dc = wx.PaintDC(self)
        self.drawBG(dc)     # Draw the background scale

        dc.SetBrush(wx.Brush(wx.Colour(140, 170, 210)))

        # Draw the indicators one by one, in the proper stacking order
        for i in range(len(self.values)):
            #Log.info('UI   OnPaint:%s, i:%i, ind:%s', self.label, i,
            #    self.indicator_val[i])
            if self.indicator_val[i]:
                self.drawIndicator(dc, self.indicator_val[i], i)

# ------Control_Slider---------------------------------------------------------
    def setIndicatorStyle(self, indicator_val, idx):
        """ Set the parameter of the indicator.(shape, size, color, position.)
        """
        self.indicator_val[idx] = indicator_val

# ------Control_Slider---------------------------------------------------------
    def setValue(self, newValue, idx):
        """ Set the slider value.
        idx: 0:main ctl, 1:aux indicator
        Return True if the value is set or return
        False if the value out of range.
        """
        #Log.debug('UI   %s setValue:%.3f, idx:%s', self.label, newValue, idx)
        newValue = self.valInverse * newValue
        newValue = max(min(newValue, self.maxValue), self.minValue)
        if self.values[idx] == newValue: return True

        if idx == 0:
            self.values[0] = newValue
            self.updateButtonPos(newValue)
            if self.thumbDisplay:
                self.updateIndicatorValue(int(self.values[idx]) * self.valInverse)
        else:
            self.values[1] = newValue
            self.Refresh(True)
        return True

# ------Control_Slider---------------------------------------------------------
    def tellNewValue(self):
        """Tell callback about new value for this control"""
        #Log.debug('UI   tellNewValue')
        try:
            if self.setValueCallback is not None:
                # if parent set a callback for value change, call it now
                self.setValueCallback(self.getValue(0))
        except ControlLockout:
            # if we are base, and don't have control, set will fail, and DataTypes
            # will have already printed out an error message, so we just need to
            # catch the exception here & restore previous values
            #Log.debug('UI   tellNewValue ControlLockout')
            self.setValue(self.previousValues[0] * self.valInverse, 0)
            self.setValue(self.previousValues[1] * self.valInverse, 1)

# ------Control_Slider---------------------------------------------------------
    def updateButtonPos(self, newValue):
        """Update position of button"""
        if self.direction == wx.SL_HORIZONTAL:
            posX = self.sizeDrawLimits[0] - (self.sizeOfButton[0] // 2) + int(
                float(newValue - self.minValue) / float(self.maxValue -
                self.minValue) * self.sizeAdj[0])
            #Log.info('UI   Control_Slider %s setValue idx:%s, newVal:%s, valInv:%s, posX:%s, mid:%s',
            #    self.label, idx, newValue, self.valInverse, posX, self.midPt)
            #Log.debug('UI   BUTTON_POINTER2 %s -> %s', self.label, (posX, 0))
            self.button_pointer.SetPosition(wx.Point(posX, HORIZ_Y_OFFSET))
        else:
            posY = self.sizeDrawLimits[0] - (self.sizeOfButton[1] // 2) + int(
                float(newValue - self.minValue) / float(self.maxValue -
                self.minValue) * self.sizeAdj[1])
            #Log.info('UI   Control_Slider %s setValue idx:%s, newVal:%s, valInv:%s,
            #    posY:%s, mid:%s',
            #    self.label, idx, newValue, self.valInverse, posY, self.midPt)
            #Log.debug('UI   BUTTON_POINTER3 %s -> %s', self.label, (0, posY))
            self.button_pointer.SetPosition(wx.Point(VERT_X_OFFSET, posY))

# ------Control_Slider---------------------------------------------------------
    def updateIndicatorValue(self, value):
        """ Update the text shown on the slider's thumb.
        :param str value: A string value need to shown on the slider thumb
        :return: True - if the thumb label is set successfully. False if the
            input value is not valid.
        """
        try:
            self.button_pointer.SetLabel(str(value))
            return True
        except Exception:
            return False

#-----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class SliderFrame(wx.Frame):
    """
    The test program to show the slider in a frame individually.
    """
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'Slider Test', size=(580, 350))
        panel = wx.Panel(self, -1)
        self.SetBackgroundColour(wx.Colour(200, 210, 200))
        self.count = 0
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.rudder_slider = Control_Slider_edit(self, -1, 0, -100, 100, size=(540, 36))
        sizer.Add(self.rudder_slider)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.stbd_slider = Control_Slider_edit(self, -1, (0, 0), -100, 100,
            size=((36, 770), (30, 20)), direction='vertical', valInverse=True,
            label=('Stbd', ('+', "-")))
        sizer2.Add(self.stbd_slider)
        self.port_slider = Control_Slider_edit(self, -1, (0, 0), -100, 100,
            size=((36, 770), (30, 20)), direction='vertical', valInverse=True,
            label=('Port', ('+', '-')))
        sizer2.Add(self.port_slider)
        sizer.Add(sizer2)
        self.SetSizer(sizer)


if __name__ == '__main__':
    app = SliderFrame()
    print('End of test')
    app.MainLoop()

"""
# uncomment this code can run the program individually for testing.
app = wx.PySimpleApp()
frame = SliderFrame()
frame.Show()
app.MainLoop()
"""
