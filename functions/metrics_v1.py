from functions.csv import percentage, read_csv, csv_data
from os.path import basename

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

COL_BFX_PROJECT = "BfxProjekt"
COL_SAMPLE_NAME = "SampleName"
COL_FILENAME = "Filename"
COL_TYPE = "Type"

def read_metrics_v1(filename: str, template = template_summary_v1) -> csv_data :
    """
    Datei unter Verwendung des summary_v1 Templates einlesen
    und Ergebnis anreichern
    """
    
    data = read_csv(filename, template)
    meta = basename(filename.replace('.cellranger_rnaseq_metrics_summary.csv', '')).split(".",1)
    
    data[0][COL_FILENAME] = filename
    data[0][COL_BFX_PROJECT] = meta[0]
    data[0][COL_SAMPLE_NAME] = meta[1]
    data[0][COL_TYPE] = "V1"

    return data