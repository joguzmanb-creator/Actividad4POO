"""
Clase CalculosNumericos con métodos estáticos y manejo de excepciones aritméticas.
Demuestra el uso de múltiples bloques except (catch) para distintos tipos de error.
"""

import math
import tkinter as tk


# ══════════════════════════════════════════════════════════════════
# EXCEPCIÓN PERSONALIZADA
# ══════════════════════════════════════════════════════════════════

class ArithmeticException(ArithmeticError):
    """
    Excepción aritmética personalizada (equivalente a la de Java).
    Hereda de ArithmeticError, la jerarquía de errores aritméticos de Python.
    """
    pass


# ══════════════════════════════════════════════════════════════════
# CLASE DE DOMINIO
# ══════════════════════════════════════════════════════════════════

class CalculosNumericos:
    """
    Clase utilitaria con operaciones numéricas estáticas.
    No requiere instanciación: sus métodos se invocan directamente sobre la clase.
    """

    @staticmethod
    def logaritmo_neperiano(valor: float) -> float:
        """
        Calcula el logaritmo neperiano (ln) de un valor positivo.
        Lanza ArithmeticException si el valor no es positivo.
        """
        if valor <= 0:
            raise ArithmeticException(
                f"No se puede calcular el logaritmo de {valor}: "
                "el valor debe ser positivo (mayor que 0)"
            )
        return math.log(valor)

    @staticmethod
    def raiz_cuadrada(valor: float) -> float:
        """
        Calcula la raíz cuadrada de un valor positivo.
        Lanza ArithmeticException si el valor no es positivo.
        """
        if valor <= 0:
            raise ArithmeticException(
                f"No se puede calcular la raíz cuadrada de {valor}: "
                "el valor debe ser positivo (mayor que 0)"
            )
        return math.sqrt(valor)


# ══════════════════════════════════════════════════════════════════
# PALETA Y FUENTES
# ══════════════════════════════════════════════════════════════════

COLORES = {
    "bg":      "#1a1a2e",
    "panel":   "#16213e",
    "borde":   "#0f3460",
    "acento":  "#e94560",
    "verde":   "#2ecc71",
    "amarillo":"#f39c12",
    "rojo":    "#e74c3c",
    "entrada": "#0d1b2a",
    "fg":      "#eaeaea",
    "fg_dim":  "#a7a9be",
}

FONT_TITULO = ("Georgia", 18, "bold")
FONT_SUB    = ("Courier New", 10)
FONT_LABEL  = ("Courier New", 11)
FONT_ENTRY  = ("Courier New", 14)
FONT_BTN    = ("Courier New", 11, "bold")
FONT_RES_L  = ("Courier New", 10)
FONT_RES_V  = ("Georgia", 16, "bold")


# ══════════════════════════════════════════════════════════════════
# COMPONENTES DE INTERFAZ
# ══════════════════════════════════════════════════════════════════

class FilaResultado(tk.Frame):
    """Fila etiqueta + valor para mostrar resultados."""

    def __init__(self, parent, etiqueta: str, color_val: str, **kwargs):
        super().__init__(parent, bg=COLORES["panel"], **kwargs)
        self.color_val = color_val

        tk.Label(self, text=etiqueta, font=FONT_RES_L, width=22, anchor="w",
                 bg=COLORES["panel"], fg=COLORES["fg_dim"]).pack(side="left")

        self.lbl_val = tk.Label(self, text="—", font=FONT_RES_V,
                                bg=COLORES["panel"], fg=COLORES["fg_dim"],
                                width=16, anchor="e")
        self.lbl_val.pack(side="right")

    def actualizar(self, valor: float):
        self.lbl_val.config(text=f"{valor:.6f}", fg=self.color_val)

    def limpiar(self):
        self.lbl_val.config(text="—", fg=COLORES["fg_dim"])


# ══════════════════════════════════════════════════════════════════
# VENTANA PRINCIPAL
# ══════════════════════════════════════════════════════════════════

