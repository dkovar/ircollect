#!/usr/bin/env python

import os
import sys
import socket
import struct
from time import gmtime, strftime



from irclib import ircutils

from irclib import irclib



if __name__=="__main__":

    filelist = {}

    irs = irclib.CollectSession()
    
    irs.options = ircutils.irc_options()

    irs.open_disk('\\\\.\\PhysicalDrive0')
        
    if not os.path.exists(irs.options.directory):
        os.makedirs(irs.options.directory)

    workdir = os.path.join(irs.options.directory, socket.gethostname())
    if not os.path.exists(workdir):
        os.makedirs(workdir)
        
    workdir = os.path.join(workdir, strftime("%Y%m%d_%H-%M-%S", gmtime()))
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    
    irs.get_mbr()
    if irs.options.standard == True:
        ircutils.write_output(irs.mbr, workdir, 'mbr')
    
    irs.get_boot_sector()

    if irs.options.standard == True:
        collect_mft(file, boot_sector, options)
        
    irs.get_filelist()
    
    if irs.options.standard == True:
        targets = (('/Windows/System32/config/SYSTEM', 'system'),
            ('/Windows/System32/config/SOFTWARE','software'),
            ('/Windows/System32/config/SECURITY','security'),
            ('/Windows/System32/config/SAM','sam'),
            ('/eula.3082.txt','eula.txt'))
        
        for t in targets():
            
            found = False
            
            # FIX = find target without looping through entire list
            for i in irs.filelist:
                if irs.filelist[i]['filename'] == targets(t,0):
                    print irs.filelist[i]['filename'], irs.filelist[i]['data']
                    filename = os.path.join(workdir, targets(t,1))    
                    irs.collect_file(irs.filelist[i]['data'], filename)
                    found = True            
            
            if found == False:
                print "Unable to locate: %s" % (targets(t, 0))
    

