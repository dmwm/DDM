"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import traceback
import time
import urllib2

from dq2.common import log as logging

from xml.dom.minidom import parseString

from dq2.victor.accountingInterface import AccountingInterface
from dq2.victor.utils import callRetry, TERA
from dq2.victor.factory import create_tool 
from dq2.victor import config    
from utils import get_json_data, get_json_data_improper, get_json_data_https
from groupPledges import groupPledges 


class AccountingInterface(AccountingInterface):
    """
    Class encapsulating the CMS Storage Information Interface.    
    """    
    __freeRatio =    {'default':0.1}
    __freeAbsolute = {'default':25*TERA}
    __targetRatio =  {'default':0.2}   
    __targetAbsolute = {}     
    __specifiedSpacetokens = []   
    __centralPledge = 0.7 
    threshold_per_site = {}
                    
    __logger = logging.getLogger("dq2.victor.AccountingInterface")
    
    #__configurationInterface='DQ2ConfigurationInterface'
        
    
    def __init__(self, name):
                
        self.__nodeusage  = self.__get_nodeusage_values()
        self.__groupusage = self.__get_groupusage_values()
        
        self.__logger.debug('NODE USAGE: %s' %self.__nodeusage)
        self.__logger.debug('GROUP USAGE: %s' %self.__groupusage)
                
        freeRatio = config.get_dict('freeRatio', type=float)
        if freeRatio is not None:
            self.__freeRatio = freeRatio
        
        freeAbsolute = config.get_dict('freeAbsolute', type='size')
        if freeAbsolute is not None:
            self.__freeAbsolute = freeAbsolute
                
        targetRatio=config.get_dict('targetRatio', type=float)
        if targetRatio is not None:
            self.__targetRatio = targetRatio
                            
        targetAbsolute=config.get_dict('targetAbsolute', type='size')
        if targetAbsolute is not None:
            self.__targetAbsolute = targetAbsolute 
        
        centralPledge=config.get_dict('centralPledge', type=float)
        if centralPledge is not None:
            self.__centralPledge = centralPledge        
        
        self.__site_name_map = self.__get_site_name_map()
	self.__sitedb_pledges = self.__get_sitedb_pledges()
    
    def __get_site_name_map(self):

	url='https://cmsweb.cern.ch/sitedb/data/prod/site-names'
        site_map_data = get_json_data_https(url)

	siteIdx=site_map_data['desc']['columns'].index('site_name')
	typeIdx=site_map_data['desc']['columns'].index('type')
	nameIdx=site_map_data['desc']['columns'].index('alias')

	site_name_map = {}

	for item in site_map_data['result']:
		try:
			(site_name_map[item[siteIdx]][item[typeIdx]]).append(item[nameIdx])
     		except KeyError:
			try:
				site_name_map[item[siteIdx]][item[typeIdx]]=[item[nameIdx]]
			except KeyError:
				site_name_map[item[siteIdx]]={item[typeIdx]:[item[nameIdx]]}
	self.__logger.debug(site_name_map)

	return site_name_map

    def __get_sitedb_pledges(self):

	url='https://cmsweb.cern.ch/sitedb/data/prod/resource-pledges'
	resource_pledge_data = get_json_data_https(url)

	siteIdx=resource_pledge_data['desc']['columns'].index('site_name')
	updateTimeIdx=resource_pledge_data['desc']['columns'].index('pledge_date')
	yearIdx=resource_pledge_data['desc']['columns'].index('quarter')
	diskIdx=resource_pledge_data['desc']['columns'].index('disk_store')
	localDiskIdx=resource_pledge_data['desc']['columns'].index('local_store')
	
	resource_pledges = {}

	current_year=time.gmtime().tm_year

	for item in resource_pledge_data['result']:
		if item[yearIdx]==current_year:
			try:
				if item[updateTimeIdx] >= resource_pledges[item[siteIdx]]['pledge_date']:
					resource_pledges[item[siteIdx]]['disk_store']=item[diskIdx]
	                                resource_pledges[item[siteIdx]]['local_store']=item[localDiskIdx]
	                                resource_pledges[item[siteIdx]]['pledge_date']=item[updateTimeIdx]
			except KeyError:
				resource_pledges[item[siteIdx]]={'disk_store':item[diskIdx], 'local_store':item[localDiskIdx], 'pledge_date':item[updateTimeIdx]}
	
	self.__logger.debug(resource_pledges)

	return resource_pledges

    def __get_nodeusage_values(self):
        
        url = "https://cmsweb.cern.ch/phedex/datasvc/json/prod/nodeusage"
        nodeusage_aux = get_json_data(url)
        nodeusage = {}
        
        #Massage information to make it more accessible        
        for site_dic in nodeusage_aux['phedex']['node']:
        
            site = site_dic["name"]
            try:
                nodeusage[site]={"src_node_bytes": int(site_dic["src_node_bytes"]),
                                 "nonsrc_node_bytes": int(site_dic["nonsrc_node_bytes"]),
                                 "noncust_dest_bytes": int(site_dic["noncust_dest_bytes"]),                                
                                 "noncust_node_bytes": int(site_dic["noncust_node_bytes"]),                                
                                 "cust_node_bytes": int(site_dic["cust_node_bytes"]),
                                 "cust_dest_bytes": int(site_dic["cust_dest_bytes"])                                 
                                }
            except:
                self.__logger.error('Incomplete information for site %s in %s' %(site, url))   
    
        return nodeusage

        
    def __get_groupusage_values(self):
        
        url = "https://cmsweb.cern.ch/phedex/datasvc/json/prod/groupusage"
        groupusage_aux = get_json_data(url)
        groupusage = {}
        
        #Massage information to make it more accessible        
        for site_dic in groupusage_aux['phedex']['node']:
        
            site = site_dic["name"]
            groupusage[site]={}
            for group_dic in site_dic['group']:
                group = group_dic["name"]
                try:
                    groupusage[site][group]={"dest_bytes": int(group_dic["dest_bytes"]),    
                                             "node_bytes": int(group_dic["node_bytes"])}
                except:
                    self.__logger.error('Incomplete information for group %s in site %s in %s' %(group, site, url))   
    
        return groupusage
    
    
    def calculateSpaceToClean(self, site, used, total, tobedeleted, indeletionqueue):
        
        site, physicsgroup = site.split('^')        
        
        targetAbsolute   = 25*TERA
        targetRatio  = 0.3
        bigsiteThreshold = 100*TERA         
         
        if total > bigsiteThreshold:                
            targetValue = total-targetAbsolute   #Targetvalue is of used diskspace                
        else:
            targetValue = total*(1-targetRatio)  #Targetvalue is of used diskspace                                                                        
        
        effectivelyused = used - tobedeleted - indeletionqueue
        
        tobecleaned = effectivelyused - targetValue
        return tobecleaned, None
    
    
    def getSites(self, spacetokens=[]):
	"""        
        @return: List with all the sites.
        """
	
	sites = []

	for site in self.__site_name_map:
		site_name = self.__site_name_map[site]['cms'][0]
		try:
        	        groups = groupPledges[site_name].keys()
	                for group in groups:
                	    sites.append('%s^%s'%(site_name, group))
            	except KeyError:
                	pass

        return sites


    def __getUsedSpaceCentral(self, site):
        
        try: 
            #Basic usage of storage
            bytes = self.__nodeusage[site]['noncust_node_bytes'] + self.__nodeusage[site]['src_node_bytes'] + self.__nodeusage[site]['nonsrc_node_bytes']
            #Add reserved space of ongoing transfers
            #bytes = bytes + self.__nodeusage[site]['noncust_dest_bytes']
            #THE PREVIOUS CASE IS ONLY VALID FOR T2s!!!
            self.__logger.info('Used space for site %s: %.2f' %(site, bytes/TERA))
            return bytes
        except Exception, e:
            self.__logger.error('No used space for site %s (%s)' %(site, e))
            return None               
        
        
    def __getUsedSpaceGroup(self, site, group):
        
        try: 
            #Basic usage of storage
                            
            bytes = self.__groupusage[site][group]['node_bytes']
            self.__logger.info('Used space for site %s by group %s: %.2f' %(site, group, bytes/TERA))
            return bytes
        except Exception, e:
            self.__logger.error('No used space for site %s by group %s (%s)' %(site, group, e))
            return None                      


    def getUsedSpace(self,site):
        
        site, physicsgroup = site.split('^')
        return self.__getUsedSpaceGroup(site, physicsgroup)


    def __getSiteDBPledge(self, site):

	for item in self.__site_name_map:
	    if self.__site_name_map[item]['cms'][0]==site:
		siteId=item

	try:
	    pledge=((self.__sitedb_pledges[siteId]['disk_store'] or 0)-(self.__sitedb_pledges[siteId]['local_store'] or 0))*TERA*self.__centralPledge
	    if pledge is not None:
               	self.__logger.info('Pledged space for site %s: %.2f' %(site, pledge/TERA))
            return pledge

	except KeyError:
	    self.__logger.error('No pledge for site %s' %(site))
	    return None
    
    def __getGroupPledge(self, site, group):
                
        try: 
            bytes = groupPledges[site][group]
            self.__logger.info('Pledged space for site %s by group %s: %.2f' %(site, group, bytes/TERA))
            return bytes
        except Exception, e:
            self.__logger.error('No pledged space for site %s by group %s (%s)' %(site, group, e))
            return None    

            
    def getTotalSpace(self,site):    

        site, physicsgroup = site.split('^')
        return self.__getGroupPledge(site, physicsgroup)
        
    
    def getToBeDeletedSpace(self,site):
        """
        MOCK. Not needed by CMS
        """
        return 0                
        
        
    def refreshSiteStatistics(self,site):            
        """
        MOCK. Not needed by CMS
        """
        return True
        
    
    def getSpaceInDeletionQueue(self,site):                    
        '''
        Return space which is freed up by deletion
        '''
        return 0
        #try: 
            #Basic usage of storage
        #    bytes = self.__nodeusage[site]['src_node_bytes'] + self.__nodeusage[site]['nonsrc_node_bytes']
        #    self.__logger.info('Space in deletion queue for site %s: %.2f' %(site, bytes/TERA))
        #    return bytes
        #except:
        #    self.__logger.error('No space in deletion queue for site %s' %(site))
        #    return 0 #It has to be 0, not None!
    
    
    def isFull(self, site, ratio, free):
        
        thresholdFree    = 0.1
        thresholdAbsFree = 15*TERA                          
                     
        if ratio > thresholdFree or free > thresholdAbsFree:
            return False
        
        return True


