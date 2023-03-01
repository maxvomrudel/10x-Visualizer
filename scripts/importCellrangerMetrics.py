import argparse
import numbers
from types import NoneType
from functions.metrics_v1 import read_metrics_v1
from functions.files import directory_files
import pandas as pd
import matplotlib.pyplot as plt
from os.path import exists
import pickle

#Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, nargs="*")  # Datei angeben
parser.add_argument("--directory", type=str, nargs="*")  #Ordner angeben
parser.add_argument("--meta", type=str, nargs="*")  # Metadatentabelle angeben
args = parser.parse_args()
files = args.file
meta = args.meta
directory = args.directory
#Check Arguments
if not directory and not files:
    print("please provide Input (--file or --directory)")
    exit()

if not meta:
    print("please provide some metadate (--meta (can be empty))")
    exit()

if directory and not files:
    files = []
    for i in directory:
        files = files + directory_files(i)

for f in files:
    if not exists(f):
        print("file don´t exists:" + f("providet by --file"))
        exit()

#parse metrics Files
metrics_data = []
for d in files:
    metrics_v1 = read_metrics_v1(d)
    metrics_data.extend(metrics_v1)

metrics_data_df = pd.DataFrame(metrics_data,
                               index=[l["SampleName"] for l in metrics_data])

#append metadata into the dataframe

list = []
list2=[]
index = 0
metadataTable = pd.read_table('metadata.tsv')
key_Column = metadataTable.loc[:,"Key"]
for r in key_Column:
    row = key_Column[index]
    bfxProjektAndSampleName = row.split(".",1)
    list.append(bfxProjektAndSampleName[1])
    list2.append(bfxProjektAndSampleName[0])
    index = index + 1

metadataTable["SampleName"]=list
metadataTable["BfxProjekt"]=list2
parts = [metadataTable, metrics_data_df]
mergedTable = pd.merge(metadataTable, metrics_data_df, how="right", on=["SampleName","BfxProjekt"])

#convert Strings in SampleDate in dates
for d in mergedTable.columns:
    if "Date" in d:
        mergedTable[d]=mergedTable[d].astype("datetime64[ns]")


with open("data/metrics_summary.pickle", 'wb') as handle:
    pickle.dump(mergedTable, handle, protocol=pickle.HIGHEST_PROTOCOL)


