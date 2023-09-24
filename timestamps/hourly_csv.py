from tqdm import tqdm
from zipfile import ZipFile
from collections import defaultdict
from datetime import datetime
import csv

grouped_by_hour = defaultdict(int)

with ZipFile('./keys-2023-09-ctimes.zip') as zf:
    for file in tqdm(zf.namelist()):
        with zf.open(file) as f:
            for line in f:
                line = line.decode('utf-8')
                timestamp = line.split()[0]
                dt = datetime.fromtimestamp(float(timestamp))
                key = (dt.year, dt.month, dt.day, dt.hour)
                grouped_by_hour[key] += 1

with open('hourly.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['hour', 'count'])
    for key, count in sorted(grouped_by_hour.items()):
        dt = datetime(*key)
        writer.writerow([dt, count])
