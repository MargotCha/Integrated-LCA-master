from setuptools import setup, find_packages

setup(
    name='IntLCA',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author='Margarita A. Charalambous',
    author_email='ritabous2@gmail.com',
    description='This package is dedicated for large scale LCA scenario analysis while modifying the technosphere matrix. It can be used to filter and modify the technosphere matrix, perform LCA calculations,and save results'
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/yourrepository',
    classifiers=[
        'Programming Language :: Python :: 39',
        'License :: OSI Approved :: BSD-3-Clause license',
        'Operating System ::  Microsoft :: Windows :: Windows 10',
    ],
    python_requires='>=3.9'
)