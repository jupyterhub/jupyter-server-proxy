import setuptools

setuptools.setup(
    name="nbserverproxy",
    version='0.8.6',
    url="https://github.com/jupyterhub/nbserverproxy",
    author="Ryan Lovett & Yuvi Panda",
    author_email="rylo@berkeley.edu",
    license="BSD 3-Clause",
    description="Jupyter server extension to proxy web services",
    packages=setuptools.find_packages(),
    install_requires=['notebook'],
    python_requires='>=3.5',
    classifiers=[
        'Framework :: Jupyter',
    ]
)
