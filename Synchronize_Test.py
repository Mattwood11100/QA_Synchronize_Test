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


# Compare the contents of the two folders
# Comparing the first layer of the two directories
comp = filecmp.dircmp(sourceDir, destinationDir)

# If the destination directory is empty, deep copy all the contents of the source folder to the destination folder
if len(comp.common) == 0 and len(comp.right_only) == 0:
    shutil.copytree(sourceDir, destinationDir, dirs_exist_ok=True)
    print(f"Copied contents of source to destination\n")

# Deep copy the file only in the source directory to the destination directory
elif len(comp.left_only) != 0:
    for file in comp.left_only:
        isFile = os.path.isfile(os.path.join(sourceDir, file))
        isDirc = os.path.isdir(os.path.join(sourceDir, file))
        # print(f"is File:\t{isFile}\n"
        #       f"is Dirc:\t{isDirc}\n")
        if isFile:
            shutil.copy2(os.path.join(sourceDir, file), destinationDir)
            print(f"Copied the single file\n")
        elif isDirc:
            shutil.copytree(os.path.join(sourceDir, file), os.path.join(destinationDir, file))
            print(f"Copied the single folder\n")


# TODO: Remove the files that are only in the destination directory
elif len(comp.right_only) != 0:
    for file in comp.right_only:
        isFile = os.path.isfile(os.path.join(destinationDir, file))
        isDirc = os.path.isdir(os.path.join(destinationDir, file))
        # print(f"is File:\t{isFile}\n"
        #       f"is Dirc:\t{isDirc}\n")
        if isFile:
            os.remove(os.path.join(destinationDir, file))
            print(f"Removed the single file\n")
        # elif isDirc:
        #     shutil.rmtree(os.path.join(destinationDir, file))
        #     print(f"Removed the single folder\n")


# TODO: Compare the common files and determine if the file is a file or directory, if there are differences between the files then
#       copy the source file to the destination directory


# TODO: store the relevant action in a log file as well as the console


# TODO: Add the command line arguments


# TODO: Make the synchronization periodic


# TODO: Add contents to the readme file
