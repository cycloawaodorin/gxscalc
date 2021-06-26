import setuptools

version = '0.0.4'
with open('README.md', 'r') as f:
	long_description = f.read()

setuptools.setup(
	name = 'gxscalc',
	version = version,
	url = 'https://github.com/cycloawaodorin/gxscalc',
	author = 'KAZOON',
	author_email = 'cycloawaodorin+pypi@gmail.com',
	maintainer = 'KAZOON',
	maintainer_email = 'cycloawaodorin+pypi@gmail.com',
	description = 'A Python package for speed-based calculation of F-ZERO GX.',
	long_description = long_description,
	long_description_content_type = 'text/markdown',
	packages = setuptools.find_packages(),
	install_requires = ['pandas', 'matplotlib'],
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
	python_requires = '>=3.7'
)
