{
    "tipo_inmueble": {
        "type": "string",
        "enum": ["casa", "departamento"],
        "description": "SOLO 'casa' o 'departamento'. If both are present, use 'departamento' only"
    },
    "comuna": {
        "type": "string",
        "description": "Nombre de la comuna en Chile (ej. 'Las Condes', 'Santiago'). If multiple, use the first one mentioned. IF there's no comuna, but there's a region, use the region."
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
        "description": "Cantidad de baños. Puede ser un número exacto o un arreglo [min, max]. Puede estar en texto, o como '2b' o '3d'."
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
    },
}



-------------


You'll be given a user_input: a message a user sends to an AI concierge, in a chilean real estate/banking platform. Your task is to extract search filters from this user_input. 

The filters relate to the search of buyable properties. 
The output is a jsonl line, in between the following tags: <jsonl_response></jsonl_response>. There should be no other text, ONLY the tags and the jsonl with the filters inside. 


There's a defined list of possible filters to apply. You cannot add filters outside of this list.

possible_filters = 
{
    "tipo_inmueble": {
        "type": "string",
        "enum": ["casa", "departamento"],
        "description": "SOLO 'casa' o 'departamento'. If both are present, use 'departamento' only"
    },
    "comuna": {
        "type": "string",
        "description": "Nombre de la comuna en Chile (ej. 'Las Condes', 'Santiago'), or region."
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
        "description": "Cantidad de baños. Puede ser un número exacto o un arreglo [min, max]. Puede estar en texto, o como '2b' o '3d'."
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
    },
}

ONLY add filters if the user is requesting them. You can NEVER add a filter the user has not asked for. 
If a user_input has no clear filters from the list, the reply should be an empty json.
There will be typos, misspellings, etc. You must recognize and define the most likely real meaning. Example: prvdncia -> providencia. 
If there's multiple comunas, use the first one mentioned.
If there's no comuna, but there's a region, put the region in the comuna filter.

<examples>
<example>
user_input = "departamento en maipu 2 dormitorios"
output = "<jsonl_response>{"tipo_inmueble": "departamento", "comuna": "Maipú", "dormitorios": 2}</jsonl_response>"
</example>
<example>
user_input = "estoy buscando una casa para una pareja de profesionales sin hijos que entre los dos generan 1.500.000 de ingresos mensuales. Estamos buscando entre linares retiro parral chillan"
output = "<jsonl_response>{"tipo_inmueble": "casa", "comuna": "Linares"}</jsonl_response>"
</example>
<example>
user_input = "casa en chiloe hasta 1500 uf"
output = "<jsonl_response>{"tipo_inmueble": "casa", "comuna": "Chiloe", "precio_max": 1500, "moneda": "UF"}</jsonl_response>"
</example>
</examples>

Now, extract the filters from the following user_input: