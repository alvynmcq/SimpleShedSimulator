import path
import unittest
from act import activity


class TestActClass(unittest.TestCase):

	def setUp(self):
		self.activity = activity()

	def test_id(self, ID = 1):
		self.activity.AssignID(ID)
		self.assertEqual(self.activity.GetID(), ID)
	
	def test_duration(self, duration = 10):
		self.activity.AssignDuration(duration)
		self.assertEqual(self.activity.GetDuration(), duration)
	

if __name__ == '__main__':
	unittest.main()

