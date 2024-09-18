import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application, convert_xor)
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Método de Newton-Raphson estándar
def newton_raphson(func_expr, initial_guess, tol=1e-12, max_iter=1000):
    return newton_raphson_base(func_expr, initial_guess, tol, max_iter)

# Método de Newton-Raphson con relajación (Acelerado)
def newton_raphson_relajado(func_expr, initial_guess, tol=1e-12, max_iter=1000, relaxation_factor=0.5):
    return newton_raphson_base(func_expr, initial_guess, tol, max_iter, relaxation_factor)

# Método de Newton-Raphson Modificado (Mejorado)
def newton_raphson_mejorado(func_expr, initial_guess, tol=1e-12, max_iter=1000):
    try:
        x = sp.symbols('x')
        transformations = (standard_transformations + (implicit_multiplication_application, convert_xor,))
        local_dict = {'e': sp.E}
        f = parse_expr(func_expr, transformations=transformations, local_dict=local_dict)
        f_prime = sp.diff(f, x)
        f_second = sp.diff(f_prime, x)

        f_lambdified = sp.lambdify(x, f)
        f_prime_lambdified = sp.lambdify(x, f_prime)
        f_second_lambdified = sp.lambdify(x, f_second)

        current_guess = initial_guess
        approximations = [current_guess]  # Lista para almacenar aproximaciones

        output_text.insert(tk.END, f"Función: {f}\n", 'bold')
        output_text.insert(tk.END, f"Derivada primera: {f_prime}\n", 'bold')
        output_text.insert(tk.END, f"Derivada segunda: {f_second}\n", 'bold')

        for i in range(1, max_iter+1):
            f_value = f_lambdified(current_guess)
            f_prime_value = f_prime_lambdified(current_guess)
            f_second_value = f_second_lambdified(current_guess)

            denominator = f_prime_value**2 - f_value * f_second_value
            if abs(denominator) < 1e-14:
                output_text.insert(tk.END, f"División por valor cercano a cero en la iteración {i}. El método no puede continuar.\n", 'error')
                return None

            next_guess = current_guess - (f_value * f_prime_value) / denominator
            approximations.append(next_guess)  # Guardar la nueva aproximación
            error = abs(next_guess - current_guess)

            output_text.insert(tk.END, f"Iteración {i}: Valor aproximado = {next_guess}, Error aproximado = {error}, f(x) = {f_value}\n", 'bold')

            if abs(f_value) < tol or error < tol:
                output_text.insert(tk.END, f"\nRaíz encontrada: {next_guess}\n", 'bold')
                output_text.insert(tk.END, f"f(x) ≈ 0 (con tolerancia {tol})\n", 'bold')
                output_text.insert(tk.END, f"Iteraciones totales: {i}\n", 'bold')
                actualizar_grafico(approximations)  # Actualizar gráfico al final
                return next_guess

            current_guess = next_guess

        output_text.insert(tk.END, "El método no converge después del número máximo de iteraciones.\n", 'error')
        return None

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar la función: {e}")
        return None

# Método base de Newton-Raphson con opción de relajación
def newton_raphson_base(func_expr, initial_guess, tol=1e-12, max_iter=1000, relaxation_factor=1.0):
    try:
        x = sp.symbols('x')
        transformations = (standard_transformations + (implicit_multiplication_application, convert_xor,))
        local_dict = {'e': sp.E}
        f = parse_expr(func_expr, transformations=transformations, local_dict=local_dict)
        f_prime = sp.diff(f, x)

        f_lambdified = sp.lambdify(x, f)
        f_prime_lambdified = sp.lambdify(x, f_prime)

        current_guess = initial_guess
        approximations = [current_guess]  # Lista para almacenar aproximaciones

        output_text.insert(tk.END, f"Función: {f}\n", 'bold')
        output_text.insert(tk.END, f"Derivada: {f_prime}\n", 'bold')

        for i in range(1, max_iter+1):
            f_value = f_lambdified(current_guess)
            f_prime_value = f_prime_lambdified(current_guess)

            if abs(f_prime_value) < 1e-14:
                output_text.insert(tk.END, f"Derivada muy pequeña en x = {current_guess}. El método no puede continuar.\n", 'error')
                return None

            next_guess = current_guess - relaxation_factor * f_value / f_prime_value
            approximations.append(next_guess)  # Guardar la nueva aproximación
            error = abs(next_guess - current_guess)

            output_text.insert(tk.END, f"Iteración {i}: Valor aproximado = {next_guess}, Error aproximado = {error}, f(x) = {f_value}\n", 'bold')

            if abs(f_value) < tol or error < tol:
                output_text.insert(tk.END, f"\nRaíz encontrada: {next_guess}\n", 'bold')
                output_text.insert(tk.END, f"Iteraciones totales: {i}\n", 'bold')
                actualizar_grafico(approximations)  # Actualizar gráfico al final
                return next_guess

            current_guess = next_guess

        output_text.insert(tk.END, "El método no converge después del número máximo de iteraciones.\n", 'error')
        return None

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar la función: {e}")
        return None

