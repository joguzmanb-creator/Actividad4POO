"""
Clase Vendedor con manejo de excepciones personalizadas e interfaz gráfica.
Demuestra el lanzamiento de excepciones (raise / throw) en métodos de una clase.
"""

import tkinter as tk
from tkinter import messagebox


# ══════════════════════════════════════════════════════════════════
# EXCEPCIÓN PERSONALIZADA
# ══════════════════════════════════════════════════════════════════

class IllegalArgumentException(Exception):
    """Excepción personalizada equivalente a IllegalArgumentException de Java."""
    pass


# ══════════════════════════════════════════════════════════════════
# CLASE DE DOMINIO
# ══════════════════════════════════════════════════════════════════

class Vendedor:
    """Representa a un vendedor con nombre, apellidos y edad."""

    def __init__(self, nombre: str, apellidos: str, edad: int):
        # La edad se valida ANTES de asignar los atributos.
        # Si no es válida, el objeto nunca se construye.
        self.verificar_edad(edad)
        self.nombre = nombre
        self.apellidos = apellidos
        self.edad = edad

    @staticmethod
    def verificar_edad(edad: int) -> None:
        """
        Verifica que la edad sea válida para un vendedor.
        Lanza IllegalArgumentException si no cumple las condiciones.
        """
        if edad < 18:
            raise IllegalArgumentException(
                "El vendedor debe ser mayor de 18 años"
            )
        if edad < 0 or edad > 120:
            raise IllegalArgumentException(
                "La edad no puede ser negativa ni mayor a 120"
            )

    def imprimir(self) -> str:
        """Devuelve una representación legible de los atributos."""
        return (
            f"Nombre:    {self.nombre}\n"
            f"Apellidos: {self.apellidos}\n"
            f"Edad:      {self.edad} años"
        )


# ══════════════════════════════════════════════════════════════════
# PALETA Y FUENTES
# ══════════════════════════════════════════════════════════════════

COLORES = {
    "bg":      "#1a1a2e",
    "panel":   "#16213e",
    "borde":   "#0f3460",
    "acento":  "#e94560",
    "verde":   "#2ecc71",
    "rojo":    "#e74c3c",
    "entrada": "#0d1b2a",
    "fg":      "#eaeaea",
    "fg_dim":  "#a7a9be",
}

FONT_TITULO = ("Georgia", 18, "bold")
FONT_SUB    = ("Courier New", 10)
FONT_LABEL  = ("Courier New", 11)
FONT_ENTRY  = ("Courier New", 13)
FONT_BTN    = ("Courier New", 11, "bold")
FONT_RES    = ("Courier New", 12)


# ══════════════════════════════════════════════════════════════════
# COMPONENTES DE INTERFAZ
# ══════════════════════════════════════════════════════════════════

class CampoEntrada(tk.Frame):
    """Etiqueta + campo de entrada reutilizable."""

    def __init__(self, parent, etiqueta: str, **kwargs):
        super().__init__(parent, bg=COLORES["panel"], **kwargs)

        tk.Label(self, text=etiqueta, width=11, anchor="w",
                 font=FONT_LABEL, bg=COLORES["panel"],
                 fg=COLORES["fg_dim"]).pack(side="left")

        tk.Label(self, text="›", font=("Courier New", 14, "bold"),
                 bg=COLORES["panel"], fg=COLORES["acento"]).pack(side="left", padx=(0, 6))

        self.entry = tk.Entry(self, font=FONT_ENTRY, width=22,
                              bg=COLORES["entrada"], fg=COLORES["fg"],
                              insertbackground=COLORES["acento"],
                              relief="flat", bd=6,
                              highlightthickness=1,
                              highlightcolor=COLORES["acento"],
                              highlightbackground=COLORES["borde"])
        self.entry.pack(side="left")

    def obtener(self) -> str:
        return self.entry.get().strip()

    def limpiar(self):
        self.entry.delete(0, tk.END)

    def focus(self):
        self.entry.focus()


# ══════════════════════════════════════════════════════════════════
# VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════════════════

