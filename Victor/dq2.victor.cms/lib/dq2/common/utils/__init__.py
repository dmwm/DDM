"""
"""
"""

@author: 
@contact: @
@since: 
@version: $Id: __init__.py,v 1.4 2010-10-04 13:24:11 vgaronne Exp $
"""


import re


def get_hostname (surl):
    """
    Returns string with hostname or empty
    string if hostname could not be derived
    
    @param surl: URL.
    @type surl: str
    
    @return: hostname.
    @rtype: str
    """
    if str(surl).find('srm://'):
       surl = surl [str(surl).find('srm://'):]

    reg = re.search('[^:]+:(/)*([^:/]+)(:[0-9]+)?(/)?.*', surl)
    host = ''
    try:
        host = reg.group(2)
    except:
        pass
    
    return host

def iter_chunks(sequence, chunk_size) :
    """"
        Iterate on sequence by chunk 
    """
    res = []
    for item in sequence :
      res.append(item)
      if len(res) >= chunk_size :
          yield res
          res = []
    if res : yield res 

def unique (seq, stable=False):
    """unique(seq, stable=False): return a list of the elements in seq in arbitrary
    order, but without duplicates.
    If stable=True it keeps the original element order (using slower algorithms)."""
    # Developed from Tim Peters version:
    #   http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52560

    #if uniqueDebug and len(str(seq))<50: print "Input:", seq # For debugging.

    # Special case of an empty s:
    if not seq: return []

    # if it's a set:
    if isinstance(seq, set): return list(seq)

    if stable:
        # Try with a set:
        seqSet= set()
        result = []
        try:
            for e in seq:
                if e not in seqSet:
                    result.append(e)
                    seqSet.add(e)
        except TypeError:
            pass # move on to the next method
        else:
            #if uniqueDebug: print "Stable, set."
            return result

        # Since you can't hash all elements, use a bisection on sorted elements
        result = []
        sortedElem = []
        try:
            for elem in seq:
                pos = bisect_left(sortedElem, elem)
                if pos >= len(sortedElem) or sortedElem[pos] != elem:
                    insort_left(sortedElem, elem)
                    result.append(elem)
        except TypeError:
            pass  # Move on to the next method
        else:
            #if uniqueDebug: print "Stable, bisect."
            return result
    else: # Not stable
        # Try using a set first, because it's the fastest and it usually works
        try:
            u = set(seq)
        except TypeError:
            pass # move on to the next method
        else:
            #if uniqueDebug: print "Unstable, set."
            return list(u)

        # Elements can't be hashed, so bring equal items together with a sort and
        # remove them out in a single pass.
        try:
            t = sorted(seq)
        except TypeError:
            pass  # Move on to the next method
        else:
            #if uniqueDebug: print "Unstable, sorted."
            return [elem for elem,group in groupby(t)]

    # Brute force:
    result = []
    for elem in seq:
        if elem not in result:
            result.append(elem)
    #if uniqueDebug: print "Brute force (" + ("Unstable","Stable")[stable] + ")."
    return result
