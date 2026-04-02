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

