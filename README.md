SimpleShedSimulator
===================

The goal of Simple Schedule Simulator is to allow the analyst to quickly perform schedule risk analysis.

There is still much work to be done and SimpleShedSimulator is not ready for use. 

For any questions, email me at anders524@hotmail.com

Contributions are much appreciated :)

A small tutorial!
==================

This is meant as a simple tutorial for creating and doing analysis on schedules

Creating activities
-------------------


Create an activity instance like so::
	
    start = activity() # initiation of activity instance
    start.AssignID(1) #The activity's ID is 1
    start.AssignSuccsesors("2FS","3FS") #activity 2 and 3 are  succsessors
    start.AssignStart(2000,3,1) #the start up date is on the format YYYY,mm,dd
    start.AssignDuration(20) #the duration is 20 days

You now have an activity object which later can be assigned to a network. Since this is going to be a network, lets add some activities!::

    Activity1 = activity()
    Activity1.AssignID(2)
    Activity1.AssignDuration(30)

    Activity2 = activity()
    Activity2.AssignID(3)
    Activity2.AssignPredecesors(1)
    Activity2.AssignDuration(6)

    end = activity()
    end.AssignID(4)
    end.AssignPredecesors("2FS","3FS")
    end.AssignDuration(60)



Creating a network
------------------
You now only have 4 activities. To do analysis you need to assign them to a network like so::

    p = network()
    p.AddActivity(start, Activity1, Activity2, end)
    p.PrintNetwork()
    p.CalculatePaths()
    p.PrintNetwork()

A Gantt chart can be obtained as follows::

    p.PlotGantt()


Simulating the network
----------------------
To simulate the Project you first need to assign min, max, and most likely values to EACH activity in the project. This is done with the .SetDurationRange() method::

    Activity1.SetDurationRange(min=5, ml=20, max=50)
    Activity2.SetDurationRange(min=50, ml=51, max=150)

Each activity's duration is then distributed triangulary according to the parameters given. To Siulate the project, use the .Simulate() method and then run the .PlotHistEnd() method to get a histogram over the end duration::

    p.Simulate()
    p.PlotHistEnd()

