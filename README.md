# Very SIMPLE ransomware detector
Ransomware Detector is a simple ransomware detector for        
an assignment of Cyber-lab SOC in Ariel-University.            
The script scans the directory every few seconds and           
checks if a file has being encrypted (or part of it)           
using last-modified, checking for non-ascii characters         
and valid english word check using PyEnchant (scan.py file)    
## Task Assumptions
- The files in the directory are text files.
- Each text file contains only letters from the ASCII table.
- Each text file contains only a meaningful text and not URLs of any kind.
- The attacker can encrypt a single word, a sentence, part of a file or even the whole directory files.

## How to run
Run the "ransomware_detector.py" python file (and not the scan.py), supply a directory path as a command-line argument.
- Example or a path argument: './textfiles' or 'C:\\mytextfiles'"
- Example for demo run: 'python ransomware_detector.py ./txtfiles'

## Dependencies
- Python 2.7
    - pyEnchant
    - (os, time, sys) from python standard library.

## Supported versions
 - Windows 10 (tested on build 1809).
 - Linux Ubuntu 18.04. 

