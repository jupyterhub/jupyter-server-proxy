import setuptools

setuptools.setup(
    name="nbrsessionproxy",
    version='0.1.6',
    url="https://github.com/ryanlovett/nbrsessionproxy",
    author="Ryan Lovett",
    description="Jupyter extensions to proxy RStudio's rsession",
    packages=setuptools.find_packages(),
    install_requires=[ 'tornado', 'notebook' ],
    package_data={'nbrsessionproxy': ['static/*']},
)
