import tkinter as tk
from tkinter import messagebox
import os


def guardar_config():
    token = entry_token.get().strip()
    url = entry_url.get().strip()

    if not token or not url:
        messagebox.showwarning("Aviso", "Por favor, rellena todos los campos.")
        return

    # Guarda los datos en un archivo oculto .env
    with open(".env", "w") as f:
        f.write(f"TELEGRAM_TOKEN={token}\n")
        f.write(f"API_URL={url}\n")

    messagebox.showinfo("Éxito", "Configuración guardada correctamente en el archivo .env")
    root.destroy()


# Configuración de la ventana principal
root = tk.Tk()
root.title("Configuración del Bot,")
root.geometry("450x250")
root.resizable(False, False)

tk.Label(root, text="Token del Bot de Telegram:", font=("Arial", 10, "bold")).pack(pady=(20, 5))
entry_token = tk.Entry(root, width=50)
entry_token.pack(pady=5)

tk.Label(root, text="URL de la API:", font=("Arial", 10, "bold")).pack(pady=(15, 5))
entry_url = tk.Entry(root, width=50)
entry_url.insert(0, "http://localhost:8000/chat")  # Valor por defecto
entry_url.pack(pady=5)

btn_guardar = tk.Button(root, text="Guardar Configuración", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                        command=guardar_config)
btn_guardar.pack(pady=25)

if os.path.exists(".env"):
    with open(".env", "r") as f:
        lineas = f.readlines()
        for linea in lineas:
            if linea.startswith("TELEGRAM_TOKEN="):
                entry_token.insert(0, linea.split("=")[1].strip())
            elif linea.startswith("API_URL="):
                entry_url.delete(0, tk.END)
                entry_url.insert(0, linea.split("=")[1].strip())

root.mainloop()