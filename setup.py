from setuptools import setup, find_packages

setup(
    name="DiskSpeedTest",
    version="1.0",
    packages=find_packages(),
    author="jaesung Jeong",
    author_email="jj161@student.london.ac.uk",
    description="A simple disk speed test tool with sequential and random read/write capabilities.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JeongHogok/DiskSpeedTest",
    license="MIT license",
    entry_points={
        'console_scripts': [
            'diskspeedtest=diskspeedtest.disk_speed:main',
        ],
    },
    install_requires=[
        'tqdm',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
