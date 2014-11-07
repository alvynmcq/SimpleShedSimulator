from simpleshedsimulator.core.act import activity
from simpleshedsimulator.core.net import network
import unittest


class TestActClass(unittest.TestCase):

	def setUp(self):
		
		activities = [activity() for number in range(10)]
		[activities[i].AssignSuccsesors(i+1) for i in range(10)]
		[activities[i].AssignDuration(0) for i in range(10)]
		[activities[i].AssignSuccsesors(i+1) for i in range(9)]
		
		
		P = Network()
		P.AddActivity(*activities)
		#P.PlotGantt()
		






if __name__ == '__main__':
	#unittest.main()
	activities = [activity() for number in range(10)]
	[activities[i].AssignID(i) for i in range(10)]
	[activities[i].AssignDuration(10) for i in range(10)]
	[activities[i].AssignSuccsesors(i+1) for i in range(9)]
	
	
	P = network()
	P.AddActivity(*activities)
	for i in P:
		print i.GetStart()
	P.PlotGantt()
