    
import os, sys, string


## 
# @private
# @brief    Get string from a OS command
#
# @param cmnd   Command which is executed
# @returns      Returns the string which the OS returned on the stdout
def getOSString(cmnd):
    call = os.popen(cmnd, 'r')
    return call.read()


