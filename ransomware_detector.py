######################### Description ############################
# Ransomware Detector is a simple ransomware detector for        #
# an assignment of Cyber-lab SOC in Ariel-University.            #
# The script scans the directory every few seconds and           #
# checks if a file has being encrypted (or part of it)           #
# using last-modified, checking for non-ascii characters         #
# and valid english word check using PyEnchant (scan.py file)    #
# - Assumptions: All files in the directory are text files.      #
#                All text files contain only ascii characters.   #
#                All text files contain meaningful english text. #
######################### Description ############################

######################### Dependencies ############################
# - Python Version: 2.7                                           #
# - Modules: PyEnchant (for english words checking)               #
#            os [Python's standard library, no need to install]   #
#            time [Python's standard library, no need to install] #
#            sys [Python's standard library, no need to install] #
######################### Dependencis #############################

##################### Supported Platforms #######################
# - Windows 10 (tested on build 1809).                          #
# - Linux Ubuntu 18.04.                                         #
##################### Supported Platforms #######################

#### Imports ####
import os   # access directory and files
import time # for sleep function
import sys  # CLI arguments
from scan import BelowThresholdError, NotAsciiError, scan_file



# Scan files for encrypted text.
## Input : filepaths set.
## Output: None.
def scan_multiple_files(filepaths):
    for filep in filepaths:
        scan_file(filep)

# Retrieve file names and last-modified timestamps from given directory path.
## Input : path as string - path to directory.
## Output: files as dictionary - [filename: modified-timestamp]
def get_directory_files(path):
    files     = {}
    filenames = os.listdir(path)
    for filename in filenames:
        filepath        = path + '/' + filename
        files[filepath] = os.path.getmtime(filepath)
    
    return files

# Filters two dictionaries of files - [filename: modified-timestamp]
# returns only those files where the last-time-modified is later.
## Input : old_files as dictionary of files - [filename: modified-timestamp]
##         new_files as dictionary of files - [filename: modified-timestamp]
## Output: files dictionary - [filename: modified-timestamp]
def filter_files_get_modified_only(old_files, new_files):
    modified_files = {}
    for o_file in old_files.keys():
        if old_files[o_file] < new_files[o_file]:
            modified_files[o_file] = new_files[o_file]
    
    return modified_files

# Note: Blocking the thread as this functions runs in an endless loop.
# the function constantly scans the directory for encrypted text files
# every [Interval] seconds.
## Input : path     - directory path as string.
##         interval - delay between scans in seconds.
## Output: None.
def ecnryption_monitor(path, interval):
    all_filepaths      = get_directory_files(path)  # dictionary
    modified_filepaths = all_filepaths              # filtered only modified files to scan.
    
    while True:
        try:
            scan_multiple_files(modified_filepaths.keys()) # scan files
        except NotAsciiError as ascii_error:
            print ascii_error
        except BelowThresholdError as below_thresh_error:
            print below_thresh_error

        time.sleep( interval )
        
        temp_filepaths     = get_directory_files(path) # get current data about the files again
        modified_filepaths = filter_files_get_modified_only(all_filepaths, temp_filepaths) # get only those who has been modified
        all_filepaths      = temp_filepaths


## Program Start ##
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Error: invalid arguments, please supply a valid path to a directory."
        print "Example: './textfiles' or 'C:\mytextfiles'"
    else: 
        ecnryption_monitor(sys.argv[1], 1)
    
    