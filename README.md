![logo file](./logo.PNG)

[![Build Status](https://travis-ci.org/winnawat/AWS-foryou.svg?branch=master)](https://travis-ci.org/winnawat/AWS-foryou) [![Coverage Status](https://coveralls.io/repos/github/winnawat/AWS-foryou/badge.svg?branch=master)](https://coveralls.io/github/winnawat/AWS-foryou?branch=master) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com//winnawat/AWS-foryou/blob/master/LICENSE) ![contributors](https://img.shields.io/github/contributors/winnawat/AWS-foryou.svg) ![codesize](https://img.shields.io/github/languages/code-size/winnawat/AWS-foryou.svg) ![pullrequests](https://img.shields.io/github/issues-pr/winnawat/AWS-foryou.svg) ![closedpullrequests](https://img.shields.io/github/issues-pr-closed-raw/winnawat/AWS-foryou.svg)


# AWS-foryou
AWS-foryou helps you decide which AWS instance to use for your machine learning project. Input your algorithm, dataset, and your choice of constraints, be it time or budget, and AWS-foryou will help you decide which instance best suits your needs.

## Project Organization
```
AWS-foryou/
  |- README.md
  |- awsforyou/
    |- __init__.py
    |- algo_runner.py
    |- aws_metadata.py
    |- aws_pricing.py
    |- benchmark_runner.py
    |- recommender.py
    |- report_generator.py
    |- total_time_component.py
    | - ui/
      | - template.html
    |- tests/
      |- __init__.py
      |- test_algo_runner.py
      |- test_aws_metadata.py
      |- test_aws_pricing.py
      |- test_benchmark_runner.py
      |- test_keras_mnist.py
      |- test_reccomender.py
      |- test_report_generator.py
      |- test_total_time_compoment.py
  |- data/
    |- aws-scorecard.csv
  |- docs/
    |- component-specification.md
    |- functional-specification.md
  |-examples/
    |-demo,py
    |-examples.ipynb
    |-sklearn_diabetes.py
    |-x_diabetes.csv
    |-y_diabetes.csv
  |- setup.py
  |- requirements.txt
  |- LICENSE
```
---
## Installation

Clone the repo and create a virtual environment in the root of the repo
```bash
python -m venv venv
source venv/bin/activate
```
If you're using Anaconda, create and activate a new conda environment.
For conda run
```bash
conda create --name awsforyou
conda activate awsforyou
```

Install the dependencies from the `requirements.txt` file using
```bash
python -m pip install -r requirements.txt
```

If you don't have `setuptools` and `wheel` install them using
```bash
python -m pip install --upgrade setuptools wheel
```

Install the package using the following command
```bash
python setup.py sdist bdist_wheel
```

This will generate the pip installation package `awsforyou-0.0.1-py3-none-any.whl` in the `dist/` directory.
The package `awsforyou` can now be installed using

```bash
pip install awsforyou-0.0.1-py3-none-any.whl
```

## Usage

To see how to use the package to get instance recommendation, 
refer to the [example notebook](examples/examples.ipynb)
