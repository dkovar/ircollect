#!/usr/bin/env python

import os
import sys
import socket
import struct
from time import gmtime, strftime

from analyzemft import mft
from analyzemft import mftsession


from lib import rrutils
from lib import mbr_parser



if __name__=="__main__":

    filelist = {}

    irs = CollectSession()
    
    irs.options = rrutils.rr_options()

    irs.opendisk('\\\\.\\PhysicalDrive0', 'rb+')
        
    if not os.path.exists(options.directory):
        os.makedirs(options.directory)

    workdir = os.path.join(options.directory, socket.gethostname())
    if not os.path.exists(workdir):
        os.makedirs(workdir)
        
    workdir = os.path.join(workdir, strftime("%Y%m%d_%H-%M-%S", gmtime()))
    if not os.path.exists(workdir):
        os.makedirs(workdir)
    
    irs.get_mbr()
    rrutils.write_output(mbr, workdir, 'mbr')
    
    irs.get_boot_sector()

    #collect_mft(file, boot_sector, options)
    filelist = irs.get_filelist()
    
    for i in filelist:
        if filelist[i]['filename'] == '/Windows/System32/config/SYSTEM':
            print filelist[i]['filename'], filelist[i]['data']
            filename = os.path.join(workdir, 'system')    
            irs.collect_file(filelist[i]['data'], filename)
        if filelist[i]['filename'] == '/eula.3082.txt':
            print filelist[i]['filename'], filelist[i]['data']
            filename = os.path.join(workdir, 'eula.txt')    
            irs.collect_file(boot_sector, filelist[i]['data'], filename)
            
            
    sys.exit()
    

