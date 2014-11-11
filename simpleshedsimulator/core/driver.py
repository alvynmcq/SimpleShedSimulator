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


from table import MakeTable
from triangular import triang


class risktable:
    """
    Creates a risktable object which can be simulated through. A risk table with 3 riskdrivers and
    4 activities is on the form:

    +------------+------------+-----------+-----------+
    |            |Riskdriver 1|Riskdriver2|Riskdriver3|
    +============+============+===========+===========+
    | activity_1 | [10,11,12] |           |           |
    +------------+------------+-----------+-----------+
    | activity_2 |            |[23,44,49] |[10,11,12] |
    +------------+------------+-----------+-----------+
    | activity_3 |            |           |[2, 3, 16] |
    +------------+------------+-----------+-----------+
    | activity_4 |            |[10,11,12] |           |
    +------------+------------+-----------+-----------+

    ex::

       P = network() #creates a network
       P.AddActivity(a,b,c,d,e,f,g,h,i) #add the activities a,b,c,..i

       R = risktable(P) #create the risk table
       R.AddRiskDriver('riskrdiver_1', [1,2,3]) #add riskdriver_1 and they are effective on activity with id 1,2 and 3
       R.AddRiskDriver('riskrdiver_2', [4,5,6]) #add riskdriver_1 and they are effective on activity with id 4, 5 and 6
       R.AddRiskDriverDuration(1, 'riskrdiver_1', [10,11,12]) #riskdriver_1 have an additional effect on activity 1
       R.AddRiskDriverDuration(2, 'riskrdiver_1', [10,11,12])
       R.AddRiskDriverDuration(3, 'riskrdiver_1', [10,11,12])
       R.AddRiskDriverDuration(4, 'riskrdiver_2', [10,11,12])
       R.AddRiskDriverDuration(5, 'riskrdiver_2', [10,11,12])
       R.AddRiskDriverDuration(6, 'riskrdiver_2', [10,11,12])
       R.PrintRiskTable() #dumps the risktable in json format
       R.GenerateTotalTimes() #generate durations based on the table

    """

    def __init__(self, net):
        self.riskdrivers = {}
        self.net = net
        self.table = {}
        for q in self.net:
            self.table[q.GetID()] = {}

    def AddRiskDriver(self, name, effectiveon = []):
        '''
        Adds a risk driver to the risktable

        Args: name (str), effectiveon (list)

        Returns: sets self.riskdrivers[name] = effectiveon

        Raises:
        '''
        self.riskdrivers[name] = effectiveon

    def Update(self):
        for q in self.table:
            for w in self.riskdrivers:
                for e in self.riskdrivers[w]:
                    self.table[e][w] = []

    def AddRiskDriverDuration(self, ID, riskdriver, parameters):
        '''
        Adds quantification and assigns which activity the riskdriver impacts.
        The risk driver must first be created with .AddRiskDriver()

        Args: ID (int), riskdriver (str) parameters (list)

        Returns: adds an impact on an activity with an effect

        Raises:

        In the example below riskdriver_1 has an effect on activity with ID=3 the effect is an additional duration
        which is distributed triangulary with min=10, ml=11 and max=12

        ex::

           R.AddRiskDriverDuration(3, 'riskrdiver_1', [10,11,12])

        '''
        self.table[ID][riskdriver] = parameters

    def PrintRiskTable(self):
        '''
        Dumps the risktable to screen

        Args:

        Returns: prints to screen in json format

        Raises:
        '''
        
        data = []
        heading = ["id"]
        for driver in self.riskdrivers.keys():
            heading.append(driver)
        data.append(heading)
        
        
        for id in self.table:
            row = []
            row.append(str(id))
            for riskdriver in self.riskdrivers:
                if id in self.riskdrivers[riskdriver]:
                    try:
                        row.append(str(self.table[id][riskdriver]))
                    except KeyError:
                        continue
                else:
                    row.append("")
            data.append(row)

        print MakeTable(data)

    
    def GenerateTotalTimes(self):
        '''
        Generate activity durations based on the quantification of the risk table

        Args:

        Returns: dictionary

        Raises:

        In the example below a risk table R has allready been created

        ex::

           R.GenerateTotalTimes() #generate durations based on the table

        '''
        times = {}
        for q in self.table:
            totaltime = []
            for w in self.table[q]:
                base_duration = self.net.GetNetworkIDDict()[q].GetDuration() #extract all durations
                params = self.table[q][w]
                T = triang(min=params[0], ml=params[1], max=params[2]).generate(1)[0]
                totaltime.append(base_duration + T)
                times[q] = sum(totaltime)

        return times




