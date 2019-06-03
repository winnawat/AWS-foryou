"""
Script that runs benchmark tests on EC2 instance multiple times.
execute by 'python run_benchmark_set.py'
"""

from awsforyou import benchmark_runner

for i in range(0, 9):
    benchmark_runner.run_benchmark(aws=True)
