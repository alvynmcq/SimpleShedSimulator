import inspect

"""Get methods(name), All docstrings, Functions, classes"""


class debug:
	def __init__(self, script):
		self.script = __import__(eval('script'))

		
	def PrintVariableNames(self):
		for q in dir(self.script):
			print q

	def PrintFunctions(self, doc=True):

		if doc == True:
			for variable in vars(self.script).values():
				if inspect.isfunction(variable):
					print variable,
					print(inspect.getdoc(variable))

		elif doc == False:
			for variable in vars(self.script).values():
				if inspect.isfunction(variable):
					print variable,
					print(inspect.getdoc(variable))
		
	def PrintMethods(self, doc=True, only_empty_docs=True):
			self.methods = []
			for variable in vars(self.script).values():
				if inspect.isclass(variable):
					for method in inspect.getmembers(variable):
						self.methods.append(method)

			if doc == True:
				
				if only_empty_docs == False:
					for method in self.methods:
						if inspect.ismethod(method[1]):
							print method[1],
							print inspect.getdoc(method[1]) 
				
				elif only_empty_docs == True:
					for method in self.methods:
						if inspect.ismethod(method[1]):
							if inspect.getdoc(method[1]) is None:
								print method[1]


			elif doc == False:
				for method in self.methods:
					if inspect.ismethod(method[1]):
						print method[1]

	
	def PrintModuleDoc(self):
		print self.script.__doc__


d = debug("act")


d.PrintMethods(only_empty_docs=True)

