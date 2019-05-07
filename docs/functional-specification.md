## Functional Specifications

### Background.
Amazon Web Services (AWS) Elastic Compute Cloud (EC2) provides users with a vast suite of on-demand virtual machines that can be spun up and used for a variety of purposes quickly and at low-cost.  However choosing the correct instance for a particular purpose can be a daunting task.  There are 5 instance optimization categories: General Purpose (A, T, M), Compute Optimized (C), Memory Optimized (R, X, Z), Accelerated Computing (P, G, F), and Storage Optimized (H, I, D).  Each of these categories contains a number of model sizes for a total of 160 different configurations each with a different price point and cost-performance tradeoffs.  Our goal is to suggest to the user which instance is most appropriate for their use case; optimizing either for highest performance within a budget, or lowest cost within a time constraint.

### User profile.
- Researchers
- Students
- Corporate personnel
The users are someone who familiar with programming multi-threaded or GPU accelerated algorithms on large datasets to be run on EC2 servers.  

### Data sources.
- AWS instance types: https://aws.amazon.com/ec2/instance-types/
- Performance benchmark on EC2: https://www.phoronix.com/scan.php?page=article&item=amazon-ec2-feb2018&num=1
- History of AWS spot prices (scraped from AWS API)

### Use cases. 
<ol>
<li>Choosing the instance which will return results as quickly as possible given a budgetary constraint
  <ol>
    <li>USER: Enters a budgetary constraint, say $100.</li>
    <li>USER: Provides location of algorithm file to be run</li>
    <li>USER: Provides location of data</li>
    <li>PROGRAM: Runs benchmark on user’s computer</li>
    <li>PROGRAM: Runs algorithm with small proportion of data</li>
    <li>OUTPUT: Suggested best instance for this use case</li>
  </ol>
</li>
<li>Choosing the instance which will return results within a time window.
  <ol>
    <li>USER: Enters a time constraint.</li>
    <li>USER: Provides location of algorithm file to be run</li>
    <li>USER: Provides location of data</li>
    <li>PROGRAM: Runs benchmark on user’s computer</li>
    <li>PROGRAM: Runs algorithm with small proportion of data</li>
    <li>OUTPUT: Suggested best instance for this use case</li>
  </ol>
</li>
</ol>
