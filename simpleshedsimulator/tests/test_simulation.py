import path
import unittest
from act import activity
from net import network


class TestActClass(unittest.TestCase):

	def setUp(self):
		
		activities = [activity() for number in range(10)]
		[activities[i].AssignSuccsesors(i+1) for i in range(10)]
		[activities[i].AssignDuration(0) for i in range(10)]
		[activities[i].AssignSuccsesors(i+1) for i in range(9)]
		P = Network()
		P.AddActivity(*activities)
		

if __name__ == '__main__':
	unittest.main()
	
