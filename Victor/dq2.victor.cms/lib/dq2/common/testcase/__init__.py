"""
@since: 0.3.0
"""

import linecache


def print_test_report (results):
    """
    Prints a test suite report.
    
    @param results: test results.
    @type results: list
    
    @author: Pedro Salgado
    @contact: pedro.salgado@cern.ch
    @since: 1.1.16
    @version: $Id: __init__.py,v 1.6 2010-10-12 08:07:10 vgaronne Exp $
    """
    
    total_tests = 0
    total_errors = 0
    total_failures = 0
    
    for r in results:
        total_tests += r.testsRun
        total_errors += len(r.errors)
        total_failures += len(r.failures)
    
    print
    print
    print
    print '*************** Final Report ***************'
    print 'Tests: %u' % (total_tests)
    red = '\x1b\x5b1;31;40m'
    white = '\x1b\x5b0;37;40m'
    if total_errors > 0:
        color = red
    else:
        color = white
    print '%sErrors: %u%s' % (color, total_errors, white)
    if total_failures > 0:
        color = red
    else:
        color = white
    print '%sFailures: %u%s' % (color, total_failures, white)
    success = total_tests - total_errors - total_failures
    
    if total_tests > 0:
        ratio = float(success) * 100 / float(total_tests)
    else:
        ratio = 0
    print 'Status: %u/%u (%.2f%%)' % (success, total_tests, ratio)
    print 
    if total_errors > 0 or total_failures > 0:
        print '%sContact and send the output of these tests to the responsible of this product.%s' % (red, white)

def traceit (frame, event, arg):
    """
    Traces python code...
    
    @since: 0.3
    
    @param frame: .
    @type frame: 
    @param event: .
    @type event: 
    @param arg: .
    @type arg: 
    
    @see: http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html
    
    @return: 
    @rtype: 
    """
    
    if event == 'line':
        
        lineno = frame.f_lineno
        filename = frame.f_globals["__file__"]
        
        if (filename.endswith(".pyc") or
            filename.endswith(".pyo")):
            filename = filename[:-1]
        
        name = frame.f_globals["__name__"]
        
        line = linecache.getline(filename, lineno)
        
        if (filename.find('dq2') > 0 or filename.find('panda') > 0) and filename.find('aspects') < 0:
            """only print dq2 or panda packages info"""
            print '%s:%s: %s' % (name.ljust(40), str(lineno).rjust(4), line.rstrip())
    
    return traceit