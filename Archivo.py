import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application, convert_xor)
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import font

# Función del método de Newton-Raphson con criterios de convergencia mejorados
def newton_raphson(func_expr, initial_guess, tol=1e-12, max_iter=1000):
    try:
        # Definir la variable simbólica
        x = sp.symbols('x')
        
        # Habilitar transformaciones para multiplicación implícita y ^ como operador de potencia
        transformations = (standard_transformations + (implicit_multiplication_application, convert_xor,))
        
        # Definir la constante e (número de Euler)
        local_dict = {'e': sp.E}
        
        # Convertir la expresión ingresada a una función simbólica, con multiplicación implícita y ^ como potencia
        f = parse_expr(func_expr, transformations=transformations, local_dict=local_dict)
        f_prime = sp.diff(f, x)  # Derivada de la función
        
        # Convertir las funciones simbólicas en funciones evaluables numéricamente
        f_lambdified = sp.lambdify(x, f)
        f_prime_lambdified = sp.lambdify(x, f_prime)
        
        # Iteración inicial
        current_guess = initial_guess
        
        # Mostrar la función y la derivada con formato en negritas y tamaño grande
        output_text.insert(tk.END, f"Función: {f}\n", 'bold')
        output_text.insert(tk.END, f"Derivada: {f_prime}\n", 'bold')
        
        for i in range(1, max_iter+1):  # Iteraciones desde 1 hasta max_iter
            # Evaluar la función y su derivada en el valor actual
            f_value = f_lambdified(current_guess)
            f_prime_value = f_prime_lambdified(current_guess)

            # Evitar división por cero o derivadas muy pequeñas
            if abs(f_prime_value) < 1e-14:
                output_text.insert(tk.END, f"Derivada es muy pequeña en x = {current_guess}. El método no puede continuar.\n", 'error')
                return None

            # Calcular la próxima aproximación
            next_guess = current_guess - f_value / f_prime_value

            # Calcular el error aproximado
            error = abs(next_guess - current_guess)

            # Mostrar el estado actual de la iteración
            output_text.insert(tk.END, f"Iteración {i}: Valor aproximado = {next_guess}, Error aproximado = {error}, f(x) = {f_value}\n", 'bold')

            # Criterio de convergencia basado en el valor de la función y el cambio en el valor de x
            if abs(f_value) < tol:
                output_text.insert(tk.END, f"\nRaíz encontrada: {next_guess}\n", 'bold')
                output_text.insert(tk.END, f"f(x) ≈ 0 (con tolerancia {tol})\n", 'bold')
                output_text.insert(tk.END, f"Iteraciones totales: {i}\n", 'bold')
                return next_guess

            if error < tol:
                output_text.insert(tk.END, f"\nRaíz encontrada: {next_guess}\n", 'bold')
                output_text.insert(tk.END, f"Error aproximado: {error}\n", 'bold')
                output_text.insert(tk.END, f"Iteraciones totales: {i}\n", 'bold')
                return next_guess

            # Actualizar el valor de la aproximación
            current_guess = next_guess

        # Si el número máximo de iteraciones se alcanza sin convergencia
        output_text.insert(tk.END, "El método no converge después del número máximo de iteraciones.\n", 'error')
        return None

    except Exception as e:
        messagebox.showerror("Error", f"Error al procesar la función: {e}")
        return None

# Función que será llamada cuando se presione el botón de cálculo
def ejecutar_newton_raphson():
    output_text.config(state=tk.NORMAL)  # Habilitar el área de texto temporalmente para escribir los resultados
    output_text.delete(1.0, tk.END)  # Limpiar el área de salida antes de mostrar resultados
    funcion = entrada_funcion.get()  # Obtener la función de la entrada
    try:
        valor_inicial = float(entrada_inicial.get())  # Obtener el valor inicial de la entrada
        newton_raphson(funcion, valor_inicial)  # Ejecutar el método de Newton-Raphson
    except ValueError:
        messagebox.showerror("Error", "El valor inicial debe ser un número válido.")
    output_text.config(state=tk.DISABLED)  # Deshabilitar el área de texto para que no sea editable

# Función para limpiar el área de texto
def limpiar_pantalla():
    output_text.config(state=tk.NORMAL)  # Habilitar el área de texto temporalmente para poder limpiarla
    output_text.delete(1.0, tk.END)
    output_text.config(state=tk.DISABLED)  # Deshabilitar de nuevo el área de texto para que no sea editable

# Función para centrar la ventana en la pantalla
def centrar_ventana(ventana, width, height):
    screen_width = ventana.winfo_screenwidth()
    screen_height = ventana.winfo_screenheight()
    pos_x = (screen_width // 2) - (width // 2)
    pos_y = (screen_height // 2) - (height // 2)
    ventana.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Método de Newton-Raphson")
ventana.state('zoomed')  # Ajustar la ventana para que ocupe toda la pantalla
centrar_ventana(ventana, 800, 500)  # Centrar la ventana en la pantalla (tamaño por defecto)

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

# Botón para ejecutar el método
boton_calcular = tk.Button(ventana, text="Calcular", command=ejecutar_newton_raphson, bg="#4CAF50", fg="white", font=fuente_boton)
boton_calcular.grid(row=2, column=0, padx=10, pady=10, sticky="e")

# Botón para limpiar el área de texto
boton_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_pantalla, bg="#F44336", fg="white", font=fuente_boton)
boton_limpiar.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Área de texto desplazable para mostrar el resultado
output_text = scrolledtext.ScrolledText(ventana, width=80, height=20, font=fuente_entradas)
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
output_text.config(state=tk.DISABLED)  # Deshabilitar el área de texto para que no sea editable

# Definir un estilo de fuente negrita y más grande para las iteraciones
output_text.tag_configure("bold", font=fuente_negrita)
output_text.tag_configure("error", foreground="red")

# Ejecutar la ventana
ventana.mainloop()
