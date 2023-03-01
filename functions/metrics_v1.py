from functions.csv import percentage, read_csv
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


def read_metrics_v1(datei, template_summary_v1=template_summary_v1):
    # Ergebnis-Typ für die Daten aus den CSV-Dateien
    
    #Vorlage für summary_v1
    result = read_csv(datei, template_summary_v1)
    result[0]["Filename"] = datei
    dateiname = datei.replace('.cellranger_rnaseq_metrics_summary.csv', '')
    dataname = basename(dateiname)

    # Format 
    x = dataname.split(".", 1)
    result[0]["BfxProjekt"] = x[0]
    result[0]["Samplename"] = x[1]
    result[0]["Type"] = "V1"

    return result