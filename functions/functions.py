import csv
from hashlib import blake2b
from multiprocessing.sharedctypes import RawValue
from os.path import isfile, join, basename
from os import listdir


def readCsv(filename: str, template: dict) :
    with open(filename, newline='') as csvfile:
        # keys des template als field names verwenden
        fieldnames = list(template)
        csvreader = csv.DictReader(csvfile, fieldnames)

        # erste zeile mit header überspringen
        next(csvreader)
    
        result: Data = []
        for lineDict in csvreader:
            #print("LINE ---- ", lineDict)
            result.append(convertValues(lineDict, template))
    return result

        
def readMetricsV1(datei, template_summary_v1):
    # Ergebnis-Typ für die Daten aus den CSV-Dateien
    #Data = list[dict]
    #Vorlage für summary_v1
    Ergebnis= readCsv(datei, template_summary_v1)
    Ergebnis[0]["Filename"]=datei
    dateiname = datei.replace('.cellranger_rnaseq_metrics_summary.csv','')
    dataname=basename(dateiname)
    
    x = dataname.split(".",1)
    Ergebnis[0]["BfxProjekt"]= x[0]
    Ergebnis[0]["Samplename"]=x[1]
    Ergebnis[0]["Type"]= "V1"
    
    return Ergebnis    

# nimmt ein dict und konvertiert alle werte entsprechend der vorlage in "template"
def convertValues(dict: dict, template: dict): 
    for fieldName in dict:
        # type conversion for each key in dictionary, according to template
        targetTypeConverter = template[fieldName]
        if fieldName in template.keys():
            rawFieldValue = dict[fieldName]
            if targetTypeConverter == int or targetTypeConverter == float:
                rawFieldValue = rawFieldValue.replace(',','')

        # Umwandlung in richtigen Typ
            dict[fieldName] = targetTypeConverter(rawFieldValue)
        else:
            raise ValueError ("key nicht in Liste enthalten")
    
    
    return dict



# konvertiert einen string, der ein prozentwert ist, in einen Wert zw. 0 (0%) und 1 (100%) 
def percentage(rawValue: str):
    rawValue = rawValue.replace('%','')
    rawValue= rawValue* 0.01
    rawValue = round(rawValue, 3)
    return float(rawValue)

# konvertiert einen string in einen Zahlenwert, 
# in Abhängigkeit davon ob der String einen "." als Dezimaltrenner enthält, wird ein 
# int oder float ausgegeben
def numeric(rawValue: str):
    rawValue = rawValue.replace(',','')
    return round(float(rawValue), 3) if '.' in rawValue else int(rawValue)

# kovertiert einen Wert, der entweder 
# - ein Zahlenwert (eventuell incl. Kommata als Tausender-Trenner), oder 
# - ein Prozent-Wert ist
def numericOrPercent(rawValue: str): 
    return percentage(rawValue) if ('%' in rawValue) else numeric(rawValue)

#function returns files from directory
def directoryFiles(mypath):
    onlyfiles = []
    for f in listdir(mypath):
        if isfile(join(mypath, f)) and f.endswith("summary.csv"):
            onlyfiles.append(join(mypath,f))
        

    return onlyfiles

