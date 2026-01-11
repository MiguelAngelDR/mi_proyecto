from pyupdater.client import Client
from client_config import ClientConfig # Generado por PyUpdater

def check_for_updates():
    # El parámetro 'refresh=True' descarga los metadatos más recientes de GitHub
    client = Client(ClientConfig(), refresh=True)
    update_obj = client.update_check('TuApp', '1.0.0')

    if update_obj:
        print("Actualización encontrada. Descargando...")
        if update_obj.download():
            print("Instalando y reiniciando...")
            update_obj.extract_restart()