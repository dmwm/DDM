"""

@author: Pedro Salgado
@contact: pedro.salgado@cern.ch
@since: 0.2
@version: $Id: ping.py,v 1.1 2008-05-29 11:15:40 psalgado Exp $
"""


import os
import re


from threading import Thread


# on cern linux : 2 packets transmitted, 2 received, 0% packet loss, time 1016ms
# on macosx     : 2 packets transmitted, 2 packets received, 0% packet loss
REG_PING_LIFELINE = re.compile("(\d) (packets )?received")
REG_PING_UNKNOWNHOST  = re.compile("unknown host")
PING_RESPONSES = ("No response", "Partial Response", "Alive")


class PingThread (Thread):
    """
    Thread to ping status.
    
    @since: 0.2.0
    
    @ivar ip: IP address.
    @type ip: str
    @ivar status: ping command status.
    @type status: int
    """


    def __init__ (self, ip):
        """
        @since: 0.2.0
        
        @param ip: IP address.
        @type ip: str
        """
        Thread.__init__(self)
        self.ip = str(ip)
        self.status = -1


    def __str__ (self):
        """
        @since: 0.2.0
        """
        return "Status for %s is '%s'." % (self.ip, ping_response(self.status))


    def run (self):
        """
        Run this thread.
        
        @since: 0.2.0
        """
        self.status = ping(self.ip)


def ping (ip):
    """
    Pings the given IP address.
    
    @since: 0.2.0
    
    Returns an int.
    None => Unknown host
    0 => No response
    1 => Partial response
    2 => Alive
    
    @return: ping command status
        None => Unknown host
        0 => No response
        1 => Partial response
        2 => Alive
    @rtype: int
    """
    pingaling = os.popen("ping -q -c2 "+ ip, "r")
    while 1:
        """read all lines until you find a line that matches the REG_PING_LIFELINE regular expression."""
        line = pingaling.readline()
        if not line: break
        if re.findall(REG_PING_UNKNOWNHOST, line):
            return None
        igot = re.findall(REG_PING_LIFELINE, line)
        if igot:
            """the REG_PING_LIFELINE regular expression found a match."""
            return int(igot[0][0])


def ping_response (status):
    """
    @since: 0.2.0
    
    @return: ping command status response.
    @rtype: str
    """
    if status is None:
        return 'Unknown host'
    return PING_RESPONSES[status]


def getHostname (url):
    """
    Return hostname from URL.
    
    @since: 0.2.0
    
    @param url: URL.
    @type url: str
    """
    reg = re.search('[^:]+:(/)*([^:/]+)(:[0-9]+)?(/)?.*', url)
    host = ''
    try:
        host = reg.group(2)
    except:
        pass
    
    return host


def pings (ips, user_friendly=False):
    """
    Pings the given IP addresses.
    
    @since: 0.2.0
    
    @param ips: list of IP addresses.
    @type ips: list
    @param user_friendly: flag to set a user-friendly response.
    @type user_friendly: bool
    
    @return: dictionary of IP adresses and host status.
        {'ip_0': status_0, ..., 'ip_N': status_N}
    @rtype: dict
    """
    
    import sys
    if sys.version[0:3] >= '2.4':
        return _pings_2_4 (ips, user_friendly=user_friendly)
    else:
        return _pings_2_2 (ips, user_friendly=user_friendly)
    return pingstatus


def _pings_2_2 (ips, user_friendly=False):
    """
    Pings the given IP addresses (Python version < 2.4).
    
    @since: 0.2.0
    
    @param ips: list of IP addresses.
    @type ips: list
    @param user_friendly: flag to set a user-friendly response.
    @type user_friendly: bool
    
    @return: dictionary of IP adresses and host status.
        {'ip_0': status_0, ..., 'ip_N': status_N}
    @rtype: dict
    """
    
    pinglist = []
    pingstatus = {}
    
    for ip in ips:
        if not ip in pingstatus.keys():
            if not user_friendly:
                pingstatus[ip] = ping(ip)
            else:
                pingstatus[ip] = PING_RESPONSES[ping(ip)]
    
    return pingstatus


def _pings_2_4 (ips, user_friendly=False):
    """
    Pings the given IP addresses (Python version >= 2.4).
    
    @since: 0.2.0
    
    @param ips: list of IP addresses.
    @type ips: list
    @param user_friendly: flag to set a user-friendly response.
    @type user_friendly: bool
    
    @return: dictionary of IP adresses and host status.
        {'ip_0': status_0, ..., 'ip_N': status_N}
    @rtype: dict
    """

    pinglist = []
    pingstatus = {}


    for ip in ips:
        current = PingThread(ip)
        pinglist.append(current)
        current.start()

    for pingle in pinglist:
        pingle.join()
        if not user_friendly:
            pingstatus[pingle.ip] = pingle.status
        else:
            pingstatus[ip] = PING_RESPONSES[pingle.status]

    return pingstatus


def main (argv):
    """
    @since: 0.2.0
    
    @param argv: .
    @type argv: list
    """
    if len(argv) < 2:
        usage()
        sys.exit(1)
    
    retries = int(argv[0])
    host = str(argv[1])
    
    
    # without threads
    print time.ctime()
    for i in range(0, retries):
        igot = ping(host)
        print ping_response(igot)
    print time.ctime()
    
    # with threads
    print time.ctime()
    ips = []
    for i in range(0, retries):
        ips.append(host)
    print pings(ips)
    print time.ctime()


def usage ():
    """
    Usage: python dq2.common.DQPing.py <number_of_retries> <host or ip address>
    
    @return: usage of this script.
    @rtype: str
    """
    print usage.__doc__


if __name__ == '__main__':
    """
    @since: 0.2.0
    """
    # main method dependencies
    import sys
    import time

    main(sys.argv[1:])
