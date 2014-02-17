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



import random

class triang:
	'''Creates a triang object

			Args: min (float), ml (float) max (float)

			Returns: Returns a triang object
			
			Raises:'''

	def __init__(self, **kwargs):
		
		for q in kwargs.items():
			if q[0] in ["min", "MIN", "Min"]:
				self.min = q[1]
			elif q[0] in ["max", "MAX", "Max"]:
				self.max = q[1]
			elif q[0] in ["ml", "ML", "Ml"]:
				self.ml = q[1]

	def cdf(self, x):
		
		'''Returns the CDF of the ttriangular distribution

			Args: x (float)

			Returns:
			
			Raises:'''
		
		if x < self.min:
			return 0
		
		elif self.min <= x <= self.ml:
			return  (x - self.min)**2 / ((self.max - self.min)*(self.ml-self.min))

		elif self.ml < x <= self.max:
			return  1 - (self.max - x)**2 / ((self.max - self.min)*(self.max-self.ml))
		
		elif x > self.max:
			return  1.0

	def pdf(self, x):
		
		'''Returns the PDF of the ttriangular distribution

			Args: x (float)

			Returns:
			
			Raises:'''
		
		if x < self.min:
			return 0
		
		elif self.min <= x <= self.ml:
			return  2 * (x - self.min) / ((self.max - self.min)*(self.ml-self.min))

		elif self.ml < x <= self.max:
			return  2 * (self.max - x) / ((self.max - self.min)*(self.max-self.ml))
		
		elif x > self.max:
			return  1.0

	def generate(self, n):
		
		'''Generates n triangular distributed variates

			Args: n (int)

			Returns:
			
			Raises:'''
		
		return [random.triangular(self.min, self.max, self.ml)for q in range(n)]
		


