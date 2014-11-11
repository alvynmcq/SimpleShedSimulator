#SimpleShedSimulator for quick schedule risk analysis
#Copyright (C) 2014  Anders Jensen
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):

    def __init__(self, parent, ID=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class RiskRegister(wx.Frame):

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, pos=wx.Point(100, 100), size=wx.Size(770, 500))
        self.CreateListCtrl()
        self.CreateMenuBar()
        self.Show(True)

    def CreateListCtrl(self):
        """Creates the list ctrl"""
        self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT)
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
            self.list_ctrl.InsertColumn(i, self.headings[i])
            self.list_ctrl.SetColumnWidth(i, column_size)
    
    def CreateMenuBar(self):
        '''Creates menubar'''
        menubar = wx.MenuBar()
        
        #File menu
        file = wx.Menu()
        OPEN = file.Append(-1, '&Open\tCtrl+o', 'Open an existing risk register')
        NEW = file.Append(-1, '&New\tCtrl+n', 'Create a new network')
        SAVEAS = file.Append(-1, '&Save as\tCtrl+s', 'Save the network')
        menubar.Append(file, '&File')
        
        #EditMenu
        edit = wx.Menu()
        ADDRISK = edit.Append(-1, '&Add risk\tCtrl+a', 'Add risk')
        DELRISK = edit.Append(-1, '&Delete risk\tCtrl+d', 'Delete risk')
        menubar.Append(edit, '&Edit')

        self.SetMenuBar(menubar) 
        
        #Bindings
        self.Bind(wx.EVT_MENU, self.OpenRegister,OPEN)
        self.Bind(wx.EVT_MENU, self.AddRisk, ADDRISK)
        self.Bind(wx.EVT_MENU, self.DeleteRisk, DELRISK)
        self.Bind(wx.EVT_MENU, self.SaveRiskRegisterAs, SAVEAS)
    
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
                    self.list_ctrl.SetStringItem(num_of_risk,num_of_items, str(riskitem.text))
                    num_of_items += 1
                num_of_risk += 1
        dlg.Destroy()

    def AddRisk(self, event):
        #this function creates a dialog which allows you to register a new risk register
        self.list_ctrl.InsertStringItem(0, "-")
        [self.list_ctrl.SetStringItem(0, i, "-") for i in range(1,7)]

    def DeleteRisk(self, event):
        #this function deletes the focused entry from memory, but not from the .csv file
        entrynumber=self.list_ctrl.GetFocusedItem()
        data=self.list_ctrl.DeleteItem(entrynumber)

    def SaveRiskRegisterAs(self, event, *args):
        
        number_of_rows=self.list_ctrl.GetItemCount()
        number_of_columns=self.list_ctrl.GetColumnCount()
        data=[]
       
        riskregister = xml.FileWriter("Risk_register")
       
        for n in range(0,number_of_rows):
            current_risk = "risk_" + str(n)
            riskregister.AddRow(current_risk)
            for m in range(0,number_of_columns):
                risk_item = self.list_ctrl.GetColumn(m).GetText().replace(" ", "")
                risk_item_value = self.list_ctrl.GetItem(n, m).GetText()
                
                riskregister.AddRowItems(current_risk, risk_item,risk_item_value)

        dlg= wx.FileDialog ( None, style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            path=dirname + '/' + filename + ".xml"
            riskregister.WriteToFile(path)
        dlg.Destroy()








if __name__ == '__main__':
    app = wx.App(False)
    frame = RiskRegister(None, 'Risk register')
    app.MainLoop()

