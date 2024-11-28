from setuptools import setup, find_packages

setup(
    name='ciaos',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        "flatbuffers",
        "requests",
        ],
    entry_points={
        'console_scripts': [],
    },
    author='cialabs'
)

