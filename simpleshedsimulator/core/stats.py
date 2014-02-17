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


import math


'''stat.py contains simple statistical formulas'''



def mean(s):
    ''' caluclates the average'''
    if len(s) == 0:
        print 'Need more observations to calculate mean'
    else:
        return sum(s)/len(s)

def var(s):
    ''' caluclates the variance'''
    if len(s) == 0:
        print 'Need more observations to calculate variance'
    elif len(s) == 1:
        return 0.0
    else:
        a=mean(s)
        terms=[]
        for q in s:
            terms.append((q-a)**2)
        return sum(terms)/(len(s)-1)
def skew():
	'must be defined'
	return

def kurt():
	'''must be defiened'''
	return

def cov(s,d):
    ''' caluclates the covariance between to lists of observations'''
    if len(s) != len(d):
        print 'Unequal list sizes, cant calculate covariance'
    elif len(s) == 0:
        print 'Need more observatons to calculate covariance'
    elif len(s) == 1:
        return 0.0
    else:
        terms=[]
        A_s=mean(s)
        A_d=mean(d)
        for q, w in zip(s,d):
            terms.append((q-A_s)*(w-A_d))
        return sum(terms)/(len(s)-1)


def cov(s,d):
    ''' caluclates the covariance between to lists of observations'''
    if len(s) != len(d):
        print 'Unequal list sizes, cant calculate covariance'
    elif len(s) == 0:
        print 'Need more observatons to calculate covariance'
    elif len(s) == 1:
        return 0.0
    else:
        terms=[]
        A_s=mean(s)
        A_d=mean(d)
        for q, w in zip(s,d):
            terms.append((q-A_s)*(w-A_d))
        return sum(terms)/(len(s)-1)

def cor(s,d):
    ''' caluclates the correlation  between to lists of observations'''
    if len(s) != len(d):
        print 'Unequal list sizes, cant calculate correlation'
    elif len(s) == 0:
        print 'Need more observatons to calculate correlation'
    elif len(s) == 1:
        print 'Only one pair of observations'
    else:
        SD_s=var(s)**0.5
        SD_d=var(d)**0.5
        return cov(s,d)/(SD_s*SD_d)

def beta(s,d):
    
    
    ''' caluclates the beta coefficient  between to lists of observations'''
    if len(s) != len(d):
        print 'Unequal list sizes, cant calculate beta'
    elif len(s) == 0:
        print 'Need more observatons to calculate beta'
    elif len(s) == 1:
        print 'Only one pair of observations'
    else:
        return cov(s,d)/var(s)

def percentile(N, percent, key=lambda x:x):
    '''Calculates the percentile value'''
    N.sort()
    k = (len(N)-1) * percent
    floor = math.floor(k)
    ceil = math.ceil(k)
    
    if floor == ceil:
        return key(N[int(k)])
    
    d0 = key(N[int(floor)]) * (ceil-k)
    d1 = key(N[int(ceil)]) * (k-floor)
    return d0+d1
    
    
    
