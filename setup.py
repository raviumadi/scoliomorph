from setuptools import setup, find_packages

setup(
    name="scoliomorph",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "matplotlib",
        "numpy-stl"
    ],
    description="Library for the Vertebral Body Rotation analysis from STL point cloud including pitch, roll, and yaw calculations",
    author="Ravi Umadi",
    author_email="ravisumadi@gmail.com",
    url="https://github.com/raviumadi/scoliomorph"
)