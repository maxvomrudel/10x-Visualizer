import pandas as pd
import pickle


with open("tableWithoutMeta", 'rb') as handle:
    source= pickle.load(handle)

#data/metrics_summary.pickle

list = []
index=0
# Read TSV file into DataFrame
metadataTable = pd.read_table('metadata.tsv')
key_Column = metadataTable.loc[:,"Key"]
for r in key_Column:
    row = key_Column[index]
    bfxProjektAndSamplename = row.split(".",1)
    list.append(bfxProjektAndSamplename[1])
    index = index + 1

metadataTable["Samplename"]=list
parts = [metadataTable, source]
mergedTable = pd.merge(metadataTable, source, how="right", on=["Samplename"])
print(mergedTable)

with open("data/metrics_summary.pickle", 'wb') as handle:
    pickle.dump(mergedTable, handle, protocol=pickle.HIGHEST_PROTOCOL)


