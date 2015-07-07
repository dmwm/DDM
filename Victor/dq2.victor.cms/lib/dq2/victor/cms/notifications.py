"""
@copyright: European Organization for Nuclear Research (CERN)
@author: Fernando H. Barreiro U{fernando.harald.barreiro.megino@cern.ch<mailto:fernando.harald.barreiro.megino@cern.ch>}, CERN, 2011
@license: Licensed under the Apache License, Version 2.0 (the "License");
You may not use this file except in compliance with the License.
You may obtain a copy of the License at U{http://www.apache.org/licenses/LICENSE-2.0}
"""

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email import Encoders


def send_mail(text, contacts, sender, subject):
    """
    Generic python email function. You have to specify the text, to(as a list of email addresses), from and subject.
    This function is not to be played with! 
    """   
    if not text:
        return
                                                                                                                      
    msg=MIMEMultipart()
    msg['From']=sender
    msg['Date']=formatdate(localtime=True)
    msg['Subject']=subject
    msg['To'] = ','.join(contacts)    
    
    # Main text
    msg.attach(MIMEText(text))
    smtp=smtplib.SMTP('localhost')

    # Send the email
    smtp.sendmail(sender, contacts, msg.as_string())
    logger.info('Mail sent to %s'%(contacts))
    logger.info('Content:\n %s'%(text))

    smtp.close()
    
    
    
