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

import datetime
import time
import sqlite3 as lite
import json
import pprint
import os
import sys
import stats
from triangular import triang
from table import MakeTable

#plotting with matplotlib:
import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib import dates
from tools import StrToInt, IntToStr, IO





class network:
    '''
    Creates an network instance. The network is based on previoulsy
    made activities

    ex::

       P = network()
       P.AddActivity(a,b,c,d,e,f,g,h,i)
       P.PrintNetwork()
       P.CalculateTotalFloats()

       for q in P:
           print q.GetID(), q.GetSlack()

       P.PlotGantt()
       P.Simulate()

    '''

    def __init__(self):
        self.activities = []
        self.today = datetime.date.today()
        self.IDs = []
        self.sortedby = ''
        self.enddate = None
        self.eddate_id = None
        self.startdate = None
        
        #find the db directory
        if os.name == 'nt':
            path_to_db = "\\".join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-1]) + "\\db"
            self.path_to_db = path_to_db + "\\Simulation_variates.db"
        elif os.name == 'posix':
            path_to_db = "/".join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-1]) + "/db"
            self.path_to_db = path_to_db + "/Simulation_variates.db"

    def __iter__(self):
        for activity in self.activities:
             yield activity

    def __getitem__(self, ID):
        return self.dictionary[ID]

    def __len__(self):
        return len(self.activities)

    def SetDictionary(self):
        d = []
        for activity in self.activities:
            d.append( (activity.GetID(),activity) )
        self.dictionary = dict(d)

    def __UpdateIDs(self):

        self.IDs = []
        try:
            for q in self.activities:
                self.IDs.append(q.GetID())
        except:
            pass

    def AssignName(self, name):

        '''Assigns a name to the activit inctance.

            Args:
                name (str): The activity name
            Returns:
                Sets self.name = name
            Raises:'''

        self.name = name

    def AddActivity(self, *args):

        '''Adds an activity to the network.

        Args:
            *args (object): the activity object name
        Returns:
            Sets self.activities and updatelinks
        Raises:'''

        initial_number_of_activities = len(self)

        #Make sure one does not add the same activity
        for i in range(0,len(args)):
            if args[i].GetID() in self.IDs: #Make sure one does not add object with same ID
                continue
            if args[i].GetID() == None: #Make sure one does not add object with  ID = None
                continue
            else:
                self.activities.append(args[i])

        self.__UpdateIDs()

        #Update links
        number_of_activities = len(self)
        if number_of_activities > initial_number_of_activities:
            self.UpdateLinks()

    def UpdateLinks(self):
        self.SetDictionary()
        for q in self.dictionary:
            try:
                a =1
                for w in self[q].GetSuccsesors():

                    #start-start
                    if IntToStr(w) in ['ss','SS','Ss','sS']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignPredecesors(qq)

                    #finish-start
                    elif IntToStr(w) in ['fs','FS','Fs','fS']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignPredecesors(qq)

                    #finish-finish
                    elif IntToStr(w) in ['ff','FF','Ff','fF']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignPredecesors(qq)

                    #start-finish
                    elif IntToStr(w) in ['sf','SF','Sf','sF']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignPredecesors(qq)

                    #no condition
                    else:
                        w = StrToInt(w)
                        self[w].AssignPredecesors(int(q))
            except:
                continue


        for q in self.dictionary:
            try:

                for w in self[q].GetPredecesors():

                    #start-start
                    if IntToStr(w) in ['ss','SS','Ss','sS']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignSuccsesors(qq)

                    #finish-start
                    elif IntToStr(w) in ['fs','FS','Fs','fS']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignSuccsesors(qq)

                    #finish-finsih
                    elif IntToStr(w) in ['ff','FF','Ff','fF']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignSuccsesors(qq)

                    #start-finish
                    elif IntToStr(w) in ['sf','SF','Sf','sF']:
                        qq = str(q) + IntToStr(w)
                        ww = StrToInt(w)
                        self[ww].AssignSuccsesors(qq)

                    #no condition
                    else:
                        w = StrToInt(w)
                        self[w].AssignSuccsesors(int(q))

            except:
                pass

    def GetNetworkIDDict(self):

        self.ID_dict = {}
        for q in self.activities:
            self.ID_dict[q.GetID()] = q

        return self.ID_dict

    def PrintNetwork(self, *args):

        '''Prints the network to terminal.

            Args:

            Returns:

            Raises:'''
        self.__ForwardPass() #recalculate project dates
        
        
        header = [heading for heading in args]
        data = [header]
        for i in self.IDs:
            try:
                row = []
                for heading in args:
                    if heading == 'ID':
                        row.append(str(self[i].GetID()))#, str(self[i].GetStart(asobject=True))]
                    if heading == 'Start':
                        row.append(str(self[i].GetStart(asobject=True)))
                    if heading == 'End':
                        row.append(str(self[i].GetEnd(asobject=True)))
                    if heading == 'Duration':
                        row.append(str(self[i].GetDuration()))
                    if heading == 'Slack':
                        row.append(str(self[i].GetSlack()))
                    if heading == 'DurationRangeML':
                        row.append(str(self[i].GetDurationRangeML()))
                    if heading == 'DurationRangeMax':
                        row.append(str(self[i].GetDurationRangeMax()))
                    if heading == 'DurationRangeMin':
                        row.append(str(self[i].GetDurationRangeMin()))
                    if heading == 'Name':
                        row.append(str(self[i].GetName()))
                    if heading == 'Predecesors':
                        row.append(str(self[i].GetPredecesors()))
                    if heading == 'Succsesors':
                        row.append(str(self[i].GetSuccsesors()))
                    if heading == 'Slack':
                        row.append(str(self[i].GetSlack()))

                
                data.append(row)
            except KeyError:
                continue
  
        print MakeTable(data)


        print "\n\n"
        print "OTHER INFORMATION:"
        print "------------------"
        print str('Deterministic Duration:').ljust(15), (self.GetNetworkEnd()-self.GetNetworkStart()).days
        print str('Deterministic Finish:').ljust(15), self.GetNetworkEnd()
        print str('Critical Path:').ljust(15), self.GetCriticalPath()
        print "\n"
        print "SIMULATION RESULTS:"
        print "-------------------"
        end_id = self.GetNetworkEnd(return_ID=True)
        start = self.GetNetworkStart(asobject=True)
        mean = self.GetSimulationMean(end_id)
        print str('E(x):').ljust(15), self.GetSimulationMean(end_id),  start + datetime.timedelta(mean)
        print str('P10:').ljust(15), self.GetSimulationPercentile(end_id, 0.1), self.GetSimulationPercentile(end_id, 0.1, date=True)
        print str('P50:').ljust(15), self.GetSimulationPercentile(end_id, 0.5), self.GetSimulationPercentile(end_id, 0.5, date=True)
        print str('P90:').ljust(15), self.GetSimulationPercentile(end_id, 0.9), self.GetSimulationPercentile(end_id, 0.9, date=True)
        print str('Var:').ljust(15), stats.var(self.GetSimulationVariates(ID = end_id))

    def GetName(self):

        '''Returns the name of the network

            Args:

            Returns:
                self.name (str)
            Raises:'''

        try:
            return self.name
        except AttributeError:
            print "No name assigend. Use the method AssignName()"

    def GetActivities(self):

        if len(self)>0:
            return self.activities
        else:
            print "No activities assigend to network. Use the method AssignActivity()"

    def __ForwardPass(self):

        '''Calculates the earliest starttimes for each activity. The
        method uses the forward pass algorithm to calculate the earliest start dates.

            Args:

            Returns:
                Assigns new starttime according to logic in network
            Raises:'''

        #Update links
        self.UpdateLinks

        for ID in self.IDs:
            try:
                P = self[ID].GetPredecesors() #predecesors for each activity i
                endtimes = []
            except KeyError:
                continue
            #handeling of predecessors
            try:
                for q in P:

                    #finish-start
                    if IntToStr(q) in ['fs','FS','Fs','fS']:
                        try:
                            endtimes.append(self.dictionary[StrToInt(q)].GetEnd(asobject=True)) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #start-start
                    elif IntToStr(q) in ['ss','SS','Ss','sS']:
                        try:
                            endtimes.append(self.dictionary[StrToInt(q)].GetStart(asobject=True)) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #finish-finish
                    elif IntToStr(q) in ['ff','FF','Ff','fF']:
                        try:
                            endtimes.append(self.dictionary[StrToInt(q)].GetEnd(asobject=True)
                                            - datetime.timedelta(days=self[ID].GetDuration())) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #start-finish
                    elif IntToStr(q) in ['Sf','SF','Sf','sF']:
                        try:
                            endtimes.append(self.dictionary[StrToInt(q)].GetStart(asobject=True)
                                            - datetime.timedelta(days=self[ID].GetDuration())) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #no condition
                    else:
                        q = int(q) #FS condition assumed
                        endtimes.append(self[q].GetEnd(asobject=True)) #endtimes for activity i's predeccesors

            except TypeError: #if no predecessor is found today is assumed
                endtimes.append(self.today) #this should be the project start date

            try:
                earliest_start_date = max(endtimes)  #max endtime equals earliest starttime
                self[ID].AssignStart(earliest_start_date.year,
                                               earliest_start_date.month,
                                               earliest_start_date.day) #assign earliest starttime
            except TypeError:
                pass

    def __BackwardPass(self):

        '''Calculates the Latest starttimes for each activity. The
        method uses the backward pass algorithm to calculate the earliest start dates.

            Args:

            Returns:
                Assigns new starttime according to logic in network
            Raises:'''

        #Update links
        enddate = self.GetNetworkEnd()
        self.UpdateLinks
        self.IDs.reverse()
        for ID in self.IDs:
            endtimes = []
            try:
                suc = self[ID].GetSuccsesors() #predecesors for each activity i
            except KeyError:
                continue
            #handeling of Succsesors
            try:
                for q in suc:

                    #finish start
                    if IntToStr(q) in ['fs','FS','Fs','fS']:
                        try:
                            endtimes.append(self[StrToInt(q)].GetStart(asobject=True)) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #start-start
                    elif IntToStr(q) in ['ss','SS','Ss','sS']:
                        try:
                            endtimes.append(self[StrToInt(q)].GetStart(asobject=True)
                                            +datetime.timedelta(days=self[ID].GetDuration())) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #finish-finish
                    elif IntToStr(q) in['ff','FF','Ff','fF']:
                        try:
                            endtimes.append(self.dictionary[StrToInt(q)].GetEnd(asobject=True)) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #start-finish
                    elif IntToStr(q) in ['Sf','SF','Sf','sF']:
                        try:
                            endtimes.append(self[StrToInt(q)].GetEnd(asobject=True)
                                            +datetime.timedelta(days=self[ID].GetDuration())) #endtimes for activity i's predeccesors
                        except KeyError:
                            continue

                    #no condition
                    else:
                        q = int(q) #FS condition assumed
                        endtimes.append(self[q].Getstart(asobject=True)) #endtimes for activity i's predeccesors

            except TypeError: #if no succsessor is found today is assumed
                endtimes.append(enddate)

            try:
                duration = datetime.timedelta(days=self[ID].GetDuration())
                earliest_start_date = min(endtimes) - duration  #max endtime equals earliest starttime
                self[ID].AssignStart(earliest_start_date.year,
                                               earliest_start_date.month,
                                               earliest_start_date.day) #assign earliest starttime
            except (TypeError, ValueError):
                pass
        self.IDs.reverse()

    def CalculateFreeFloats(self):
        '''
        Calculates each activity's free float for every activity in the network. For each activity instance the
        .SetSlack(free=True) method is called.
        '''
        #Update links and dates
        self.UpdateLinks
        self.__ForwardPass

        for i in self.IDs:
            try:
                S = self[i].GetSuccsesors() #predecesors for each activity i
                starttimes = []
            except KeyError:
                continue
            #handeling of predecessors
            try:
                for q in S:
                    if IntToStr(q) in ['fs','FS','Fs','fS']:
                        try:
                            starttimes.append(self[StrToInt(q)].GetStart(asobject=True)) #endtimes for activity i's succesors
                        except KeyError:
                            continue
                    else:
                        q = int(q) #FS condition assumed
                        starttimes.append(self[q].GetStart(asobject=True)) #endtimes for activity i's predeccesors

            except TypeError: #if no predecessor is found today is assumed
                starttimes.append(self.today)
            try:
                earlist_predesecor_starttime = min(starttimes)
                free_slack =  earlist_predesecor_starttime - self[i].GetEnd(asobject=True)

                self[i].SetSlack(free_slack, free = True)
            except:
                pass

    def GetPaths(self, start_activity_id=1, from_successors=True):

        def f(d):
            paths = []
            for key, value in d.items():
                if value is None:
                    paths.append([key, value])
                else:
                    internal_lists = f(value)
                    for l in internal_lists:
                        paths.append([key] + l)
            return paths

        if from_successors == True:
            def getsuccessors(ID):
                try:
                    path = {}
                    for q in self[StrToInt(ID)].GetSuccsesors():
                        path[StrToInt(q)] = getsuccessors(StrToInt(q))
                    return path
                except TypeError:
                    pass

            self.paths = getsuccessors(start_activity_id)

        else:
            def getpredecessors(ID):
                try:
                    path = {}
                    for q in self[StrToInt(ID)].GetPredecesors():
                        path[StrToInt(q)] = getpredecessors(StrToInt(q))

                    return path
                except TypeError:
                    pass

            self.paths = getpredecessors(start_activity_id)



        paths = f(self.paths)
        for path in paths:
            path.insert(0,start_activity_id)

        return paths

    def GetCriticalPath(self):
        '''
        Returns a list consisting of those activities which are critical. That is those activities which
        .GetSlack(free=False) = 0

        Args:

        Returns:
            list
        Raises:
        '''
        #find activity with latest enddate:
        network_end_ID = self.GetNetworkEnd(return_ID =True)
        paths = self.GetPaths(start_activity_id=network_end_ID, from_successors=False)

        critical_path = None
        duration = 0
        for path in paths:
            if duration < self.CalculatePathDuration(path):
                duration = self.CalculatePathDuration(path)
                critical_path = path

        return [x for x in critical_path if x is not None] #removes None values

    def CalculateTotalFloats(self):
        '''Calculates the total floats and assigns that float to corresponding activity'''

        self.__ForwardPass()
        early_starts = [q.GetStart(asobject=True) for q in self]

        self.__BackwardPass()
        late_starts = [q.GetStart(asobject=True) for q in self]

        ID = [q.GetID() for q in self]

        for ls, es, i in zip(late_starts,early_starts, ID):
            slack = (ls-es).days
            self[i].SetSlack(slack,free=False)

        self.__ForwardPass()

    def CalculatePathDuration(self, path):
        durations = []
        for ID in path:
            if ID is not None:
                durations.append(self[ID].GetDuration())

        return sum(durations)

    def GetNetworkEnd(self, asobject=True, return_ID=False):

        '''Get the last activity's end date

            Args:

            Returns:
                Returns a dattimeobject or a list
            Raises:'''

        #This should be updated to search throug those activities which only has None Succsessors
        self.__ForwardPass() #recalculate project dates
        if return_ID == False:
            enddates = []
            for q in self.activities:
                enddates.append(q.GetEnd(asobject))
            self.enddate = max(enddates)
            return self.enddate

        else:
            enddates = {}
            for q in self.activities:
                enddates[q.GetID()] = q.GetEnd(asobject)
            self.enddate_id = max(enddates, key=enddates.get)
            return self.enddate_id

    def GetNetworkStart(self, asobject=True):

        '''Get the first activity's start date

            Args:

            Returns:
                Returns a dattimeobject or a list
            Raises:'''
        starts = []
        for activity in self:
            starts.append(activity.GetStart(asobject=True))

        self.startdate = min(starts)
        return self.startdate

    def Simulate(self, n=10, WriteToDB=True, DbName="Simulation_variates.db", RiskTable = None):

        '''Simulates the network. n = 10 itterations is default (which off course is not enough!)
         Currently, the only avilable distribution is the triangular
         distribution (http://en.wikipedia.org/wiki/Triangular_distribution)
         The method allso gives you the opportunity to write the resulting endates, that is the duration (days) from
         project start to the relevant activity's enddate to a database file called Simulation_variates.db using SQLite
         This file is by default located in /db. You may allso simulate through a Risk table, for that see the documentation of the Driver module


            Args: n (int) number of itterations
                  WriteToDB (boealen) if True writes the endates to database
                  DbName (str) Name of database to create
                  end (boelan) write all activity's enddates to database (not yet working)

            Returns:
                Writes simulation variates to SQLite DB
            Raises:'''

        #updating the project
        #Removing old database file
        try:
            os.remove(DbName)
        except OSError:
            pass

        DbName = self.path_to_db
        current_durations = [activity.GetDuration() for activity in self]
        if WriteToDB == True:
            #Constructing appropriate database using SQLite
            db_string = ""
            for q in self.activities:
                db_string = db_string + "ID" + str(q.GetID()) + " TEXT" +  ", "
            db_string_dates =  "CREATE TABLE SimulationResults(" +  db_string[:-2] + ")"
            db_string_critical =  "CREATE TABLE SimulationResults_critical(" +  db_string[:-2] + ")"

            #Creating database
            con = lite.connect(DbName)
            cur = con.cursor()
            try:
                cur.execute(db_string_dates)
                cur.execute(db_string_critical)
            except:
                print "Database allready exists"
            con.commit() # Save (commit) the changes

        self.networkends = []
        """
        This loops assigns a random duration for each activity in the
        network, and calculates the endtime. This is done n times
        """
        #Generates n variates

        if RiskTable == None:

            for i in range(n):
                self.CalculateTotalFloats()
                #each activity is assigned a new duration here:
                for q in self.activities:
                    try:
                        Time = triang(min = q.minduration,
                                      ml = q.mlduration,
                                      max = q.maxduration)
                        T = Time.generate(1)[0]
                        q.AssignDuration(T)
                    except AttributeError:
                        continue
                self.__ForwardPass()
                #Only initiate if you want to write resukts to db
                if WriteToDB == True:
                    #Every endate for each activity is here:
                    enddates = []
                    criticality = []
                    for q in self.activities:
                        try:
                            duration = q.GetEnd(asobject=True)-self.GetNetworkStart(asobject=True)
                            enddates.append(duration.days)
                            critical = q.GetSlack(free=False)
                            criticality.append(critical)

                        except AttributeError:
                            continue
                    enddates = str(tuple(enddates))
                    criticality= str(tuple(criticality))
                    db_string_dates = "INSERT INTO SimulationResults VALUES" + enddates
                    db_string_criticality = "INSERT INTO SimulationResults_critical VALUES" + criticality
                    cur.execute(db_string_dates)
                    cur.execute(db_string_criticality)


                    enddate = (self.GetNetworkEnd() - self.GetNetworkStart()).days
                    self.networkends.append(enddate)


        else:

            for i in range(n):
                self.CalculateTotalFloats()
                #each activity is assigned a new duration here:
                T = RiskTable.GenerateTotalTimes() #this is a dict on the form {'ID':totaltime}
                for ID in T:
                    self.GetNetworkIDDict()[ID].AssignDuration(T[ID]) #activityinstance
                self.__ForwardPass()

                #Only initiate if you want to write resukts to db
                if WriteToDB == True:
                    #Every endate for each activity is here:
                    enddates = []
                    criticality = []
                    for q in self.activities:
                        try:
                            duration = q.GetEnd(asobject=True)-self.GetNetworkStart(asobject=True)
                            enddates.append(duration.days)
                            critical = q.GetSlack(free=False)
                            criticality.append(critical)


                        except AttributeError:
                            continue
                    enddates = str(tuple(enddates))
                    criticality= str(tuple(criticality))
                    db_string_dates = "INSERT INTO SimulationResults VALUES" + enddates
                    db_string_criticality = "INSERT INTO SimulationResults_critical VALUES" + criticality
                    cur.execute(db_string_dates)
                    cur.execute(db_string_criticality)

                    enddate = (self.GetNetworkEnd() - self.GetNetworkStart()).days
                    self.networkends.append(enddate)
        con.commit()
        con.close()
        
        for duration, activity in zip(current_durations, self):
            activity.AssignDuration(duration)


    def GetSimulationVariates(self,DbName="Simulation_variates.db", ID = 1, table="SimulationResults"):

        '''Returns the simulated variates from the simulation

            Args: DbName (str) name of database. by default: Simulation_variates.db
                  ID (str) The Id of the activity one whish to retriev variates of

            Returns:
                Returns a list consisting of integers. (days from project start to activity finish)
            Raises:'''
        DbName = self.path_to_db
        ID = "ID" + str(ID)
        try:
            con = lite.connect(DbName)
            cur = con.cursor()
            argument = "SELECT %s FROM %s" % (ID, table) #this should not be done like this, ses e python docs
            cur.execute(argument)
            return [int(i[0]) for i in cur.fetchall()]
        except:
            raise AttributeError('Could not find database file')

    def GetSimulationMean(self, I):
        return stats.mean(self.GetSimulationVariates(ID = I))

    def GetSimulationPercentile(self, I, p, date=False):
        variates = self.GetSimulationVariates(ID = I)
        variate = stats.percentile(variates, p)

        if date == True:

            return self.GetNetworkStart(asobject = True) + datetime.timedelta(variate)

        elif date == False:

            return int(variate)

    def PlotHistEnd(self, ID=1, cumulative = False, bins=20, normed = True):

        '''Plots the network enddate as a histogram (currently uses Matplotlib). By default the duration of activity 1 is plotted

            Args: ID (int), Cumulative (boolean), bins (int), normed (boolean)

            Returns:
                Returns a matplotlib object
            Raises:'''

        data = self.GetSimulationVariates(ID = ID)
        plt.hist(data, cumulative = cumulative, bins = bins, normed=normed)
        plt.grid()
        plt.show()

    def IncrementNetworkAt(self, ID, increment):

        '''Increment IDs ad ID. This is used to add activities

            Args: ID (int), increment (int)

            Returns:
                Increments the IDs
            Raises:'''

        for i in self.IDs:
            try:
                if i > ID:
                    self[i].IncrementID(increment)
                else:
                    continue
            except KeyError:
                continue

        #Updates those predecesors which id is bigger than ID
        for i in self.IDs:
                    try:
                        for pre in self[i].GetPredecesors():
                            IncrementedValues = []
                            #Checks which predecessors are bigger than the IDs and increment
                            if StrToInt(pre) > ID:
                                self[i].P.remove(pre) #Remove element
                                condition = IntToStr(pre)
                                IncrementedValues.append(str(StrToInt(pre) + increment) + condition) #Adds an incremented ID
                        self[i].P = self[i].P + IncrementedValues #Adds an incremented ID to initial list P

                    except TypeError:
                        continue

        #Updates successros which id is bigger than ID
        for i in self.IDs:
                    try:
                        for suc in self[i].GetSuccsesors():
                            IncrementedValues = []
                            #Checks which successros are bigger than the IDs and increment
                            if StrToInt(suc) > ID:
                                if self[i].GetID() < ID:
                                    self[i].S.remove(suc) #Remove element
                                    condition = IntToStr(suc)
                                    IncrementedValues.append(str(StrToInt(suc) + increment) + condition) #Adds an incremented ID

                        self[i].S = self[i].S + IncrementedValues #Adds an incremented ID to initial list P

                    except TypeError:
                        continue

        self[ID].IncrementID(increment, ID=False) #Increment Succsessors to activity ID asswell

        #dont forget to update the idlist:
        self.IDs = [q.GetID() for q in self]

    def InsertActivity(self, ID):
        '''
        Inserts an activity above ID
        ex::
           P.InsertActivity(ID=5)

        '''

        #make room for new activity
        self.IncrementNetworkAt(ID-1, increment = 1)

        # create a new activity instance
        Activity = activity()
        Activity.AssignDuration(1)
        Activity.AssignID(ID )
        Activity.AssignSuccsesors(ID+1)
        self.AddActivity(Activity)

        #Don't forget to sort the network
        self.SortNetwork()

    def SortNetwork(self, sorton = "x.GetID()"):
        '''
        Sorts the network acording to the sorton variable.

        Args: sorton (str)

        Returns:
                Sorts the list self.IDs
        Raises:''

        ex::
           P.SortNetwork(sorton = "x.GetDuration()")

        '''
        self.activities.sort(key = lambda x: eval(sorton))

        self.sortedby = sorton

        #dont forget to update the idlist:
        self.IDs = [q.GetID() for q in self]

    def PlotGantt(self):

        '''Plots the network in a ganttchart (currently uses Matplotlib). Currently, only the unic successors are marked with arrows
           It is only possible to plot a Gannt cahrt which is sorted acording to the activity IDs.

            Args:

            Returns:
                Returns a matplotlib object
            Raises:'''

        if self.sortedby is not "x.GetID()":
            self.SortNetwork()
        self.__ForwardPass()
        startdate = self.GetNetworkStart()
        enddate = self.GetNetworkEnd()
        ids = []
        starts = []
        ends = []
        preid = []
        for ID in self.IDs:
            ids.append(ID)
            starts.append((self[ID].GetStart(asobject=True) - startdate).days)
            ends.append((self[ID].GetEnd(asobject=True) - startdate).days)
            #adding horisontal lines to critical path
            try:
                pre = {}
                for preds in self[ID].GetPredecesors():
                    pre[self[StrToInt(preds)].GetEnd(asobject=True)] = preds
                preid.append(StrToInt(pre[max(pre)]))
            except:
                preid.append(None)

        # Plot a line for every activity
        plt.ylim(min(self.IDs)-1,max(self.IDs)+1)

        names = []
        for ID in self.IDs:
            if self[StrToInt(ID)].GetName() is not None:
                names.append(str(self[StrToInt(ID)].GetName()))
            else:
                names.append(str(ID))

        plt.yticks(self.IDs)
        plt.gca().set_yticklabels(names)
        plt.gca().invert_yaxis()
        plt.grid()
        plt.hlines(range(1,len(ids)+1), starts, ends, colors = 'green', lw = 9)
        plt.vlines(starts, ids, preid, colors = 'black', lw = 0)




        for q, w, e in zip(starts, range(1,len(ids)+1), preid):
            if e is not None:
                plt.annotate('', xy=(q,w), xytext=(q,e),arrowprops=dict(arrowstyle="-|>",
                            connectionstyle="angle,angleA=0,angleB=-100,rad=5")
                            )

        def mjrFormatter(x, pos):
            start = self.GetNetworkStart()
            difference = datetime.timedelta(x)
            return start + difference

        plt.gca().xaxis.set_major_formatter(mpl.ticker.FuncFormatter(mjrFormatter))

        plt.show()

    def SaveNetwork(self, path, heading=True):
        '''
        Saves the network to a .csv file

        Args: path

        Returns:

        Raises:
        '''

        self.__ForwardPass() #recalculate project dates

        output = open(path, 'w')

        if heading == True:
            output.write("ID;NAME;START;END;DURATION;SUCCSESSOR;PREDESESSOR;MINDURATION;MLDURATION;MAXDURATION \n")

        for i in self.IDs:
            #try:
            output.write(str(self[i].GetID()) + ";")
            output.write(str(self[i].GetName()) + ";"),
            output.write(str(self[i].GetStart(asobject=False)) + ";"),
            output.write(str(self[i].GetEnd(asobject=False)) + ";"),
            output.write(str(self[i].GetDuration()) + ";"),
            output.write(str(self[i].GetSuccsesors()) + ";"),
            output.write(str(self[i].GetPredecesors()) + ";"),
            output.write(str(self[i].GetDurationRangeMin()) + ";"),
            output.write(str(self[i].GetDurationRangeML()) + ";"),
            output.write(str(self[i].GetDurationRangeMax()) + ";"),
            output.write("\n")

    def OpenNetwork(self, path):

        input = open(path, 'r')
        for line in input:

            i = line.split(";")
            a = activity()
            a.AssignID(i[0])
            a.AssignName(i[1])

            start = eval(i[2])
            try:
                a.AssignStart(*start)
            except TypeError:
                pass

            end = eval(i[3])
            try:
                a.AssignEnd(*end)
            except TypeError:
                pass

            duration = int(i[4])
            a.AssignDuration(duration)

            sucsessor = eval(i[5])
            try:
                a.AssignSuccsesors(*sucsessor)
            except TypeError:
                pass

            predecessor = eval(i[6])
            try:
                a.AssignPredecesors(*predecessor)
            except TypeError:
                pass

            try:
                minduration = int(i[7])
                a.SetDurationRangeMin(minduration)
            except:
                pass

            try:
                mlduration = int(i[8])
                a.SetDurationRangeML(mlduration)
            except:
                pass

            try:
                maxduration = int(i[9])
                a.SetDurationRangeMax(maxduration)
            except:
                pass
            self.AddActivity(a)



