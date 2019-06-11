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

### Component 3: (total_time_estimate)
Input (runtime per percent of total rows(default is 1%, 5%, 10%) and the row percents, from Component 2)  
Fit four optimized curves to the data points using scipy:  
- Linear  
- Exponential  
- Logn
- nLogn
Choose the function with the best fit (smallest residuals)

Output (expected total time on 100% data)
  
### Component 4: (benchmark_runner)  
Input (none)  
Run known benchmark on user computer  
Return (time taken for benchmark)  

### Component 5: (price_crawler)
Input (None)  
API connection to AWS real-time EC2 prices  
Return (Price per hour of each instance in on-demand service)  

### Component 6: (recommender)
Input (Times to run benchmark file on users machine from Component 2, expected total time from Component 3, time taken for the benchmark on AWS from Component 4, and EC2 spot prices from Component 5)  
Create a dataframe of EC2 instances with added expected time and expected cost columns

Output (Dataframe with cost and time estimates)  
