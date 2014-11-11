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



import xml.etree.ElementTree as ET




class FileWriter:
	
	'''The class provides a interface for writing risk registers to xml files.
	
	Example::

	    riskregister = FileWriter("Risk_register")
	    riskregister.AddRow("b")
	    riskregister.AddRow("c")
	    riskregister.AddRow("d")
	    riskregister.AddRowItems("c", "jippi",33)
	    riskregister.AddRowAttribute("b", "attr", "value")
	    riskregister.WriteToFile("my_xml_file.xml")
	
	Rownames are treated as unique, which means that two rows can not have identical names.
	'''

	def __init__(self, filename):

		self.filename = filename
		register = ET.Element(filename)
		self.tree = ET.ElementTree(register)

	def AddRow(self, rowname):
		"""Adds riskdescription to risk register"""
		ET.SubElement(self.tree.findall(".")[0],rowname)
		ET.dump(self.tree.findall(".")[0]) 

	def AddRowItems(self, rowname, tag, value):
		"""Adds a risk attribute to the specified risk"""
		Cur_row_tag = self.tree.findall("." + rowname)[0]
		ID = ET.SubElement(Cur_row_tag,tag)
		ID.text = str(value)

	def AddRowAttribute(self, rowname, attribute_name, attribute_value):
		'''Adds an attribute to the specified row
		
		Example::
		
		    <attribute_name="attribute_value">blabla</step>
		
		'''
		
		Cur_row_tag = self.tree.findall("." + rowname)[0]
		Cur_row_tag.set(attribute_name, attribute_value)
		

	def WriteToFile(self, name="filename.xml"):
		"""Saves the current tree to an xml file"""
		self.tree.write(name)



class FileReader:

	def ReadFile(self, name):
		f = open(name, 'r')
		data = f.read()
		root = ET.fromstring(data)
		return root



