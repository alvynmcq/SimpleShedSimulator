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

    if not N:
        return None
    k = (len(N)-1) * percent
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return key(N[int(k)])
    d0 = key(N[int(f)]) * (c-k)
    d1 = key(N[int(c)]) * (k-f)
    return d0+d1
    
    
    
