import sympy as sp
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application, convert_xor)

def newton_raphson(func_expr, initial_guess, tol=1e-6, max_iter=100):
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

        # Mostrar la función y su derivada
        print(f"Función: {f}")
        print(f"Derivada: {f_prime}")
        
        # Convertir las funciones simbólicas en funciones evaluables numéricamente
        f_lambdified = sp.lambdify(x, f)
        f_prime_lambdified = sp.lambdify(x, f_prime)

        # Iteración inicial
        current_guess = initial_guess
        for i in range(max_iter):
            # Evaluar la función y su derivada en el valor actual
            f_value = f_lambdified(current_guess)
            f_prime_value = f_prime_lambdified(current_guess)

            # Evitar división por cero en caso de que la derivada sea 0
            if f_prime_value == 0:
                print("Derivada es cero. El método no puede continuar.")
                return None

            # Calcular la próxima aproximación
            next_guess = current_guess - f_value / f_prime_value

            # Comprobar la tolerancia (criterio de convergencia)
            if abs(next_guess - current_guess) < tol:
                print(f"Raíz encontrada: {next_guess} después de {i+1} iteraciones.")
                return next_guess

            # Actualizar el valor de la aproximación
            current_guess = next_guess

        # Si el número máximo de iteraciones se alcanza sin convergencia
        print("El método no converge después del número máximo de iteraciones.")
        return None

    except Exception as e:
        print(f"Error al procesar la función: {e}")
        return None

# Ejemplo de uso con funciones trigonométricas, logarítmicas o exponenciales
funcion = input("Introduce la función f(x) (usa sin, cos, exp, log, etc.): ")
initial_guess = float(input("Introduce el valor inicial para la aproximación: "))
newton_raphson(funcion, initial_guess)
