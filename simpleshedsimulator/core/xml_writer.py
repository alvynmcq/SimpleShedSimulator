import xml.etree.ElementTree as ET




class FileWriter:
	
	'''The class provides a interface for writing xml files.
	Example:
		riskregister = FileWriter("Risk_register")
		riskregister.AddRow("b")
		riskregister.AddRow("c")
		riskregister.AddRow("d")
		riskregister.AddRowItems("c", "jippi",33)
		riskregister.WriteToFile("my_xml_file.xml)
	'''

	def __init__(self, filename):

		self.filename = filename
		register = ET.Element(filename)
		self.tree = ET.ElementTree(register)

	def AddRow(self, rowname):
		ET.SubElement(self.tree.findall(".")[0],rowname)
		ET.dump(self.tree.findall(".")[0]) 

	def AddRowItems(self, rowname, tag, value):
			Cur_row_tag = self.tree.findall("." + rowname)[0]
			ID = ET.SubElement(Cur_row_tag,tag)
			ID.text = str(value)

	def WriteToFile(self, name="filename.xml"):
		self.tree.write(name)



class FileReader:

	def ReadFile(self, name):
		f = open(name, 'r')

		data = f.read()
		root = ET.fromstring(data)
		return root




	


