import re
import pprint

#wx
import wx
import wx.lib.mixins.listctrl  as  listmix
import wx.grid as  gridlib
import wx.stc as stc
import code
import __main__

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
import riskregister
path = os.path.dirname(os.path.realpath(__file__))
path = os.path.abspath(path)
path = os.path.split(path)[0]

picturepath = os.path.join(path, 'pictures')
dbpath = os.path.join(path, 'db')

sys.path.append(path)


from core import act
from core import xml_writer as xml

class II(code.InteractiveInterpreter):
    def __init__(self, locals):
        code.InteractiveInterpreter.__init__(self, locals)
    def Runit(self, cmd):
        code.InteractiveInterpreter.runsource(self, cmd)




class RiskTable(wx.Frame):
    """Enables the Risk driver method"""

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
        
        #add sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.grid, 1,wx.RIGHT|wx.EXPAND, 5)
        sizer.Add(sizer1)
        panel.SetSizer(sizer)
        
        #add menubar
        menubar = wx.MenuBar()
        #File menu
        file = wx.Menu()
        OPEN = file.Append(-1, '&Open risk table\tCtrl+o', 'Open an existing risk table')
        SAVE = file.Append(-1, '&Save risk table\tCtrl+s', 'Save current risk table')
        file.AppendSeparator()
        LOAD = file.Append(-1, '&Import risk drivers\tCtrl+o', 'Load risk drivers from excisting riskregister')
        menubar.Append(file, '&File')
        
        #File menu
        analysis = wx.Menu()
        ADDRISKDRIVER = analysis.Append(-1, '&Add risk driver\tCtrl+a', 'Add risk driver to project')
        SIMULATE = analysis.Append(-1, '&Simulate\tCtrl+s', 'Simulate through risk table')
        menubar.Append(analysis, '&Analysis')
        self.SetMenuBar(menubar)
        
        #Bindings
        self.Bind(wx.EVT_MENU, self.LoadRiskAreas, LOAD)
        self.Bind(wx.EVT_MENU, self.SimulateRiskTable, SIMULATE)
        self.Bind(wx.EVT_MENU, self.AddRiskDriver, ADDRISKDRIVER)
        self.Bind(wx.EVT_MENU, self.SaveRiskTable, SAVE)
        self.Bind(wx.EVT_MENU, self.OpenRiskTable, OPEN)
        
        #add  statusbar
        self.CreateStatusBar() 
        
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

    def AddRiskDriver(self, event, riskdriver_name=" "):
        '''Enables the Risk driver method'''
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
                self.grid.SetCellValue(0, i, riskdriver_name)
                self.grid.SetColLabelValue(i, "")
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
        
    def SimulateRiskTable(self, event):
        """
        Simulates the risk table
        Args:
                
        Returns:
               
        Raises:
        """
        #create risk table
        self.CreateRiskTable(event)
        
        #Get number of iterations from user
        dlg = wx.TextEntryDialog(self, 'Number of iterations:',"Simulation","1000", style=wx.OK)
        dlg.ShowModal()
        n = int(dlg.GetValue())
        dlg.Destroy()

        #Update from GUI network
        frame.panel.GetFromGui(event)
        Panel.dbfile =  os.path.join(dbpath, "simulationvariates.db")
        frame.panel.project.Simulate(n, RiskTable=self.R,DbName = Panel.dbfile )

    def LoadRiskAreas(self, event):
        """
        Opens a dialog and allows you to parse riskregisters for risk drivers. Then inserts the risk drivers to the 
        grid 
        Args:
                
        Returns:
               
        Raises:
        """

        dlg = wx.FileDialog(self, message="Open file ...",  style=wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            register = xml.FileReader().ReadFile(path)
            
            risk_drivers = []
            for riskdescriptions in register:
                for items in riskdescriptions:
                    if items.tag == "RiskDriver":
                        risk_drivers.append(items.text)

            
            for riskdriver in risk_drivers:
                self.AddRiskDriver(event) 
            
            for i in range(len(risk_drivers)):
                self.grid.SetCellValue(0, 3*i+1, risk_drivers[i]) #r3*1 because each 3 cells are merged

    def SaveRiskTable(self, event):
        '''
        This method reads the risk table, opens a save as dialog and then writes the risk table to an "xml file"
        
        Cannot treat activities having multiple names
        '''
        
        #establis xmlobject
        risktable = xml.FileWriter("risk_table")
        
        #Get number of cols and row, this should be global variables...
        number_of_cols = self.grid.GetNumberCols()
        number_of_rows = self.grid.GetNumberRows()
        
        #Obtaining activities
        for j in range(number_of_rows):
            activity = str(self.grid.GetRowLabelValue(j))
            if not activity == " ":
                activity = activity.replace(" ", "_")

                risktable.AddRow(activity)
                
                #Obtaining base durations
                risktable.AddRowAttribute(activity, "baseduration", self.grid.GetCellValue(j,0)) 
                
                #Obtaining Riskdrivers and setting quantification
                for i in range(1,number_of_cols,3):
                    riskdriver = self.grid.GetCellValue(0,i)
                    Min = self.grid.GetCellValue(j,i+0)
                    ML = self.grid.GetCellValue(j,i+1)
                    Max = self.grid.GetCellValue(j,i+2)
                    quantification = str(Min) + "-" + str(ML) + "-" + str(Max)
                    risktable.AddRowItems(activity, riskdriver, quantification)
        

        #Save dialog
        dlg= wx.FileDialog ( None, style = wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            path=dirname + '/' + filename + ".xml"
            risktable.WriteToFile(path)
        dlg.Destroy()

    def OpenRiskTable(self, event):
        '''
        This method opens an existing "xml like file containing a risk table
        '''
        #Open dialog
        dlg= wx.FileDialog ( None, style = wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetFilename()
            dirname = dlg.GetDirectory()
            path=dirname + '/' + filename 

            #make risktable object
            risktable = xml.FileReader().ReadFile(path)
            
            #Deletes existing risktable by cols and rows
            [self.grid.DeleteRows(0) for i in range(self.grid.GetNumberRows())] 
            [self.grid.DeleteCols(0) for i in range(self.grid.GetNumberCols())]

            #Creation of grid
            number_of_activities = len(risktable)

            #Fix the columns and headers accordingly
            self.grid.AppendRows(number_of_activities+2)
            self.grid.SetRowLabelValue(0, " ") #this is where Riskdriver comes
            self.grid.SetRowLabelValue(1, " ") #this is where ML min max comes
            
            self.grid.SetRowLabelAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
            self.grid.SetRowLabelSize(150) # should do this with self.grid.AutoSizeRow(i)
            
            self.grid.InsertCols(pos=0, numCols = 1, updateLabels = False)
            collor = self.grid.GetLabelBackgroundColour()
            self.grid.SetCellBackgroundColour (0, 0, collor)
            self.grid.SetCellBackgroundColour (1, 0, collor)
        
            self.grid.SetCellValue(1,0, "Base")
            self.grid.SetCellAlignment(1,0, wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
            
            #Insert activity names
            for i in range(len(risktable)):
                rowlabel = str(risktable[i].tag).replace("_", " ")
                self.grid.SetRowLabelValue(2+i, rowlabel)
                self.grid.SetCellValue(2+i, 0, str(risktable[i].attrib['baseduration']))
            
            risk_drivers = risktable[0][:]
            
            #Add riskdrivers to table
            for riskdriver in risk_drivers:
                self.AddRiskDriver(event) 
            
            #Insert riskdrivers 
            for i in range(len(risk_drivers)):
                self.grid.SetCellValue(0, 3*i+1, str(risk_drivers[i].tag)) #r3*1 because each 3 cells are merged
            
            #Insert quantification by looping trhough each activity's riskdrivers and count
            row_number = 2
            for activity in risktable:
                
                col_number = 1
                for quant in activity:
                    
                    if quant.text == "--":
                        col_number = col_number + 3
                        continue
                        
                    else:
                        quantification = quant.text.split("-")
                        self.grid.SetCellValue(row_number, col_number+0, quantification[0])
                        self.grid.SetCellValue(row_number, col_number+1, quantification[1])
                        self.grid.SetCellValue(row_number, col_number+2, quantification[2])
                        col_number = col_number + 3

                row_number = row_number + 1
            
        dlg.Destroy()




class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):

    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class NoteBook(wx.Notebook):
    
    def __init__(self, panel, style=wx.BK_RIGHT):
        wx.Notebook.__init__(self, panel)


class Terminal(stc.StyledTextCtrl):

    def __init__(self, parent, ID, style=0):
        stc.StyledTextCtrl.__init__(self, parent, style)
        sys.stdout = self
        sys.stderr = self
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.cmd = ''
        self.lastpos = self.GetCurrentPos()
        self.AppendTextUTF8("Welcome to SimpleShedSimulator! \n ...\n")
    def SetInter(self, interpreter):
        self.inter = interpreter
    def write(self, ln):
        self.AppendTextUTF8('%s'%str(ln))
        self.GotoLine(self.GetLineCount())
    def OnKeyPressed(self, event):
        self.changed = True 
        char = event.GetKeyCode() # get code of keypress
        if (self.GetCurrentPos() < self.lastpos) and (char <314) or (char > 317):
            pass
            # need to check for arrow keys in this
        elif char == 13:
            """
            What to do if <enter> is pressed? It depends if
            there are enough
            instructions
            """
            lnno = self.GetCurrentLine()
            ln = self.GetLine(lnno)
            self.cmd = self.cmd + ln + '\r\n'
            self.NewLine()
            self.tabs = ln.count('\t') #9
            if (ln.strip() == '') or ((self.tabs < 1) and (':' not in ln)):
                # record command in command list
                self.cmd = self.cmd.replace('\r\n','\n')
                # run command now
                self.inter.Runit(self.cmd)
                self.cmd = ''
                self.lastpos = self.GetCurrentPos()
            else:
                if ':' in ln:
                    self.tabs = self.tabs + 1
                    self.AppendText('\t' * self.tabs)
                    # change cursor position now
                    p = self.GetLineIndentPosition(lnno + 1)
                    self.GotoPos(p)
        else:
            event.Skip() # ensure keypress is shown


class TabPanel(wx.Panel, wx.ListCtrl):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        #make plot area
        self.figure = Figure(figsize=(1.0, 1.0))
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        toolbar = NavigationToolbar2WxAgg(self.canvas)
        self.axes.grid()
        
        self.list_ctrl = EditableListCtrl(self, style=wx.LC_REPORT)

        
        
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
    
    def DrawCriticalActivities(self, data=None, cla=True):
        if cla == True:
            self.axes.cla()
            self.axes.grid()
        self.axes.hist(data, cumulative = False, bins = 25, normed=True)
        self.canvas.draw()
    
    def FillListCtrl(self, activities):
        for i in range(len(activities)):
            self.list_ctrl.InsertStringItem(i, activities[i])

    def DrawGannt(self):
        pass


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
        #self.CreateTerminal(panel) #To enable terminal:uncomment here!
        self.CreateSizers()

    def CreateSizers(self):
        """Creates the main sizers"""
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer1 =  wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.sizer1,1, wx.ALL|wx.EXPAND, 5)
        self.sizer1.Add(self.list_ctrl, 2, wx.ALL|wx.EXPAND, 5)
        #self.sizer1.Add(self.terminal, 1, wx.ALL|wx.EXPAND, 5) #To enable terminal:uncomment here!
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
                         'Predecessor',
                         'Min Duration',
                         'ML. Duration',
                         'Max Duration'
                         ]
        column_size = 110
        for i in range(0,len(self.headings)):
            self.list_ctrl.InsertColumn(i, self.headings[i])
            self.list_ctrl.SetColumnWidth(i, column_size)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.UpdatePlot, self.list_ctrl)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnSelected, self.list_ctrl) #Dont use wx.EVT_LIST_END_LABEL_EDIT because of late update
        #self.Bind(wx.wx.EVT_LIST_END_LABEL_EDIT, self.OnSelected, self.list_ctrl)
        
        
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

    def CreateTerminal(self, panel):
        self.terminal = Terminal(self, -1) 

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
                suc = [str(q) for q in re.split('; |, |-|\n|;|,|',self.list_ctrl.GetItem(i,5).GetText())]
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
        
        names = [q.GetName() for q in self.project]

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
        for q in p:

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
        
        data = self.project.GetSimulationVariates(ID = Id, DbName=self.dbfile)
       
        data_criticality = self.project.GetSimulationVariates(ID = Id, DbName=self.dbfile, table = "SimulationResults_critical")

        #Updating
        self.tabOne.DrawHistogram(data)
        self.tabFive.DrawSCurve(data)
        self.tabTwo.DrawCriticalActivities(data_criticality)
        
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

        self.GetFromGui(event)
        self.project.UpdateLinks()
        self.WriteNetworkToGUI(event, self.project)
        self.project.PrintNetwork()
    
    def OpenRiskTable(self,event):
        risktable = RiskTable(self.project.GetActivities())
        risktable.Show(True)
    
    def OpenRiskRegister(self,event):
        app = riskregister.wx.PySimpleApp()
        frame = riskregister.RiskRegister(None, 'Risk register')
        frame.Show()
        app.MainLoop()


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
        RISKREGISTER = analysis.Append(-1, '&Risk register\tCtrl+r', 'Risk register')
        
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
        self.Bind(wx.EVT_MENU, self.panel.OpenRiskRegister, RISKREGISTER)
        
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
I = II(None)
frame = MainFrame()
#frame.panel.terminal.SetInter(I) #To enable terminal:uncomment here!

app.MainLoop()




