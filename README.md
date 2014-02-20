SimpleShedSimulator
===================

The goal of Simple Schedule Simulator is to allow the analyst to quickly perform schedule risk analysis.

There is still much work to be done and SimpleShedSimulator is not ready for use. 

For any questions, email me at anders524@hotmail.com

Contributions are much appreciated :)


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
Create a network object like so::

    P = network()
    P.AddActivity(a,b,c,d,e,f,g,h,i,j)
    P.CalculateTotalFloats()
    P.Simulate(n=1000)
    P.PlotGantt()
    P.PrintNetwork()
    
Wich outputs::

    ______________________________________________________________________________________________
    ID Start           End          Duration   Min   ML    Max      Slack     Succsesors               
    ----------------------------------------------------------------------------------------------
    1  2014-02-20      2014-02-25   5          None  None  None     15        ['2FS', '7FS']           
    2  2014-02-25      2014-03-04   7          None  None  None     15        ['7FS', '4SS', '10FF']   
    3  2014-02-20      2014-03-22   30         None  None  None     0         ['5FS']                  
    4  2014-02-25      2014-03-07   10         None  None  None     15        ['5FS']                  
    5  2014-03-22      2014-03-25   3          0     0     10       0         ['6FS']                  
    6  2014-03-25      2014-04-02   8          1     8     8        0         ['7FS', '8SS']           
    7  2014-04-02      2014-04-12   10         1     4     10       0         ['9FS']                  
    8  2014-03-25      2014-04-04   10         3     7     23       8         ['9FS']                  
    9  2014-04-12      2014-04-22   10         3     7     50       0         None                     
    10 2014-02-27      2014-03-04   5          None  None  None     49        None                     
    ______________________________________________________________________________________________


    OTHER INFORMATION:
    -----------------
    Deterministic Duration: 61
    Deterministic Finish: 2014-04-22
    Critical Path:  [9, 8, 6, 5, 3]


    SIMULATION RESULTS:
    -----------------
    E(x):           83 2014-05-14
    P10:            69 2014-04-30
    P50:            82 2014-05-13
    P90:            100 2014-05-31
    Var:            141





