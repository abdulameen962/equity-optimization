import os
import csv
import shutil
from datetime import datetime

data_dir = 'data'
valid_dir = os.path.join(data_dir, 'valid_from_2010')
excluded_dir = os.path.join(data_dir, 'excluded_post_2010')

os.makedirs(valid_dir, exist_ok=True)
os.makedirs(excluded_dir, exist_ok=True)

files = [f for f in os.listdir(data_dir) if f.endswith('.csv') and os.path.isfile(os.path.join(data_dir, f))]

results = []

for f in files:
    filepath = os.path.join(data_dir, f)
    dates = []
    with open(filepath, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            d_str = row['Date'].strip()
            try:
                dt = datetime.strptime(d_str, '%m/%d/%Y')
                dates.append(dt)
            except ValueError:
                try:
                    dt = datetime.strptime(d_str, '%Y-%m-%d')
                    dates.append(dt)
                except Exception:
                    pass
    
    if dates:
        min_date = min(dates)
        max_date = max(dates)
        num_rows = len(dates)
        has_2010 = (min_date.year <= 2010)
        results.append({
            'filename': f,
            'min_date': min_date.strftime('%Y-%m-%d'),
            'max_date': max_date.strftime('%Y-%m-%d'),
            'min_year': min_date.year,
            'num_rows': num_rows,
            'has_2010': has_2010
        })

print(f"Total CSV files analyzed: {len(results)}\n")
header_str = f"{'Filename':<45} | {'Start Date':<10} | {'End Date':<10} | {'Rows':<5} | {'Status'}"
print(header_str)
print('-' * len(header_str))

valid_count = 0
excluded_count = 0

for r in sorted(results, key=lambda x: x['filename']):
    if r['has_2010']:
        status = "VALID (<= 2010)"
        valid_count += 1
        shutil.copy(os.path.join(data_dir, r['filename']), os.path.join(valid_dir, r['filename']))
    else:
        status = f"EXCLUDED (Starts {r['min_year']})"
        excluded_count += 1
        shutil.copy(os.path.join(data_dir, r['filename']), os.path.join(excluded_dir, r['filename']))
    
    row_str = f"{r['filename']:<45} | {r['min_date']:<10} | {r['max_date']:<10} | {r['num_rows']:<5} | {status}"
    print(row_str)

print('-' * len(header_str))
print(f"Total Valid Stocks (Data from 2010 or earlier): {valid_count}")
print(f"Total Excluded Stocks (Data started after 2010): {excluded_count}")
