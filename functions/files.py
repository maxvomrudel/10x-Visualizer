from os.path import isfile, join
from os import listdir

#function returns files from directory
def directory_files(mypath):
    only_files = []
    for f in listdir(mypath):
        if isfile(join(mypath, f)) and f.endswith("summary.csv"):
            only_files.append(join(mypath, f))

    return only_files
