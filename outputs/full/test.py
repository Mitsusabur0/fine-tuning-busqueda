import pandas as pd
import json

# 1. Define your massive system prompt
SYS_PROMPT = """
You will receive a `user_input`: a message written in Spanish by a user interacting with an AI concierge on a Chilean real estate/banking platform.

Your task is to extract search filters from that `user_input`.

These filters apply to the search for properties available for purchase.

Output requirements:
- Return exactly one JSON object wrapped between these tags: `<json_response></json_response>`.
- Do not include any text outside those tags.
- Only use filters from the predefined list below.
- Never invent filters that are not explicitly requested by the user.

There is a defined list of possible filters. You cannot add filters outside this list.

possible_filters =
{
    "tipo_inmueble": {
        "type": "string",
        "enum": ["casa", "departamento"],
        "description": "SOLO 'casa' o 'departamento'. Si aparecen ambos, usa solo 'departamento'"
    },
    "comuna": {
        "type": "string",
        "description": "Nombre de la comuna en Chile (ej. 'Las Condes', 'Santiago') o región."
    },
    "dormitorios": {
        "anyOf": [
            {"type": "integer"},
            {"type": "array", "items": {"type": "integer"}}
        ],
        "description": "Cantidad de dormitorios. Puede ser un número exacto o un arreglo [min, max]"
    },
    "banos": {
        "anyOf": [
            {"type": "integer"},
            {"type": "array", "items": {"type": "integer"}}
        ],
        "description": "Cantidad de baños. Puede ser un número exacto o un arreglo [min, max]. Puede estar en texto o como '2b' o '3d'."
    },
    "precio_min": {
        "type": "number",
        "description": "Valor mínimo o exacto del precio"
    },
    "precio_max": {
        "type": "number",
        "description": "Valor máximo o exacto del precio"
    },
    "moneda": {
        "type": "string",
        "enum": ["UF", "CLP"],
        "description": "Tipo de moneda del precio ('UF' o 'CLP')"
    },
    "superficie_min": {
        "type": "number",
        "description": "Superficie mínima en m²"
    },
    "superficie_max": {
        "type": "number",
        "description": "Superficie máxima en m²"
    },
    "estacionamientos": {
        "type": "integer",
        "description": "Cantidad de estacionamientos"
    },
    "bodegas": {
        "type": "integer",
        "description": "Cantidad de bodegas"
    },
    "sostenibilidad_certificada": {
        "type": "boolean",
        "description": "Amenidad: sostenibilidad certificada"
    },
    "con_subsidio": {
        "type": "boolean",
        "description": "Amenidad: con subsidio"
    },
    "piscina": {
        "type": "boolean",
        "description": "Amenidad: piscina"
    },
    "areas_verdes": {
        "type": "boolean",
        "description": "Amenidad: áreas verdes"
    },
    "gimnasio": {
        "type": "boolean",
        "description": "Amenidad: gimnasio"
    },
    "salon_eventos": {
        "type": "boolean",
        "description": "Amenidad: salón de eventos"
    },
    "zona_educacion": {
        "type": "boolean",
        "description": "Zonas: SOLO si menciona colegio, escuela, universidad"
    },
    "zona_transporte": {
        "type": "boolean",
        "description": "Zonas: SOLO si menciona metro, bus, transporte público"
    },
    "zona_centros_salud": {
        "type": "boolean",
        "description": "Zonas: SOLO si menciona hospital, clínica, centro médico"
    }
}

Extraction rules:
- Add a filter only if the user is clearly requesting it.
- Never add a filter the user did not ask for.
- If the `user_input` has no clear filters from the list, return an empty JSON object.
- User messages may include typos, misspellings, or informal phrasing. Infer the most likely intended meaning.
- If multiple comunas are mentioned, use the first one mentioned.
- If no comuna is mentioned but a region is mentioned, place the region in the `comuna` filter.
- Make sure to start your output with <json_response> and to end it with </json_response>. DO NOT include ANYTHING else.

Now extract the filters from the following `user_input`:
""".strip()

# 2. Load your CSV (Replace 'my_dataset.csv' with your actual filename)
# Using utf-8 is crucial for Spanish characters (ñ, á, é, etc.)
df = pd.read_csv("training_set.csv", encoding="utf-8")

# 3. Open the output .jsonl file
output_file = "llama32_finetune_data.jsonl"
valid_rows = 0

with open(output_file, "w", encoding="utf-8") as f:
    for index, row in df.iterrows():
        
        # Get the user text
        user_text = str(row['user_input']).strip()
        
        # Handle the JSON text safely
        json_text = row['filters_json']
        
        # Check if the cell is blank/NaN. If so, make it an empty JSON
        if pd.isna(json_text) or str(json_text).strip() == "":
            json_text = "{}"
        else:
            json_text = str(json_text).strip()
            
        # SAFETY CHECK: Verify it is valid JSON before writing
        try:
            # We load and dump it to ensure it's perfectly formatted
            parsed_json = json.loads(json_text)
            clean_json_string = json.dumps(parsed_json, ensure_ascii=False, indent=2)
        except json.JSONDecodeError:
            print(f"⚠️ WARNING: Invalid JSON found on row {index + 2}. Skipping this row.")
            print(f"Broken JSON text: {json_text}\n")
            continue # Skip this row and move to the next one
            
        # 4. Wrap the valid JSON in your required XML tags
        assistant_content = f"<json_response>\n{clean_json_string}\n</json_response>"
        
        # 5. Build the Method 1 (messages) dictionary
        example = {
            "messages": [
                {"role": "system", "content": SYS_PROMPT},
                {"role": "user", "content": user_text},
                {"role": "assistant", "content": assistant_content}
            ]
        }
        
        # Write to the jsonl file
        f.write(json.dumps(example, ensure_ascii=False) + "\n")
        valid_rows += 1

print(f"✅ Success! Generated {valid_rows} highly-formatted examples.")
print(f"📁 Saved to: {output_file}")