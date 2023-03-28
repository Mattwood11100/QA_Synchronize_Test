# QA_Synchronize_Test

The purpose of this script is to perform a one way sync between a source and destination folders. The script takes the source
folder, destination folder, sync interval and log file path as command line arguments. The sync interval is give in minutes. The
information
captured in the log file is
replicated in the console. The path for the source folder, destination folder and log file are checked, they do not exist then the 
program will throw an exception and exit.
