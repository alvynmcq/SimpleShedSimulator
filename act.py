import datetime
import time
import pickle
import sqlite3 as lite
import json
import pprint
import os

try:
	from triangular import triang
except:
	print "Could not find module for simulation"

#plotting with matplotlib:
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.dates import date2num




def StrToInt(string):
	try:
		return int(''.join(ele for ele in string if ele.isdigit()))
	except TypeError:
		return string

def IntToStr(integer):
	try:
		result =  ''.join([i for i in integer if not i.isdigit()])
		return result
	except TypeError:
		return integer



class IO:
	def WriteNetworkToFile(self, path, projectinctance):
		
		'''Writes the network inctance as a bytestream to file using the pickle module

			Args: path (str)

			Returns:
				Writes a .sss file to path
			Raises:'''
		
		output = open(path, 'wb')
		pickle.dump(projectinctance, output)
		output.close()
	
	def ReadNetworkFromFile(self, path):
		
		'''Reads a networkfile using the pickle module

			Args: path (str)

			Returns:
				Writes a .sss file to path
			Raises:'''
		
		print path, "hehehehehejek"
		output = open(path, 'rb')
		print output
		project = pickle.load(output)
		return project
	
		output.close()





class activity:


	def __init__(self):

		self.today = datetime.date.today()
		self.critical = False
		self.critical_time = None

	def __eq__(self, other) :
                
			return self.ID == other.ID

	def AssignID(self,ID):

		'''Assigns an ID to the activity.

			Args:
				ID (int): Preffered ID of the activity
			Returns:
				Sets self.ID = ID.
			Raises:
			'''
		try:
			self.ID = int(ID)
		except:
			print "Assigned ID must be integer"

	def AssignName(self, name):
                
		'''Assigns a name to the activit inctance.

			Args:
				name (str): The activity name
			Returns:
				Sets self.name = name
			Raises:'''
		
		self.name = name

	def AssignStart(self,Y,M,D):
                
		'''Assigns a startdate to the activit inctance.

			Args:
				Y,M,D (int): The activity's startdate
			Returns:
				Sets self.start = datetime.date(Y,M,D) and calculates endate if possible.
			Raises:'''

		self.start = datetime.date(Y,M,D)
		try:
			difference = datetime.timedelta(self.duration)
			newdate = self.start + difference
			self.AssignEnd(newdate.year, newdate.month, newdate.day)
		except AttributeError:
			try:
				delta = self.end - self.start
				self.duration = delta.days
			except AttributeError:
				pass

	def AssignEnd(self,Y,M,D):
                
		'''Assigns a enddate to the activit inctance.

			Args:
				Y,M,D (int): The activity's enddate given as YYYY, mm, dd
			Returns:
				Sets self.end = datetime.date(Y,M,D) and sets the duration if possible.
			Raises:'''
		
		self.end = datetime.date(Y,M,D)
		try:
			delta = self.end - self.start
			self.duration = delta.days
		except AttributeError:
			pass

	def AssignDuration(self, duration):
                
		'''Assigns a Duration to the activity inctance.

			Args:
				duraton (int): The activity's duration
			Returns:
				Sets self.duration = duration and sets the enddate if possible.
			Raises:
			
			'''
		
		self.duration = duration
		try:
			difference = datetime.timedelta(days=duration)
			newdate = self.start + difference
			self.AssignEnd(newdate.year, newdate.month, newdate.day)
		except AttributeError:
			return "No startdate assigend. Use the method AssignStart"

	def AssignSuccsesors(self,*args):
                
		'''Assigns succerssors to the activity inctance.

			Args:
				*args (int): The activity's successors
			Returns:
				Sets self.S = [] (list).
			Raises:'''
		
		#Add FS condition to empty predecessors	
		arguments = []
		for q in args:
			try:
				q = int(q)
				if isinstance(q, int):
					arguments.append(str(q) + 'FS')
				else:
					arguments.append(q)
			except ValueError:
				arguments.append(q)
		args = arguments

		try:
			for q in args:
				if self.ID < StrToInt(q):
					self.S.append(q)
				elif self.ID > StrToInt(q):
					raise AttributeError('Successor ID smaaler then Activity ID ')
			
			#remove duplicates and convert to str()
			self.S = [str(i) for i in self.S]
			self.S = list(set(self.S))
			
			#Convert to uppercase
			suc = []
			for s in self.S:
				try:
					suc.append(s.upper())
				except SyntaxError:
					suc.append(s)
					continue
			self.S = suc
			
			
		except:
			self.S = []
			for q in args:
				if self.ID < StrToInt(q):
					self.S.append(q)
				elif self.ID > StrToInt(q):
					raise AttributeError('Successor ID smaaler then Activity ID ')
			
			#remove duplicates and convert to str()
			self.S = [str(i) for i in self.S]
			self.S = list(set(self.S))
			
			#Convert to uppercase
			suc = []
			for s in self.S:
				try:
					suc.append(s.upper())
				except SyntaxError:
					suc.append(s)
					continue
			self.S = suc

	def AssignPredecesors(self,*args):
                
		'''Assigns predecesors to the activity inctance.

			Args:
				*args (int): The activity's predecesors
			Returns:
				Sets self.P = [] (list).
			Raises:'''
		
		#Add FS condition to empty predecessors	
		arguments = []
		for q in args:
			try:
				q = int(q)
				if isinstance(q, int):
					arguments.append(str(q) + 'FS')
				else:
					arguments.append(q)
			except ValueError:
				arguments.append(q)
		args = arguments
		
		try:
			for q in args:
				if self.ID > StrToInt(q):
					self.P.append(q)
				elif self.ID < StrToInt(q):
					raise AttributeError('Predecessor ID bigger then Activity ID ')
			
			#remove duplicates and convert to str()
			self.P = [str(i) for i in self.P]
			self.P = list(set(self.P))
			
			#Convert to uppercase
			pre = []
			for p in self.P:
				try:
					pre.append(p.upper())
				except SyntaxError:
					pre.append(p)
					continue
			self.P = pre
			
		except:
			self.P = []
			for q in args:
				if self.ID > StrToInt(q):
					self.P.append(q)
				elif self.ID < StrToInt(q):
					raise AttributeError('Predecessor ID bigger then Activity ID ')
			#remove duplicates and convert to str()
			self.P = [str(i) for i in self.P]
			self.P = list(set(self.P))
			
			#Convert to uppercase
			pre = []
			for p in self.P:
				try:
					pre.append(p.upper())
				except SyntaxError:
					pre.append(p)
					continue
			self.P = pre

	def GetStart(self, asobject=False):
                
		'''returns the startdate either as a list of times or as a datetimeobject.

			Args:
				asobject (boolean): Determines wether to return a timedateobject or a list of times
			Returns:
				return a timedateobject or a list of times
			Raises:'''
		
		try:
			if asobject == False:
				Start = []
				for q in str(self.start).split('-'):
					Start.append(int(q))
				return Start
			elif asobject == True:
				return self.start
		except AttributeError:
			pass

	def GetEnd(self, asobject=False):
                
		'''returns the enddate either as a list of times or as a datetimeobject.

			Args:
				asobject (boolean): Determines wether to return a timedateobject or a list of times
			Returns:
				return a timedateobject or a list of times
			Raises:'''
		
		try:
			if asobject == False:
				End = []
				for q in str(self.end).split('-'):
					End.append(int(q))
				return End
			elif asobject == True:
				return self.end

		except AttributeError:
			pass

	def GetDuration(self):
		
		'''Returns the duration of the activity

			Args:
				
			Returns:
				self.duration (int)
			Raises:'''
		
		try:
			return self.duration
		except AttributeError:
			pass

	def GetName(self):
		
		'''Returns the name of the activity

			Args:
				
			Returns:
				self.name (str)
			Raises:'''
		
		try:
			return self.name
		except AttributeError:
			print None

	def GetID(self):
		
		'''Returns the ID of the activity

			Args:
				
			Returns:
				self.ID (int)
			Raises:'''
			
		try:
			return self.ID
		except:
			print "No ID assigned. Use AssignID()."

	def GetSuccsesors(self):
		
		'''Returns the succsessors of the activity

			Args:
				
			Returns:
				self.S (list)
			Raises:'''
					
		try:
			return self.S
		except:
			return None

	def GetPredecesors(self):
		
		'''Returns the predecessors of the activity

			Args:
				
			Returns:
				self.P (list)
			Raises:'''
		
		try:
			return self.P
		except:
			return None # "This activity has no  assigned Predecesors. Use AssignPredecesors()."

	def GetSummary(self):
		self.summary = []
		self.summary.append(self.GetID())
		self.summary.append(self.GetName())
		self.summary.append(self.GetDuration())
		self.summary.append(self.GetStart())
		self.summary.append(self.GetEnd())
		self.summary.append(self.GetSuccsesors())
		self.summary.append(self.GetPredecesors())
		return self.summary

	def EstablilshPredecesor(self, activity):
		startdate = activity.GetEnd()
		self.AssignStart(startdate[0], startdate[1], startdate[2])

	def SetCritical(self, critical):
		if critical in ["yes", True, "y", "Y", 1, "YES", "Yes" ]:
			self.critical = True

	def GetCritical(self):
		return self.critical

	def SetCriticalTime(self, time):
		if time <= 0.0:
			self.SetCritical(True)

		self.critical_time = time

	def GetCriticalTime(self):

		return self.critical_time
	
	def SetDurationRange(self, **kwargs):
		
		for q in kwargs.items():
			if q[0] in ["min", "MIN", "Min"]:
				self.minduration = q[1]
			elif q[0] in ["max", "MAX", "Max"]:
				self.maxduration = q[1]
			elif q[0] in ["ml", "ML", "Ml"]:
				self.mlduration = q[1]
	
	def SetDurationRangeMin(self, MIN):
		self.minduration = MIN
	
	def SetDurationRangeML(self,ML):
		self.mlduration = ML
	
	def SetDurationRangeMax(self,MAX):
		self.maxduration = MAX
	
	def GetDurationRangeMin(self):
		try:
			return self.minduration
		except:
			return None

	def GetDurationRangeML(self):
		try:
			return self.mlduration
		except:
			return None

	def GetDurationRangeMax(self):
		try:
			return self.maxduration
		except:
			return None

	def IncrementID(self, increment, SUC=True, PRE=False, ID = True):

		if ID == True:
			#increment id
			current_ID = self.GetID()
			newID = current_ID + increment
			self.AssignID(newID)
		
		#Increment Succsesors
		if SUC == True:
			newS = []
			try:
				for suc in self.S:
					condition = IntToStr(suc)
					newS.append(str(StrToInt(suc) + increment) + condition)
				
				self.S = newS
			
			except AttributeError:
				pass

