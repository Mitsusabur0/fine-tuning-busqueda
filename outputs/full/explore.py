import csv
import json

casa_count = 0
departamento_count = 0

with open('outputs/full/training_set.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            filters = json.loads(row['filters_json'])
            tipo = filters.get('tipo_inmueble', '')
            if tipo == 'casa':
                casa_count += 1
            elif tipo == 'departamento':
                departamento_count += 1
        except (json.JSONDecodeError, KeyError):
            pass  # skip malformed rows

print(f"casa:         {casa_count}")
print(f"departamento: {departamento_count}")