"""
Database library for Victor 

@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-2012
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

from django.db import connection, transaction
import traceback


def getAccountingSummary():

    cursor = connection.cursor()
    cursor.execute("SELECT round(total/power(10, 12), 1), round(used/power(10, 12), 1), round(toBeDeleted/power(10, 12), 1), round(inDeletionQueue/power(10, 12), 1), round(newlyCleaned/power(10, 12), 1), siteName FROM CMS_CLEANING_AGENT.T_ACCOUNTING_RECORD WHERE runId=(SELECT MAX(runId) FROM CMS_CLEANING_AGENT.t_run WHERE finished = 1) ORDER BY siteName")
    rows = cursor.fetchall()

    return rows


def getDatasetsToClean(association):

    cursor = connection.cursor()
    query = """
            SELECT dst.cont, min(dst.rcdate), max(dst.rcdate), round(sum(dst.dssize)/power(10, 9), 2), sum(dst.nacc), sum(dst.cputime), count(*), min(run.runDate), min(NVL(nblock, 0)), min(NVL(maxAccsCont, 0)), min(NVL(totalAccsCont, 0))
            FROM CMS_CLEANING_AGENT.t_cleaned_dataset dst, CMS_CLEANING_AGENT.t_run run 
            WHERE dst.runId = run.runId AND run.runId=(SELECT MAX(runId) FROM CMS_CLEANING_AGENT.t_run WHERE finished = 1) AND siteName=\'%s\' GROUP BY dst.cont
            """%(association)
    cursor.execute(query)
    rows = cursor.fetchall()

    return rows


def getBlocksForDataset(association, dataset):

    cursor = connection.cursor()
    #query = """
    #        SELECT dst.dsn, dst.rcdate, round(dst.dssize/power(10, 9), 2), dst.nacc, dst.cputime FROM CMS_CLEANING_AGENT.t_cleaned_dataset dst, CMS_CLEANING_AGENT.t_run run 
    #        WHERE dst.runId = run.runId AND run.runId=(SELECT MAX(runId) FROM CMS_CLEANING_AGENT.t_run WHERE finished = 1) AND siteName=\'%s\' AND dst.cont=\'%s\' ORDER BY dst.dsn
    #        """%(association, dataset)
    
    query = """
            SELECT dst.dsn FROM CMS_CLEANING_AGENT.t_cleaned_dataset dst, CMS_CLEANING_AGENT.t_run run 
            WHERE dst.runId = run.runId AND run.runId=(SELECT MAX(runId) FROM CMS_CLEANING_AGENT.t_run WHERE finished = 1) AND siteName=\'%s\' AND dst.cont=\'%s\' ORDER BY dst.dsn
            """%(association, dataset)
    
    cursor.execute(query)
    rows = cursor.fetchall()

    return rows


def getAssociationEvolution(association):

    cursor = connection.cursor()
    cursor.execute("SELECT acc.total/power(10, 12), acc.used/power(10, 12), run.runDate FROM CMS_CLEANING_AGENT.t_accounting_record acc, CMS_CLEANING_AGENT.t_run run WHERE acc.siteName=\'%s\' and acc.runId = run.runId order by acc.runId"%(association))
    rows = cursor.fetchall()

    return rows


def getAssociations():

    cursor = connection.cursor()
    #cursor.execute("SELECT siteName FROM CMS_CLEANING_AGENT.t_run_site WHERE runId=(SELECT MAX(runId) FROM CMS_CLEANING_AGENT.t_run WHERE finished = 1) ORDER BY siteName")
    cursor.execute("SELECT siteName FROM CMS_CLEANING_AGENT.t_run_site WHERE runId=(SELECT MAX(runId) FROM CMS_CLEANING_AGENT.t_run WHERE finished = 1) ORDER BY siteName") 
    rows = cursor.fetchall()

    return rows


def getGroupsOnSiteEvolutions(site):

    cursor = connection.cursor()
    cursor.execute("SELECT acc.siteName, round(acc.used/power(10, 12), 1), run.runDate  FROM CMS_CLEANING_AGENT.t_accounting_record acc, CMS_CLEANING_AGENT.t_run run WHERE run.runid = acc.runid and acc.siteName like %s ORDER BY acc.siteName, acc.runId", [site+'%'])
    rows = cursor.fetchall()

    return rows


def getSitesForGroupEvolutions(group):

    cursor = connection.cursor()
    cursor.execute("SELECT acc.siteName, round(acc.used/power(10, 12), 1), run.runDate  FROM CMS_CLEANING_AGENT.t_accounting_record acc, CMS_CLEANING_AGENT.t_run run WHERE run.runid = acc.runid and acc.siteName like %s ORDER BY acc.siteName, acc.runId", ['%'+group])
    rows = cursor.fetchall()

    return rows


def getTotalEvolutionSite(site):

    cursor = connection.cursor()
    cursor.execute("SELECT round(sum(acc.total)/power(10, 12), 1), run.runDate FROM CMS_CLEANING_AGENT.t_accounting_record acc, CMS_CLEANING_AGENT.t_run run WHERE run.runid = acc.runid AND acc.siteName like %s GROUP BY run.runDate ORDER BY run.runDate", [site+'%'])    
    rows = cursor.fetchall()

    return rows

def getTotalEvolutionGroup(group):

    cursor = connection.cursor()
    cursor.execute("SELECT round(sum(acc.total)/power(10, 12), 1), run.runDate FROM CMS_CLEANING_AGENT.t_accounting_record acc, CMS_CLEANING_AGENT.t_run run WHERE run.runid = acc.runid AND acc.siteName like %s GROUP BY run.runDate ORDER BY run.runDate", ['%'+group])    
    rows = cursor.fetchall()

    return rows

