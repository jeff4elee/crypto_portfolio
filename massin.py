#! /usr/bin/python

# mass installs dependencies from 'requirements.txt' (requires pip)

import pip

if __name__ == '__main__':

	mass_install()

def install(package):
	pip.main(['install', package])

def mass_install():

	with open("requirements.txt") as f:
		packages = f.readlines()

	packages = [p.strip() for p in packages]

	for p in packages:
		pip.main(['install', p])