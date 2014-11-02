'''
    SimpleShedSimulator for quick schedule risk analysis
    Copyright (C) 2014  Anders Jensen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''


from simpleshedsimulator.core.act import activity
from simpleshedsimulator.core.net import network
from simpleshedsimulator.core.driver import risktable


if __name__ == "__main__":
    a = activity()
    a.AssignID(1)
    a.AssignDuration(5)
    a.AssignSuccsesors(2)

    b = activity()
    b.AssignID(2)
    b.AssignDuration(7)
    b.AssignSuccsesors("4ff")



    c = activity()
    c.AssignID(3)
    c.AssignDuration(30)

    d = activity()
    d.AssignID(4)
    d.AssignDuration(10)
    #d.AssignPredecesors(2)
    d.AssignSuccsesors(5)


    e = activity()
    e.AssignID(5)
    e.AssignDuration(3)
    e.AssignPredecesors(3,4)
    e.SetDurationRange(min=0, ml=0,max=10)

    f = activity()
    f.AssignID(6)
    f.AssignDuration(8)
    f.AssignPredecesors(5)
    f.SetDurationRange(min=1, ml=8,max=8)

    g = activity()
    g.AssignID(7)
    g.AssignDuration(10)
    g.AssignPredecesors(6,2,1)
    g.SetDurationRange(min=1, ml=4,max=10)

    h = activity()
    h.AssignID(8)
    h.AssignDuration(10)
    h.AssignPredecesors('6ss')
    h.SetDurationRange(min=3, ml=7,max=23)

    i = activity()
    i.AssignID(9)
    i.AssignDuration(10)
    i.AssignPredecesors(7,8)
    i.SetDurationRange(min=3, ml=7,max=50)

    j = activity()
    j.AssignID(10)
    j.AssignDuration(5)
    j.AssignPredecesors(2)


    P = network()
    
    P.AddActivity(a,b,c,d,e,f,g,h,i,j)

    P.CalculateTotalFloats()

    P.Simulate(n=1000)
    P.PrintNetwork('ID', 'Start','Duration', 'End', 'Slack', 'DurationRangeMin', 'DurationRangeML', 'DurationRangeMax')
    R = risktable(P) #create the risk table
    R.AddRiskDriver('riskrdiver_1', [1,2,3]) #add riskdriver_1 and they are effective on activity with id 1,2 and 3
    R.AddRiskDriver('riskrdiver_2', [4,5,6]) #add riskdriver_1 and they are effective on activity with id 4, 5 and 6
    R.AddRiskDriver('riskrdiver_3', [6,7,8,9,10]) #add riskdriver_1 and they are effective on activity with id 4, 5 and 6

    
    R.AddRiskDriverDuration(1, 'riskrdiver_1', [10,11,12]) #riskdriver_1 have an additional effect on activity 1
    R.AddRiskDriverDuration(2, 'riskrdiver_1', [10,11,12])
    R.AddRiskDriverDuration(3, 'riskrdiver_1', [10,11,12])
    R.AddRiskDriverDuration(4, 'riskrdiver_2', [10,11,12])
    R.AddRiskDriverDuration(5, 'riskrdiver_2', [10,11,12])
    R.AddRiskDriverDuration(6, 'riskrdiver_2', [10,11,12])
    R.AddRiskDriverDuration(6, 'riskrdiver_3', [10,11,12])
    [R.AddRiskDriverDuration(id, 'riskrdiver_3', [10,11,12]) for id in range(7,11)]
        
    R.PrintRiskTable() #dumps the risktable in json format
    R.GenerateTotalTimes() #generate durations based on the table







