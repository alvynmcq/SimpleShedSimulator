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
            self.assertIsNone(activities.GetCritical(), msg)

if __name__ == '__main__':
    unittest.main()

