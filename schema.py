extraction_schema = {
    "type": "object",
    "properties": {
        "tipo_inmueble": {
            "type": "string",
            "enum": ["casa", "departamento"],
            "description": "SOLO 'casa' o 'departamento'. No incluir si no se menciona o no está en los filtros actuales."
        },
        "comuna": {
            "type": "string",
            "description": "Nombre de la comuna en Chile (ej. 'Las Condes', 'Santiago')"
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
            "description": "Cantidad de baños. Puede ser un número exacto o un arreglo [min, max]"
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
        "cocina_equipada": {
            "type": "boolean",
            "description": "Amenidad: cocina equipada"
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
        "quincho": {
            "type": "boolean",
            "description": "Amenidad: quincho"
        },
        "juegos_ninos": {
            "type": "boolean",
            "description": "Amenidad: juegos para niños"
        },
        "lavanderia": {
            "type": "boolean",
            "description": "Amenidad: lavandería"
        },
        "coworking": {
            "type": "boolean",
            "description": "Amenidad: coworking"
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
        "zona_comercio": {
            "type": "boolean",
            "description": "Zonas: SOLO si menciona mall, tienda, supermercado"
        },
        "zona_bancos": {
            "type": "boolean",
            "description": "Zonas: SOLO si menciona banco, cajero"
        }
    },
    "required": [],
    "additionalProperties": False
}