Tutorial 2 - More on simulation
===============================
Besides doing simple planning related tasks as mentioned in tutorial 1 SimpleShedSimulator allso lets you do more in-depth analysis. 

Exploring criticalities
-----------------------
Considder the following network consisting of 4 activities::

  activities = [activity() for number in range(4)]
  [activities[i].AssignID(i+1) for i in range(4)]
  [activities[i].AssignDuration(duration) for duration, i in zip([5,10,20,3], range(4))]
  [activities[i].AssignDurationRange(min=50, ml=100, max=150)   
        
  activities[0].AssignSuccsesors(2)
  activities[1].AssignSuccsesors(4)
  activities[2].AssignSuccsesors(4)  
        
  P = network()
  P.AddActivity(*activities)


You may construct a histogram of activity 1 endates by applying the method::

  P.Simulate(1000)
  P.PlotHistEnd(ID=1, cumulative=False, bins=20, normed=True)

During the simulation, SimpleShedSimulator allso counts the number of times the activity was on the critical path. The probability of and activity being on the critical path is obtained with the method::

   for activity in P:
      ID = activity.GetID() 
      print P.GetProbabiltyOfCritical(ID=ID)
   
