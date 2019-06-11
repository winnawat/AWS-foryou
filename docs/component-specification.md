## Software Components

### Component 1: (user_interface)
A GUI that takes as input whether to optimize time or optimize for budget.  
Input boxes to determine user constraints for budget and time.  
Final results output:  
Output (Projected price or time for each EC2 instance to complete the allotted task).  

### Component 2: (algo_runner)
Input (.py file, dataset)  
If dataset.rows <= 10,000:  
Run the ,py file against 1%, 5%, 10% of dataset  
Else:  
Run the .py file against 1,000, 5,000, 10,000 rows  
Return time taken to run the .py file against the three datasets  

### Component 3: (algo_analyzer)
Input (runtime per row count from algo-runtimes, time taken for benchmark)  
Fit a curve to the data points:  
- Linear  
- Exponential  
- Ln  
Use scikit learn to regress the three data points.  
Choose the function with the best fit  
Return (expected total time on 100% data)  
  
### Component 4: (benchmark_runner)  
Input (none)  
Run known benchmark on user computer(training of keras' percreptron on a full mnist dataset)  
Return (benchmark runtime)  

### Component 5: (price_crawler)
Input (None)  
API connection to AWS real-time EC2 prices  
Return (Price per hour of each instance in on-demand service)  

### Component 6: (instance_recommender)
Input (expected total time, time taken for benchmark,E2 spot prices)  
Predict the runtime needed for each EC instance.  
Rank the EC2 instances according to the constraints
Return (Sorted list of recommended EC2 constraints)  


---
### Components interaction
1. User passes string that will be used to call the user's algorithm. String contains data_loc = <data csv path>, target_loc = <target csv path>, and any other parameters.
2. algo_runner takes in the string. Subsets the data and target into small fractions and run user's algorithm on small sets of data. algo_runner returns the fractions of data used to run, and their respective runtime.
3. total_time_component takes in this information and fit a curve through the data points. This is used to estimate the time user's algorithm will take to run at 100% of the data. total_time_component returns this estimate.
4. Meanwhile, benchmark_runnner runs a predetermined menchmark test on user's computer. benchmark_runner retuns runtime of this benchmark test on user's computer.
5. Meanwhile, aws_pricing crawls Amazon AWS API for spot and on demand prices at that moment.
6. instance_recommender takes in the output from total_time_component(3), benchmark_runner(4), and aws_pricing(5) to merge them all into one table together with our own benchmark dataset on various AWS instance tpyes. This information is used to build a table of estimated time and cost to run uset's algorithm on various AWS instance types. This table is then sorted and filtered according to user's constraints.
