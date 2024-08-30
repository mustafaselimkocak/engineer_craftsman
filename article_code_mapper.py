import re
import csv

file_path = 'docs/pax.js'

# Read js file
with open(file_path, 'r') as file:
    content = file.read()

# Specify the regex pattern to capture all id and replacedBy rows
pattern = r'id: "(\d+)"|replacedBy:\s*"(\d+)"'

# Find all matches
matches = re.findall(pattern, content)

# Mapping id's and replacedBy's
mapped_pairs = []
previous_ids = []

for match in matches:
    if match[0]:  # Eğer bir id varsa
        previous_ids.append(match[0])
    elif match[1] and len(previous_ids) >= 2:  # Eğer bir replacedBy varsa ve en az iki önceki id varsa
        # İki önceki id ile replacedBy değerini eşleştir
        mapped_pairs.append((previous_ids[-1], match[1]))

# Results
print (mapped_pairs)
print (len(mapped_pairs))

# Specify the output file path
output_file = 'docs/mapped_pairs.csv'

# Write to CSV file
with open(output_file, 'w', newline='') as csvfile:
    fieldnames = ['id', 'replacedBy']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()  # Write the header row
    for id_value, replaced_by_value in mapped_pairs:
        writer.writerow({'id': id_value, 'replacedBy': replaced_by_value})

print(f"CSV file has been written to {output_file}")
