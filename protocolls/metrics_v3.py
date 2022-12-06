from metrics_csv import readCsv, numericOrPercent

template = {
    "lib_or_sample": str,
    "lib_type": str,
    "group_by": str,
    "group_name": str,
    "metric_name": str,
    "value": numericOrPercent
}

data = readCsv(
    '10k_PBMC_TBNK_connect_10k_PBMC_TBNK_connect_metrics_summary.csv',
    template)

# print(data)


# Funktion, die die Daten aus dem CSV-File mit einer übergebenen query-Funktion filtert
# und vom Ergebnis nur die Werteliste liefert
def valuesFiltered(query) -> list:
    dataFiltered = filter(query, data)
    return list(map(lambda x: x["value"], dataFiltered))


# ---------------------------------------------------------
# Helfer zur besseren Lesbarkeit


def isSample(x: dict) -> bool:
    return x['lib_or_sample'] == "Sample"


def isLibrary(x: dict) -> bool:
    return x['lib_or_sample'] == "Library"


def hasType(x: dict, libtype: str) -> bool:
    return x['lib_type'] == libtype


def hasMetric(x: dict, metric: str) -> bool:
    return x['metric_name'] == metric


# ---------------------------------------------------------
# Statistiken

# Werte für jede Probe im Experiment einzeln
# -> alle Werte, für die "lib_or_sample" den Wert "Sample" hat
query1 = isSample
print("Query 1: ", valuesFiltered(query1))

# Statistik "Number of reads" zum einen für den Library Type (2. Spalte) "Gene expression"
# und zum anderen für den Library Type "Antibody Capture" insgesamt im Experiment interessieren
# (das wäre 1. Spalte/Library or Sample mit dem Wert "Library")
query2 = lambda x: isLibrary(x) and hasType(x, "Gene Expression") and hasMetric(x, "Number of reads")
print("Query 2: ", valuesFiltered(query2))
