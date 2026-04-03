"""
Plantilla para resolver sistemas de ecuaciones no lineales usando SymPy
Incluye ejemplos y métodos diferentes para solucionar sistemas complejos
"""

from sympy import symbols, solve, Eq, nsolve, simplify
from sympy import exp, sin, cos, log, sqrt, pi
import numpy as np
from sympy.utilities.lambdify import lambdify

# COLORES ANSI
class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_header(text):
    """Imprime un encabezado bonito"""
    print(f"\n{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{text.center(70)}{Color.END}")
    print(f"{Color.BOLD}{Color.CYAN}{'='*70}{Color.END}\n")

def print_section(text):
    """Imprime una sección"""
    print(f"{Color.BOLD}{Color.BLUE}┌─ {text}{Color.END}")
    
def print_item(label, value, indent=2):
    """Imprime un item"""
    spaces = " "*indent
    print(f"{spaces}{Color.GREEN}• {label}:{Color.END} {value}")

def print_equation(num, eq):
    """Imprime una ecuación formateada"""
    print(f"{Color.YELLOW}  eq{num}: {eq}{Color.END}")

def print_solution(i, sol_dict):
    """Imprime una solución formateada"""
    print(f"\n{Color.BOLD}{Color.GREEN}  ✓ Solución {i}:{Color.END}")
    for var, val in sol_dict.items():
        print(f"{Color.GREEN}    {var} = {val}{Color.END}")

# =============================================================================
# MÉTODO 1: Resolución simbólica exacta
# =============================================================================

def resolver_sistema_simbolico():
    """
    Resuelve un sistema no lineal de forma simbólica (exacta)
    Funciona mejor para sistemas pequeños o con soluciones simples
    """
    print_header("RESOLUCIÓN SIMBÓLICA EXACTA")
    
    # Definir variables simbólicas
    A, B, R1, R2, t1, t2 = symbols('A B R1 R2 t1 t2', real=True, positive=True)
    
    # Definir ecuaciones: A*exp(B/t1) = R1   y   A*exp(B/t2) = R2
    eq1 = Eq(A*exp(B/t1), R1)
    eq2 = Eq(A*exp(B/t2), R2)
    
    print_section("ECUACIONES DEL SISTEMA")
    print_equation(1, eq1)
    print_equation(2, eq2)
    
    print_section("INFORMACIÓN")
    print_item("Variables a despejar", "A, B", indent=2)
    print_item("Parámetros conocidos", "R1, R2, t1, t2", indent=2)

    print(f"\n{Color.YELLOW}→ Resolviendo sistema...{Color.END}\n")
    
    # Resolver sistema
    soluciones = solve([eq1, eq2], [A, B])
    
    print_section(f"RESULTADOS ({len(soluciones)} solución{'es' if len(soluciones) != 1 else ''})")
    
    for i, sol in enumerate(soluciones, 1):
        sol_dict = {A: simplify(sol[0]), B: simplify(sol[1])}
        print_solution(i, sol_dict)
        
        # Intentar mostrar forma numérica si es posible
        try:
            A_val = float(sol[0])
            B_val = float(sol[1])
            print(f"{Color.CYAN}    (Numérica: A ≈ {A_val:.10f}, B ≈ {B_val:.10f}){Color.END}")
        except:
            print(f"{Color.CYAN}    (Requiere valores específicos de R1, R2, t1, t2){Color.END}")
    
    # Mostrar con valores de ejemplo
    print_section("EVALUACIÓN CON EJEMPLO")
    print_item("Valores de prueba", "R1=100, R2=200, t1=1, t2=2", indent=2)
    
    for i, sol in enumerate(soluciones, 1):
        try:
            A_ejemplo = sol[0].subs({R1: 100, R2: 200, t1: 1, t2: 2})
            B_ejemplo = sol[1].subs({R1: 100, R2: 200, t1: 1, t2: 2})
            A_val = float(A_ejemplo)
            B_val = float(B_ejemplo)
            
            print(f"\n{Color.BOLD}{Color.GREEN}  Solución {i}:{Color.END}")
            print(f"    A = {Color.CYAN}{A_val:.10f}{Color.END}")
            print(f"    B = {Color.CYAN}{B_val:.10f}{Color.END}")
            break
        except:
            pass
    
    return soluciones


if __name__ == "__main__":
    print(f"\n{Color.BOLD}{Color.HEADER}{'█'*70}{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'█ RESOLVER SISTEMAS NO LINEALES CON SYMPY'.ljust(69)}█{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'█'*70}{Color.END}")
    
    # Ejecutar la resolución
    soluciones = resolver_sistema_simbolico()
    
    print(f"\n{Color.BOLD}{Color.GREEN}✓ Proceso completado exitosamente{Color.END}")
    print(f"{Color.BOLD}{Color.HEADER}{'█'*70}{Color.END}\n")