class VentanaVendedor(tk.Tk):
    """Ventana principal para registrar un vendedor."""

    def __init__(self):
        super().__init__()
        self.title("Registro de Vendedor")
        self.resizable(False, False)
        self.configure(bg=COLORES["bg"])

        self._construir_ui()
        self.campo_nombre.focus()

    # ── Construcción de la UI ──────────────────────────────────────

    def _construir_ui(self):
        self._construir_titulo()
        self._sep()
        self._construir_entradas()
        self._construir_mensaje()
        self._construir_botones()
        self._sep()
        self._construir_resultado()

    def _construir_titulo(self):
        frm = tk.Frame(self, bg=COLORES["bg"], pady=18)
        frm.pack(fill="x")
        tk.Label(frm, text="✦ REGISTRO DE VENDEDOR ✦",
                 font=FONT_TITULO, bg=COLORES["bg"],
                 fg=COLORES["acento"]).pack()
        tk.Label(frm, text="Ingresa los datos del vendedor",
                 font=FONT_SUB, bg=COLORES["bg"],
                 fg=COLORES["fg_dim"]).pack(pady=(2, 0))

    def _sep(self):
        tk.Frame(self, bg=COLORES["borde"], height=2).pack(fill="x", padx=20)

    def _construir_entradas(self):
        frm = tk.Frame(self, bg=COLORES["panel"], padx=30, pady=20)
        frm.pack(fill="x", padx=20, pady=12)

        self.campo_nombre    = CampoEntrada(frm, "Nombre")
        self.campo_apellidos = CampoEntrada(frm, "Apellidos")
        self.campo_edad      = CampoEntrada(frm, "Edad")

        for campo in [self.campo_nombre, self.campo_apellidos, self.campo_edad]:
            campo.pack(fill="x", pady=5)

        # Permite avanzar con Enter
        self.campo_nombre.entry.bind("<Return>",    lambda e: self.campo_apellidos.focus())
        self.campo_apellidos.entry.bind("<Return>", lambda e: self.campo_edad.focus())
        self.campo_edad.entry.bind("<Return>",      lambda e: self._registrar())

    def _construir_mensaje(self):
        self.lbl_mensaje = tk.Label(self, text="", font=FONT_LABEL,
                                    bg=COLORES["bg"], fg=COLORES["rojo"])
        self.lbl_mensaje.pack(pady=(0, 4))

    def _construir_botones(self):
        frm = tk.Frame(self, bg=COLORES["bg"], pady=4)
        frm.pack()

        tk.Button(frm, text="REGISTRAR", command=self._registrar,
                  font=FONT_BTN, fg=COLORES["fg"], bg=COLORES["acento"],
                  activebackground=COLORES["acento"], activeforeground="#ffffff",
                  relief="flat", bd=0, padx=22, pady=8,
                  cursor="hand2").pack(side="left", padx=8)

        tk.Button(frm, text="LIMPIAR", command=self._limpiar,
                  font=FONT_BTN, fg=COLORES["fg_dim"], bg=COLORES["borde"],
                  activebackground=COLORES["acento"], activeforeground="#ffffff",
                  relief="flat", bd=0, padx=22, pady=8,
                  cursor="hand2").pack(side="left", padx=8)

    def _construir_resultado(self):
        frm = tk.Frame(self, bg=COLORES["panel"], padx=30, pady=18)
        frm.pack(fill="x", padx=20, pady=12)

        tk.Label(frm, text="DATOS REGISTRADOS",
                 font=("Courier New", 10, "bold"),
                 bg=COLORES["panel"], fg=COLORES["acento"]).pack(anchor="w", pady=(0, 10))

        self.lbl_resultado = tk.Label(
            frm, text="— sin registro —",
            font=FONT_RES, bg=COLORES["panel"], fg=COLORES["fg_dim"],
            justify="left", anchor="w"
        )
        self.lbl_resultado.pack(anchor="w")

    # ── Lógica de eventos ──────────────────────────────────────────

    def _registrar(self):
        """Toma los datos de los campos y trata de instanciar un Vendedor."""
        nombre    = self.campo_nombre.obtener()
        apellidos = self.campo_apellidos.obtener()
        edad_str  = self.campo_edad.obtener()

        # Validamos que no haya campos vacíos
        if not nombre or not apellidos or not edad_str:
            self._mostrar_error("⚠ Todos los campos son obligatorios.")
            return

        # Intentamos construir el vendedor capturando excepciones
        try:
            edad = int(edad_str)
        except ValueError:
            self._mostrar_error(f"⚠ '{edad_str}' no es un número entero válido.")
            return

        try:
            vendedor = Vendedor(nombre, apellidos, edad)
        except IllegalArgumentException as e:
            self._mostrar_error(f"⚠ {e}")
            self.lbl_resultado.config(text="— sin registro —",
                                      fg=COLORES["fg_dim"])
            return

        # Éxito: mostramos los datos del vendedor
        self.lbl_mensaje.config(text="✓ Vendedor registrado correctamente",
                                fg=COLORES["verde"])
        self.lbl_resultado.config(text=vendedor.imprimir(),
                                  fg=COLORES["fg"])

    def _mostrar_error(self, mensaje: str):
        self.lbl_mensaje.config(text=mensaje, fg=COLORES["rojo"])

    def _limpiar(self):
        for campo in [self.campo_nombre, self.campo_apellidos, self.campo_edad]:
            campo.limpiar()
        self.lbl_mensaje.config(text="")
        self.lbl_resultado.config(text="— sin registro —",
                                  fg=COLORES["fg_dim"])
        self.campo_nombre.focus()


# ══════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = VentanaVendedor()
    app.mainloop()
