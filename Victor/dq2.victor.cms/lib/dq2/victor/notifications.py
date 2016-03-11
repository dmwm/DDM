"""
Mail notifications library 

@copyright: European Organization for Nuclear Research (CERN)
@author: Andrii Thykonov U{andrii.tykhonov@ijs.si<mailto:andrii.tykhonov@ijs.si>}, CERN, 2010-2011
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import formatdate

from dq2.victor import config

__SUBJECT='[Victor notification]'
__SIGNATURE='This is an automatically generated notification. Please do not reply to this mail.'

__stopAlerts=True
stopAlerts = config.get_config('stopAlerts', type=bool)
if stopAlerts is not None:
    __activateAlerts = stopAlerts

__opsRecipients=['andrii.tykhonov@ijs.si', 'fernando.harald.barreiro.megino@cern.ch']
opsRecipients = config.get_config('opsRecipients', type=list)
if opsRecipients:
    __opsRecipients = opsRecipients
    
__devRecipients=['andrii.tykhonov@ijs.si', 'fernando.harald.barreiro.megino@cern.ch']
devRecipients = config.get_config('devRecipients', type=list)
if devRecipients:
    __devRecipients = devRecipients                  
        
#Development: Overwrite temporarily
__opsRecipients=['fernando.harald.barreiro.megino@cern.ch']
__devRecipients=['fernando.harald.barreiro.megino@cern.ch']    

__sender='ddmusr01@cern.ch'


def __send_mail(text, contacts, sender, subject):
    
    if not text:
        return
                                                                                                                           
    msg=MIMEMultipart()
    msg['From']    = sender
    msg['Date']    = formatdate(localtime=True)
    msg['Subject'] = subject
    msg['To']      = ','.join(contacts)          # Main text
    msg.attach(MIMEText(text))
    smtp=smtplib.SMTP('localhost')
    
    # Send the email
    smtp.sendmail(sender, contacts, msg.as_string())    
    smtp.close()
    
def sendUncleanedMail(clean_status): 
    
    subject='%s %s'%(__SUBJECT, 'Incompletely cleaned sites')
    
    text="Victor failed to successfully clean following sites:\n"
    
    for site in clean_status:
        if not clean_status[site]:
            text = "%s\n%s"%(text, site)
    
    text = "%s\n%s"%(text, __SIGNATURE)    
    __send_mail(text, __opsRecipients, __sender, subject)

    
def sendErrorMail(errortext):
    subject='%s %s'%(__SUBJECT, 'Victor excepted and needs attention') 
    text="The exception was raised:\n%s\n%s"%(errortext, __SIGNATURE)
    if not stopAlerts:                
        __send_mail(text, __devRecipients, __sender, subject)


def sendWarningMail(text):
    subject=__SUBJECT 
    #subject="DiskSpaceMonitor warning"                    
    __send_mail('%s%s'%(__HEADER, text), __opsRecipients, __sender, subject)
            