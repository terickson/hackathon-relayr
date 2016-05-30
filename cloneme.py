# $Id$
'''
cloneme.py will the atclib sample project to a new project directory
it will only clone the appropriate files for a standard atclib deployment
'''
import os
import sys
import shutil
import errno

debug = True

if len(sys.argv) < 2:
    print('Please run script in the form cloneme.py <newprojectname>')
    sys.exit()


def copy(src, dest):
    # wrote our own copy routine to handle both files and directories
    # we also exclude the files we know we don't want to copy
    try:
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns('README.md', 'examples', 'config.ini', '.DS_Store', '.git', 'sample_user-anaconda.sublime-settings.txt', 'update_atclib.log'))
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)


workingPath = os.path.abspath(os.curdir)
parentPath = os.path.abspath(os.pardir)
sourceProjectName = (workingPath.split(os.sep))[-1]

if debug:
    print('Working path: ' + workingPath)
    print('Parent path: ' + parentPath)
    print('Source project name: ' + sourceProjectName)

# get the destination as passed to us and ten carve up the path
destLocationPassed = sys.argv[1]
destLocationPathList = destLocationPassed.split(os.sep)

print(destLocationPathList)

# if we were given just a name, use it and create the project parallel to the current project,
# otherwise use the full path we were given for the destination
if len(destLocationPathList) > 1:
    newProjectPath = destLocationPassed
    newProjectName = destLocationPathList[-1]
else:
    newProjectPath = parentPath + os.sep + destLocationPassed
    newProjectName = destLocationPassed


if debug:
    print('destination project ' + newProjectName + ' - path: ' + newProjectPath)

# actually do the copy
copy(workingPath, newProjectPath)

# create new README.md in new location
readmePath = newProjectPath + os.sep + 'README.md'
readmeText = newProjectName + "\n==================\n\nThis project was cloned from " + sourceProjectName
readmeFile = open(readmePath, "w")
readmeFile.write(readmeText)
readmeFile.close()
