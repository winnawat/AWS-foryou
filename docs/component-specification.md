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
Run known benchmark on user computer  
Return (time taken for benchmark)  

### Component 5: (price_crawler)
Input (None)  
API connection to AWS real-time EC2 prices  
Return (Price per hour of each instance in on-demand service)  

### Component 6: (instance_recommender)
Input (expected total time, time taken for benchmark,E2 spot prices)  
Predict the runtime needed for each EC instance.  
Rank the EC2 instances according to the constraints
Return (Sorted list of recommended EC2 constraints)  
