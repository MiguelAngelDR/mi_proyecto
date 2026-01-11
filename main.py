from github import Github
from gui.inicio import MiApp

g = Github()

repo = g.get_repo("MiguelAngelDR/mi_proyecto")

print(f"Descripcion: {repo.description}")
print(f"Creacion: {repo.created_at}")

release = repo.get_latest_release()
print(f"Última versión: {release.tag_name}")
print(f"Nombre del release: {release.title}")

# Listar los archivos subidos (Assets) en ese release
for asset in release.get_assets():
    print(f"Archivo disponible: {asset.name} - URL: {asset.browser_download_url}")

app = MiApp()
app.mainloop()