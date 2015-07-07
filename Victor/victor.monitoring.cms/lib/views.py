"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011-2012
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""
from __future__ import print_function

from django.http      import HttpResponseNotFound
from django.http      import HttpResponseRedirect
from django.shortcuts import render_to_response
from datetime import date
import time
import victorDao
import decimal

threshold = 0.9

def invalidView(request):
    return HttpResponseNotFound('<h1>INVALID URL</h1> <P> <a href="/victor/accounting">Back to starting page</a>')
    
    
def splitAssociation(association):
    
    site, group = association.split('^')
    
    site_split = site.split('_')
    tier  = site_split[0]
    cloud = site_split[1]
    site  = '_'.join(site_split[2:])
    return cloud, site, tier, group


def generateAssociationMenu():
    
    rows = victorDao.getAssociations()
    structure = {} 
    
    for row in rows:
        association = str(row[0])
        cloud, site, tier, group = splitAssociation(association)
        structure.setdefault(cloud, {})
        structure[cloud].setdefault(site, [])
        structure[cloud][site].append(group)
    
    #Flatten out the structure
    flat_structure = []
    
    clouds = sorted(structure.keys())
    for cloud in clouds:
        print (cloud)                
        sites = sorted(structure[cloud].keys())
        site_dicts = []
        for site in sites:
            groups = sorted(structure[cloud][site])
            site_dicts.append({'name': site, 'groups': groups})
            
        flat_structure.append({'name': cloud, 'sites': site_dicts})
        
    return flat_structure    
    
    
def accountingView(request):    

    rows = victorDao.getAccountingSummary()
    clouds_dict = {}
    rows_massaged = []
    
    for row in rows: 
        total, used, toBeDeleted, inDeletionQueue, newlyCleaned, association = row

        if isinstance(total, decimal.Decimal):
            total = float(total)
        if isinstance(used, decimal.Decimal):
            used = float(used)

        full = False
        if used!=None and total!=None:
            if float(used)/float(total) > threshold:
                full = True            
        
        cloud, site, tier, group = splitAssociation(association)        
        rows_massaged.append([cloud, site, tier, group, total, used, newlyCleaned, full])
        
        clouds_dict.setdefault(cloud, {'total_list': [], 'threshold_list': [], 'used_list': [], 'toBeDeleted_list': [], 'inDeletionQueue_list': [], 'newlyCleaned_list': [], 'site_list': []})
        
        if total != None and used != None:
            clouds_dict[cloud]['total_list'].append(total)
            clouds_dict[cloud]['threshold_list'].append(threshold*total)
            clouds_dict[cloud]['used_list'].append(used)
            clouds_dict[cloud]['site_list'].append('%s: %s'%(site, group))
            
        if full:
            clouds_dict.setdefault('full', {'total_list': [], 'threshold_list': [], 'used_list': [], 'toBeDeleted_list': [], 'inDeletionQueue_list': [], 'newlyCleaned_list': [], 'site_list': []})
            clouds_dict['full']['threshold_list'].append(threshold*total)
            clouds_dict['full']['total_list'].append(total)
            clouds_dict['full']['used_list'].append(used)
            clouds_dict['full']['site_list'].append('%s: %s'%(site, group))                

            #clouds_dict[cloud]['toBeDeleted_list'].append(toBeDeleted)
            #clouds_dict[cloud]['inDeletionQueue_list'].append(inDeletionQueue)
            #clouds_dict[cloud]['newlyCleaned_list'].append(newlyCleaned)
            
    #Flatten out the dictionary
    clouds = sorted(clouds_dict.keys())
    clouds_flat = map(lambda cloud: (cloud, clouds_dict[cloud]), clouds)
    
    if 'full' in clouds:
        default_tab = len(clouds)-1
    else:
        default_tab = 0    
    
    today = str(date.today())    
    menu = generateAssociationMenu()
    
    return render_to_response('overview.html', {'today': today, 'clouds': clouds_flat, 'rows': rows_massaged, 'regions': menu, 'default_tab': default_tab})

def sortByBlock(datasets):
    
    return datasets_by_block


