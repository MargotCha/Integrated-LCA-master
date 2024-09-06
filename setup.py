from setuptools import setup, find_packages

setup(
    name='IntLCA-dev',
    version='0.1.0',
    author='Margarita A. Charalambous',
    author_email='ritabous2@gmail.com',
    description='IntLCA package for integrating emerging technologies in inventory matrices and performing large scale scenario analysis.' ,
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/MargotCha/Integrated_LCA/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',  # Updated classifier
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    packages=find_packages(),
    python_requires=">=3.8, <=3.12",
    install_requires=[
        "brightway2==2.4.3",
        "premise>=1.5.1",
        "ipython==8.12.3",
        "jupyterlab",
    ]
)