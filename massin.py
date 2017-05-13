#! /usr/bin/python

# mass installs dependencies from 'requirements.txt' (requires pip)

import pip

if __name__ == '__main__':

	with open("requirements.txt") as f:
		packages = f.readlines()

	packages = [p.strip() for p in packages]

	for p in packages:
		pip.main(['install', p])