def associationView(request, site = None, group = None):    

    group_req = group
    site_req  = site
    
    #Get the data to generate the table of datasets to clean
    runDate = None
    blockTable = False
    datasets = victorDao.getDatasetsToClean('%s^%s' %(site, group_req))    
    if datasets:
        runDate = datasets[0][6]
        blockTable = True                
    
    #Get the data to generate the space evolution plot for the ASSOCIATION
    rows = victorDao.getAssociationEvolution('%s^%s' %(site, group_req))
    data_used = []
    data_total = []
    
    for row in rows:
        total, used, runDate = row 
        timestamp = time.mktime(runDate.timetuple()) * 1000 #multiply by 1000 for javascript 
        if used!=None:
            data_used.append([timestamp,  int(used)])
        if total!=None:
            data_total.append([timestamp, int(total)])
    
    full = False
    if used and total:
        if float(used)/float(total)>0.9:        
            full = True
    
    #------------------------------------------------------------------------                
    #Get the data to generate the space evolution plot for the SITE with all groups
    #------------------------------------------------------------------------
    rows_groups = victorDao.getGroupsOnSiteEvolutions(site_req)
    group_accounting = {}
    for row in rows_groups:
         association, used, run_date = row
         if not used:
             continue 
         group = association.split('^')[1]
         group_accounting.setdefault(group, [])         
         group_accounting[group].append([time.mktime(run_date.timetuple())*1000, float(used)])               
    
    group_accounting_flat = []
    for group in group_accounting:
        group_accounting_flat.append([group, group_accounting[group]])            

    rows_total = victorDao.getTotalEvolutionSite(site_req)
    total_processed_group = []    
    for row in rows_total:
         total, run_date = row
         total_processed_group.append([time.mktime(run_date.timetuple())*1000, float(total)])  

    #------------------------------------------------------------------------                
    #Get the data to generate the space evolution plot for the GROUP on all sites
    #------------------------------------------------------------------------
    rows_sites = victorDao.getSitesForGroupEvolutions(group_req)
    site_accounting = {}
    for row in rows_sites:
         association, used, run_date = row
         if not used:
             continue 
         site = association.split('^')[0]
         site_accounting.setdefault(site, [])         
         site_accounting[site].append([time.mktime(run_date.timetuple())*1000, float(used)])               
    
    site_accounting_flat = []
    for site in site_accounting:
        site_accounting_flat.append([site, site_accounting[site]])            

    rows_total = victorDao.getTotalEvolutionGroup(group_req)
    total_processed_site = []    
    for row in rows_total:
         total, run_date = row
         total_processed_site.append([time.mktime(run_date.timetuple())*1000, float(total)])  


    #Get the date and the menu                  
    today = str(date.today())
    menu = generateAssociationMenu()
    
    return render_to_response('space_evolution_view.html', {'site': site_req, 'full': full, 'group': group_req, 'today': today, 'run_date': runDate, 'datasets': datasets, 
                                                            'block_table': blockTable,'data_used': str(data_used), 'data_total': str(data_total),
                                                            'data_site': group_accounting_flat, 'totals_site': total_processed_group, 
                                                            'data_group': site_accounting_flat, 'totals_group': total_processed_site,  
                                                            'regions': menu})


def getBlocksForDataset(request, info = None):    
    
    association = info.split('/')[0]
    dataset = '/%s'%('/'.join(info.split('/')[1:]))
    
    blocks_string=''
    blocks = victorDao.getBlocksForDataset(association, dataset)    
    
    for block in blocks:
        if blocks_string=='':
            blocks_string = '%s'%(str(block[0]))
        else:
            blocks_string = '%s, %s'%(blocks_string, str(block[0]))
            
    return render_to_response('blocks_table.html', {'blocks': blocks_string})


def siteView(request, site = None):                    

    #Get the data to generate the space evolution plot for the complete SITE
    rows_groups = victorDao.getGroupEvolutions(site)
    group_accounting = {}
    for row in rows_groups:
         association, used, run_date = row
         group = association.split('^')[1]
         group_accounting.setdefault(group, [])
         group_accounting[group].append([time.mktime(run_date.timetuple())*1000, float(used)])  
    
    group_accounting_flat = []
    for group in group_accounting:
        group_accounting_flat.append([group, group_accounting[group]])            

    #Get the data to generate the space evolution plot
    rows_total = victorDao.getTotalEvolution(site)
    total_processed = []    
    for row in rows_total:
         total, run_date = row
         total_processed.append([time.mktime(run_date.timetuple())*1000, float(total)])  

                      
    today = str(date.today())
    menu = generateAssociationMenu()
    
    return render_to_response('site_evolution_chart.html', {'site': site, 'today': today, 'data': group_accounting_flat, 'totals': total_processed, 'regions': menu})


def aboutView(request):                    
    menu = generateAssociationMenu()
    return render_to_response('about.html', {'regions': menu})

