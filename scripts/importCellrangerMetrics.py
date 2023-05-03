import argparse
from functions.metrics_v1 import read_metrics_v1, COL_BFX_PROJECT, COL_SAMPLE_NAME
from functions.files import find_summary_files
import pandas as pd
from os.path import exists
import pickle

# ---------------------------------------------------------------
def parse_commandline():
    """
    parse command line and check for required arguments
    """   
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, nargs="*")  # Datei angeben
    parser.add_argument("--directory", type=str, nargs="*")  #Ordner angeben
    parser.add_argument("--meta", type=str, nargs="*")  # Metadatentabelle angeben
    args = parser.parse_args()

    check_args(args)
    return args


# ---------------------------------------------------------------
def check_args(args):
    """
    check command line arguments
    """
    if not args.directory and not args.file:
        print("please provide Input (--file or --directory)")
        exit()

    if not args.meta:
        print("please provide some metadata (--meta (can be empty))")
        exit()


# ---------------------------------------------------------------
def find_metrics_files(files, directories) -> list[str]: 
    if directories and not files:
        files = []
        for dir in directories:
            files = files + find_summary_files(dir)

    for file in files:
        if not exists(file):
            print("file don´t exists:" + file("provided by --file"))
            exit()
    
    return files


# ---------------------------------------------------------------
def parse_metrics(files: list[str]) -> pd.DataFrame:
    """
    parse all metrics CSV files into a single Pandas DataFrame
    """
    metrics_data = []
    for file in files:
        metrics_v1 = read_metrics_v1(file)
        metrics_data.extend(metrics_v1)

    metrics_data_df = pd.DataFrame(metrics_data, index=[line[COL_SAMPLE_NAME] for line in metrics_data])
    
    return metrics_data_df


# ---------------------------------------------------------------
def parse_metadata(filename: str) -> pd.DataFrame:    

    meta_df = pd.read_table(filename)

    # split BfxProject and SampleName in two columns
    sample_names = []
    bfx_projects=[]
    index = 0
    key_Column = meta_df.loc[:,"Key"]
    for r in key_Column:
        row = key_Column[index]
        bfxProjektAndSampleName = row.split(".",1)
        sample_names.append(bfxProjektAndSampleName[1])
        bfx_projects.append(bfxProjektAndSampleName[0])
        index =+ 1

    meta_df[COL_SAMPLE_NAME]=sample_names
    meta_df[COL_BFX_PROJECT]=bfx_projects

    # fix Date column
    for column in meta_df.columns:
        if "Date" in column:
            date_Column = meta_df.loc[:,column]
            index2=0
            for r in date_Column:
                x = date_Column[index2]
                if x.len() == 0:
                    date_Column[index2]= "  "
                index2 = index2 +1

    return meta_df


# ---------------------------------------------------------------
def merge_and_store(target_filename: str, metrics_df: pd.DataFrame, metadata_df: pd.DataFrame):
    parts = [metadata_df, metrics_df]
    mergedTable = pd.merge(metadata_df, metrics_df, how="right", on=[COL_SAMPLE_NAME,COL_BFX_PROJECT])

    #convert Strings in SampleDate in dates
    for column in mergedTable.columns:
        if "Date" in column:
            mergedTable[column]=mergedTable[column].astype("datetime64[ns]")

    with open(target_filename, 'wb') as handle:
        pickle.dump(mergedTable, handle, protocol=pickle.HIGHEST_PROTOCOL)


# ---------------------------------------------------------------

# metadata 
METADATA_FILENAME = 'metadata.tsv'

# where to store the serialized data table
OUTPUT_FILENAME = "data/metrics_summary.pickle"

args = parse_commandline()
files = find_metrics_files(args.file, args.directory)
metrics_df = parse_metrics(files)
metadata_df = parse_metadata(METADATA_FILENAME)
merge_and_store(OUTPUT_FILENAME, metrics_df, metadata_df)
