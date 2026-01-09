import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import tkinter.font as font

# ─── Funciones de cifrado (igual que antes) ─────────────────────────────────

def cesar_cifrar(texto: str, desplazamiento: int) -> str:
    resultado = []
    desplazamiento = desplazamiento % 26
    for c in texto:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            nuevo = (ord(c) - base + desplazamiento) % 26 + base
            resultado.append(chr(nuevo))
        else:
            resultado.append(c)
    return ''.join(resultado)


def texto_a_desplazamiento(clave_texto: str) -> int:
    if not clave_texto:
        return 0
    total = sum(ord(c) - ord('A') for c in clave_texto.upper() if c.isalpha())
    return total % 26


def cesar_descifrar(texto: str, desplazamiento: int) -> str:
    return cesar_cifrar(texto, -desplazamiento)


def fuerza_bruta_cesar(texto_cifrado: str) -> list:
    resultados = []
    for clave in range(26):
        intento = cesar_descifrar(texto_cifrado, clave)
        resultados.append((clave, intento))
    return resultados


def repeticion_cifrar(texto: str, clave: str) -> str:
    resultado = []
    clave_bytes = clave.encode('utf-8')
    texto_bytes = texto.encode('utf-8')
    for i in range(len(texto_bytes)):
        c = texto_bytes[i]
        k = clave_bytes[i % len(clave_bytes)]
        resultado.append(c ^ k)
    return bytes(resultado).hex().upper()


def repeticion_descifrar(hex_cifrado: str, clave: str) -> str:
    try:
        datos = bytes.fromhex(hex_cifrado)
    except:
        return "[Error: formato hexadecimal inválido]"
        
    clave_bytes = clave.encode('utf-8')
    resultado = []
    for i in range(len(datos)):
        c = datos[i]
        k = clave_bytes[i % len(clave_bytes)]
        resultado.append(c ^ k)
    try:
        return bytes(resultado).decode('utf-8')
    except:
        return "[No se pudo decodificar como UTF-8]"


# ─── Interfaz gráfica ───────────────────────────────────────────────────────

class CifradoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Proyecto Cifrado")
        self.root.geometry("940x680")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        # Colores tema oscuro moderno
        self.bg = "#1e1e2e"
        self.fg = "#cdd6f4"
        self.accent = "#89b4fa"
        self.input_bg = "#302d41"
        self.button_bg = "#45475a"
        self.result_bg = "#2a2a3e"

        # Fuentes
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=11)
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")

        self.create_widgets()


    def create_widgets(self):
        # Título
        title = tk.Label(self.root, text="PROYECTO CIFRADO", font=self.title_font,
                        bg=self.bg, fg=self.accent)
        title.pack(pady=(20, 5))

        subtitle = tk.Label(self.root, text="César • César con palabra • Fuerza bruta • Repetición (XOR)",
                           font=self.subtitle_font, bg=self.bg, fg="#94e2d5")
        subtitle.pack(pady=(0, 15))

        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # ── Entrada ────────────────────────────────────────────────────────────
        input_frame = tk.LabelFrame(main_frame, text=" Entrada ", bg=self.bg, fg=self.accent,
                                  font=self.subtitle_font, padx=10, pady=10)
        input_frame.pack(fill="x", pady=5)

        tk.Label(input_frame, text="Texto:", bg=self.bg, fg=self.fg).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.texto_input = scrolledtext.ScrolledText(input_frame, height=5, width=80,
                                                    bg=self.input_bg, fg=self.fg, insertbackground="white",
                                                    font=("Consolas", 11))
        self.texto_input.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        # ── Panel de controles ─────────────────────────────────────────────────
        control_frame = tk.Frame(main_frame, bg=self.bg)
        control_frame.pack(fill="x", pady=10)

        # Botones principales (grid de 2x3)
        btn_style = {"bg": self.button_bg, "fg": self.fg, "activebackground": self.accent,
                    "font": ("Helvetica", 10, "bold"), "width": 20, "bd": 0, "pady": 8}

        tk.Button(control_frame, text="Cifrar César (número)", command=self.cesar_num_cifrar, **btn_style).grid(row=0, column=0, padx=8, pady=6)
        tk.Button(control_frame, text="Descifrar César (número)", command=self.cesar_num_descifrar, **btn_style).grid(row=0, column=1, padx=8, pady=6)
        tk.Button(control_frame, text="Cifrar César (palabra)", command=self.cesar_texto_cifrar, **btn_style).grid(row=0, column=2, padx=8, pady=6)

        tk.Button(control_frame, text="Descifrar César (palabra)", command=self.cesar_texto_descifrar, **btn_style).grid(row=1, column=0, padx=8, pady=6)
        tk.Button(control_frame, text="Fuerza Bruta César", command=self.ejecutar_fuerza_bruta, **btn_style).grid(row=1, column=1, padx=8, pady=6)
        tk.Button(control_frame, text="Cifrar/Descifrar Repetición", command=self.repeticion_dialog, **btn_style).grid(row=1, column=2, padx=8, pady=6)

        # ── Resultado ──────────────────────────────────────────────────────────
        result_frame = tk.LabelFrame(main_frame, text=" Resultado ", bg=self.bg, fg=self.accent,
                                   font=self.subtitle_font, padx=10, pady=10)
        result_frame.pack(fill="both", expand=True)

        self.result_text = scrolledtext.ScrolledText(result_frame, height=14, width=90,
                                                    bg=self.result_bg, fg="#a6e3a1", font=("Consolas", 11),
                                                    insertbackground="white")
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)


    def clear_result(self):
        self.result_text.delete("1.0", tk.END)


    def show_result(self, title, content):
        self.clear_result()
        self.result_text.insert(tk.END, f"┌─ {title} ─{'─'*60}\n\n")
        self.result_text.insert(tk.END, content + "\n\n")
        self.result_text.insert(tk.END, f"{'─'*70}┘\n")


    def get_texto(self):
        texto = self.texto_input.get("1.0", tk.END).strip()
        if not texto:
            messagebox.showwarning("Atención", "Por favor escribe un texto")
            return None
        return texto


    # ─── Acciones César numérico ──────────────────────────────────────────────

    def cesar_num_cifrar(self):
        texto = self.get_texto()
        if not texto: return

        dialog = tk.Toplevel(self.root)
        dialog.title("Clave numérica")
        dialog.geometry("380x180")
        dialog.configure(bg=self.bg)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Desplazamiento (0-25):", bg=self.bg, fg=self.fg).pack(pady=15)
        entry = tk.Entry(dialog, width=10, justify="center", font=("Helvetica", 12))
        entry.pack(pady=10)

        def ok():
            try:
                clave = int(entry.get())
                if 0 <= clave <= 25:
                    resultado = cesar_cifrar(texto, clave)
                    self.show_result(f"CIFRADO CÉSAR - desplazamiento {clave}", resultado)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "El número debe estar entre 0 y 25")
            except:
                messagebox.showerror("Error", "Debe ingresar un número")

        tk.Button(dialog, text="Aceptar", command=ok, bg=self.accent, fg="black", font=("Helvetica", 10, "bold")).pack(pady=15)


    def cesar_num_descifrar(self):
        texto = self.get_texto()
        if not texto: return

        dialog = tk.Toplevel(self.root)
        dialog.title("Clave numérica")
        dialog.geometry("380x180")
        dialog.configure(bg=self.bg)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Desplazamiento (0-25):", bg=self.bg, fg=self.fg).pack(pady=15)
        entry = tk.Entry(dialog, width=10, justify="center", font=("Helvetica", 12))
        entry.pack(pady=10)

        def ok():
            try:
                clave = int(entry.get())
                if 0 <= clave <= 25:
                    resultado = cesar_descifrar(texto, clave)
                    self.show_result(f"DESCIFRADO CÉSAR - desplazamiento {clave}", resultado)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", "El número debe estar entre 0 y 25")
            except:
                messagebox.showerror("Error", "Debe ingresar un número")

        tk.Button(dialog, text="Aceptar", command=ok, bg=self.accent, fg="black", font=("Helvetica", 10, "bold")).pack(pady=15)


    # ─── Acciones César con texto ─────────────────────────────────────────────

    def cesar_texto_cifrar(self):
        texto = self.get_texto()
        if not texto: return

        dialog = tk.Toplevel(self.root)
        dialog.title("Clave de texto")
        dialog.geometry("480x200")
        dialog.configure(bg=self.bg)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Palabra/clave:", bg=self.bg, fg=self.fg).pack(pady=15)
        entry = tk.Entry(dialog, width=40, font=("Helvetica", 11))
        entry.pack(pady=10)

        def ok():
            clave = entry.get().strip()
            if not clave:
                messagebox.showwarning("Atención", "Escribe una clave")
                return
            desp = texto_a_desplazamiento(clave)
            resultado = cesar_cifrar(texto, desp)
            self.show_result(f"CIFRADO CÉSAR con clave '{clave}' (desplazamiento {desp})", resultado)
            dialog.destroy()

        tk.Button(dialog, text="Cifrar", command=ok, bg=self.accent, fg="black", font=("Helvetica", 10, "bold")).pack(pady=15)


    def cesar_texto_descifrar(self):
        texto = self.get_texto()
        if not texto: return

        dialog = tk.Toplevel(self.root)
        dialog.title("Clave de texto")
        dialog.geometry("480x200")
        dialog.configure(bg=self.bg)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Palabra/clave:", bg=self.bg, fg=self.fg).pack(pady=15)
        entry = tk.Entry(dialog, width=40, font=("Helvetica", 11))
        entry.pack(pady=10)

        def ok():
            clave = entry.get().strip()
            if not clave:
                messagebox.showwarning("Atención", "Escribe una clave")
                return
            desp = texto_a_desplazamiento(clave)
            resultado = cesar_descifrar(texto, desp)
            self.show_result(f"DESCIFRADO CÉSAR con clave '{clave}' (desplazamiento {desp})", resultado)
            dialog.destroy()

        tk.Button(dialog, text="Descifrar", command=ok, bg=self.accent, fg="black", font=("Helvetica", 10, "bold")).pack(pady=15)


    def ejecutar_fuerza_bruta(self):
        texto = self.get_texto()
        if not texto: return

        resultados = fuerza_bruta_cesar(texto)
        salida = ""
        for clave, texto in resultados:
            salida += f"[{clave:2d}]   {texto}\n"
            if (clave + 1) % 5 == 0:
                salida += "─" * 60 + "\n"

        self.show_result("FUERZA BRUTA - Todas las 26 posibilidades", salida)


    def repeticion_dialog(self):
        texto = self.get_texto()
        if not texto: return

        dialog = tk.Toplevel(self.root)
        dialog.title("Cifrado por Repetición (Vernam/XOR)")
        dialog.geometry("520x280")
        dialog.configure(bg=self.bg)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(dialog, text="Clave (se usará para cifrar y descifrar):", bg=self.bg, fg=self.fg).pack(pady=10)

        clave_frame = tk.Frame(dialog, bg=self.bg)
        clave_frame.pack(pady=5)

        clave_var = tk.StringVar()
        entry = tk.Entry(clave_frame, textvariable=clave_var, width=45, show="*", font=("Helvetica", 11))
        entry.pack(side="left", padx=10)

        show_var = tk.BooleanVar()
        tk.Checkbutton(clave_frame, text="Mostrar", variable=show_var,
                      command=lambda: entry.config(show="" if show_var.get() else "*"),
                      bg=self.bg, fg=self.fg, selectcolor=self.input_bg).pack(side="left")

        tk.Label(dialog, text="¿Qué quieres hacer?", bg=self.bg, fg=self.fg).pack(pady=15)

        def cifrar():
            clave = clave_var.get()
            if not clave:
                messagebox.showwarning("Atención", "Escribe una clave")
                return
            resultado = repeticion_cifrar(texto, clave)
            self.show_result(f"CIFRADO REPETICIÓN (XOR) - clave: {clave}", resultado)
            dialog.destroy()

        def descifrar():
            clave = clave_var.get()
            if not clave:
                messagebox.showwarning("Atención", "Escribe una clave")
                return
            resultado = repeticion_descifrar(texto, clave)
            self.show_result("DESCIFRADO REPETICIÓN (XOR)", resultado)
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg=self.bg)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Cifrar", command=cifrar, bg="#fab387", fg="black", font=("Helvetica", 10, "bold"), width=15).pack(side="left", padx=20)
        tk.Button(btn_frame, text="Descifrar", command=descifrar, bg="#94e2d5", fg="black", font=("Helvetica", 10, "bold"), width=15).pack(side="left", padx=20)


# ─── Inicio del programa ─────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = CifradoApp(root)
    root.mainloop()