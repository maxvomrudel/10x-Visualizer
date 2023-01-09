import csv
from hashlib import blake2b
from multiprocessing.sharedctypes import RawValue
from os.path import isfile, join, basename
from os import listdir

# Ergebnistyp beim Einlesen der CSV-Dateien
Data = list[dict]

def read_csv(filename: str, template: dict):
    with open(filename, newline='') as csvfile:
        # keys des template als field names verwenden
        fieldnames = list(template)
        csvreader = csv.DictReader(csvfile, fieldnames)

        # erste zeile mit header überspringen
        next(csvreader)

        result: Data = []
        for line_dict in csvreader:
            #print("LINE ---- ", lineDict)
            result.append(convert_values(line_dict, template))
    return result


def read_metrics_v1(datei, template_summary_v1):
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


# nimmt ein dict und konvertiert alle werte entsprechend der vorlage in "template" und liefert das dict zurück
def convert_values(dict: dict, template: dict):
    for fieldName in dict:
        # type conversion for each key in dictionary, according to template
        target_type_converter = template[fieldName]
        if fieldName in template.keys():
            rawFieldValue = dict[fieldName]
            if target_type_converter == int or target_type_converter == float:
                rawFieldValue = rawFieldValue.replace(',', '')

        # Umwandlung in richtigen Typ
            dict[fieldName] = target_type_converter(rawFieldValue)
        else:
            raise ValueError("key nicht in Liste enthalten")

    return dict


# konvertiert einen string, der ein prozentwert ist, in einen Wert zw. 0 (0%) und 1 (100%)
def percentage(rawValue: str):
    rawValue = rawValue.replace('%', '')
    rawValue = rawValue * 0.01
    rawValue = round(rawValue, 3)
    return float(rawValue)


# konvertiert einen string in einen Zahlenwert,
# in Abhängigkeit davon ob der String einen "." als Dezimaltrenner enthält, wird ein
# int oder float ausgegeben
def numeric(rawValue: str):
    rawValue = rawValue.replace(',', '')
    return round(float(rawValue), 3) if '.' in rawValue else int(rawValue)


# kovertiert einen Wert, der entweder
# - ein Zahlenwert (eventuell incl. Kommata als Tausender-Trenner), oder
# - ein Prozent-Wert ist
def numeric_or_percent(rawValue: str):
    return percentage(rawValue) if ('%' in rawValue) else numeric(rawValue)


#function returns files from directory
def directory_files(mypath):
    only_files = []
    for f in listdir(mypath):
        if isfile(join(mypath, f)) and f.endswith("summary.csv"):
            only_files.append(join(mypath, f))

    return only_files
