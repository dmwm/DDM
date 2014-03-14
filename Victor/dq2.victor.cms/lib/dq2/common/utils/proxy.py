"""
Contains some utilities to parse proxy.

@license: Apache License 2.0
@author: Vincent Garonne <vincent.garonne@cern.ch>
"""
"""
Copyright (c) ATLAS Distributed Data Management project, 2009.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
"""
import re
import commands

            
def check_for_certificate():
    
        proxycheck = 'voms-proxy-info'
        
        status, output = commands.getstatusoutput('%s -e'%proxycheck)

        if 'command not found' in output:
            print 'WARNING: Missing voms-proxy-init binary. Unable to verify proxy at the client. Continuing!'
            proxycheck = 'grid-proxy-info'
            status, output = commands.getstatusoutput('%s -e'%proxycheck)
            if 'command not found' in output:
                raise Exception('Missing both voms-proxy-info and grid-proxy-info binaries. Please use the correct setup.sh!')
                sys.exit(-1)
        elif status not in (0,256):
            raise Exception('Missing voms proxy. Create one with: voms-proxy-init -voms atlas')
            sys.exit(-1)
        
        return True
            
def get_user_name_from_dn (dn):
    '''
    Convert a dn into a valid atlas user name
    '''    
    dn = dn[dn.find('/CN=')+len('/CN='):]
    if dn.find('/')> 0: dn = dn[:dn.find('/')]    
    
    # Remove bad chars
    chars = [' - ATLAS',' ','-','_', '.', "'"]
    for c in chars: dn = dn.replace (c,'')        
    
    # Remove digits
    dn = re.sub("\d", "", dn)
    
    return dn

def get_dn ():
   '''
   Parse voms-proxy-info output to get the list of fqans
   '''
   status, output = commands.getstatusoutput ('voms-proxy-info')
   if status not in (0,256): raise Exception('Missing voms proxy. Create one with: voms-proxy-init -voms atlas')
   prefix = 'issuer    : '
   return filter (lambda s: prefix in s, output.split ('\n'))[0][len(prefix):]

def get_fqans ():
   '''
   Parse voms-proxy-info output to get the list of fqans
   '''
   status, output = commands.getstatusoutput ('voms-proxy-info --all')
   if status not in (0,256): raise Exception('Missing voms proxy. Create one with: voms-proxy-init -voms atlas')
   prefix     = 'attribute : '
   suffix     = '/Capability=NULL'
   experiment = '/atlas/'
   return map (lambda s: (s.replace(prefix,'')).replace (suffix, ''), filter (lambda s: prefix and experiment in s, output.split('\n')))

if __name__ == "__main__":
    
  print 'check_for_certificate:' , check_for_certificate ()
  print 'fqans:'                 , get_fqans ()
  print 'dn:'                    , get_dn ()
  print 'user name:'             , get_user_name_from_dn(get_dn())