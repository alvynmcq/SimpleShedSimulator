Tutorial 1 - Building simple networks
=====================================

The goal of SimpleShedSimulator is to let the analyst quickly perform schedule risk analysis.

There is still much work to be done and SimpleShedSimulator is not ready for use. 

For any questions, email me at anders524@hotmail.com

You are welcome to join :)


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

	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| ID                     | Start                  | End                    | Duration               | Succsesors             |
	+========================+========================+========================+========================+========================+
	| 1                      | 2014-11-02             | 2014-11-07             | 5                      | ['2FS', '7FS']         |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 2                      | 2014-11-07             | 2014-11-14             | 7                      | ['7FS', '4SS', '10FF'] |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 3                      | 2014-11-02             | 2014-12-02             | 30                     | ['5FS']                |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 4                      | 2014-11-07             | 2014-11-17             | 10                     | ['5FS']                |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 5                      | 2014-12-02             | 2014-12-06             | 4                      | ['6FS']                |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 6                      | 2014-12-06             | 2014-12-13             | 7                      | ['7FS', '8SS']         |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 7                      | 2014-12-13             | 2014-12-16             | 3                      | ['9FS']                |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 8                      | 2014-12-06             | 2014-12-23             | 17                     | ['9FS']                |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 9                      | 2014-12-23             | 2014-12-31             | 8                      | None                   |
	+------------------------+------------------------+------------------------+------------------------+------------------------+
	| 10                     | 2014-11-09             | 2014-11-14             | 5                      | None                   |
	+------------------------+------------------------+------------------------+------------------------+------------------------+



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

Creating a Risktable
---------------------
Create a risktable object object like so::


    R = risktable(P) #create the risk table
    R.AddRiskDriver('riskrdiver_1', [1,2,3]) #add riskdriver_1 and they are effective on activity with id 1,2 and 3
    R.AddRiskDriver('riskrdiver_2', [4,5,6]) #add riskdriver_1 and they are effective on activity with id 4, 5 and 6
    R.AddRiskDriver('riskrdiver_3', [6,7,8,9,10]) #add riskdriver_1 and they are effective on activity with id 4, 5 and 6

    
    R.AddRiskDriverDuration(1, 'riskrdiver_1', [10,11,12]) #riskdriver_1 have an additional effect on activity 1
    R.AddRiskDriverDuration(2, 'riskrdiver_1', [10,11,12])
    R.AddRiskDriverDuration(3, 'riskrdiver_1', [10,11,12])
    R.AddRiskDriverDuration(4, 'riskrdiver_2', [10,11,12])
    R.AddRiskDriverDuration(5, 'riskrdiver_2', [10,11,12])
    R.AddRiskDriverDuration(6, 'riskrdiver_2', [10,11,12])
    R.AddRiskDriverDuration(6, 'riskrdiver_3', [10,11,12])
    [R.AddRiskDriverDuration(id, 'riskrdiver_3', [10,11,12]) for id in range(7,11)]
        
    R.PrintRiskTable() #dumps the risktable in json format
    R.GenerateTotalTimes() #generate durations based on the table


Wich outputs::

	+--------------+--------------+--------------+--------------+
	| id           | riskrdiver_2 | riskrdiver_3 | riskrdiver_1 |
	+==============+==============+==============+==============+
	| 1            |              |              | [10, 11, 12] |
	+--------------+--------------+--------------+--------------+
	| 2            |              |              | [10, 11, 12] |
	+--------------+--------------+--------------+--------------+
	| 3            |              |              | [10, 11, 12] |
	+--------------+--------------+--------------+--------------+
	| 4            | [10, 11, 12] |              |              |
	+--------------+--------------+--------------+--------------+
	| 5            | [10, 11, 12] |              |              |
	+--------------+--------------+--------------+--------------+
	| 6            | [10, 11, 12] | [10, 11, 12] |              |
	+--------------+--------------+--------------+--------------+
	| 7            |              | [10, 11, 12] |              |
	+--------------+--------------+--------------+--------------+
	| 8            |              | [10, 11, 12] |              |
	+--------------+--------------+--------------+--------------+
	| 9            |              | [10, 11, 12] |              |
	+--------------+--------------+--------------+--------------+
	| 10           |              | [10, 11, 12] |              |
	+--------------+--------------+--------------+--------------+
