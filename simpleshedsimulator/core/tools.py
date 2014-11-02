'''
    SimpleShedSimulator for quick schedule risk analysis
    Copyright (C) 2014  Anders Jensen

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import pickle


def StrToInt(string):
    try:
        return int(''.join(ele for ele in string if ele.isdigit()))
    except TypeError:
        return string

def IntToStr(integer):
    try:
        result = ''.join([i for i in integer if not i.isdigit()])
        return result
    except TypeError:
        return integer

class IO:
    def WriteNetworkToFile(self, path, projectinctance):

        '''Writes the network inctance as a bytestream to file using
           the pickle module

            Args: path (str)

            Returns:
                Writes a .sss file to path
            Raises:'''

        output = open(path, 'wb')
        pickle.dump(projectinctance, output)
        output.close()

    def ReadNetworkFromFile(self, path):

        '''Reads a networkfile using the pickle module

            Args: path (str)

            Returns:
                Writes a .sss file to path
            Raises:'''

        print path, "hehehehehejek"
        output = open(path, 'rb')
        print output
        project = pickle.load(output)
        return project

        output.close()
