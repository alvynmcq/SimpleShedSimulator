# SimpleShedSimulator for quick schedule risk analysis
# Copyright (C) 2014  Anders Jensen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


