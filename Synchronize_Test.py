import os
import filecmp
import shutil
import pathlib
import argparse

# parser = argparse.ArgumentParser(description="This program will synchronize the contents of one folder to another folder",
#                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)


CWD = os.getcwd()

sourceDir = os.path.join(CWD, "Source")
destinationDir = os.path.join(CWD, "Destination")

# sourceDir2 = pathlib.Path(os.path.join(CWD, "Source"))
# sourceDir2 = pathlib.Path("Source")
# destinationDir2 = pathlib.Path(os.path.join(CWD, "Destination"))


# print(f"CWD:\t{CWD}\n"
#       f"Source:\t{sourceDir}\n"
#       f"Destination:\t{destinationDir}")
#
# print(f"Contents of Source:\t{os.listdir(sourceDir)}\n")
# print(f"Recursive Contents of Source:\t{list(sourceDir2.rglob('*'))[1]}\n")
# print(f"Recursive Contents of Destination:\t{list(destinationDir2.rglob('*'))}\n")
#
comparison = filecmp.dircmp(sourceDir, destinationDir)
#
print(f"Common:\t\t\t\t{comparison.common}\n"
      f"Source only:\t\t{comparison.left_only}\n"
      f"Destination only:\t{comparison.right_only}\n")
# print("Done")


# TODO: Compare the contents of the two folders
# Comparing the first layer of the two directories
firstComp = filecmp.dircmp(sourceDir, destinationDir)

# TODO: If the destination directory is empty
if len(firstComp.right_only) == 0:
    shutil.copytree(sourceDir, destinationDir, dirs_exist_ok=True)


# TODO: Deep copy the file only in the source directory to the destination directory
# TODO: Remove the files that are only in the destination directory


# TODO: Compare the common files and determine if the file is a file or directory, if there are differences between the files then
#       copy the source file to the destination directory


# TODO: store the relevant action in a log file as well as the console


# TODO: Add the command line arguments


# TODO: Make the synchronization periodic


# TODO: Add contents to the readme file
