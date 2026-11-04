"""
Construye datos_uruguay.json a partir de un CSV de resultados por departamento
(datos oficiales de la Corte Electoral). Reemplaza el dataset DEMO.

Uso:
    python build_desde_csv.py resultados.csv "Presidencial 2024 · 1ª vuelta" pres2024v1

CSV esperado (encabezado, UTF-8, separador coma):
    departamento,partido,votos,habilitados
    Montevideo,Frente Amplio,472500,1050000
    Montevideo,Partido Nacional,189000,1050000
    ...
- 'departamento' debe coincidir con los nombres del mapa (uruguay.geo.json):
  Montevideo, Canelones, Maldonado, Salto, Colonia, San José, Paysandú, Rivera,
  Tacuarembó, Soriano, Cerro Largo, Rocha, Artigas, Florida, Durazno, Lavalleja,
  Río Negro, Treinta y Tres, Flores.
- 'habilitados' es opcional (para calcular participación); si falta, se omite.
- Los partidos no listados en COLORES caen en "Otros" (OT).

Editá COLORES para fijar id, nombre visible y color de cada fuerza.
"""
import csv, json, sys, unicodedata

# id -> (nombre visible, color). El orden define el orden en la ficha/leyenda.
COLORES = {
    "FA": ("Frente Amplio",     "#2a4b9b"),
    "PN": ("Partido Nacional",  "#5aa0d6"),
    "PC": ("Partido Colorado",  "#e23b3b"),
    "CA": ("Cabildo Abierto",   "#3bb6a6"),
    "IS": ("Identidad Soberana","#8a6fc0"),
    "OT": ("Otros",             "#9aa0ad"),
}
# nombre en el CSV (normalizado) -> id. Agregá variantes si tu CSV usa otros nombres.
ALIAS = {
    "frente amplio": "FA", "fa": "FA",
    "partido nacional": "PN", "nacional": "PN", "pn": "PN",
    "partido colorado": "PC", "colorado": "PC", "pc": "PC",
    "cabildo abierto": "CA", "cabildo": "CA", "ca": "CA",
    "identidad soberana": "IS", "is": "IS",
}

def norm(s):
    s = unicodedata.normalize("NFD", str(s)).encode("ascii","ignore").decode().lower().strip()
    return s

def main():
    if len(sys.argv) < 4:
        sys.exit("Uso: python build_desde_csv.py <csv> <label> <id>")
    csv_path, label, eid = sys.argv[1], sys.argv[2], sys.argv[3]
    deptos = {}
    with open(csv_path, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            dep = row["departamento"].strip()
            pid = ALIAS.get(norm(row["partido"]), "OT")
            votos = int(float(row["votos"] or 0))
            hab = row.get("habilitados")
            d = deptos.setdefault(dep, {"votos": {}, "habilitados": None})
            d["votos"][pid] = d["votos"].get(pid, 0) + votos
            if hab and str(hab).strip():
                d["habilitados"] = int(float(hab))
    # limpiar None y asegurar todas las claves de partido
    for dep, d in deptos.items():
        if d["habilitados"] is None:
            d.pop("habilitados")

    partidos = [{"id": k, "nombre": v[0], "color": v[1]} for k, v in COLORES.items()]
    data = {
        "titulo": "Atlas electoral de Uruguay",
        "elecciones": [{
            "id": eid, "label": label, "demo": False,
            "fuente": "Corte Electoral de Uruguay (datos oficiales).",
            "partidos": partidos,
            "departamentos": deptos,
        }],
    }
    with open("datos_uruguay.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("datos_uruguay.json escrito:", len(deptos), "departamentos ·", label)

if __name__ == "__main__":
    main()
