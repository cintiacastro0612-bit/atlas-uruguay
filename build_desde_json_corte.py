"""
Convierte los archivos JSON oficiales de la Corte Electoral (ResumenGeneral_*_DPTOS.json)
al formato de datos_uruguay.json del atlas.

Uso:
    python build_desde_json_corte.py RV__JSON_2019.zip "Nacionales 2019 · votos por lema" nac2019
    python build_desde_json_corte.py carpeta_con_jsons "Nacionales 2019" nac2019 --tipo P
    python build_desde_json_corte.py RV__JSON_2019.zip "..." nac2019 --solo

- El primer argumento puede ser el .zip o una carpeta con los JSON.
- --tipo D (por defecto): escrutinio departamental, 100 % de circuitos.
  --tipo P: conteo primario (noche de elección).
- Si datos_uruguay.json ya existe, agrega o reemplaza esta elección (mismo id) y
  conserva las demás. Con --solo se escribe un archivo nuevo, solo con esta elección.
- Sale con error si un departamento no coincide con el mapa o si los totales no cierran.
"""
import json, sys, os, zipfile, unicodedata

COLORES = {  # id: (nombre visible, color). El orden define el de la ficha/leyenda.
    "FA": ("Frente Amplio",      "#2a4b9b"),
    "PN": ("Partido Nacional",   "#5aa0d6"),
    "PC": ("Partido Colorado",   "#e23b3b"),
    "CA": ("Cabildo Abierto",    "#3bb6a6"),
    "IS": ("Identidad Soberana", "#8a6fc0"),
    "PI": ("Partido Independiente", "#e8913a"),
    "OT": ("Otros",              "#9aa0ad"),
}
ALIAS = [  # (texto contenido en el nombre normalizado del lema, id)
    ("frente amplio", "FA"), ("partido nacional", "PN"), ("partido colorado", "PC"),
    ("cabildo abierto", "CA"), ("identidad soberana", "IS"), ("partido independiente", "PI"),
]
DEPARTAMENTOS = ["Artigas", "Canelones", "Cerro Largo", "Colonia", "Durazno", "Flores",
    "Florida", "Lavalleja", "Maldonado", "Montevideo", "Paysandú", "Río Negro", "Rivera",
    "Rocha", "Salto", "San José", "Soriano", "Tacuarembó", "Treinta y Tres"]

def norm(s):
    return unicodedata.normalize("NFD", str(s)).encode("ascii", "ignore").decode().lower().strip()

def lema_id(nombre):
    n = norm(nombre)
    for txt, pid in ALIAS:
        if txt in n:
            return pid
    return "OT"

def leer(origen, nombre):
    if os.path.isdir(origen):
        with open(os.path.join(origen, nombre), encoding="utf-8-sig") as f:
            return json.load(f)
    with zipfile.ZipFile(origen) as z:
        with z.open(nombre) as f:
            return json.loads(f.read().decode("utf-8-sig"))

def main():
    argv = sys.argv[1:]
    tipo = "D"
    if "--tipo" in argv:
        i = argv.index("--tipo")
        tipo = argv[i + 1].upper() if i + 1 < len(argv) else ""
        del argv[i:i + 2]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 3:
        sys.exit(__doc__)
    origen, label, eid = args[0], args[1], args[2]
    if tipo not in ("D", "P"):
        sys.exit("--tipo debe ser D o P")

    filas = leer(origen, f"ResumenGeneral_{tipo}_DPTOS.json")
    pais = leer(origen, f"ResumenGeneral_{tipo}.json")[0]

    deptos, usados = {}, set()
    for x in filas:
        nombre = x["DepNombre"].strip()
        if nombre not in DEPARTAMENTOS:
            sys.exit(f"Departamento no reconocido: {nombre!r}")
        votos = {}
        for l in x["EleccionNacional"]:
            pid = lema_id(l["LemaNombre"])
            votos[pid] = votos.get(pid, 0) + int(l["Total"])
        if sum(votos.values()) != int(x["TotalVotosALemas"]):
            sys.exit(f"{nombre}: la suma por lema no coincide con TotalVotosALemas")
        usados.update(votos)
        deptos[nombre] = {
            "habilitados": int(x["TotalHabilitados"]),
            "emitidos": int(x["TotalEmitidos"]),
            "blancos": int(x["TotalEnBlanco"]),
            "anulados": int(x["TotalAnulados"]),
            "votos": votos,
        }
    faltan = set(DEPARTAMENTOS) - set(deptos)
    if faltan:
        sys.exit(f"Faltan departamentos: {sorted(faltan)}")
    # control contra el total nacional
    if sum(d["habilitados"] for d in deptos.values()) != int(pais["TotalHabilitados"]):
        sys.exit("La suma de habilitados por departamento no coincide con el total del país")
    if sum(sum(d["votos"].values()) for d in deptos.values()) != int(pais["TotalVotosALemas"]):
        sys.exit("La suma de votos por departamento no coincide con el total del país")

    partidos = [{"id": k, "nombre": v[0], "color": v[1]} for k, v in COLORES.items() if k in usados]
    eleccion = {
        "id": eid, "label": label, "demo": False,
        "fuente": f"Corte Electoral de Uruguay, archivos JSON oficiales "
                  f"({'escrutinio departamental' if tipo == 'D' else 'conteo primario'}, "
                  f"consulta del {pais['FechaConsulta']}, circuitos escrutados: "
                  f"{pais['CircuitosEscrutados']} de {pais['CircuitosTotal']}).",
        "partidos": partidos,
        "departamentos": deptos,
    }

    data = {"titulo": "Atlas electoral de Uruguay", "elecciones": []}
    if os.path.exists("datos_uruguay.json") and "--solo" not in sys.argv:
        with open("datos_uruguay.json", encoding="utf-8") as f:
            data = json.load(f)
    data["elecciones"] = [e for e in data.get("elecciones", []) if e["id"] != eid] + [eleccion]
    with open("datos_uruguay.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("datos_uruguay.json escrito:", len(deptos), "departamentos ·", label,
          "· elecciones en el archivo:", [e["id"] for e in data["elecciones"]])

if __name__ == "__main__":
    main()
