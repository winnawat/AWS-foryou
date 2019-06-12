import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="awsforyou",
    version="1.0.0",
    author=["Vivek Kumar", "John Mahoney", "Win Nawat S", "Peter Meleney"],
    author_email=["vivekuma@uw.edu", "jm888@uw.edu", "nawats@uw.edu", "pmeleney@uw.edu"],
    description="Instance in an Instant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/winnawat/AWS-foryou",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
