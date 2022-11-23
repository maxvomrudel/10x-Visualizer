from metrics_csv import readCsv, percentage

# Vorlage für summary_v1
template_summary_v1 = {
    "num_cells": int,
    "mean_reads": int,
    "median_per_cell": int,
    "num_reads": int,
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

metrics_v1 = readCsv('metrics_summary_v1.csv', template_summary_v1)
print(metrics_v1)

