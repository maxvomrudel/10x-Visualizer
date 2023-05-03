import csv

# Ergebnistyp beim Einlesen der CSV-Dateien
csv_data = list[dict]

def read_csv(filename: str, template: dict) -> csv_data:
    """
    Versucht den übergebenen Dateinamen als CSV-Datei einzulesen. 
    Ergebnis ist eine Liste von Dicts, wobei die Spalten als Schlüssel abgelegt sind.
    Das übergeben Template dient dabei zur Typ-Konvertierung der einzelnen Werte.
    """
    with open(filename, newline='') as csvfile:
        # keys des template als field names verwenden
        fieldnames = list(template)
        csvreader = csv.DictReader(csvfile, fieldnames)

        # erste zeile mit header überspringen
        next(csvreader)

        result: csv_data = []
        for line_dict in csvreader:
            #print("LINE ---- ", lineDict)
            result.append(convert_values(line_dict, template))
    return result

# nimmt ein dict und konvertiert alle werte entsprechend der vorlage in "template" und liefert das dict zurück
def convert_values(dict: dict, template: dict) -> dict:
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


def percentage(rawValue: str) -> float: 
    """konvertiert einen string, der ein prozentwert ist, in einen Wert zw. 0 (0%) und 1 (100%)"""
    rawValue = rawValue.replace('%', '')
    value = float(rawValue) * 0.01
    return round(value, 3)


def numeric(rawValue: str):
    """
    konvertiert einen string in einen Zahlenwert, 
    in Abhängigkeit davon ob der String einen "." als Dezimaltrenner enthält, wird ein
    int oder float ausgegeben
    """
    rawValue = rawValue.replace(',', '')
    return round(float(rawValue), 3) if '.' in rawValue else int(rawValue)


def numeric_or_percent(rawValue: str):
    """ kovertiert einen Wert, der entweder
    - ein Zahlenwert (eventuell incl. Kommata als Tausender-Trenner), oder 
    - ein Prozent-Wert ist
    """
    return percentage(rawValue) if ('%' in rawValue) else numeric(rawValue)
