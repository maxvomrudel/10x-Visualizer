import argparse
import numbers
from types import NoneType
from functions.functions import percentage, read_metrics_v1, directory_files
import pandas as pd
import matplotlib.pyplot as plt
from os.path import exists, isfile, join
from os import listdir
import pickle

template_summary_v1 = {
    "Estimated Number of Cells": int,
    "Mean Reads per Cell": int,
    "Median Genes per Cell": int,
    "Number of Reads": int,
    "Valid Barcodes": percentage,
    "Sequencing Saturation": percentage,
    "Q30 Bases in Barcode": percentage,
    "Q30 Bases in RNA Read": percentage,
    "Q30 Bases in UMI": percentage,
    "Reads Mapped to Genome": percentage,
    "Reads Mapped Confidently to Genome": percentage,
    "Reads Mapped Confidently to Intergenic Regions": percentage,
    "Reads Mapped Confidently to Intronic Regions": percentage,
    "Reads Mapped Confidently to Exonic Regions": percentage,
    "Reads Mapped Confidently to Transcriptome": percentage,
    "Reads Mapped Antisense to Gene": percentage,
    "Fraction Reads in Cells": percentage,
    "Total Genes Detected": int,
    "Median UMI Counts per Cell": int,
}

#Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str, nargs="*")  # Datei angeben
parser.add_argument("--directory", type=str, nargs="*")  #Ordner angeben
parser.add_argument("--table", type=str)  #Dateiname der Outputdatei
parser.add_argument("--append", type=bool, default=False)
args = parser.parse_args()
files = args.file
table = args.table
directory = args.directory
append = args.append
#Check Arguments
if not directory and not files:
    print("please provide Input (--file or --directory)")
    exit()

if directory and not files:
    files = []
    for i in directory:
        files = files + directory_files(i)

if not table:
    print("filename for output Table missing (--table)")
    exit()
for f in files:
    if not exists(f):
        print("file don´t exists:" + f("providet by --file"))
        exit()

#parse metrics Files
metrics_data = []
for d in files:
    metrics_v1 = read_metrics_v1(d, template_summary_v1)
    metrics_data.extend(metrics_v1)

metrics_data_df = pd.DataFrame(metrics_data,
                               index=[l["Samplename"] for l in metrics_data])

#bestehende Datei wird geladen und durch neuen Inhalt erweitert
if append and exists(table):
    with open(table, 'rb') as handle:
        old_metrics_data_df = pickle.load(handle)
        metrics_data_df = pd.concat([old_metrics_data_df, metrics_data_df])

#Inhalt wird in Datei geschrieben
with open(table, 'wb') as handle:
    pickle.dump(metrics_data_df, handle, protocol=pickle.HIGHEST_PROTOCOL)
metrics_data_df.to_csv("metrics.csv")
#nur zum Reinschauen benötigt
