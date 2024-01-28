from setuptools import setup, find_packages

setup(
    name='s1_client_test',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'uvicorn',
        'requests',
        'python-multipart',
        'fastapi',
    ],
    entry_points={
        'console_scripts': [],
    },
    author='cialabs'
)
