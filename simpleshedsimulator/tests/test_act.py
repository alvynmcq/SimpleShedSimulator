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

