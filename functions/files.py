from os.path import isfile, join
from os import listdir


def find_summary_files(path: str) -> list[str]:
    """takes a directory path, and returns all *summary.csv files from this directory"""
    summary_files = []
    for file in listdir(path):
        if isfile(join(path, file)) and file.endswith("summary.csv"):
            summary_files.append(join(path, file))

    return summary_files