class network:


	def __init__(self):
		self.activities = []
		self.today = datetime.date.today()
		self.IDs = []

	def __UpdateIDs(self):
		
		self.IDs = []
		try:
			for q in self.activities:
				self.IDs.append(q.GetID())
		except:
			pass

	def AssignName(self, name):
                
		'''Assigns a name to the activit inctance.

			Args:
				name (str): The activity name
			Returns:
				Sets self.name = name
			Raises:'''
		
		self.name = name

	def AddActivity(self, *args):
                
		'''Adds an activity to the network.

		Args:
			*args (object): the activity object name
		Returns:
			Sets self.activities and updatelinks
		Raises:'''
		
		initial_number_of_activities = len(self.activities)
		
		#Make sure one does not add the same activity
		for i in range(0,len(args)):
			if args[i].GetID() in self.IDs: #Make sure one does not add object with same ID
				continue
			if args[i].GetID() == None: #Make sure one does not add object with  ID = None
				continue
			else:
				self.activities.append(args[i])

		self.__UpdateIDs()
		
		#Update links
		number_of_activities = len(self.activities)
		if number_of_activities > initial_number_of_activities:
			self.__UpdateLinks()

	def __UpdateLinks(self):
		d = []
		for q in self.activities:
			d.append( (q.GetID(),q) )
		self.dictionary = dict(d)
		for q in self.dictionary:
			try:
				a =1
				for w in self.dictionary[q].GetSuccsesors():
					
					if IntToStr(w) in ['fs','FS','Fs','fS']:
						qq = str(q) + IntToStr(w)
						ww = StrToInt(w)
						self.dictionary[ww].AssignPredecesors(qq)
					else:
						print a
						w = StrToInt(w)
						self.dictionary[w].AssignPredecesors(int(q))
			except:
				continue
				
				
		for q in self.dictionary:
			try:

				for w in self.dictionary[q].GetPredecesors():
					if IntToStr(w) in ['fs','FS','Fs','fS']:
						qq = str(q) + IntToStr(w)
						ww = StrToInt(w)
						self.dictionary[ww].AssignSuccsesors(qq)
					else:
						w = StrToInt(w)
						self.dictionary[w].AssignSuccsesors(int(q))
						
			except:
				pass

	def GetNetworkIDDict(self):
		
		self.ID_dict = {}
		for q in self.activities:
			self.ID_dict[q.GetID()] = q
		
		return self.ID_dict

	def PrintNetwork(self):
		 
		'''Prints the network to terminal.

			Args:

			Returns:
				
			Raises:'''
		self.__CalculateDates() #recalculate project dates
		print "_____________________________________________________________"

		print str('ID').ljust(2),
		#print str('Name').ljust(9),
		print str('Start').ljust(15),
		print str('End').ljust(9),
		print str('Duration').ljust(7),
		print str('Succsesors').ljust(15),
		print str('Predecesors').ljust(7)
		for i in self.IDs:
			try:
				print str(self.dictionary[i].GetID()).ljust(2),
				#print str(self.dictionary[i].GetName()).ljust(9),
				print str(self.dictionary[i].GetStart(asobject=True)).ljust(15),
				print str(self.dictionary[i].GetEnd(asobject=True)).ljust(9),
				print str(self.dictionary[i].GetDuration()).ljust(7),
				print str(self.dictionary[i].GetSuccsesors()).ljust(15),
				print str(self.dictionary[i].GetPredecesors()).ljust(7)
		
			except KeyError:
				continue
			
		print "_____________________________________________________________"

	def GetName(self):
		        
		'''Returns the name of the network

			Args:

			Returns:
				self.name (str)
			Raises:'''
			
		try:
			return self.name
		except AttributeError:
			print "No name assigend. Use the method AssignName()"

	def GetActivities(self):
		if len(self.activities)>0:
			return self.activities
		else:
			print "No activities assigend to network. Use the method AssignActivity()"

	def __CalculateDates(self):
                
		'''Calculates the earliest starttimes for each activity.

			Args:

			Returns:
				Assigns new starttime according to logic in network
			Raises:'''
		
		#Update links
		self.__UpdateLinks
		
		for i in self.IDs:
			try:
				P = self.dictionary[i].GetPredecesors() #predecesors for each activity i
				endtimes = []
			except KeyError:
				continue
			try:
				for q in P:
					if IntToStr(q) in ['fs','FS','Fs','fS']:
						try:
							endtimes.append(self.dictionary[StrToInt(q)].GetEnd(asobject=True)) #endtimes for activity i's predeccesors
						except KeyError:
							continue
					else:
						q = int(q)
						endtimes.append(self.dictionary[q].GetEnd(asobject=True)) #endtimes for activity i's predeccesors

			except TypeError:
				endtimes.append(self.today)
			
			try:
				earliest_start_date = max(endtimes)  #max endtime equals earliest starttime
				self.dictionary[i].AssignStart(earliest_start_date.year, earliest_start_date.month, earliest_start_date.day) #assign earliest starttime
			except TypeError:
				pass

	def GetNetworkEnd(self, asobject=True):
		
		'''Get the last activity's end date

			Args:

			Returns:
				Returns a dattimeobject or a list 
			Raises:'''
		
		#This should be updated to search throug thos activities which onlye has None Succsessors	
		self.__CalculateDates() #recalculate project dates
		enddates = []
		for q in self.activities:
			enddates.append(q.GetEnd(asobject))
		
		return max(enddates)

	def GetNetworkStart(self, asobject=True):
		
		'''Get the first activity's start date

			Args:

			Returns:
				Returns a dattimeobject or a list 
			Raises:'''
			
		self.__CalculateDates() #recalculate project dates
		
		last_activity_ID = len(self.dictionary)
		return self.dictionary[1].GetStart(asobject)

	def Simulate(self, n=10, WriteToDB=True, DbName="Simulation_variates.db", RiskTable = None):
		
		'''Simulates the network. n = 1000 itterations is default.
		 Currently, the only avilable distribution is the triangular 
		 distribution (http://en.wikipedia.org/wiki/Triangular_distribution)
		 The method allso gives you the opportunity to write the resulting endates, that is the duration (days) from 
		 project start to the relevant activity's enddate to a database file called Simulation_variates.db using SQLite

			Args: n (int) number of itterations
			      WriteToDB (boealen) if True writes the endates to database
			      DbName (str) Name of database to create
			      end (boelan) write all activity's enddates to database (not yet working)

			Returns:
				Returns a dattimeobject or a list 
			Raises:'''
		
		#Removing old database file
		try:
			os.remove("Simulation_variates.db")
		except OSError:
			pass
		
		if WriteToDB == True:
			#Constructing appropriate database using SQLite
			db_string = ""
			for q in self.activities:
				db_string = db_string + "ID" + str(q.GetID()) + " TEXT" +  ", " 
			db_string =  "CREATE TABLE SimulationResults(" +  db_string[:-2] + ")"  
			print db_string
			#Creating database
			con = lite.connect(DbName)
			cur = con.cursor()
			try:
				cur.execute(db_string)
			except:
				print "Database allready exists"
			con.commit() # Save (commit) the changes

		self.networkends = []
		"""	
		this loops assigns a random duration for each activity in the
		network, and calculates the endtime. This is done n times
		"""
		#Generates n variates

		if RiskTable == None:

			for i in range(n):

				#each activity is assigned a new duration here:
				for q in self.activities:
					try:
						Time = triang(min = q.minduration,
									  ml = q.mlduration,
									  max = q.maxduration)
						T = Time.generate(1)[0]
						q.AssignDuration(T)
					except AttributeError:
						continue
				self.__CalculateDates()
				#Only initiate if you want to write resukts to db
				if WriteToDB == True:
					#Every endate for each activity is here:
					enddates = []
					for q in self.activities:
						try:
							duration = q.GetEnd(asobject=True)-self.GetNetworkStart(asobject=True)
							enddates.append(duration.days)
						
						
						except AttributeError:
							continue
					enddates = str(tuple(enddates))
					db_string = "INSERT INTO SimulationResults VALUES" + enddates 
					cur.execute(db_string)
				

					enddate = (self.GetNetworkEnd() - self.GetNetworkStart()).days
					self.networkends.append(enddate)


		else:

			for i in range(n):
				#each activity is assigned a new duration here:
				T = RiskTable.GenerateTotalTimes() #this is a dict on the form {'ID':totaltime}
				for ID in T:
					self.GetNetworkIDDict()[ID].AssignDuration(T[ID]) #activityinstance
				self.__CalculateDates()

				#Only initiate if you want to write resukts to db
				if WriteToDB == True:
					#Every endate for each activity is here:
					enddates = []
					for q in self.activities:
						try:
							duration = q.GetEnd(asobject=True)-self.GetNetworkStart(asobject=True)
							enddates.append(duration.days)
						
						
						except AttributeError:
							continue
					enddates = str(tuple(enddates))
					db_string = "INSERT INTO SimulationResults VALUES" + enddates 
					cur.execute(db_string)
				

					enddate = (self.GetNetworkEnd() - self.GetNetworkStart()).days
					self.networkends.append(enddate)
		con.commit()
		con.close()

	def GetSimulationVariates(self,DbName="Simulation_variates.db", ID = "ID1"):
		
		'''Returns the simulated variates from the simulation

			Args: DbName (str) name of database. by default: Simulation_variates.db
			      ID (str) The Id of the activity one whish to retriev variates of

			Returns:
				Returns a list consisting of integers. (days from project start to activity finish)
			Raises:'''
		
		try:
			con = lite.connect(DbName)
			cur = con.cursor()
			argument = "SELECT %s FROM SimulationResults" % ID
			cur.execute(argument)
			print "hello"
			return [int(i[0]) for i in cur.fetchall()]
		except:
			raise AttributeError('Could not find database file')

	def PlotHistEnd(self, cumulative = False, bins=20, normed = True):
		
		'''Plots the network enddate as a histogram (currently uses Matplotlib). 

			Args: Cumulative (boolean), bins (int), normed (boolean)

			Returns:
				Returns a matplotlib object
			Raises:'''
			
		data = self.GetSimulationVariates()
		print data, "her"
		plt.hist(data, cumulative = cumulative, bins = bins, normed=normed)
		plt.grid()
		plt.show()

	def IncrementNetworkAt(self, ID, increment):
		
		'''Increment IDs ad ID. This is used to add activities 

			Args: ID (int), increment (int)

			Returns:
				Increments the IDs
			Raises:'''

		for i in self.IDs:
			try:
				if i > ID:
					self.dictionary[i].IncrementID(increment) 
				else:
					continue
			except KeyError:
				continue

		#Updates those predecesors which id is bigger than ID 
		for i in self.IDs:
					try:
						for pre in self.dictionary[i].GetPredecesors():
							IncrementedValues = []
							#Checks which predecessors are bigger than the IDs and increment
							if StrToInt(pre) > ID: 
								self.dictionary[i].P.remove(pre) #Remove element
								condition = IntToStr(pre) 
								IncrementedValues.append(str(StrToInt(pre) + increment) + condition) #Adds an incremented ID
						self.dictionary[i].P = self.dictionary[i].P + IncrementedValues #Adds an incremented ID to initial list P
	
					except TypeError:
						continue

		#Updates successros which id is bigger than ID 
		for i in self.IDs:
					try:
						for suc in self.dictionary[i].GetSuccsesors():
							IncrementedValues = []
							#Checks which successros are bigger than the IDs and increment
							if StrToInt(suc) > ID:
								if self.dictionary[i].GetID() < ID:
									self.dictionary[i].S.remove(suc) #Remove element
									condition = IntToStr(suc) 
									IncrementedValues.append(str(StrToInt(suc) + increment) + condition) #Adds an incremented ID
						self.dictionary[i].S = self.dictionary[i].S + IncrementedValues #Adds an incremented ID to initial list P
	
					except TypeError:
						continue

		self.dictionary[ID].IncrementID(increment, ID=False) #Increment Succsessors to activity ID asswell

		#dont forget to update the idlist:
		self.IDs = [q.GetID() for q in self.GetActivities()]

	def InsertActivity(self, ID):
		
		#make room for new activity
		self.IncrementNetworkAt(ID-1, increment = 1)
		
		# create a new activity instance
		Activity = activity()
		Activity.AssignDuration(1)
		Activity.AssignID(ID )
		Activity.AssignSuccsesors(ID+1)
		self.AddActivity(Activity)
		
		#Don't forget to sort the network
		self.SortNetwork()

	def SortNetwork(self):
		self.activities.sort(key = lambda x: x.ID)

		#dont forget to update the idlist:
		self.IDs = [q.GetID() for q in self.GetActivities()]

	def PlotGantt(self):

		'''Plots the network in a ganttchart (currently uses Matplotlib). 

			Args: 

			Returns:
				Returns a matplotlib object
			Raises:'''
		
		startdate = self.GetNetworkStart()
		enddate = self.GetNetworkEnd()
		ids = []
		starts = []
		ends = []
		preid = []
		for q in self.IDs:
			ids.append(q)
			starts.append((self.dictionary[q].GetStart(asobject=True) - startdate).days)
			ends.append((self.dictionary[q].GetEnd(asobject=True) - startdate).days)
			#adding horisontal lines to critical path
			try:
				pre = {}
				for i in self.dictionary[q].GetPredecesors():
					pre[self.dictionary[StrToInt(i)].GetEnd(asobject=True)] = i
				preid.append(StrToInt(pre[max(pre)]))
			except:
				preid.append(None)
		
		# Plot a line for every activity
		plt.ylim(min(self.IDs)-1,max(self.IDs)+1)
		plt.yticks(self.IDs)
		#plt.yticks(range(max(self.IDs)+1))
		plt.grid()
		plt.hlines(ids, starts, ends, colors = 'green', lw = 15)
		plt.vlines(starts, ids, preid, colors = 'black', lw = 1.5)
		plt.show()

	def SaveNetwork(self, path, heading=True):
		 
		self.__CalculateDates() #recalculate project dates
		
		output = open(path, 'w')
		
		if heading == True:
			output.write("ID;NAME;START;END;DURATION;SUCCSESSOR;PREDESESSOR;MINDURATION;MLDURATION;MAXDURATION \n")
		
		for i in self.IDs:
			#try:
			output.write(str(self.dictionary[i].GetID()) + ";")
			output.write(str(self.dictionary[i].GetName()) + ";"),
			output.write(str(self.dictionary[i].GetStart(asobject=False)) + ";"),
			output.write(str(self.dictionary[i].GetEnd(asobject=False)) + ";"),
			output.write(str(self.dictionary[i].GetDuration()) + ";"),
			output.write(str(self.dictionary[i].GetSuccsesors()) + ";"),
			output.write(str(self.dictionary[i].GetPredecesors()) + ";"),
			output.write(str(self.dictionary[i].GetDurationRangeMin()) + ";"),
			output.write(str(self.dictionary[i].GetDurationRangeML()) + ";"),
			output.write(str(self.dictionary[i].GetDurationRangeMax()) + ";"),
			output.write("\n")

	def OpenNetwork(self, path):
		
		input = open(path, 'r')
		for line in input:

			i = line.split(";")
			a = activity()
			a.AssignID(i[0])
			a.AssignName(i[1])
			
			start = eval(i[2])
			try:
				a.AssignStart(*start)
			except TypeError:
				pass
			
			end = eval(i[3])
			try:
				a.AssignEnd(*end)
			except TypeError:
				pass
			
			duration = int(i[4])
			a.AssignDuration(duration)
			
			sucsessor = eval(i[5])
			try:
				a.AssignSuccsesors(*sucsessor)
			except TypeError:
				pass
			
			predecessor = eval(i[6])
			try:
				a.AssignPredecesors(*predecessor)
			except TypeError:
				pass
			
			try:
				minduration = int(i[7])
				a.SetDurationRangeMin(minduration)
			except:
				pass
				
			try:
				mlduration = int(i[8])
				a.SetDurationRangeML(mlduration)
			except:
				pass
				
			try:
				maxduration = int(i[9])
				a.SetDurationRangeMax(maxduration)
			except:
				pass
			self.AddActivity(a)



