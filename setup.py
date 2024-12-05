from setuptools import setup

install_requires = []
with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="s4.a.01_applications",
    author="aldauge",
    install_requires=install_requires
)