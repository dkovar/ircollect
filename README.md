ircollect
=========

ircollect is a Python tool designed to collect files of interest in an incident response investigation
or triage effort. Running as local admin, it:

* Opens the raw disk
* Reads the master boot record, collects a copy of it, and uses the MBR to find partition and disk information
* Using the MBR information, it finds the NTFS partitions.
* Working from the start of the NTFS partition, it finds the $MFT
* It collects a copy of the $MFT and then builds a list of all the files on the system and their data runs
* Using the file list and data runs, it collects interesting files through direct reads from the disk,
bypassing access controls.

All collected files are stored in a directory specified with the -d option. They are further organized by
hostname and the date-time the script was run.

Requirements:
-------------

pip install analyzemft

Status:
-------

VERY beta. Active development daily, often hourly.

Currently collects master boot record, $MFT, and live (corrupted) registry hives. User can modify table in ircollect.py
to specify any files they desire. 

Upcoming features:
------------------

File an issue, please, if there is something you'd like.

- [ ] Windows executable
- [ ] Netcat support
- [ ] Handle Win7 vs XP hive location differences
- [ ] Add configuration file support
- [ ] Collect uncorrupted registry hives. (Requires a snapshot. If you create a snapshot, might as well collect everything that way.
- 


Notes:
------

Unless I am missing something, you cannot recover the live registry hives through direct disk reads. Well, you can,
but they are corrupted. I'm currently getting them via a created snapshot. But, if you're going to create a snapshot,
you might as well get all of the interesting files from the snapshot.... Yes? No? Could rebuild the corrupted hives,
but that is a completely different problem.

Bugs:
-----

Many

Thank you to:
-------------

* Jamie Levy for mbr_parser
* Willi Ballenthin - bit manipulation code, lots of useful tips for analyzeMFT
