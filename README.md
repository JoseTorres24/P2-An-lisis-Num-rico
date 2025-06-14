# P2-AnalisisNumérico

**P2-AnalisisNumérico** es una aplicación interactiva desarrollada en Python que implementa diferentes variantes del método **Newton-Raphson**. Diseñada para estudiantes y profesionales de métodos numéricos, permite calcular raíces de funciones matemáticas mediante una interfaz gráfica intuitiva.

---

## Características

- **Implementaciones de Newton-Raphson**:
  - **Clásico**: Método estándar.
  - **Relajado**: Con factor de relajación para optimizar la convergencia.
  - **Mejorado**: Considera derivadas de mayor orden.
- **Interfaz Gráfica**:
  - Basada en `Tkinter`.
  - Campos interactivos para ingresar funciones y configuraciones.
- **Visualización de Resultados**:
  - Gráficos dinámicos de las aproximaciones en cada iteración.
- **Notificaciones de Errores**:
  - Mensajes detallados si no se encuentra una solución.

---

## Requisitos

1. **Python 3.x**  
   Descárgalo desde [aquí](https://www.python.org/downloads/).

2. **Librerías Necesarias**  
   Instálalas ejecutando:
   ```bash
   pip install sympy matplotlib
