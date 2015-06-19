from collections import defaultdict
from django.db import connection, transaction
from Apps.popCommon.utils.utility import assignValue

def genericTranslateInListVict(cursor, theKey, theVal):
    
    res = defaultdict(dict)

    #search the position of the key and of the val in the tuple 
    i=0;
    for row in cursor.description:
        if(row[0]==theKey):
            ikey=i
        if(row[0]==theVal):
            ival=i
        i+=1

    #start filling the res container
    key=''
    val=''
    counter=-1
    d = {} #Dictionary of results {'SiteName':name, 'collName' : [val1, val2, ...]}
    for row in cursor.fetchall():
        if key != row[ikey]:
            if counter!=-1:
                d[theKey]=key
                d[theVal]=l
                res[counter]=d.copy()

            counter+=1
            key=row[ikey]
            l=[]
        l.append(row[ival])

    #for the last entries, need to do that outside the loop
    if counter!=-1:
        d[theKey]=key
        d[theVal]=l
        res[counter]=d.copy()
        
    return res

def genericTranslateInListDictVict(cursor, theKey, theVal):
    
    res = defaultdict(dict)

    #search the position of the key and of the val in the tuple 
    i=0;
    others = {}
    
    for row in cursor.description:
        if(row[0]==theKey):
            ikey=i
        elif(row[0]==theVal):
            ival=i
        else:
            others[i]=row[0]
        i+=1

    #start filling the res container
    key=''
    val=''
    counter=-1
    d = {} #Dictionary of results {'SiteName':name, 'collName' : [val1, val2, ...]}
    for row in cursor.fetchall():
        if key != row[ikey]:
            if counter!=-1:
                res[key]=l.copy()

            counter+=1
            key=row[ikey]
            l={}
        l[row[ival]]=dict((v, assignValue(row[k])) for k, v in others.items())

    #for the last entries, need to do that outside the loop
    if counter!=-1:
        res[key]=l.copy()
        
    return res


