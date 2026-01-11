import os
import sys
import requests
import subprocess
from github import Github

# --- CONFIGURACIÓN ---
REPO_NAME = "tu_usuario/tu_repositorio"  # Ejemplo: "juanperez/mi-app"
VERSION_ACTUAL = "1.0.0"


# ---------------------

def check_for_update():
    if not getattr(sys, 'frozen', False):
        print("Ejecutando en modo desarrollo (No se busca actualización)")
        return

    print(f"Buscando actualizaciones... (Actual: {VERSION_ACTUAL})")
    try:
        g = Github()
        repo = g.get_repo(REPO_NAME)
        latest_release = repo.get_latest_release()
        tag_nueva = latest_release.tag_name.replace("v", "")  # Quita la 'v' si existe

        if tag_nueva != VERSION_ACTUAL:
            print(f"¡Nueva versión detectada: {tag_nueva}!")
            for asset in latest_release.get_assets():
                if asset.name.endswith(".exe"):
                    descargar_y_reemplazar(asset.browser_download_url, asset.name)
                    break
        else:
            print("Estás al día.")
    except Exception as e:
        print(f"Error: {e}")


def descargar_y_reemplazar(url, nombre_exe):
    print("Descargando nueva versión...")
    path_nuevo = "temp_update.exe"
    path_actual = sys.executable  # Ruta real del .exe que está corriendo

    r = requests.get(url, stream=True)
    with open(path_nuevo, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

    # Creamos un script .bat que espere a que la app cierre, reemplace y reinicie
    with open("update.bat", "w") as f:
        f.write(f"""
@echo off
timeout /t 2 /nobreak > nul
del /f /q "{path_actual}"
move /y "{path_nuevo}" "{path_actual}"
start "" "{path_actual}"
del "%~f0"
        """)

    print("La actualización se aplicará al cerrar.")
    os.startfile("update.bat")
    sys.exit()


if __name__ == "__main__":
    check_for_update()