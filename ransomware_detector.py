from scan import scan_file, NotAsciiError, BelowThresholdError
import os
import time
## Assumptions: ALL files are text files, all text files contain only ascii characters, all text files contain meaningful english text.

def scan_directory_files(filepaths):
    for filep in filepaths:
        scan_file(filep)


def get_directory_files(path):
    files = {}
    filenames = os.listdir(path)
    for filename in filenames:
        filepath = path + '/' + filename
        files[filepath] = os.path.getctime(filepath)
    
    return files

def filter_files_get_modified_only(old_files, new_files):
    modified_files = {}
    for o_file in old_files.keys():
        if old_files[o_file] < new_files[o_file]:
            modified_files[o_file] = new_files[o_file]
    
    return modified_files

## Program Start ##
if __name__ == "__main__":
    path = './txtfiles'
    interval = 7
    filepaths = get_directory_files(path) # dictionary
    print filepaths
    while True:
        try:
            scan_directory_files(filepaths.keys())
        except NotAsciiError as ascii_error:
            print ascii_error
        except BelowThresholdError as below_thresh_error:
            print below_thresh_error

        time.sleep( interval )
        temp_filepaths = get_directory_files(path)
        filepaths = filter_files_get_modified_only(filepaths, temp_filepaths)
