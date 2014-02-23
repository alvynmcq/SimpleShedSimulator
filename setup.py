from distutils.core import setup

setup(
    name='SimpleShedSimulator',
    version='0.1dev',
    author='Anders Jensen',
    url='https://github.com/Egdus/SimpleShedSimulator',
    author_email='anders524@hotmail.com',
    packages=['simpleshedsimulator',
              'simpleshedsimulator.core',
              'simpleshedsimulator.gui',
              'simpleshedsimulator.pictures',
              'simpleshedsimulator.db'],
    package_data={'simpleshedsimulator.pictures': ['*.bmp'],
                  'simpleshedsimulator.db': ['*.db']}, 
    license='GPLv3',
    long_description=open('README.md').read(),
)
