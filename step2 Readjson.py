import glob
import os
import json

jsonpath = r'D:\A-Projects\Urban Heat Island'

json_files = glob.glob(os.path.join(jsonpath, "*.json"))
json_files = sorted(json_files) 

if not json_files:
    print("No JSON files found in the specified directory.")
else:
    print(f"Found {len(json_files)} JSON files.")

for jsonfile in json_files:
    print(f"Processing {jsonfile}...") 
    try:
        with open(jsonfile, 'r', encoding='utf-8') as jsonf:
            json_data = json.load(jsonf)
            print(f"Loaded data from {jsonfile}")
    except Exception as e:
        print(f"Failed to load {jsonfile}: {e}")

for jsonfile in json_files:
    print(f"Processing {jsonfile}...") 
    try:
        with open(jsonfile, 'r', encoding='utf-8') as jsonf:
            json_data = json.load(jsonf)
            print(f"Loaded data from {jsonfile}")

            if not json_data:
                print(f"No data in {jsonfile}")
            else:
                urls = []
                for key, value in json_data.items():
                    if 'url' in value:
                        full_url = "https://ladsweb.modaps.eosdis.nasa.gov" + value['url']
                        urls.append(full_url + '\n')

                if urls:
                    output_filename = jsonfile.replace('.json', '_urls.txt')
                    print(f"Writing URLs to {output_filename}...")
                    with open(output_filename, 'w', encoding='utf-8') as output_file:
                        output_file.writelines(urls)
                else:
                    print(f"No 'url' keys found in {jsonfile}")
    except Exception as e:
        print(f"Failed to process {jsonfile}: {e}")
