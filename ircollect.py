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
    ircutils.write_output(irs.mbr, workdir, 'mbr')
    
    irs.get_boot_sector()

    #collect_mft(file, boot_sector, options)
    irs.get_filelist()
    
    for i in irs.filelist:
        #print irs.filelist[i]['filename']
        if irs.filelist[i]['filename'] == '/Windows/System32/config/SYSTEM':
            print irs.filelist[i]['filename'], irs.filelist[i]['data']
            filename = os.path.join(workdir, 'system')    
            irs.collect_file(irs.filelist[i]['data'], filename)
        if irs.filelist[i]['filename'] == '/eula.3082.txt':
            print irs.filelist[i]['filename'], irs.filelist[i]['data']
            filename = os.path.join(workdir, 'eula.txt')    
            irs.collect_file(irs.filelist[i]['data'], filename)
            
            
    sys.exit()
    

