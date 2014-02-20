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


Create activity objects like so::
	
    a = activity()
    a.AssignID(1)
    a.AssignDuration(5)
    a.AssignSuccsesors(2)

    b = activity()
    b.AssignID(2)
    b.AssignDuration(7)
    b.AssignSuccsesors("4ss")

    c = activity()
    c.AssignID(3)
    c.AssignDuration(30)

    d = activity()
    d.AssignID(4)
    d.AssignDuration(10)
    d.AssignSuccsesors(5)

    e = activity()
    e.AssignID(5)
    e.AssignDuration(3)
    e.AssignPredecesors(3,4)
    e.SetDurationRange(min=0, ml=0,max=10)

    f = activity()
    f.AssignID(6)
    f.AssignDuration(8)
    f.AssignPredecesors(5)
    f.SetDurationRange(min=1, ml=8,max=8)

    g = activity()
    g.AssignID(7)
    g.AssignDuration(10)
    g.AssignPredecesors(6,2,1)
    g.SetDurationRange(min=1, ml=4,max=10)
    
    h = activity()
    h.AssignID(8)
    h.AssignDuration(10)
    h.AssignPredecesors('6ss')
    h.SetDurationRange(min=3, ml=7,max=23)
    
    i = activity()
    i.AssignID(9)
    i.AssignDuration(10)
    i.AssignPredecesors(7,8)
    i.SetDurationRange(min=3, ml=7,max=50)

    j = activity()
    j.AssignID(10)
    j.AssignDuration(5)
    j.AssignPredecesors("2ff")



Creating a network
------------------
You now only have 4 activities. To do analysis you need to assign them to a network like so::

    P = network()
    P.AddActivity(a,b,c,d,e,f,g,h,i,j)
    P.CalculateTotalFloats()
    P.Simulate(n=1000)
    P.PrintNetwork()
    P.PlotGantt()







