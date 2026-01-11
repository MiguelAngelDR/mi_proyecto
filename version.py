import requests
import os
import sys

VERSION_ACTUAL = "v1.0.0"
REPO = "tu_usuario/tu_repositorio"
URL_API = f"https://api.github.com/repos/{REPO}/releases/latest"


def verificar_actualizacion():
    try:
        response = requests.get(URL_API)
        data = response.json()
        nueva_version = data['tag_name']

        if nueva_version != VERSION_ACTUAL:
            print(f"Nueva versión disponible: {nueva_version}")
            descargar_url = data['assets'][0]['browser_download_url']
            nombre_archivo = data['assets'][0]['name']

            # Descargar el nuevo archivo
            print("Descargando actualización...")
            r = requests.get(descargar_url)
            with open(f"nueva_version_{nombre_archivo}", "wb") as f:
                f.write(r.content)

            print("Descarga completada. Reiniciando para aplicar cambios...")
            aplicar_actualizacion(nombre_archivo)
        else:
            print("Estás en la última versión.")
    except Exception as e:
        print(f"Error al verificar actualizaciones: {e}")


def aplicar_actualizacion(archivo_nombre):
    # En Windows, no puedes sobrescribir el .exe que se está ejecutando.
    # Creamos un script temporal (.bat) que reemplaza los archivos y reinicia la app.
    if sys.platform == "win32":
        with open("update.bat", "w") as f:
            f.write(f"""
            @echo off
            timeout /t 2 /nobreak > nul
            del {sys.argv[0]}
            move nueva_version_{archivo_nombre} {sys.argv[0]}
            start {sys.argv[0]}
            del "%~f0"
            """)
        os.startfile("update.bat")
        sys.exit()


# Ejecutar al inicio del programa
if __name__ == "__main__":
    verificar_actualizacion()
    print("Iniciando programa principal...")