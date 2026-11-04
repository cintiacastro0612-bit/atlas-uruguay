"""
Genera datos_uruguay.json con una elección de EJEMPLO (no oficial) para que el
atlas se vea funcionando. Reemplazar por datos oficiales de la Corte Electoral
con build_desde_csv.py.

Patrón cualitativo real de 2024 (1a vuelta): FA gana Montevideo, Canelones y
buena parte del sur/litoral; PN gana el interior. Las cifras son ILUSTRATIVAS.
"""
import json

# Padrón aproximado por departamento (habilitados). ILUSTRATIVO.
PADRON = {
    "Montevideo": 1050000, "Canelones": 430000, "Maldonado": 170000,
    "Salto": 110000, "Colonia": 105000, "San José": 100000, "Paysandú": 95000,
    "Rivera": 90000, "Tacuarembó": 80000, "Soriano": 75000, "Cerro Largo": 75000,
    "Rocha": 65000, "Artigas": 63000, "Florida": 62000, "Durazno": 55000,
    "Lavalleja": 55000, "Río Negro": 50000, "Treinta y Tres": 45000, "Flores": 22000,
}

# % por fuerza por departamento (FA, PN, PC, CA, IS). El resto va a "Otros".
# ILUSTRATIVO — refleja el patrón general, no son resultados oficiales.
SHARES = {
    "Montevideo":    (50, 20, 14, 2, 5), "Canelones": (47, 24, 14, 2, 5),
    "Salto":         (45, 28, 14, 2, 4), "Artigas":   (45, 29, 13, 2, 4),
    "Paysandú":      (42, 31, 15, 2, 4), "Río Negro": (41, 33, 15, 2, 3),
    "Rocha":         (43, 32, 13, 3, 4), "Maldonado": (40, 34, 15, 3, 4),
    "Rivera":        (38, 36, 16, 2, 3), "Treinta y Tres": (38, 37, 14, 3, 3),
    "Cerro Largo":   (36, 40, 15, 3, 3), "Tacuarembó":(35, 41, 15, 3, 3),
    "San José":      (38, 38, 15, 3, 3), "Soriano":   (34, 42, 15, 3, 3),
    "Colonia":       (36, 40, 16, 2, 3), "Florida":   (34, 43, 15, 3, 2),
    "Durazno":       (33, 44, 15, 3, 2), "Lavalleja": (33, 44, 15, 3, 2),
    "Flores":        (31, 46, 16, 2, 2),
}

PARTIDOS = [
    {"id": "FA", "nombre": "Frente Amplio",   "color": "#2a4b9b"},
    {"id": "PN", "nombre": "Partido Nacional","color": "#5aa0d6"},
    {"id": "PC", "nombre": "Partido Colorado","color": "#e23b3b"},
    {"id": "CA", "nombre": "Cabildo Abierto",  "color": "#3bb6a6"},
    {"id": "IS", "nombre": "Identidad Soberana","color": "#8a6fc0"},
    {"id": "OT", "nombre": "Otros",            "color": "#9aa0ad"},
]

deptos = {}
for dep, pad in PADRON.items():
    fa, pn, pc, ca, is_ = SHARES[dep]
    ot = max(0, 100 - (fa + pn + pc + ca + is_))
    emitidos = round(pad * 0.90)  # participación ~90% (ilustrativo)
    votos = {
        "FA": round(emitidos * fa / 100), "PN": round(emitidos * pn / 100),
        "PC": round(emitidos * pc / 100), "CA": round(emitidos * ca / 100),
        "IS": round(emitidos * is_ / 100), "OT": round(emitidos * ot / 100),
    }
    deptos[dep] = {"habilitados": pad, "votos": votos}

data = {
    "titulo": "Atlas electoral de Uruguay",
    "elecciones": [{
        "id": "pres2024v1",
        "label": "Presidencial 2024 · 1ª vuelta",
        "demo": True,
        "fuente": "DATOS DE EJEMPLO — no oficiales. Reemplazar con la Corte Electoral.",
        "partidos": PARTIDOS,
        "departamentos": deptos,
    }],
}

with open("datos_uruguay.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("datos_uruguay.json escrito:", len(deptos), "departamentos")