class VentanaCalculos(tk.Tk):
    """Ventana principal de la calculadora de logaritmo neperiano y raíz cuadrada."""

    def __init__(self):
        super().__init__()
        self.title("Cálculos Numéricos")
        self.resizable(False, False)
        self.configure(bg=COLORES["bg"])

        self._construir_ui()
        self.entry_valor.focus()

    # ── Construcción de la UI ──────────────────────────────────────

    def _construir_ui(self):
        self._construir_titulo()
        self._sep()
        self._construir_entrada()
        self._construir_mensaje()
        self._construir_botones()
        self._sep()
        self._construir_resultados()
        self._construir_footer()

    def _construir_titulo(self):
        frm = tk.Frame(self, bg=COLORES["bg"], pady=18)
        frm.pack(fill="x")
        tk.Label(frm, text="✦ CÁLCULOS NUMÉRICOS ✦",
                 font=FONT_TITULO, bg=COLORES["bg"],
                 fg=COLORES["acento"]).pack()
        tk.Label(frm, text="Logaritmo neperiano y raíz cuadrada",
                 font=FONT_SUB, bg=COLORES["bg"],
                 fg=COLORES["fg_dim"]).pack(pady=(2, 0))

    def _sep(self):
        tk.Frame(self, bg=COLORES["borde"], height=2).pack(fill="x", padx=20)

    def _construir_entrada(self):
        frm = tk.Frame(self, bg=COLORES["panel"], padx=30, pady=20)
        frm.pack(fill="x", padx=20, pady=12)

        fila = tk.Frame(frm, bg=COLORES["panel"])
        fila.pack()

        tk.Label(fila, text="Valor", width=8, anchor="w",
                 font=FONT_LABEL, bg=COLORES["panel"],
                 fg=COLORES["fg_dim"]).pack(side="left")

        tk.Label(fila, text="›", font=("Courier New", 14, "bold"),
                 bg=COLORES["panel"], fg=COLORES["acento"]).pack(side="left", padx=(0, 6))

        self.entry_valor = tk.Entry(fila, font=FONT_ENTRY, width=18,
                                    bg=COLORES["entrada"], fg=COLORES["fg"],
                                    insertbackground=COLORES["acento"],
                                    relief="flat", bd=6,
                                    highlightthickness=1,
                                    highlightcolor=COLORES["acento"],
                                    highlightbackground=COLORES["borde"])
        self.entry_valor.pack(side="left")

        # Enter ejecuta ambos cálculos
        self.entry_valor.bind("<Return>", lambda e: self._calcular_ambos())

    def _construir_mensaje(self):
        self.lbl_mensaje = tk.Label(self, text="", font=FONT_LABEL,
                                    bg=COLORES["bg"], fg=COLORES["rojo"])
        self.lbl_mensaje.pack(pady=(2, 4))

    def _construir_botones(self):
        frm = tk.Frame(self, bg=COLORES["bg"], pady=4)
        frm.pack()

        tk.Button(frm, text="ln (x)", command=self._calcular_ln,
                  font=FONT_BTN, fg=COLORES["fg"], bg=COLORES["acento"],
                  activebackground=COLORES["acento"], activeforeground="#ffffff",
                  relief="flat", bd=0, padx=18, pady=8,
                  cursor="hand2").pack(side="left", padx=6)

        tk.Button(frm, text="√ x", command=self._calcular_raiz,
                  font=FONT_BTN, fg=COLORES["fg"], bg=COLORES["acento"],
                  activebackground=COLORES["acento"], activeforeground="#ffffff",
                  relief="flat", bd=0, padx=18, pady=8,
                  cursor="hand2").pack(side="left", padx=6)

        tk.Button(frm, text="AMBOS", command=self._calcular_ambos,
                  font=FONT_BTN, fg=COLORES["bg"], bg=COLORES["amarillo"],
                  activebackground=COLORES["amarillo"], activeforeground=COLORES["bg"],
                  relief="flat", bd=0, padx=18, pady=8,
                  cursor="hand2").pack(side="left", padx=6)

        tk.Button(frm, text="LIMPIAR", command=self._limpiar,
                  font=FONT_BTN, fg=COLORES["fg_dim"], bg=COLORES["borde"],
                  activebackground=COLORES["acento"], activeforeground="#ffffff",
                  relief="flat", bd=0, padx=18, pady=8,
                  cursor="hand2").pack(side="left", padx=6)

    def _construir_resultados(self):
        frm = tk.Frame(self, bg=COLORES["panel"], padx=30, pady=20)
        frm.pack(fill="x", padx=20, pady=12)

        tk.Label(frm, text="RESULTADOS", font=("Courier New", 10, "bold"),
                 bg=COLORES["panel"], fg=COLORES["acento"]).pack(anchor="w", pady=(0, 10))

        self.fila_ln   = FilaResultado(frm, "ln (x)         logaritmo", COLORES["verde"])
        self.fila_raiz = FilaResultado(frm, "√ x            raíz cuadrada", COLORES["amarillo"])

        self.fila_ln.pack(fill="x", pady=4)
        self.fila_raiz.pack(fill="x", pady=4)

    def _construir_footer(self):
        tk.Label(self,
                 text="  El valor debe ser positivo (mayor que 0)  ",
                 font=("Courier New", 8),
                 bg=COLORES["bg"], fg="#555577").pack(pady=(0, 10))

    # ── Lógica de eventos ──────────────────────────────────────────
    # Cada handler demuestra el uso de MÚLTIPLES bloques except (catch)
    # ────────────────────────────────────────────────────────────────

    def _obtener_valor(self) -> float | None:
        """Convierte la entrada en float, capturando ValueError si falla."""
        texto = self.entry_valor.get().strip()
        if not texto:
            self._mostrar_error("⚠ Ingresa un valor numérico.")
            return None
        try:
            return float(texto)
        except ValueError:
            self._mostrar_error(f"⚠ '{texto}' no es un número válido.")
            return None

    def _calcular_ln(self):
        """Calcula el logaritmo neperiano con múltiples catch."""
        valor = self._obtener_valor()
        if valor is None:
            self.fila_ln.limpiar()
            return

        try:
            resultado = CalculosNumericos.logaritmo_neperiano(valor)
            self.fila_ln.actualizar(resultado)
            self._mostrar_exito("✓ Logaritmo neperiano calculado.")
        except ArithmeticException as e:
            self._mostrar_error(f"⚠ {e}")
            self.fila_ln.limpiar()
        except Exception as e:
            self._mostrar_error(f"⚠ Error inesperado: {e}")
            self.fila_ln.limpiar()

    def _calcular_raiz(self):
        """Calcula la raíz cuadrada con múltiples catch."""
        valor = self._obtener_valor()
        if valor is None:
            self.fila_raiz.limpiar()
            return

        try:
            resultado = CalculosNumericos.raiz_cuadrada(valor)
            self.fila_raiz.actualizar(resultado)
            self._mostrar_exito("✓ Raíz cuadrada calculada.")
        except ArithmeticException as e:
            self._mostrar_error(f"⚠ {e}")
            self.fila_raiz.limpiar()
        except Exception as e:
            self._mostrar_error(f"⚠ Error inesperado: {e}")
            self.fila_raiz.limpiar()

    def _calcular_ambos(self):
        """Calcula ambas operaciones, mostrando MÚLTIPLES catch en acción."""
        valor = self._obtener_valor()
        if valor is None:
            self.fila_ln.limpiar()
            self.fila_raiz.limpiar()
            return

        # Un solo bloque try con múltiples except (multi-catch)
        try:
            ln    = CalculosNumericos.logaritmo_neperiano(valor)
            raiz  = CalculosNumericos.raiz_cuadrada(valor)
            self.fila_ln.actualizar(ln)
            self.fila_raiz.actualizar(raiz)
            self._mostrar_exito("✓ Ambos cálculos realizados correctamente.")
        except ArithmeticException as e:
            self._mostrar_error(f"⚠ Error aritmético: {e}")
            self.fila_ln.limpiar()
            self.fila_raiz.limpiar()
        except ValueError as e:
            self._mostrar_error(f"⚠ Valor inválido: {e}")
        except Exception as e:
            self._mostrar_error(f"⚠ Error inesperado: {e}")

    def _mostrar_error(self, mensaje: str):
        self.lbl_mensaje.config(text=mensaje, fg=COLORES["rojo"])

    def _mostrar_exito(self, mensaje: str):
        self.lbl_mensaje.config(text=mensaje, fg=COLORES["verde"])

    def _limpiar(self):
        self.entry_valor.delete(0, tk.END)
        self.fila_ln.limpiar()
        self.fila_raiz.limpiar()
        self.lbl_mensaje.config(text="")
        self.entry_valor.focus()


# ══════════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ══════════════════════════════════════════════════════════════════

def main():
    """Método main que crea y ejecuta la ventana principal."""
    app = VentanaCalculos()
    app.mainloop()


if __name__ == "__main__":
    main()
