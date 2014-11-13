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
#standard modules
"""
The act module contains the activity class which is used to handle
activities. It implements various methods to handle and implement 
activities and every simpleshedsimulator project must have instances of
this class. The methods are mainly "setting"- and "getting" methods 
where various attributes can be assigned, changed or retrieved. After
initiating activity objects as in your project these objectes are then 
assigned to a network object which then allows yoy to control your 
network. For further information see the net module 
"""

import datetime
import time
import sqlite3 as lite
import os

#Simpleshedsimulator modules
import stats
from triangular import triang
from table import MakeTable
from tools import StrToInt, IntToStr, IO

#plotting with matplotlib:
import numpy as np
import matplotlib as mpl
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from matplotlib import dates



class activity:
    '''Creates an activity instance which later can be used by a
       network object

        Args:

        Returns:
            Object
        Raises:

        ex::

           a = activity()
           a.AssignID(1)
           a.AssignDuration(5)
           a.AssignSuccsesors(2)

                '''

    def __init__(self):

        self.today = datetime.date.today()

        self.free_critical = False
        self.total_critical = False
        self.free_critical_slack = None
        self.total_critical_slack = None

        self.early_start = None
        self.late_start = None
        self.early_finish = None
        self.late_finish = None

    def __eq__(self, other):

        return self.ID == other.ID

    def AssignID(self, ID):

        '''Assigns an ID to the activity. The smallest allowed ID is 1.

            Args:
                ID (int): Preffered ID of the activity
            Returns:
                Sets self.ID = ID.
            Raises:
            '''
        if ID < 1:
            errormessage = 'Cant have ID less than 1.'
            raise AttributeError(errormessage)
        else:  
            try:
                self.ID = int(ID)
            except:
                print "Assigned ID must be integer"

    def AssignName(self, name):

        '''Assigns a name to the activity inctance.

            Args:
                name (str): The activity name
            Returns:
                Sets self.name = name
            Raises:'''

        self.name = name

    def AssignStart(self, Y, M, D):

        '''Assigns a startdate to the activit inctance.

            Args:
                Y,M,D (int): The activity's startdate
            Returns:
                Sets self.start = datetime.date(Y,M,D) and calculates
                endate if possible.
            Raises:'''

        self.start = datetime.date(Y, M, D)
        try:
            difference = datetime.timedelta(self.duration)
            newdate = self.start + difference
            self.AssignEnd(newdate.year, newdate.month, newdate.day)
        except AttributeError:
            try:
                delta = self.end - self.start
                self.duration = delta.days
            except AttributeError:
                pass

    def AssignEnd(self, Y, M, D):

        '''Assigns a enddate to the activit inctance.

            Args:
                Y,M,D (int): The activity's enddate given as YYYY, mm,
                 dd
            Returns:
                Sets self.end = datetime.date(Y,M,D) and sets the
                duration if possible.
            Raises:'''

        self.end = datetime.date(Y, M, D)
        try:
            delta = self.end - self.start
            self.duration = delta.days
        except AttributeError:
            pass

    def AssignDuration(self, duration):

        '''Assigns a Duration to the activity inctance.

            Args:
                duraton (int): The activity's duration
            Returns:
                Sets self.duration = duration and sets the enddate
                if possible.
            Raises:

            '''

        self.duration = duration
        try:
            difference = datetime.timedelta(days=duration)
            newdate = self.start + difference
            self.AssignEnd(newdate.year, newdate.month, newdate.day)
        except AttributeError:
            return "No startdate assigend. Use the method AssignStart"

    def AssignSuccsesors(self, *args):

        '''Assigns succerssors to the activity inctance.

            Args:
                *args (int): The activity's successors
            Returns:
                Sets self.S = [] (list).
            Raises:'''

        #Add FS condition to empty predecessors
        arguments = []
        for q in args:
            try:
                q = int(q)
                if isinstance(q, int):
                    arguments.append(str(q) + 'FS')
                else:
                    arguments.append(q)
            except ValueError:
                arguments.append(q)
        args = arguments

        try:
            for q in args:
                if self.ID < StrToInt(q):
                    self.S.append(q)
                elif self.ID > StrToInt(q):
                    errormessage = 'Successor ID smaaler then Activity ID '
                    raise AttributeError(errormessage)

            #remove duplicates and convert to str()
            self.S = [str(i) for i in self.S]
            self.S = list(set(self.S))

            #Convert to uppercase
            suc = []
            for s in self.S:
                try:
                    suc.append(s.upper())
                except SyntaxError:
                    suc.append(s)
                    continue
            self.S = suc


        except:
            self.S = []
            for q in args:
                if self.ID < StrToInt(q):
                    self.S.append(q)
                elif self.ID > StrToInt(q):
                    errormessage = 'Successor ID smaaler then Activity ID '
                    raise AttributeError(errormessage)

            #remove duplicates and convert to str()
            self.S = [str(i) for i in self.S]
            self.S = list(set(self.S))

            #Convert to uppercase
            suc = []
            for s in self.S:
                try:
                    suc.append(s.upper())
                except SyntaxError:
                    suc.append(s)
                    continue
            self.S = suc

    def AssignPredecesors(self, *args):

        '''Assigns predecesors to the activity inctance.

            Args:
                *args (int): The activity's predecesors
            Returns:
                Sets self.P = [] (list).
            Raises:'''

        #Add FS condition to empty predecessors
        arguments = []
        for q in args:
            try:
                q = int(q)
                if isinstance(q, int):
                    arguments.append(str(q) + 'FS')
                else:
                    arguments.append(q)
            except ValueError:
                arguments.append(q)
        args = arguments

        try:
            for q in args:
                if self.ID > StrToInt(q):
                    self.P.append(q)
                elif self.ID < StrToInt(q):
                    raise AttributeError('Predecessor ID bigger then Activity ID ')

            #remove duplicates and convert to str()
            self.P = [str(i) for i in self.P]
            self.P = list(set(self.P))

            #Convert to uppercase
            pre = []
            for p in self.P:
                try:
                    pre.append(p.upper())
                except SyntaxError:
                    pre.append(p)
                    continue
            self.P = pre

        except:
            self.P = []
            for q in args:
                if self.ID > StrToInt(q):
                    self.P.append(q)
                elif self.ID < StrToInt(q):
                    raise AttributeError('Predecessor ID bigger then Activity ID ')
            #remove duplicates and convert to str()
            self.P = [str(i) for i in self.P]
            self.P = list(set(self.P))

            #Convert to uppercase
            pre = []
            for p in self.P:
                try:
                    pre.append(p.upper())
                except SyntaxError:
                    pre.append(p)
                    continue
            self.P = pre

    def GetStart(self, asobject=False):

        '''returns the startdate either as a list of times or
        as a datetimeobject.

            Args:
                asobject (boolean): Determines wether to return a
                timedateobject or a list of times
            Returns:
                return a timedateobject or a list of times
            Raises:'''

        try:
            if asobject == False:
                Start = []
                for q in str(self.start).split('-'):
                    Start.append(int(q))
                return Start
            elif asobject == True:
                return self.start
        except AttributeError:
            pass

    def GetEnd(self, asobject=False):

        '''returns the enddate either as a list of times or as a
         datetimeobject.

            Args:
                asobject (boolean): Determines wether to return
                a timedateobject or a list of times
            Returns:
                return a timedateobject or a list of times
            Raises:'''

        try:
            if asobject == False:
                End = []
                for q in str(self.end).split('-'):
                    End.append(int(q))
                return End
            elif asobject == True:
                return self.end

        except AttributeError:
            pass

    def GetDuration(self):

        '''Returns the duration of the activity

            Args:

            Returns:
                self.duration (int)
            Raises:'''

        try:
            return self.duration
        except AttributeError:
            pass

    def GetName(self):

        '''Returns the name of the activity

            Args:

            Returns:
                self.name (str)
            Raises:'''

        try:
            return self.name
        except AttributeError:
            pass

    def GetID(self):

        '''Returns the ID of the activity

            Args:

            Returns:
                self.ID (int)
            Raises:'''

        try:
            return self.ID
        except:
            print "No ID assigned. Use AssignID()."

    def GetSuccsesors(self):

        '''Returns the succsessors of the activity

            Args:

            Returns:
                self.S (list)
            Raises:'''

        try:
            return self.S
        except:
            return None

    def GetPredecesors(self):

        '''Returns the predecessors of the activity

            Args:

            Returns:
                self.P (list)
            Raises:'''

        try:
            return self.P
        except:
            return None

    def GetSummary(self):
        self.summary = []
        self.summary.append(self.GetID())
        self.summary.append(self.GetName())
        self.summary.append(self.GetDuration())
        self.summary.append(self.GetStart())
        self.summary.append(self.GetEnd())
        self.summary.append(self.GetSuccsesors())
        self.summary.append(self.GetPredecesors())
        return self.summary

    def EstablilshPredecesor(self, activity):
        startdate = activity.GetEnd()
        self.AssignStart(startdate[0], startdate[1], startdate[2])

    def SetCritical(self, critical, free=True):
        '''Sets the activity to critical

        Args: free (True/False)

        Returns:

        Raises:'''
        if free == True:
            if critical in ["yes", True, "y", "Y", "YES", "Yes"]:
                self.free_critical = True
        else:
            if critical in ["yes", True, "y", "Y", "YES", "Yes"]:
                self.total_critical = True

    def GetCritical(self, free=False):
        '''Returns True/false depending on criticality of activity
        (.SetCritical())

        Args: free (True/False)

        Returns:

        Raises:'''
        try:
            if free == True:
                return free_critical
            else:
                return total_critical
        except:
            return "None"

    def SetSlack(self, slack, free=False):
        '''Sets the slack of the activity

        Args: slack (int), free (True/False)

        Returns:

        Raises:'''
        if free == True:

            self.free_critical_slack = slack.days
            if self.free_critical_slack <= 0.0:
                self.free_critical_slack = 0
                self.SetCritical(True, free = True)

            elif self.free_critical_slack > 0.0:
                self.SetCritical(False, free = True)

        else:
            self.total_critical_slack = slack
            if self.total_critical_slack <= 0.0:
                self.SetCritical(True, free = False)
            elif self.total_critical_slack > 0.0:
                self.SetCritical(False, free = False)

    def GetSlack(self, free=False):
        '''Returns the slack of the activity

        Args:  free (True/False)

        Returns: int

        Raises:'''
        if free == True:
            return self.free_critical_slack
        else:
            return self.total_critical_slack

    def AssignDurationRange(self, **kwargs):
        '''Sets the duration range of the activity such that the 
        activity's duration is in the intervall [min, max] and mode 
        equal to ml.

        Args:

        Returns:

        Raises:

        ex::

           activity.AssignDurationRang(min=1, ml=2, max=3)

        '''

        for args in kwargs.items():
            if args[0] in ["min", "MIN", "Min"]:
                self.minduration = args[1]
            elif args[0] in ["max", "MAX", "Max"]:
                self.maxduration = args[1]
            elif args[0] in ["ml", "ML", "Ml"]:
                self.mlduration = args[1]

    def SetDurationRangeMin(self, MIN):
        '''Sets the minimum duration of the activity

        Args: MIN (int)

        Returns:

        Raises:

        '''
        self.minduration = MIN

    def SetDurationRangeML(self,ML):
        '''Sets the most likely duration of the activity

        Args: ML (int)

        Returns:

        Raises:

        '''
        self.mlduration = ML

    def SetDurationRangeMax(self,MAX):
        '''Sets the maximum duration of the activity

        Args: MAX (int)

        Returns:

        Raises:

        '''
        self.maxduration = MAX

    def GetDurationRangeMin(self):
        '''Returns the minimum duration

        Args:

        Returns: self.minduration (int)

        Raises:

        '''
        try:
            return self.minduration
        except:
            return None

    def GetDurationRangeML(self):
        '''Returns the most likely duration

        Args:

        Returns: self.mlduration (int)

        Raises:

        '''
        try:
            return self.mlduration
        except:
            return None

    def GetDurationRangeMax(self):
        '''Returns the maximum duration

        Args:

        Returns: self.maxduration (int)

        Raises:

        '''
        try:
            return self.maxduration
        except:
            return None

    def IncrementID(self, increment, SUC=True, PRE=False, ID = True):

        if ID == True:
            #increment id
            current_ID = self.GetID()
            newID = current_ID + increment
            self.AssignID(newID)

        #Increment Succsesors
        if SUC == True:
            newS = []
            try:
                for suc in self.S:
                    condition = IntToStr(suc)
                    newS.append(str(StrToInt(suc) + increment) + condition)

                self.S = newS

            except AttributeError:
                pass