# Función que será llamada cuando se presione el botón de cálculo
def ejecutar_newton_raphson():
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    funcion = entrada_funcion.get()
    try:
        valor_inicial = float(entrada_inicial.get())
        metodo_seleccionado = metodo_var.get()
        
        if metodo_seleccionado == "Newton-Raphson clásico":
            newton_raphson(funcion, valor_inicial)
        elif metodo_seleccionado == "Newton-Raphson relajado":
            newton_raphson_relajado(funcion, valor_inicial)
        elif metodo_seleccionado == "Newton-Raphson mejorado":
            newton_raphson_mejorado(funcion, valor_inicial)
    except ValueError:
        messagebox.showerror("Error", "El valor inicial debe ser un número válido.")
    output_text.config(state=tk.DISABLED)

# Función para limpiar el área de texto
def limpiar_pantalla():
    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)
    actualizar_grafico([])  # Limpiar gráfica también

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, width, height):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    pos_x = (screen_width // 2) - (width // 2)
    pos_y = (screen_height // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

# Función para actualizar la gráfica
def actualizar_grafico(approximations):
    ax.clear()
    ax.set_title("Aproximaciones de Newton-Raphson")
    ax.set_xlabel("Iteraciones")
    ax.set_ylabel("Valor aproximado")
    ax.plot(approximations, marker='o', color='b')
    canvas.draw()

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Método de Newton-Raphson")
ventana.state('zoomed')
centrar_ventana(ventana, 800, 500)

# Estilos y fuentes
fuente_entradas = font.Font(family="Helvetica", size=12)
fuente_boton = font.Font(family="Helvetica", size=10, weight="bold")
fuente_negrita = font.Font(family="Helvetica", size=12, weight="bold")

# Etiquetas y campos de entrada
tk.Label(ventana, text="Introduce la función f(x):", font=fuente_entradas).grid(row=0, column=0, padx=10, pady=10, sticky="e")
entrada_funcion = tk.Entry(ventana, width=40, font=fuente_entradas)
entrada_funcion.grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Introduce el valor inicial:", font=fuente_entradas).grid(row=1, column=0, padx=10, pady=10, sticky="e")
entrada_inicial = tk.Entry(ventana, width=20, font=fuente_entradas)
entrada_inicial.grid(row=1, column=1, padx=10, pady=10)

# Menú desplegable para seleccionar el método
metodo_var = tk.StringVar(ventana)
metodo_var.set("Newton-Raphson clásico")
metodo_menu = tk.OptionMenu(ventana, metodo_var, "Newton-Raphson clásico", "Newton-Raphson relajado", "Newton-Raphson mejorado")
metodo_menu.config(font=fuente_boton)
metodo_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Botón para ejecutar el método
boton_calcular = tk.Button(ventana, text="Calcular", command=ejecutar_newton_raphson, bg="#4CAF50", fg="white", font=fuente_boton)
boton_calcular.grid(row=2, column=0, padx=10, pady=10, sticky="e")

# Botón para limpiar el área de texto
boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_pantalla, bg="#F44336", fg="white", font=fuente_boton)
boton_limpiar.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Área de texto desplazable para mostrar el resultado
output_text = scrolledtext.ScrolledText(ventana, width=80, height=20, font=fuente_entradas)
output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
output_text.config(state=tk.DISABLED)

# Definir un estilo de fuente negrita y más grande para las iteraciones
output_text.tag_configure("bold", font=fuente_negrita)
output_text.tag_configure("error", foreground="red")

# Crear la figura para la gráfica
fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().grid(row=0, column=2, rowspan=5, padx=10, pady=10)

# Ejecutar la ventana
ventana.mainloop()
