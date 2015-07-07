import cx_Oracle

def genericTranslateInDict(cursor):
    """
    Translate a query cursor into a dictionari containing result row
    """
    
    data = {}
    key = []
    for row in cursor.description:
        key.append(row[0])

    jkey = 0
    for row in cursor.fetchall():
        i = 0
        dic = {}
        for val in row:
            dic[key[i]] = val
            i += 1
        data[jkey] = dic.copy()
        jkey += 1
    return data

startdate = "2015/05/04 12:00:00"
enddate = "2015/05/04 14:00:00"

startdate1 = "2015/05/04 11:45:00"
enddate1 = "2015/05/04 14:15:00"

# Get data from crab popularity db
connection_string="connection string for crabdb"
connection = cx_Oracle.Connection(connection_string)
cursor = cx_Oracle.Cursor(connection)
query = "SELECT * from CMS_POPULARITY_SYSTEM.RAW_FILE where STARTEDRUNNINGTIMESTAMP between TO_DATE ('%s', 'yyyy/mm/dd hh24:mi:ss') and TO_DATE ('%s',  'yyyy/mm/dd hh24:mi:ss') and FINISHEDTIMESTAMP between TO_DATE ('%s', 'yyyy/mm/dd hh24:mi:ss') and TO_DATE ('%s',  'yyyy/mm/dd hh24:mi:ss')" %(startdate1, enddate1, startdate1, enddate1)
cursor.execute(query)

# Get data from CMSSW db
connection_string2="connection string for cmsswdb"
connection2 = cx_Oracle.Connection(connection_string2)
cursor2 = cx_Oracle.Cursor(connection2)
query2 = "SELECT * from T_RAW_CMSSW where START_DATE between TO_DATE ('%s', 'yyyy/mm/dd hh24:mi:ss') and TO_DATE ('%s', 'yyyy/mm/dd hh24:mi:ss') AND END_DATE between TO_DATE ('%s', 'yyyy/mm/dd hh24:mi:ss') and TO_DATE ('%s', 'yyyy/mm/dd hh24:mi:ss')"%(startdate, enddate, startdate, enddate)
cursor2.execute(query2)

# transcripe both into dicts
list1 = genericTranslateInDict(cursor)
list2 = genericTranslateInDict(cursor2)

# match entries of first list to second
matching = []
only_crab = []
for e1 in list1:
    if list1[e1]['FILENAME'].find("/store/"):
        list1[e1]['FILENAME'] = list1[e1]['FILENAME'][list1[e1]['FILENAME'].find("/store/"):]
    for e2 in list2:
        if list2[e2]['FILE_LFN'].find("/store/"):
            list2[e2]['FILE_LFN'] = list2[e2]['FILE_LFN'][list2[e2]['FILE_LFN'].find("/store/"):]
        if (list1[e1]['SITENAME'] == list2[e2]['SITE_NAME'] and list2[e2]['FILE_LFN'] == list1[e1]['FILENAME'] and list1[e1]['STARTEDRUNNINGTIMESTAMP'] <= list2[e2]['START_DATE'] and list2[e2]['START_DATE'] < list1[e1]['FINISHEDTIMESTAMP'] and list1[e1]['STARTEDRUNNINGTIMESTAMP'] < list2[e2]['END_DATE'] and list2[e2]['END_DATE'] <= list1[e1]['FINISHEDTIMESTAMP']):
            matching.append(list1[e1])
            break
        elif list1[e1] not in only_crab:
            only_crab.append(list1[e1])

print "Overlap: ", len(matching)/float(len(list1))
print "Only in crab ", len(only_crab), " crab entries ", len(list1), " cmssw entries ", len(list2)
