from metrics_csv import readCsv

template_summary_v2 = {
    "lib_or_sample": str,
    "lib_type": str,
    "group_by": str,
    "group_name": str,
    "metric_name": str,
    "value": str
}

summary_v2 = readCsv('metrics_summary_v2.csv', template_summary_v2)
print(summary_v2)