import setuptools

setuptools.setup(
    name="nbserverproxy",
    version='0.3.2',
    url="https://github.com/jupyterhub/nbserverproxy",
    author="Ryan Lovett",
    author_email="rylo@berkeley.edu",
    license="BSD 3-Clause",
    description="Jupyter server extension to proxy web services",
    packages=setuptools.find_packages(),
    install_requires=['notebook'],
    classifiers=[
        'Framework :: Jupyter',
    ]
)
