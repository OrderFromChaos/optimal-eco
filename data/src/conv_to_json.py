import json
import csv

# Methodology:
# 1. Write up eco on Google Sheets
# 2. Put the CSV in the ~/data/SkyblockOriginal folder, call it ecoinfo.csv
# 3. This code will convert it to json

def convertCSV(server_name: str) -> None:
    outJSON = dict()
    subfolder = '../' + server_name + '/'
    with open(subfolder + 'ecoinfo.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != 'Shop Prices' and row[0] != 'Resource':
                row = [row[0]] + [(float(x) if x != '' else None) for x in row[1:]]
                outJSON[row[0]] = {
                    'Buy Price': row[1],
                    'Sell Price': row[2]
                }
    with open(subfolder + 'ecoinfo.json', 'w') as f:
        json.dump(outJSON, f, indent=4)

if __name__ == '__main__':
    server_name = 'Craftscade'
    convertCSV(server_name)