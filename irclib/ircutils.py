import sys
import os
from optparse import OptionParser
     
def irc_options():

    parser = OptionParser()
    parser.set_defaults(debug=False,localtz=False,directory='')
    
    parser.add_option("-v", "--version", action="store_true", dest="version",
                      help="report version and exit")
    
    parser.add_option("-d", "--directory", dest="directory",
                      help="Output all results to specified directory", metavar="OUTDIR")
    
    parser.add_option("--debug",
                      action="store_true", dest="debug",
                      help="turn on debugging output")
                      
    (options, args) = parser.parse_args()
    
    if options.directory == '':
        print "Must specify an output directory"
        sys.exit()
        
    return options

def write_output(data, workdir, name):
    try:
        filename = os.path.join(workdir, name)
        outfile = open(filename,'w+')
        outfile.write(data)
        outfile.close()
    except IOError, e:
        print e.errno
        print e
        print "Unable to open: %s" % (filename)
        sys.exit()

def print_hex(data):
    formatted_hex = ':'.join(data[i:i+2] for i in range(0, len(data), 2))
    print formatted_hex
