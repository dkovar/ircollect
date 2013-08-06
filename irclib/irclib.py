#!/usr/bin/env python

# Author: David Kovar [dkovar <at> gmail [dot] com]
# Name: analyzeMFT.py
#
# Copyright (c) 2010 David Kovar. All rights reserved.
# This software is distributed under the Common Public License 1.0
#
# Date: May 2013
#

import sys
import os
import struct

import mbr_parser
from analyzemft import mft
from analyzemft import mftsession

VERSION = "v0.0.1"

class CollectSession:
    
    def __init__(self):
        self.bs = {}
        self.part = {}
        self.filelist = {}

    def open_disk(self, path):
        
        try:
            self.rd = open(path, 'rb+')            #code
        except (IOError, TypeError):
            print "Unable to open %s" % (path)
            sys.exit()
           
    def get_mbr(self):
        
        data = self.rd.read(512)
        if len(data) == 512:
            myMBR = mbr_parser.MBRParser(data)
        elif len(data) == 440:
            myMBR = mbr_parser.MBRParser(data, True)
        else:
            print "MBR file too small"
            return
    
        lines = myMBR.print_self()
        for l in lines:
            print l
            
        self.mbr = data

    # BIOS parameter block - http://www.ntfs.com/ntfs-partition-boot-sector.htm
    def get_boot_sector(self):

        part_offset = 2048 * 512      # Offset to first partition = right after LBA
        self.part['start'] = part_offset
        self.rd.seek(self.part['start']) 
        data = self.rd.read(512)
    
        (self.part['bps'], self.part['spc']) = struct.unpack_from('=HB', data, 11) # bytes/sec, sec/cluster
        mftcluster = struct.unpack_from('=Q',data,48) # Offset to $MFT in clusters

        # MFT cluster offset * (sectors per cluster * bytes per sector) + start of partition
        # This is hardwired, but if the partition isn't the first one, this'll break
        self.part['mftstart'] = mftcluster[0] * self.part['bps'] * self.part['spc'] + part_offset
    
    
    def collect_mft(self):
    
        self.rd.seek(self.part['mftstart'])
        data = self.rd.read(1024)
    
        record = mft.parse_record(data, options)
        
        collect_file(record['data',0], filename)

    def collect_file(self, runs, outname):
    
        outfile = open(outname,'wb')
    
        # BROKEN = only collects the last datarun
        try:
            for i in range(0, runs['ndataruns']):
                (length, offset) = (runs['dataruns'][i][0], runs['dataruns'][i][1])
                print length, offset
            
        except Exception:
            pass
        
        # print (block['p1_start'] + (offset * block['spc'] * block['bps']))
        self.rd.seek(self.part['start'] + (offset * self.part['spc'] * self.part['bps']))
        for i in range(0, length * 4096, 8):
            buffer = self.rd.read(8)
            outfile.write(buffer)
        outfile.close()
                
    def get_filelist(self):
    
        num_records = 0
        record = {}
        
        self.rd.seek(self.part['mftstart'], 0)
        raw_record = self.rd.read(1024)
    
        record = mft.parse_record(raw_record, self.options)
    
        length = record['data',0]['dataruns'][0][0] * 4096
        offset = record['data',0]['dataruns'][0][1] * \
                    self.part['spc'] * self.part['bps'] * self.part['start']        
    
        self.rd.seek(self.part['mftstart'], 0)
    
        for i in range(0, length, 1024):    
            raw_record = self.rd.read(1024)
    
            record = {}
            minirec = {}
            record = mft.parse_record(raw_record, self.options)
            if self.options.debug: print record
                   
            minirec['filename'] = record['filename']
            minirec['fncnt'] = record['fncnt']
            if record['fncnt'] == 1:
                minirec['par_ref'] = record['fn',0]['par_ref']
                minirec['name'] = record['fn',0]['name']
            if record['fncnt'] > 1:
                minirec['par_ref'] = record['fn',0]['par_ref']
                minirec['name'] = record['fn', record['fncnt']-1]['name']		
            
            # Corrupt records don't have data elements. Fix in analyzeMFT
            try:
                minirec['data'] = record['data', 0]                #code
                minirec['datacnt'] = record['datacnt']               
            except Exception:
                minirec['data'] = ''
                minirec['datacnd'] = 0
    
            self.filelist[num_records] = minirec
    
            num_records = num_records + 1
    
        self.gen_filepaths()
        
    def gen_filepaths(self):
    
        for i in self.filelist:
    
    #            if filename starts with / or ORPHAN, we're done.
    #            else get filename of parent, add it to ours, and we're done.
    
        # If we've not already calculated the full path ....
            if (self.filelist[i]['filename']) == '':
        
                 if (self.filelist[i]['fncnt'] > 0 ):
                      self.get_folder_path(self.filelist, i)
                 else:
                      self.filelist[i]['filename'] == 'NoFNRecord'

    def get_folder_path(self, mftrecords, seqnum):
    
        if seqnum not in mftrecords:
             return 'Orphan'
    
        # If we've already figured out the path name, just return it
        if (mftrecords[seqnum]['filename']) != '':
             return mftrecords[seqnum]['filename']
    
        try:
            #if (self.mft[seqnum]['fn',0]['par_ref'] == 0) or (self.mft[seqnum]['fn',0]['par_ref'] == 5):  # There should be no seq number 0, not sure why I had that check in place.
            if (mftrecords[seqnum]['par_ref'] == 5): # Seq number 5 is "/", root of the directory
                mftrecords[seqnum]['filename'] = '/' + mftrecords[seqnum]['name']
                return mftrecords[seqnum]['filename']
        except:  # If there was an error getting the parent's sequence number, then there is no FN record
            mftrecords[seqnum]['filename'] = 'NoFNRecord'
            return mftrecords[seqnum]['filename']
    
        # Self referential parent sequence number. The filename becomes a NoFNRecord note
        if (mftrecords[seqnum]['par_ref']) == seqnum:
            mftrecords[seqnum]['filename'] = 'ORPHAN/' + mftrecords[seqnum]['name']
            return mftrecords[seqnum]['filename']
    
        # We're not at the top of the tree and we've not hit an error
        parentpath = self.get_folder_path(mftrecords, (mftrecords[seqnum]['par_ref']))
        mftrecords[seqnum]['filename'] =  parentpath + '/' + mftrecords[seqnum]['name']
    
        return mftrecords[seqnum]['filename']