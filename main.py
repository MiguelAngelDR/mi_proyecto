from gui.inicio import MiApp
from updater import check_for_update
import sys
from updater import check_for_update


def main():
    if getattr(sys, 'frozen', False):
        check_for_update()

        print("hola! Esta es mi aplicacion ejecutandose desde un ejecutable")
        input("presiona ENTER para salir...")

    if check_for_update():
        print("Verificador actualizado correctamente")
    else:
        print("No se pudo actualizar el verificador")

        app = MiApp()
        app.mainloop()

if __name__ == "__main__":
    main()