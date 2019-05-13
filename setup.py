from setuptools import setup, find_packages

setup(
    name='celine-simplerequest',
    version='1.0.4',
    author='Celine Yeh',
    author_email='cat841230@gmail.com',
    description='A simple request.',
    url='https://github.com/CatMao1230/celine-simplerequest',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
