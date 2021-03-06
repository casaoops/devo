import wx

class SaveChangesDialog(wx.Dialog):
    def __init__(self, parent, message, title="Unsaved Changes"):
        wx.Dialog.__init__(self, parent, title=title)
        btnsizer = wx.StdDialogButtonSizer()
        btn_save = wx.Button(self, wx.ID_YES, "&Save")
        btn_save.SetDefault()
        btnsizer.AddButton(btn_save)
        btnsizer.AddButton(wx.Button(self, wx.ID_NO, "&Don't Save"))
        btnsizer.AddButton(wx.Button(self, wx.ID_CANCEL, "&Cancel"))
        btnsizer.Realize()
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        warning_bitmap = wx.ArtProvider.GetBitmap(wx.ART_WARNING, wx.ART_MESSAGE_BOX)
        bmp = wx.StaticBitmap(self, wx.ID_ANY, warning_bitmap)
        hsizer.Add(bmp, 0, wx.ALIGN_CENTRE | wx.RIGHT, 15)
        hsizer.Add(wx.StaticText(self, label=message), 1, wx.ALIGN_CENTRE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 15)
        sizer.Add(btnsizer, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Fit()
        self.Centre()
        size = self.GetSize()
        self.SetMinSize(size)
        self.SetMaxSize(size)
        self.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(evt.GetId()))
