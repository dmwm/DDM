"""
Different utilities

@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import time
import simplejson
import os
import datetime

TODAY = datetime.date.today().strftime("%Y/%m/%d")
PATH = '/tmp/data/victor/%s'%(TODAY) #Will create subdirectories for year, month and day    
LATEST = '/tmp/data/victor/latest'


GIGA = 10.0**9
TERA = 10.0**12
PETA = 10.0**15

HOUR = 3600

def callRetry(call, *args, **kwargs):
    """
    Wrapper to make remote calls reliable.
    """
    natt, sleepatt = 3, 5
    for i in xrange(1, natt+1):
        try:
            return call(*args, **kwargs)
        except:
            if i < natt:
                time.sleep(sleepatt)
            else:
                raise


def castListToIntegers(lst):
    
    return map(lambda x: int(x), lst)


def epochTime(datetime_var):
    
    return time.mktime(datetime_var.timetuple())


def create_shards(lst, n):
    blk, i = [], 0
    for el in lst:
        blk.append(el)
        i += 1
        if i == n:
            yield blk
            blk, i = [], 0
    if i > 0: yield blk    


def dumpTemporaryInfo(data, path, name):
    
    import simplejson
    import os
    import datetime    

    f=open('%s/%s'%(path, name), 'w')
    simplejson.dump(data, f)
    f.close()
    
    return


def dumpInfo(data, name):
    
    createDirectory()
    f=open('%s/%s.json'%(PATH, name), 'w')
    simplejson.dump(data, f)
    f.close()
    
    return


def dumpAccountingInfo(data):    
    
    f=open('%s/AccountingSummary.csv'%(PATH), 'w')
    f.write('site used(TB) total(TB) tobedeleted(TB) indeletionqueue(TB)\n')
    
    sites=sorted(data.keys())
    
    for site in sites:
        if data[site]['used']:
            used = round(data[site]['used']/TERA, 2)
        else:
            used = None
        if data[site]['total']:
            total = round(data[site]['total']/TERA, 2)
        else:
            total = None
        if data[site]['tobedeleted']:
            tobedeleted = round(data[site]['tobedeleted']/TERA, 2)
        else:
            tobedeleted = None
        if data[site]['indeletionqueue']:
            indeletionqueue = round(data[site]['indeletionqueue']/TERA, 2)
        else:
            indeletionqueue = None
        if data[site]['newlycleaned']:
            newlycleaned = round(data[site]['newlycleaned']/TERA, 2)
        else:
            newlycleaned = None
            
        f.write('%s %s %s %s %s %s\n' %(site, used, total, tobedeleted, indeletionqueue, newlycleaned))
    f.close()
    
    return


def dumpCleaningInfo(site, datasets, sizes, creationdates, cpus, naccs, spacesummary, cleaned, nBlocks, maxAccsCont, totalAccsCont):
            
    createDirectory()

    #Print datasets to delete        
    f=open('%s/%s.csv'%(PATH, site), 'w')
    f.write('dataset size cdate cputime nacc\n')
    
    siteInfo = []

    for dataset, size, cdate, cpu, nacc, nBlock, maxAccCont, totalAccCont in zip(datasets, sizes, creationdates, cpus, naccs, nBlocks, maxAccsCont, totalAccsCont):

        f.write('%s %.2fGB %s %s %s\n' %(dataset, size/GIGA, datetime.datetime.fromtimestamp(cdate).strftime("%d/%m/%Y"), cpu, nacc))
        siteInfo.append({'dataset': dataset, 'size': size, 'cdate': cdate, 'cpu': cpu, 'nacc': nacc, 'nBlock': nBlock, 'maxAccCont': maxAccCont, 'totalAccCont': totalAccCont})
    
    #Print overall summary of how the site was left
    used, total, cleanedspace = spacesummary        
    f.write('-----------------------------------------------------------------\n')
    f.write('USED: %.2fTB TOTAL: %.2fTB CLEANED: %.2fTB STATUS: %s\n' %(used/TERA, total/TERA, cleanedspace/TERA, cleaned))
    
    f.close()
    
    dumpInfo(siteInfo, site)
    
    return


def createDirectory():
    try:        
        os.makedirs(PATH)
        os.unlink(LATEST)
        os.symlink(PATH, LATEST)
    except OSError:
        pass

    
def prepareSummary(data):
    
    createDirectory()
    
    dumpAccountingInfo(data)
    dumpInfo(data, 'AccountingSummary')
    return
