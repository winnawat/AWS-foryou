## Software Components

### Component 1: (user_input)
A GUI that takes as input whether to optimize time or optimize for budget.
Input boxes to determine user constraints for budget and time

### Component 2: (algo_runtimes)
Input (.py file, dataset)
If dataset.rows <= 10,000:
Run the ,py file against 1%, 5%, 10% of dataset
Else:
Run the .py file against 1,000, 5,000, 10,000 rows
Return time taken to run the .py file against the three datasets

### Component 3: (expected_time)
Input (runtime per row count from algo-runtimes, time taken for benchmark)
	Fit a curve to the data points:
Linear
Exponential
Ln
	Use scikit learn to regress the three data points.
Choose the function with the best fit
	Return (expected total time on 100% data)
  
### Component 4: (user_benchmark)
Input (none)
	Run known benchmark on user computer
	Return(time taken for benchmark)
  
### Component 5: (prediction_engine)
Input (expected total time, time taken for benchmark)
  Predict the runtime needed for each EC instance.

### Component 6: (AWS_EC2_API)
Input (None)
API connection to AWS real-time EC2 prices
Return (Price per hour of each instance in on-demand service)

### Component 7: Output
Input (expected total flops on 100% of dataset)
Output (Projected price or time for each EC2 instance to complete the allotted task).
