import os
import sys
import requests
import subprocess
from github import Github

# --- CONFIGURACIÓN ---
REPO_NOMBRE = "MiguelAngelDR/mi_proyecto"  # Cámbialo por el tuyo
VERSION_ACTUAL = "0.0.1"  # La versión que tiene este código


# ---------------------

def ejecutar_actualizacion():
    # 1. Conectar con GitHub
    g = Github()  # Si el repo es público, no necesitas token
    repo = g.get_repo(REPO_NOMBRE)
    ultima_release = repo.get_latest_release()
    tag_nueva = ultima_release.tag_name.replace("v", "")

    # 2. Comparar versiones
    if tag_nueva == VERSION_ACTUAL:
        print("Ya tienes la última versión.")
        return

    print(f"Nueva versión {tag_nueva} encontrada. Iniciando descarga...")

    # 3. Buscar el archivo .exe en los Assets del Release
    url_descarga = None
    nombre_archivo_remoto = None

    for asset in ultima_release.get_assets():
        if asset.name.endswith(".exe"):
            url_descarga = asset.browser_download_url
            nombre_archivo_remoto = asset.name
            break

    if not url_descarga:
        print("No se encontró un archivo ejecutable en el release.")
        return

    # 4. Descargar el nuevo archivo con un nombre temporal
    nombre_temporal = "nueva_version_temp.exe"
    respuesta = requests.get(url_descarga, stream=True)

    with open(nombre_temporal, "wb") as f:
        for chunk in respuesta.iter_content(chunk_size=8192):
            f.write(chunk)

    # 5. Obtener la ruta del ejecutable que está corriendo ahora
    # Si ejecutas desde Python es main.py, si es exe es main.exe
    ruta_actual = os.path.abspath(sys.argv[0])

    # 6. Crear el script de intercambio (.bat)
    # Este script: espera 2 segundos -> borra el viejo -> renombra el nuevo -> lanza la app
    with open("instalar_update.bat", "w") as f:
        f.write(f"""
@echo off
timeout /t 2 /nobreak > nul
del /f /q "{ruta_actual}"
move /y "{nombre_temporal}" "{ruta_actual}"
start "" "{ruta_actual}"
del "%~f0"
        """)

    print("Descarga completa. El programa se reiniciará para actualizarse.")

    # 7. Ejecutar el .bat y cerrar este programa inmediatamente
    os.startfile("instalar_update.bat")
    sys.exit()


if __name__ == "__main__":
    # Solo intentamos actualizar si el programa está compilado como .exe
    # (Para evitar que borre tu código fuente .py mientras programas)
    if getattr(sys, 'frozen', False):
        ejecutar_actualizacion()
    else:
        print("Modo desarrollo: saltando actualización automática.")