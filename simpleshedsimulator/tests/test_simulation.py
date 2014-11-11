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


import path
import unittest
from act import activity
from net import network


class TestNetClass(unittest.TestCase):
    """
    This class is meant for developing. The class defines some tests for
    the network class loacted in the net module
    """


    def setUp(self):
        activities = [activity() for number in range(9)]
        [activities[i].AssignID(i+1) for i in range(9)]
        [activities[i].AssignDuration(10) for i in range(9)]
        [activities[i].AssignDurationRange(MIN=5, ML=9, MAX=40) for i in range(9)]
        [activities[i].AssignSuccsesors(i+2) for i in range(8)]
        self.P = network()
        self.P.AddActivity(*activities)

    def test_DurationsAfterSimulation(self):
        """ Tests if durations are set to original values after simulation"""
        pre_baseduration = [activity.GetDuration() for activity in self.P]
        self.P.Simulate(10)
        post_baseduration = [activity.GetDuration() for activity in self.P]
        msg = "Durations NOT set to original values after simulation"
        self.assertSequenceEqual(pre_baseduration, post_baseduration, msg)

    def test_GetCritical(self):
        """Test if the .GetCritical() method returns None values"""
        msg = "Get Critical returns None"
        self.P.CalculateTotalFloats()
        for activities in self.P:
            self.assertIsNotNone(activities.GetCritical(), msg)

if __name__ == '__main__':
    unittest.main()

