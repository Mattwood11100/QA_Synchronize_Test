# Imported libraries
import os
import filecmp
import shutil
import stat
import argparse
from datetime import datetime
from apscheduler.schedulers.background import BlockingScheduler

# Command line arguments
parser = argparse.ArgumentParser(description='A script to perform a one way sync between a source folder and a destination folder.')
parser.add_argument("Source", help="File path of the source folder")
parser.add_argument("Destination", help="File path of the destination folder")
parser.add_argument("Sync_Interval", help="Number of minutes between consecutive synchronizations ")
parser.add_argument("Logfile", help="File path of the log file")
args = parser.parse_args()

# Assigning the command line arguments to relevant variables
sourceDir = args.Source
destinationDir = args.Destination
syncInterval = args.Sync_Interval
logFileDir = args.Logfile

# Checking if the paths provides exist
try:
    if not os.path.exists(sourceDir):
        raise ValueError(f"The provided source path does not exist.")
except ValueError as error:
    print(repr(error))

try:
    if not os.path.exists(destinationDir):
        raise ValueError(f"The provided destination path does not exist.")
except ValueError as error:
    print(repr(error))

try:
    if not os.path.exists(logFileDir):
        raise ValueError(f"The provided log file path does not exist.")
except ValueError as error:
    print(repr(error))


def errorHandler(function, path, executeInformation):
    os.chmod(path, stat.S_IWRITE)
    function(path)


def syncFolder(sourceDir, destinationDir, logFile):
    # Compare the contents of the source and destination folders
    comp = filecmp.dircmp(sourceDir, destinationDir)
    syncCheck = False
    with open(logFileDir, "a") as log:

        # Printing a line of * so that the text file and console are easier to read
        log.write(f"*" * 80 + "\n")
        print(f"*" * 80 + "\n")

        # If the destination directory is empty, deep copy all the contents of the source folder to the destination folder
        if not comp.common and not comp.right_only:
            shutil.copytree(sourceDir, destinationDir, dirs_exist_ok=True, symlinks=True)
            syncCheck = True
            for file in comp.left_only:
                log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was created.\n")
                print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was created.\n")

        else:

            # Deep copy the file only in the source directory to the destination directory
            if comp.left_only:
                for file in comp.left_only:
                    # Checking if the element in the list is a file or directory
                    isFile = os.path.isfile(os.path.join(sourceDir, file))
                    isDirc = os.path.isdir(os.path.join(sourceDir, file))
                    syncCheck = True

                    if isFile:
                        shutil.copy2(os.path.join(sourceDir, file), destinationDir)
                        log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was copied.\n")
                        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was copied.\n")

                    elif isDirc:
                        shutil.copytree(os.path.join(sourceDir, file), os.path.join(destinationDir, file))
                        log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was copied.\n")
                        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was copied.\n")

            # Remove the files that are only in the destination directory
            if comp.right_only:
                for file in comp.right_only:
                    # Checking if the element in the list is a file or directory
                    isFile = os.path.isfile(os.path.join(destinationDir, file))
                    isDirc = os.path.isdir(os.path.join(destinationDir, file))
                    syncCheck = True

                    if isFile:
                        os.remove(os.path.join(destinationDir, file))
                        log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was removed.\n")
                        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was removed.\n")

                    elif isDirc:
                        shutil.rmtree(os.path.join(destinationDir, file), onerror=errorHandler)
                        log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was removed.\n")
                        print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was removed.\n")

            # Compare the common files and determine if the file is a file or directory, if there are differences between the files
            # then copy the source file to the destination directory
            if comp.common:
                for file in comp.common:
                    # Checking if the element in the list is a file or directory
                    isFile = os.path.isfile(os.path.join(destinationDir, file))
                    isDirc = os.path.isdir(os.path.join(destinationDir, file))

                    if isFile:
                        fileMatch, fileDifferent, fileErrors = filecmp.cmpfiles(sourceDir, destinationDir, common=[file])

                        if fileDifferent:
                            syncCheck = True
                            shutil.copy2(os.path.join(sourceDir, file), destinationDir)
                            log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was replaced.\n")
                            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was replaced.\n")

                    elif isDirc:
                        dirDifferent = filecmp.dircmp(os.path.join(sourceDir, file), os.path.join(destinationDir, file)).diff_files

                        if dirDifferent:
                            syncCheck = True
                            shutil.rmtree(os.path.join(destinationDir, file), onerror=errorHandler)
                            shutil.copytree(os.path.join(sourceDir, file), os.path.join(destinationDir, file))
                            log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was replaced.\n")
                            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}-->\t{destinationDir}\{file} was replaced.\n")

        if not syncCheck:
            log.write(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} --> No changes have occurred\n")
            print(f"{datetime.now().strftime('%d/%m/%Y %H:%M:%S')} --> No changes have occurred\n")

        syncCheck = False

        # Printing a line of = so that the text file and console are easier to read
        log.write(f"=" * 80 + "\n\n")
        print(f"=" * 80 + "\n\n")


# Creates a background scheduler
syncScheduler = BlockingScheduler()

syncScheduler.add_job(func=syncFolder, trigger='interval', args=[sourceDir, destinationDir, logFileDir], minutes=int(syncInterval))
# syncScheduler.add_job(func=syncFolder, trigger='interval', args=[sourceDir, destinationDir, logFileDir], seconds=)

# Starts the Scheduled jobs
syncScheduler.start()
