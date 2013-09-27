import re
import pprint

#wx
import wx
import wx.lib.mixins.listctrl  as  listmix
import wx.grid as  gridlib

#plotting with matplotlib:
import random
from numpy import arange, sin, pi
import matplotlib
from matplotlib.backends.backend_wxagg import  NavigationToolbar2WxAgg
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure


import os
import sys
path = os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(path)
path = os.path.split(path)[0]

picturepath = os.path.join(path, 'pictures')
dbpath = os.path.join(path, 'db')

sys.path.append(path)


from core import act



class RiskTable(wx.Frame):


    def __init__(self, activities):
        wx.Frame.__init__(self, None, wx.ID_ANY, "Risktable")
 
        # Add a panel and a grid
        panel = wx.Panel(self, wx.ID_ANY)
        self.grid = gridlib.Grid(panel)
        
        #Fix the columns and headers accordingly
        number_of_activities = len(activities)
        self.grid.CreateGrid(number_of_activities+2,0)
        self.grid.SetRowLabelValue(0, " ") #this is where Riskdriver comes
        self.grid.SetRowLabelValue(1, " ") #this is where ML min max comes
        
        for i in range(number_of_activities):
            self.grid.SetRowLabelValue(2+i, str(activities[i].GetName()))
        
        self.grid.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
        self.grid.SetRowLabelSize(150) # should do this with self.grid.AutoSizeRow(i)
        
        #Hide Columns
        self.grid.SetColLabelSize(0) 
        
        #Add buttons and bind them
        self.button1 = wx.Button(panel, -1, "Add Risk Driver")
        self.button1.Bind(wx.EVT_BUTTON, self.AddRiskDriver)
        self.button2 = wx.Button(panel, -1, "Create risk table")
        self.button2.Bind(wx.EVT_BUTTON, self.CreateRiskTable)
        self.button3 = wx.Button(panel, -1, "Simulate risk table")
        self.button3.Bind(wx.EVT_BUTTON, self.SimulateRiskTable)
        
        #add sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.grid, 1,wx.RIGHT|wx.EXPAND, 5)
        sizer.Add(sizer1)
        sizer1.Add(self.button1, 0, wx.RIGHT, 5)
        sizer1.Add(self.button2, 0, wx.RIGHT, 5)
        sizer1.Add(self.button3, 0, wx.RIGHT, 5)
        panel.SetSizer(sizer)
        
        #Add base duration
        self.grid.InsertCols(pos=0, numCols = 1, updateLabels = False)
        collor = self.grid.GetLabelBackgroundColour()
        self.grid.SetCellBackgroundColour (0, 0, collor)
        self.grid.SetCellBackgroundColour (1, 0, collor)
        
        self.grid.SetCellValue(1,0, "Base")
        self.grid.SetCellAlignment(1,0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        for i in range(number_of_activities):
            self.grid.SetCellValue(i+2,0, str(activities[i].GetDuration()))
            self.grid.SetCellAlignment(i+2,0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        
    def AddRiskDriver(self, event):
        #Add riskdrivers
        number_of_riskdrivers = self.grid.GetNumberCols()
        self.grid.InsertCols(pos=number_of_riskdrivers, numCols = 3, updateLabels = False)
        
        #fix proper formating of grid
        number_of_riskdrivers = self.grid.GetNumberCols()
        collor = self.grid.GetLabelBackgroundColour()

        for i in range(number_of_riskdrivers):
            j = i
            i = i+1 #Increment by one because of Base duration col
            if j % 3 == 0:
                self.grid.SetCellSize(0, i, 1, 3)
                self.grid.SetColLabelValue(i, " ")
                self.grid.SetCellValue(1, i, "Min")
                self.grid.SetCellAlignment(1,i, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grid.SetCellAlignment(0,i, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grid.SetCellBackgroundColour (1, i, collor)
                self.grid.SetCellBackgroundColour (0, i, collor)

            elif j % 3 == 1:
                self.grid.SetColLabelValue(i, " ")
                self.grid.SetCellValue(1, i, "M.L")
                self.grid.SetCellAlignment(1,i, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grid.SetCellBackgroundColour (1, i, collor)
            
            elif j % 3 == 2:
                self.grid.SetColLabelValue(i, " ")
                self.grid.SetCellValue(1, i, "Max")
                self.grid.SetCellAlignment(1,i, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.grid.SetCellBackgroundColour (1, i, collor)
            
    def CreateRiskTable(self, event):
        
        #Create a risktable ooject
        R = act.risktable(frame.panel.project) # note that project is an instance which lives in panel which lives in frame

        #Adding riskdrivers and and effect:
        number_of_cols = self.grid.GetNumberCols()
        number_of_rows = self.grid.GetNumberRows()
        
        for i in range(0,number_of_cols,3):
            effect_on = []
            for j in range(number_of_rows):
                if not self.grid.GetCellValue(j+2,i+1) == "":
                    effect_on.append(int(j+2))
            
            R.AddRiskDriver(str(self.grid.GetCellValue(0,i+1)), effectiveon=effect_on)
             
            #Adding Riskdriver duration
            for i in range(0,number_of_cols,3):
                for j in range(number_of_rows):
                    if not self.grid.GetCellValue(j+2,i+1) == "":
                        Min = int(self.grid.GetCellValue(j+2,i+1))
                        ML = int(self.grid.GetCellValue(j+2,i+2))
                        Max = int(self.grid.GetCellValue(j+2,i+3))
                        R.AddRiskDriverDuration(int(j+1), str(self.grid.GetCellValue(0,i+1)), [Min,ML,Max])
        
        self.R = R
        
        pprint.pprint(self.R.GenerateTotalTimes())
        
    def SimulateRiskTable(self, event):
        
        #Get number of iterations from user
        dlg = wx.TextEntryDialog(self, 'Number of iterations:',"Simulation","1000", style=wx.OK)
        dlg.ShowModal()
        n = int(dlg.GetValue())
        dlg.Destroy()

        #Update from GUI network
        frame.panel.GetFromGui(event)
        frame.panel.project.Simulate(n, RiskTable=self.R)

        #Draw the histogram to tab one on Notebook
        #frame.panel.tabOne.DrawHistogram(self.project.networkends)
        #Draw the histogram to tab one on Notebook
        #frame.panel.tabFive.DrawSCurve(self.project.networkends)


class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):

    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class NoteBook(wx.Notebook):
    
    def __init__(self, panel, style=wx.BK_RIGHT):
        wx.Notebook.__init__(self, panel)


class TabPanel(wx.Panel, wx.ListCtrl):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        #make plot area
        self.figure = Figure(figsize=(1.0, 1.0))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        toolbar = NavigationToolbar2WxAgg(self.canvas)
        self.axes.grid()
        
        #make listctrl for activities
        self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0,"Assumptions and premisses")
        self.list_ctrl.SetColumnWidth(0, 450)
        
        #sizers
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 2, wx.EXPAND)
        self.sizer1 = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer1,1, wx.EXPAND|wx.ALL)
        self.sizer1.Add(toolbar)
        self.sizer1.Add(self.list_ctrl, 1, wx.EXPAND|wx.ALL)
        self.SetSizer(self.sizer)

    def DrawHistogram(self, data, cla=True):
        if cla == True:
            self.axes.cla()
            self.axes.grid()
        self.axes.hist(data, cumulative = False, bins = 25, normed=True)
        self.canvas.draw()
    
    def DrawSCurve(self, data, cla=True):
        if cla == True:
            self.axes.cla()
            self.axes.grid()
        self.axes.hist(data, cumulative = True, bins = len(data), normed=False, histtype='step', linewidth=2)
        self.canvas.draw()
    
    def FillListCtrl(self, activities):
        for i in range(len(activities)):
            self.list_ctrl.InsertStringItem(i, activities[i])
    

class Panel(wx.Panel):

    def __init__(self, parent):

        #splashscreen
        path = picturepath + "/Splash.bmp"
        image = wx.Image(path, wx.BITMAP_TYPE_BMP)
        bmp = image.ConvertToBitmap()
        wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 1000, None, -1)
        wx.Yield()
        
        panel = wx.Panel.__init__(self, parent)
        self.panel = panel
        #Setting constants
        self.index = 0
        self.activities = []
        self.today = act.datetime.date.today()
        
        #Building the wigits
        #self.CreateButtonBar(panel)
        self.CreateListCtrl(panel)
        self.CreateNoteBook(panel)
        self.CreateSizers()

    def CreateSizers(self):
        """Creates the main sizers"""
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        #self.sizer.Add(self.sizer1)
        self.sizer.Add(self.list_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(self.sizer)

    def CreateButtonBar(self, panel):
        #Buttons
        
        self.btn = wx.Button(self, label="Add Activity")
        self.btn.Bind(wx.EVT_BUTTON, self.AddActivity)
        self.btn1 = wx.Button(self, label="Simulate")
        self.btn1.Bind(wx.EVT_BUTTON, self.GetFromGui)
        #Set sizers
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer1.Add(self.btn, 0, wx.ALL|wx.CENTER, 5)
        self.sizer1.Add(self.btn1, 0, wx.ALL|wx.CENTER, 5)

    def CreateListCtrl(self, panel):
        """Creates the list ctrl"""
        self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT)
        self.headings = ['ID',
                         'Name',
                         'Start',
                         'End',
                         'Duration',
                         'Successor',
                         'predecessor',
                         'Min Duration',
                         'ML. Duration',
                         'Max Duration']
        column_size = 100
        for i in range(0,len(self.headings)):
            self.list_ctrl.InsertColumn(i, self.headings[i])
            self.list_ctrl.SetColumnWidth(i, column_size)
        
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnSelected, self.list_ctrl)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.UpdatePlot, self.list_ctrl)

    def CreateNoteBook(self, panel):
        self.notebook = NoteBook(self, panel)

        self.tabOne = TabPanel(self.notebook)
        
        self.tabTwo = TabPanel(self.notebook)
        self.tabThree = TabPanel(self.notebook)
        self.tabFour = TabPanel(self.notebook)

        self.tabFive = TabPanel(self.notebook)

        self.tabSix = TabPanel(self.notebook)

        self.notebook.AddPage(self.tabOne, "Histogram")
        self.notebook.AddPage(self.tabTwo, "Criticality")
        self.notebook.AddPage(self.tabThree, "Tronadodiagram")
        self.notebook.AddPage(self.tabFour, "Gantt Chart")
        self.notebook.AddPage(self.tabFive, "S - Curves")
        self.notebook.AddPage(self.tabSix, "Risk drivers")

    def AddActivity(self, event):
        number_of_activities = self.list_ctrl.GetItemCount()
        line = str(number_of_activities +1)
        l = int(line)-1
        self.list_ctrl.InsertStringItem(l, line)
        self.list_ctrl.SetStringItem(l, 1, "Name")
        self.list_ctrl.SetStringItem(l, 2, str(self.today))
        self.list_ctrl.SetStringItem(l, 3, str(self.today))
        self.list_ctrl.SetStringItem(l, 4, '1')
        
        #uodate network
        self.UpdateNetwork(event)

    def GetFromGui(self, event):
        try:
            del(self.project)
        except AttributeError:
            print "no project asigned"
        self.activities = []
        number_of_activities = self.list_ctrl.GetItemCount()
        number_of_headings = len(self.headings)
        self.project = act.network()
        
        for i in range(0,number_of_activities):
            self.activities.append(act.activity())
            try:
                self.activities[i].AssignID(int(self.list_ctrl.GetItem(i,0).GetText()))
            except:
                raise ValueError('Activity must have an ID')
            try:
                self.activities[i].AssignName(self.list_ctrl.GetItem(i,1).GetText())
            except ValueError:
                pass
            
            try:
                start = re.split('; |, |-|\n',self.list_ctrl.GetItem(i,2).GetText())
                self.activities[i].AssignStart(int(start[0]),int(start[1]),int(start[2]))
            except ValueError:
                pass  
            try:
                end = re.split('; |, |-|\n',self.list_ctrl.GetItem(i,3).GetText())
                self.activities[i].AssignEnd(int(end[0]),int(end[1]),int(end[2]))
            except ValueError:
                pass
            try:
                self.activities[i].AssignDuration(int(self.list_ctrl.GetItem(i,4).GetText()))
            except ValueError:
                pass
           
            try:
                suc = [str(q) for q in re.split('; |, |-|\n',self.list_ctrl.GetItem(i,5).GetText())]
                print suc
                self.activities[i].AssignSuccsesors(*suc)
            except ValueError:
                pass          
            try:
                pre = [int(q) for q in re.split('; |, |-|\n',self.list_ctrl.GetItem(i,6).GetText())]
                self.activities[i].AssignPredecesors(*pre)
            except ValueError:
                pass
            try:
                self.activities[i].SetDurationRangeMin(int(self.list_ctrl.GetItem(i,7).GetText()))
            except ValueError:
                pass
            try:
                self.activities[i].SetDurationRangeML(int(self.list_ctrl.GetItem(i,8).GetText()))
            except ValueError:
                pass
            try:
                self.activities[i].SetDurationRangeMax(int(self.list_ctrl.GetItem(i,9).GetText()))
            except ValueError:
                pass

        self.project.AddActivity(*self.activities)
        
        names = [q.GetName() for q in self.project.GetActivities()]

    def SaveFileAs(self, event):
        
        #update from GUI network
        self.GetFromGui(event)
        #dialogd
        dlg = wx.FileDialog(self, message="Save file as ...",  style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.project.SaveNetwork(path, heading=False)
        dlg.Destroy()

    def WriteNetworkToGUI(self, event, p):
        self.list_ctrl.DeleteAllItems()
        self.index = 0
        for q in p.GetActivities():

            self.list_ctrl.InsertStringItem(self.index, str(q.GetID()))
            self.list_ctrl.SetStringItem(self.index,1, str(q.GetName()))
            self.list_ctrl.SetStringItem(self.index,2, str(q.GetStart(asobject=True)))
            self.list_ctrl.SetStringItem(self.index,3, str(q.GetEnd(asobject=True)))
            self.list_ctrl.SetStringItem(self.index,4, str(q.GetDuration()))
            
            try:
                self.list_ctrl.SetStringItem(self.index,5, str(", ".join( str(e) for e in q.GetSuccsesors() )))
            except TypeError:
                pass
            try:
                self.list_ctrl.SetStringItem(self.index,6, str(", ".join( str(e) for e in q.GetPredecesors() )))
            except TypeError:
                pass
            
            self.list_ctrl.SetStringItem(self.index,7, str(q.GetDurationRangeMin()))
            self.list_ctrl.SetStringItem(self.index,8, str(q.GetDurationRangeML()))
            self.list_ctrl.SetStringItem(self.index,9, str(q.GetDurationRangeMax()))
            
            self.index= self.index + 1

    def OpenFile(self, event):
        self.list_ctrl.DeleteAllItems()
        dlg = wx.FileDialog(self, message="Open file ...",  style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            p = act.network()
            p.OpenNetwork(path)
            #write the network to the lisctrl
            self.WriteNetworkToGUI(event, p)
        #update from GUI network
        self.GetFromGui(event)
        dlg.Destroy()

    def Simulate(self, event):
        
        #Get number of iterations from user
        dlg = wx.TextEntryDialog(self.panel, 'Number of iterations:',"Simulation","1000", style=wx.OK)
        dlg.ShowModal()
        n = int(dlg.GetValue())
        dlg.Destroy()

        #Update from GUI network
        self.GetFromGui(event)

        self.dbfile =  os.path.join(dbpath, "simulationvariates.db")
        self.project.Simulate(n, DbName = self.dbfile)

        #Draw the histogram to tab one on Notebook
        self.tabOne.DrawHistogram(self.project.networkends)
        #Draw the histogram to tab one on Notebook
        self.tabFive.DrawSCurve(self.project.networkends)
    
    def UpdatePlot(self, event):
        
        #Getting id and variates
        CurrentRow = event.m_itemIndex
        Id = int(self.list_ctrl.GetItem(CurrentRow,0).GetText())
        Id = "ID" + str(Id)
        data = self.project.GetSimulationVariates(ID = Id, DbName=self.dbfile)
        
        #Updating
        self.tabOne.DrawHistogram(data)
        self.tabFive.DrawSCurve(data)
        
    def NewNetwork(self, event):

        self.list_ctrl.DeleteAllItems()
        self.SaveFileAs(event)
    
    def ShowGantt(self,event):
        self.GetFromGui(event)
        self.project.PlotGantt()

    def DeleteActivity(self, event):
        line_to_delete = self.list_ctrl.GetFocusedItem()
        self.list_ctrl.DeleteItem(line_to_delete)
        self.GetFromGui(event)
        self.WriteNetworkToGUI(event, self.project)

    def InsertActivity(self, event):
        self.GetFromGui(event)
        
        line_to_insert = self.list_ctrl.GetFocusedItem()
        line = str(line_to_insert +1)
        l = int(line)-1
        
        self.project.InsertActivity(ID=int(line))

        self.WriteNetworkToGUI(event, self.project)
        
        self.GetFromGui(event)
        
        self.PrintNetwork()
       
    def UpdateNetwork(self, event):
        self.GetFromGui(event)
        self.WriteNetworkToGUI(event, self.project)

    def OnSelected(self, event):
        CurrentColumn = int(event.m_col)
        CurrentRow = event.m_itemIndex
        ID = int(self.list_ctrl.GetItem(CurrentRow,0).GetText())
        Activitydict = self.project.GetNetworkIDDict()

        #update
        value_to_replace = event.GetText()
        print value_to_replace
        if CurrentColumn == 0:
            Activitydict[ID].AssignID(int(value_to_replace))
        
        elif CurrentColumn == 1:
            Activitydict[ID].AssignName(str(value_to_replace))

        elif CurrentColumn == 2:
            start = re.split('; |, |-|\n',str(value_to_replace))
            Activitydict[ID].AssignStart(int(start[0]),int(start[1]),int(start[2]))

        elif CurrentColumn == 3:
            end = re.split('; |, |-|\n',str(value_to_replace))
            Activitydict[ID].AssignEnd(int(end[0]),int(end[1]),int(end[2]))

        elif CurrentColumn == 4:
            Activitydict[ID].AssignDuration(int(value_to_replace))
            
        elif CurrentColumn == 5:
            suc = [str(q) for q in re.split('; |, |-|\n|,',str(value_to_replace))]
            print suc, "hehehejk"
            Activitydict[ID].AssignSuccsesors(*suc)

        elif CurrentColumn == 6:
            pre = [str(q) for q in re.split('; |, |-|\n|,',str(value_to_replace))]
            Activitydict[ID].AssignPredecesors(*pre)
        
        elif CurrentColumn == 7:
            Activitydict[ID].SetDurationRangeMin(int(value_to_replace))
        
        elif CurrentColumn == 8:
            Activitydict[ID].SetDurationRangeML(int(value_to_replace))
        
        elif CurrentColumn == 9:
            Activitydict[ID].SetDurationRangeMax(int(value_to_replace))

        
        self.WriteNetworkToGUI(event, self.project)
        self.GetFromGui(event)
        self.WriteNetworkToGUI(event, self.project)
        self.project.PrintNetwork()
    
    def OpenRiskTable(self,event):
        risktable = RiskTable(self.project.GetActivities())
        risktable.Show(True)


class MainFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "SimpleShedSimulator", pos=(0,0), size=wx.DisplaySize())
        self.panel = Panel(self)

        #topmenu
        menubar = wx.MenuBar()
        
        file = wx.Menu()
        OPEN = file.Append(-1, '&Open\tCtrl+o', 'Open a new document')
        NEW = file.Append(-1, '&New\tCtrl+n', 'Create a new network')
        SAVE_AS = file.Append(-1, '&Save as\tCtrl+s', 'Save the network')
        PRINT =  file.Append(-1, '&Print\tCtrl+p', 'Print the network')
        file.AppendSeparator()
        ABOUT = file.Append(-1, 'About')
        file.AppendSeparator()
        EXIT = file.Append(-1, 'Exit')
        #NEW.SetBitmap(wx.Bitmap('exit.png'))
        menubar.Append(file, '&File')
        
        network = wx.Menu()
        add_activity = network.Append(-1, '&Add activity\tCtrl+a', 'Add a new activity to the network')
        DELETE_ACTIVITY = network.Append(-1, '&Delete activity\tCtrl+d', 'Deletes the selected activity from the network')
        INSERT_ACTIVITY = network.Append(-1, '&Insert activity\tCtrl+i', 'Insert activity above selected activity')
        UPDATE_NETWORK = network.Append(-1, '&Update network\tF5', 'Updates the network')
        menubar.Append(network, '&Network')
        
        analysis = wx.Menu()
        SIMULATE = analysis.Append(-1, '&Simulate\tCtrl+s', 'Simulate network')
        RISKTABLE = analysis.Append(-1, '&Risk table\tCtrl+t', 'View and edit risktable')
        GENERATEREPORT = analysis.Append(-1, '&Generate report\tCtrl+g', 'Generate report')
        
        menubar.Append(analysis, '&Analysis')
        
        plotting = wx.Menu()
        SCURVE = plotting.Append(-1, '&S - Curve', 'Show cumulative distribution')
        HISTOGRAM = plotting.Append(-1, '&Histogram', 'Show distribution density')
        GANTT = plotting.Append(-1, '&Gantt Chart\tCtrl+g', 'View Gantt chart')
        menubar.Append(plotting, '&Plotting')
        
        self.SetMenuBar(menubar)  
        self.CreateStatusBar(number = 3)

        #Bindings
        self.Bind(wx.EVT_MENU, self.panel.OpenFile, OPEN)
        self.Bind(wx.EVT_MENU, self.panel.NewNetwork, NEW)
        self.Bind(wx.EVT_MENU, self.panel.SaveFileAs, SAVE_AS)
        self.Bind(wx.EVT_MENU, self.panel.Simulate, SIMULATE)
        self.Bind(wx.EVT_MENU, self.panel.AddActivity, add_activity)
        self.Bind(wx.EVT_MENU, self.panel.ShowGantt, GANTT)
        self.Bind(wx.EVT_MENU, self.OnPrint, PRINT)
        self.Bind(wx.EVT_MENU, self.panel.DeleteActivity, DELETE_ACTIVITY)
        self.Bind(wx.EVT_MENU, self.panel.InsertActivity, INSERT_ACTIVITY)
        self.Bind(wx.EVT_MENU, self.panel.UpdateNetwork, UPDATE_NETWORK)
        self.Bind(wx.EVT_MENU, self.OnQuit, EXIT)
        self.Bind(wx.EVT_MENU, self.OnAbout, ABOUT)
        self.Bind(wx.EVT_MENU, self.panel.OpenRiskTable, RISKTABLE)
        
        #Hotkeys
        OPEN_ID = wx.NewId()
        INSERT_ACTIVITY_ID = wx.NewId()
        UPDATE_NETWORK_ID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.panel.OpenFile, id=OPEN_ID)
        self.Bind(wx.EVT_MENU, self.panel.InsertActivity, id=INSERT_ACTIVITY_ID)
        self.Bind(wx.EVT_MENU, self.panel.UpdateNetwork, id=UPDATE_NETWORK_ID)
        
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL,  ord('o'), OPEN_ID),
                                         (wx.ACCEL_CTRL,  ord('i'), INSERT_ACTIVITY_ID),
                                         (wx.ACCEL_CTRL,  ord('u'), UPDATE_NETWORK_ID)
                                        ])
        
        self.SetAcceleratorTable(accel_tbl)
        
        self.Show()
    def OnPrint(self, event):
        data = wx.PrintDialogData()
        data.EnableSelection(True)
        data.EnablePrintToFile(True)
        data.EnablePageNumbers(True)
        data.SetMinPage(1)
        data.SetMaxPage(5)
        data.SetAllPages(True)
        dlg = wx.PrintDialog(self, data)
 
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetPrintDialogData()
            print 'GetAllPages: %d\n' % data.GetAllPages()
        dlg.Destroy()

    def OnAbout(self, event):
        info = wx.AboutDialogInfo()
        
        description = 'her er description'

        info.SetIcon(wx.Icon('Splash.bmp', wx.BITMAP_TYPE_BMP))
        info.SetName('SimpleShedSimulator')
        info.SetVersion('0.01')
        #info.SetDescription(description)
        info.SetCopyright('GPL')
        info.SetWebSite('https://github.com/Egdus/SimpleShedSimulator')
        #info.SetLicence(licence)
        info.AddDeveloper('Anders Jensen')
        info.AddDocWriter('Anders Jensen')
        info.AddArtist('Anders Jensen')
        info.AddTranslator('Anders Jensen')

        wx.AboutBox(info)

    def OnQuit(self, event):
        self.Close()


app = wx.App(False)
frame = MainFrame()
app.MainLoop()




