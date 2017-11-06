import setuptools

setuptools.setup(
    name="nbrsessionproxy",
    version='0.3.0',
    url="https://github.com/ryanlovett/nbrsessionproxy",
    author="Ryan Lovett",
    description="Jupyter extensions to proxy RStudio's rsession",
    packages=setuptools.find_packages(),
	keywords=['Jupyter'],
	classifiers=['Framework :: Jupyter'],
    install_requires=[ 'tornado', 'notebook', 'nbserverproxy' ],
    package_data={'nbrsessionproxy': ['static/*']},
)
