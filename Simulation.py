import wx
import AppointmentSim
import numpy


class SimGui(wx.Frame):
    def __init__(self, *args, **kw):
        super(SimGui, self).__init__(*args, **kw)

        self.H_Upper = None
        self.C_Upper = None
        self.D_Upper = None
        self.Ha_Upper = None
        self.Pf_Upper = None
        self.Hf_Upper = None
        self.G_Upper = None
        self.B_Upper = None
        self.T_Upper= None

        self.Inc_Label = None
        self.Upper_Label = None

        self.InitUI()

    def InitUI(self):
        self.pnl = wx.Panel(self)

        closeButton = wx.Button(self.pnl, label='Run Simulation', pos=(150, 320))
        closeButton.Bind(wx.EVT_BUTTON, self.RunSim)

        params = wx.StaticBox(self.pnl, label="Parameters", pos=(5, 1), size=(420, 350))

        """ ================= Test Values ================= """

        wx.StaticText(self.pnl, label=' Planning Horizon', pos=(15, 30))
        self.H = wx.SpinCtrl(self.pnl, value='4', pos=(125, 30), size=(60, -1), min=1, max=360)

        wx.StaticText(self.pnl, label=' Capacity', pos=(15, 60))
        self.C = wx.SpinCtrl(self.pnl, value='10', pos=(125, 60), size=(60, -1), min=1, max=120)

        wx.StaticText(self.pnl, label=' Day Types ', pos=(15, 90))
        self.D = wx.SpinCtrl(self.pnl, value='2', pos=(125, 90), size=(60, -1), min=1, max=360)

        wx.StaticText(self.pnl, label=' Acute Horizon ', pos=(15, 120))
        self.Ha = wx.SpinCtrl(self.pnl, value='2', pos=(125, 120), size=(60, -1), min=1, max=120)

        wx.StaticText(self.pnl, label=' Prob Follow-Up ', pos=(15, 150))
        self.Pf = wx.SpinCtrlDouble(self.pnl, value='0.2', pos=(125, 150), size=(60, -1), min=0.0, max=1.0,
                                    initial=0.2, inc=0.01)

        wx.StaticText(self.pnl, label=' Follow-Up Horizon ', pos=(15, 180))
        self.Hf = wx.SpinCtrl(self.pnl, value='2', pos=(125, 180), size=(60, -1), min=1, max=120)

        wx.StaticText(self.pnl, label=' Gamma ', pos=(15, 210))
        self.G = wx.SpinCtrlDouble(self.pnl, value='0.1', pos=(125, 210), size=(60, -1), min=0.0, max=1.0,
                                    initial=0.1, inc=0.01)

        wx.StaticText(self.pnl, label=' Beta ', pos=(15, 240))
        self.B = wx.SpinCtrlDouble(self.pnl, value='0.1', pos=(125, 240), size=(60, -1), min=0.0, max=1.0,
                                    initial=0.1, inc=0.01)

        wx.StaticText(self.pnl, label=' Theta ', pos=(15, 270))
        self.T = wx.SpinCtrlDouble(self.pnl, value='1.0', pos=(125, 270), size=(60, -1), min=0.0, max=5.0,
                                    initial=1.0, inc=0.1)


        """ ================= Range Check Boxes ================= """

        wx.StaticText(self.pnl, label="Test Range?", pos=(200, 20))

        self.H_range_box = wx.CheckBox(self.pnl,label="", pos=(225, 35))
        self.Bind(wx.EVT_CHECKBOX, self.H_range_check, self.H_range_box)

        self.C_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 65))
        self.Bind(wx.EVT_CHECKBOX, self.C_range_check, self.C_range_box)

        self.D_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 95))
        self.Bind(wx.EVT_CHECKBOX, self.D_range_check, self.D_range_box)

        self.Ha_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 125))
        self.Bind(wx.EVT_CHECKBOX, self.Ha_range_check, self.Ha_range_box)

        self.Pf_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 155))
        self.Bind(wx.EVT_CHECKBOX, self.Pf_range_check, self.Pf_range_box)

        self.Hf_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 185))
        self.Bind(wx.EVT_CHECKBOX, self.Hf_range_check, self.Hf_range_box)

        self.G_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 215))
        self.Bind(wx.EVT_CHECKBOX, self.G_range_check, self.G_range_box)

        self.B_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 245))
        self.Bind(wx.EVT_CHECKBOX, self.B_range_check, self.B_range_box)

        self.T_range_box = wx.CheckBox(self.pnl, label="", pos=(225, 275))
        self.Bind(wx.EVT_CHECKBOX, self.T_range_check, self.T_range_box)

        self.SetSize((450, 390))
        self.SetTitle('Simulation Parameters')
        self.Centre()

    def H_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.H_range_box.GetValue():
            self.H_Upper = wx.SpinCtrl(self.pnl, value=str(self.H.GetValue()+1), pos=(275, 30), size=(60, -1), min=self.H.GetValue()+1, max=365)
            self.H_Step = wx.SpinCtrl(self.pnl, value=str(1), pos=(350, 30), size=(60, -1), min=1, max=365)
        else:
            self.H_Upper.Hide()
            self.H_Step.Hide()
            self.H_Upper = None
            self.H_Step = None
        return True

    def C_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.C_range_box.GetValue():
            self.C_Upper = wx.SpinCtrl(self.pnl, value=str(self.C.GetValue()+1), pos=(275, 60), size=(60, -1), min=self.C.GetValue()+1, max=50)
            self.C_Step = wx.SpinCtrl(self.pnl, value=str(1), pos=(350, 60), size=(60, -1), min=1, max=50)
        else:
            self.C_Upper.Hide()
            self.C_Step.Hide()
            self.C_Upper = None
            self.C_Step= None

        return True

    def D_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.D_range_box.GetValue():
            self.D_Upper = wx.SpinCtrl(self.pnl, value=str(self.D.GetValue()+1), pos=(275, 90), size=(60, -1), min=self.D.GetValue()+1, max=7)
            self.D_Step = wx.SpinCtrl(self.pnl, value=str(1), pos=(350, 90), size=(60, -1), min=1, max=3)
        else:
            self.D_Upper.Hide()
            self.D_Step.Hide()
            self.D_Upper = None
            self.D_Step = None
        return True

    def Ha_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.Ha_range_box.GetValue():
            self.Ha_Step = wx.SpinCtrl(self.pnl, value=str(1), pos=(350, 120), size=(60, -1), min=1, max=365)
            self.Ha_Upper = wx.SpinCtrl(self.pnl, value=str(self.Ha.GetValue()+1), pos=(275, 120), size=(60, -1), min=self.Ha.GetValue()+1, max=365)
        else:
            self.Ha_Upper.Hide()
            self.Ha_Step.Hide()
            self.Ha_Upper = None
            self.Ha_Step = None

        return True

    def Pf_range_check(self, e):
        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.Pf_range_box.GetValue():
            self.Pf_Upper = wx.SpinCtrlDouble(self.pnl, value=str(self.Pf.GetValue()+0.01), pos=(275, 150), size=(60, -1), min=0.0, max=1.0,
                                    initial=self.Pf.GetValue()+0.01, inc=0.01)
            self.Pf_Step = wx.SpinCtrlDouble(self.pnl, value=str(0.01), pos=(350, 150),
                                              size=(60, -1), min=0.0, max=1.0,
                                              initial=0.01, inc=0.01)
        else:
            self.Pf_Upper.Hide()
            self.Pf_Step.Hide()
            self.Pf_Step = None
            self.Pf_Upper = None
        return True

    def Hf_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.Hf_range_box.GetValue():
            self.Hf_Upper = wx.SpinCtrl(self.pnl, value=str(self.Hf.GetValue()+1), pos=(275, 180), size=(60, -1), min=self.Hf.GetValue()+1, max=365)
            self.Hf_Step = wx.SpinCtrl(self.pnl, value=str(1), pos=(350, 180), size=(60, -1), min=1, max=365)
        else:
            self.Hf_Upper.Hide()
            self.Hf_Step.Hide()
            self.Hf_Step = None
            self.Hf_Upper = None
        return True

    def G_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.G_range_box.GetValue():
            self.G_Upper = wx.SpinCtrlDouble(self.pnl, value=str(self.G.GetValue()+0.01), pos=(275, 210), size=(60, -1), min=0.0, max=1.0,
                                    initial=self.G.GetValue()+0.01, inc=0.01)
            self.G_Step = wx.SpinCtrlDouble(self.pnl, value=str(0.01), pos=(350, 210),
                                         size=(60, -1), min=0.0, max=1.0,
                                         initial=0.01, inc=0.01)
        else:
            self.G_Upper.Hide()
            self.G_Step.Hide()
            self.G_Step = None
            self.G_Upper = None

        return True

    def B_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.B_range_box.GetValue():
            self.B_Upper = wx.SpinCtrlDouble(self.pnl, value=str(self.B.GetValue()+0.01), pos=(275, 240), size=(60, -1), min=0.0, max=1.0,
                            initial=self.B.GetValue()+0.01, inc=0.01)
            self.B_Step = wx.SpinCtrlDouble(self.pnl, value=str(0.01), pos=(350, 240),
                                             size=(60, -1), min=0.0, max=1.0,
                                             initial=0.01, inc=0.01)
        else:
            self.B_Upper.Hide()
            self.B_Step.Hide()
            self.B_Step = None
            self.B_Upper = None
        return True

    def T_range_check(self, e):

        if self.Inc_Label is None or self.Upper_Label is None:
            wx.StaticText(self.pnl, label="Min", pos=(135, 10))
            wx.StaticText(self.pnl, label="Max", pos=(285, 10))
            wx.StaticText(self.pnl, label='Step', pos=(360, 10))

        if self.T_range_box.GetValue():
            self.T_Upper = wx.SpinCtrlDouble(self.pnl, value=str(self.T.GetValue()+0.01), pos=(275, 270), size=(60, -1), min=0.0, max=1.0,
                                    initial=self.T.GetValue()+0.01, inc=0.01)
            self.T_Step = wx.SpinCtrlDouble(self.pnl, value=str(0.01), pos=(350, 270),
                                             size=(60, -1), min=0.0, max=1.0,
                                             initial=0.01, inc=0.01)
        else:
            self.T_Upper.Hide()
            self.T_Step.Hide()
            self.T_Step = None
            self.T_Upper = None

        return True

    def RunSim(self, e):

        self.H_Range = [self.H.GetValue()] if not self.H_Upper else list(numpy.arange(self.H.GetValue(), self.H_Upper.GetValue()+1, self.H_Step.GetValue()))
        self.C_Range = [self.C.GetValue()] if not self.C_Upper else list(numpy.arange(self.C.GetValue(), self.C_Upper.GetValue()+1, self.C_Step.GetValue()))
        self.D_Range = [self.D.GetValue()] if not self.D_Upper else list(numpy.arange(self.D.GetValue(), self.D_Upper.GetValue()+1, self.D_Step.GetValue()))
        self.Ha_Range = [self.Ha.GetValue()] if not self.Ha_Upper else list(numpy.arange(self.Ha.GetValue(), self.Ha_Upper.GetValue()+1, self.Ha_Step.GetValue()))
        self.Pf_Range = [self.Pf.GetValue()] if not self.Pf_Upper else list(numpy.arange(self.Pf.GetValue(), self.Pf_Upper.GetValue()+0.01, self.Pf_Step.GetValue()))
        self.Hf_Range =  [self.Hf.GetValue()] if not self.Hf_Upper else list(numpy.arange(self.Hf.GetValue(), self.Hf_Upper.GetValue()+1, self.Hf_Step.GetValue()))
        self.G_Range =  [self.G.GetValue()] if not self.G_Upper else list(numpy.arange(self.G.GetValue(), self.G_Upper.GetValue()+0.01, self.G_Step.GetValue()))
        self.B_Range =  [self.B.GetValue()] if not self.B_Upper else list(numpy.arange(self.B.GetValue(), self.B_Upper.GetValue()+0.01, self.B_Step.GetValue()))
        self.T_Range =  [self.T.GetValue()] if not self.T_Upper else list(numpy.arange(self.T.GetValue(), self.T_Upper.GetValue()+0.01, self.T_Step.GetValue()))

        self.Close()

        AppointmentSim.main(self.H_Range, self.C_Range, self.D_Range, self.Ha_Range, self.Pf_Range, self.Hf_Range, self.G_Range,
                            self.B_Range, self.T_Range)


if __name__ == '__main__':
    app = wx.App()
    ex = SimGui(None)
    ex.Show()
    app.MainLoop()


