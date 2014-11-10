import path
import unittest
from act import activity
from net import network


class TestActClass(unittest.TestCase):

	def setUp(self):
		activities = [activity() for number in range(9)]
		[activities[i].AssignID(i+1) for i in range(9)]
		[activities[i].AssignDuration(10) for i in range(9)]
		[activities[i].AssignDurationRange(MIN=5, ML=9, MAX=40) for i in range(9)]
		[activities[i].AssignSuccsesors(i+2) for i in range(8)]
		self.P = network()
		self.P.AddActivity(*activities)

	def test_simulation(self):
		""" Tests if durations are set to original values after simulation"""
		pre_baseduration = [activity.GetDuration() for activity in self.P]
		self.P.Simulate(10)
		post_baseduration = [activity.GetDuration() for activity in self.P]
		msg = "Durations NOT set to original values after simulation"
		self.assertSequenceEqual(pre_baseduration, post_baseduration, msg)



if __name__ == '__main__':
	unittest.main()
	
