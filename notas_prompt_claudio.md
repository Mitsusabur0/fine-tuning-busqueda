
1: 

CLP REGLA DE PRECIO EXACTO vs RANGO: • PRECIO EXACTO (sin "hasta", "máximo", "desde", "mínimo") → usa precio_min Y precio_max con mismo valor: - "casa de 3000 UF" → "precio_min":3000,"precio_max":3000,"moneda":"UF"

* Creo que es demasiado restringido que min y max sea el mismo número. Creo que debe haber un margen, al menos hacia abajo (500uf? no sé)


---

2: 

MAPEO DE REFERENCIAS GEOGRÁFICAS: Mall Parque Arauco → {"comuna":"Las Condes","zona_comercio":true}###END### Metro Tobalaba → {"comuna":"Providencia","zona_transporte":true}###END### UDD → {"comuna":"Las Condes","zona_educacion":true}###END### Hospital Las Condes → {"comuna":"Las Condes","zona_centros_salud":true}###END### Usa conocimiento general de Chile para identificar CUALQUIER comuna. 

* Creo que no es útil, el modelo no tiene conocimiento suficiente de chile para que valga la pena poner esto.

---

3:

Filtros actuales: representan los filtros que la persona tiene seleccionados en este momento. 

Input del usuario: corresponde a la solicitud actual para modificar esos filtros. Los filtros actuales se enviarán en el PENÚLTIMO mensaje del historial con el siguiente formato: [ESTOS SON LOS FILTROS ACTUALES]: • Tipo: casa • Comuna: Las Condes • Dormitorios: 2 

* Creo que los filtros actuales deberían enviarse en formato jsonl