import tkinter as tk
from collections import Counter
import string

# ---------------- FUNCIONES DE CIFRADO ----------------

def cifrado_cesar(texto, clave):
    resultado = ""
    for letra in texto.upper():
        if letra in string.ascii_uppercase:
            nueva = (ord(letra) - 65 + clave) % 26 + 65
            resultado += chr(nueva)
        else:
            resultado += letra
    return resultado


def descifrado_cesar(texto, clave):
    return cifrado_cesar(texto, -clave)


def fuerza_bruta(texto):
    resultados = ""
    for clave in range(1, 26):
        resultados += f"Clave {clave:2}: {descifrado_cesar(texto, clave)}\n"
    return resultados


def analisis_repeticion(texto):
    texto = texto.upper()
    letras = [c for c in texto if c in string.ascii_uppercase]
    conteo = Counter(letras)

    resultado = "Frecuencia de letras:\n\n"
    for letra, cantidad in conteo.most_common():
        resultado += f"{letra}: {cantidad}\n"
    return resultado


# ---------------- FUNCIONES INTERFAZ ----------------

def cifrar():
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, cifrado_cesar(entrada_texto.get(), int(entrada_clave.get())))


def descifrar():
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, descifrado_cesar(entrada_texto.get(), int(entrada_clave.get())))


def brute_force():
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, fuerza_bruta(entrada_texto.get()))


def repeticion():
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, analisis_repeticion(entrada_texto.get()))


def limpiar():
    entrada_texto.delete(0, tk.END)
    entrada_clave.delete(0, tk.END)
    salida.delete("1.0", tk.END)


# ---------------- VENTANA PRINCIPAL ----------------

ventana = tk.Tk()
ventana.title("Sistema de Cifrado César")
ventana.geometry("600x550")
ventana.config(bg="#2c3e50")

# ---------------- TITULO ----------------

tk.Label(
    ventana,
    text="Codificador y Descifrador César",
    bg="#2c3e50",
    fg="white",
    font=("Arial", 16, "bold")
).pack(pady=10)

# ---------------- FRAME ENTRADA ----------------

frame_entrada = tk.Frame(ventana, bg="#34495e", padx=10, pady=10)
frame_entrada.pack(pady=10)

tk.Label(
    frame_entrada,
    text="Mensaje:",
    bg="#34495e",
    fg="white"
).grid(row=0, column=0, sticky="w")

entrada_texto = tk.Entry(frame_entrada, width=45)
entrada_texto.grid(row=0, column=1, pady=5)

tk.Label(
    frame_entrada,
    text="Clave (1-25):",
    bg="#34495e",
    fg="white"
).grid(row=1, column=0, sticky="w")

entrada_clave = tk.Entry(frame_entrada, width=10)
entrada_clave.grid(row=1, column=1, sticky="w")

# ---------------- BOTONES ----------------

frame_botones = tk.Frame(ventana, bg="#2c3e50")
frame_botones.pack(pady=10)

tk.Button(
    frame_botones,
    text="Cifrar",
    width=18,
    command=cifrar
).grid(row=0, column=0, padx=5)

tk.Button(
    frame_botones,
    text="Descifrar",
    width=18,
    command=descifrar
).grid(row=0, column=1, padx=5)

tk.Button(
    frame_botones,
    text="Fuerza Bruta",
    width=18,
    command=brute_force
).grid(row=1, column=0, padx=5, pady=5)

tk.Button(
    frame_botones,
    text="Análisis Repetición",
    width=18,
    command=repeticion
).grid(row=1, column=1, padx=5, pady=5)

tk.Button(
    frame_botones,
    text="Limpiar",
    width=38,
    command=limpiar
).grid(row=2, column=0, columnspan=2, pady=10)

# ---------------- SALIDA ----------------

frame_salida = tk.Frame(ventana, bg="#34495e", padx=10, pady=10)
frame_salida.pack(pady=10)

tk.Label(
    frame_salida,
    text="Resultado:",
    bg="#34495e",
    fg="white"
).pack(anchor="w")

salida = tk.Text(frame_salida, width=65, height=12)
salida.pack()

ventana.mainloop()
