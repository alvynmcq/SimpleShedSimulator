import os
import wx
import wx.lib.mixins.listctrl  as  listmix

import sys
path = os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(path)
path = os.path.split(path)[0]

picturepath = os.path.join(path, 'pictures')
dbpath = os.path.join(path, 'db')

sys.path.append(path)

from core import xml_writer as xml

[wxID_FRAME1, wxID_FRAME1BUTTON1, wxID_FRAME1BUTTON2, wxID_FRAME1BUTTON3, 
 wxID_FRAME1BUTTON4, wxID_FRAME1LISTCTRL1, wxID_FRAME1PANEL1, 
 wxID_FRAME1STATUSBAR1, 
] = [wx.NewId() for _init_ctrls in range(8)]

[wxID_FRAME1FILITEMS0, wxID_FRAME1FILITEMS1, wxID_FRAME1MENU1ITEMS3, 
 wxID_FRAME1MENU1ITEMS4, 
] = [wx.NewId() for _init_coll_Fil_Items in range(4)]

[wxID_FRAME1EDITITEMS0] = [wx.NewId() for _init_coll_Edit_Items in range(1)]

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):

    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class Frame1(wx.Frame):

    def __init__(self, parent):
        self._init_ctrls(parent)

    def _init_coll_flexGridSizer1_Items(self, parent):
        # generated method, don't edit

        parent.AddWindow(self.button2)
        parent.AddWindow(self.button3)
        parent.AddWindow(self.button4)

    def _init_coll_boxSizer1_Items(self, parent):
        parent.AddSizer(self.flexGridSizer1, 0)
        parent.AddWindow(self.listCtrl1, 1, flag=wx.EXPAND | wx.ALL)

    def _init_coll_menuBar1_Menus(self, parent):
        parent.Append(menu=self.Fil, title=u'File')
        parent.Append(menu=self.Edit, title=u'Edit')

    def _init_coll_Fil_Items(self, parent):
        parent.Append(help='', id=wxID_FRAME1FILITEMS0, kind=wx.ITEM_NORMAL,text=u'Open register')
        parent.Append(help='', id=wxID_FRAME1FILITEMS1, kind=wx.ITEM_NORMAL,text=u'New')
        parent.Append(help='', id=wxID_FRAME1MENU1ITEMS3, kind=wx.ITEM_NORMAL, text=u'Save')
        parent.Append(help='', id=wxID_FRAME1MENU1ITEMS4, kind=wx.ITEM_NORMAL, text=u'Save register as...')
        
        self.Bind(wx.EVT_MENU, self.OpenRegister, id=wxID_FRAME1FILITEMS0)
        self.Bind(wx.EVT_MENU, self.AddRisk, id=wxID_FRAME1FILITEMS1)
        self.Bind(wx.EVT_MENU, self.OnFilU1items4Menu, id=wxID_FRAME1MENU1ITEMS4)

    def _init_coll_Edit_Items(self, parent):
        # generated method, don't edit

        parent.Append(help='', id=wxID_FRAME1EDITITEMS0, kind=wx.ITEM_NORMAL, text=u'Delete entry')
        self.Bind(wx.EVT_MENU, self.OnButton4Button, id=wxID_FRAME1EDITITEMS0)

    def _init_coll_listCtrl1_Columns(self, parent):
        
        self.headings = ['ID',
                         'Risk Driver',
                         'Name',
                         'Probability',
                         'Effect',
                         'Impact',
                         'Owner',
                         ]
        column_size = 110
        for i in range(0,len(self.headings)):
            parent.InsertColumn(i, self.headings[i])
            parent.SetColumnWidth(i, column_size)

    def _init_utils(self):
        # generated method, don't edit
        self.menuBar1 = wx.MenuBar()

        self.Fil = wx.Menu(title=u'')

        self.Edit = wx.Menu(title=u'')

        self._init_coll_menuBar1_Menus(self.menuBar1)
        self._init_coll_Fil_Items(self.Fil)
        self._init_coll_Edit_Items(self.Edit)

    def _init_sizers(self):
        # generated method, don't edit
        self.boxSizer1 = wx.BoxSizer(orient=wx.VERTICAL)

        self.flexGridSizer1 = wx.FlexGridSizer(cols=0, hgap=0, rows=1, vgap=0)

        self._init_coll_boxSizer1_Items(self.boxSizer1)
        self._init_coll_flexGridSizer1_Items(self.flexGridSizer1)

        self.panel1.SetSizer(self.boxSizer1)

    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, parent=prnt,
              pos=wx.Point(335, 158), size=wx.Size(882, 560),
              style=wx.DEFAULT_FRAME_STYLE, title=u'Risk register')
        
        self._init_utils()

        self.SetMenuBar(self.menuBar1)

        self.panel1 = wx.Panel(id=-1,parent=self,style=wx.TAB_TRAVERSAL, size=wx.Size(882, 535))

        self.button2 = wx.Button(id=-1, label=u'Add entry', name='button2', parent=self.panel1)
        self.button2.Bind(wx.EVT_BUTTON, self.AddRisk)
        
        self.listCtrl1 = EditableListCtrl(self, style=wx.LC_REPORT)
       
        self._init_coll_listCtrl1_Columns(self.listCtrl1)
        
        self.listCtrl1.Bind(wx.EVT_LEFT_DCLICK, self.AddRisk)

        self.button3 = wx.Button(id=-1, label=u'Find', name='button3', parent=self.panel1)
        self.button3.Bind(wx.EVT_BUTTON, self.OnButton3Button)

        self.button4 = wx.Button(id=wxID_FRAME1BUTTON4, label=u'Del entry', name='button4', parent=self.panel1, pos=wx.Point(284, 5),size=wx.Size(85, 29), style=0)
        self.button4.Bind(wx.EVT_BUTTON, self.OnButton4Button, id=wxID_FRAME1BUTTON4)

        self.statusBar1 = wx.StatusBar(id=wxID_FRAME1STATUSBAR1, name='statusBar1', parent=self, style=0)
        self.SetStatusBar(self.statusBar1)

        self._init_sizers()

    def OnButton3Button(self, event):
            """ Open a file"""
            self.dirname = ''
            dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.txt", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                path=self.dirname + self.filename
                print path
                data=reg.read_register(path)
                n=0
                for q in data:
                    self.listCtrl1.InsertStringItem(n,data[n][0])
                    m=0
                    for w in q:
                        self.listCtrl1.SetStringItem(n,m, data[n][m])
                        m=m+1
                    n=n+1
            dlg.Destroy()

    def OpenRegister(self, event):
        """parses an xml file and writes it to Listcrtl"""
        dlg = wx.FileDialog(self, message="Open file ...",  style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            register = xml.FileReader().ReadFile(path)
            
            for riskdescriptions in register:
                self.AddRisk(event)
            
            num_of_risk = 0
            for riskdescriptions in register:
                num_of_items = 0
                for riskitem in riskdescriptions:
                    print num_of_risk,num_of_items, str(riskitem.text)
                    self.listCtrl1.SetStringItem(num_of_risk,num_of_items, str(riskitem.text))
                    num_of_items += 1
                num_of_risk += 1

        dlg.Destroy()
    
    def AddRisk(self, event):
        #this function creates a dialog which allows you to register a new risk register
        self.listCtrl1.InsertStringItem(0,"ID")

    def OnMenu1Items2Menu(self, event):
        event.Skip()

    def OnButton4Button(self, event):
        #this function deletes the focused entry from memory, but not from the .csv file
        entrynumber=self.listCtrl1.GetFocusedItem()
        data=self.listCtrl1.DeleteItem(entrynumber)

    def OnButton1Button(self, event):
        event.Skip()

    def OnFilU1items4Menu(self, event, *args):
        #number_of_rows=self.listCtrl1.GetItemCount()
        #number_of_columns=self.listCtrl1.GetColumnCount()
        #data=[]
        #for n in range(0,number_of_rows):
            #intermediate=[]
            #for m in range(0,number_of_columns):
                #risk = self.listCtrl1.GetItem(n, m).GetText()
                #intermediate.append(str(risk))
                
            #data.append(intermediate)
        
        number_of_rows=self.listCtrl1.GetItemCount()
        number_of_columns=self.listCtrl1.GetColumnCount()
        data=[]
       
        riskregister = xml.FileWriter("Risk_register")
       
        for n in range(0,number_of_rows):
            current_risk = "risk_" + str(n)
            riskregister.AddRow(current_risk)
            for m in range(0,number_of_columns):
                risk_item = self.listCtrl1.GetColumn(m).GetText().replace(" ", "")
                risk_item_value = self.listCtrl1.GetItem(n, m).GetText()
                
                riskregister.AddRowItems(current_risk, risk_item,risk_item_value)

        dlg= wx.FileDialog ( None, style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            path=dirname + '/' + filename + ".xml"
            riskregister.WriteToFile(path)
        dlg.Destroy()



if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = Frame1(None)
    frame.Show()

    app.MainLoop()