class risktable:
	def __init__(self, net):
		self.riskdrivers = {}
		self.net = net
		self.table = {}
		for q in self.net.GetActivities():
			self.table[q.GetID()] = {}
		
	def AddRiskDriver(self, name, effectiveon = []):
		
		self.riskdrivers[name] = effectiveon
	
	def Update(self):
		for q in self.table:
			for w in self.riskdrivers:
				for e in self.riskdrivers[w]:
					self.table[e][w] = []

	def AddRiskDriverDuration(self, ID, riskdriver, parameters):

		self.table[ID][riskdriver] = parameters

	def PrintRiskTable(self):
		print json.dumps(self.table, indent=10)
		
		#pprint.pprint(self.table)

	def GenerateTotalTimes(self):
		times = {}
		for q in self.table:
			totaltime = []
			for w in self.table[q]:
				params = self.table[q][w]
				T = triang(min=params[0], ml=params[1], max=params[2]).generate(1)[0]
				totaltime.append(T)
				times[q] = sum(totaltime)
		
		return times







if __name__ == "__main__":
	a = activity()
	a.AssignID(1)
	a.AssignDuration(5)
	a.AssignSuccsesors(2)

	b = activity()
	b.AssignID(2)
	b.AssignDuration(7)
	b.AssignSuccsesors(4)

	c = activity()
	c.AssignID(3)
	c.AssignDuration(19)

	d = activity()
	d.AssignID(4)
	d.AssignDuration(12)
	d.AssignSuccsesors(5)


	e = activity()
	e.AssignID(5)
	e.AssignDuration(3)
	e.AssignPredecesors(3,4)

	f = activity()
	f.AssignID(6)
	f.AssignDuration(8)
	f.AssignPredecesors(5)

	g = activity()
	g.AssignID(7)
	g.AssignDuration(10)
	g.AssignPredecesors(6, 1,2)

	P = network()
	P.AddActivity(a,b,c,d,e,f,g)

	P.PrintNetwork()


	P.InsertActivity(ID=5)
	

	P.PrintNetwork()








