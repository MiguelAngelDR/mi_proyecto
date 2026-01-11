import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class MiApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configuracion de la ventana
        self.title = "Mi Interfaz Moderna"
        self.geometry("400x300")

        # crear widgets
        self.label = ctk.CTkLabel(self, text="¡Hola, mundo!")
        self.label.pack(pady=20)

        self.entry = ctk.CTkEntry(self, placeholder_text="Nombre...")
        self.entry.pack(pady=10)

        self.button = ctk.CTkButton(self, text="Saludar", command=self.saludar)
        self.button.pack(pady=10)

    def saludar(self):
        pass