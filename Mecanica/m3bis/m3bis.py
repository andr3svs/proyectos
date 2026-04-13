import pandas as pd
import uncertainties
import matplotlib.pyplot as plt
import matplotlib as mpl
from uncertainties import unumpy
import numpy as np
from scipy.optimize import curve_fit
from scipy import odr
import os
from pathlib import Path
"""
Functions separate_uncertainties
In: unumpy.array
Returns the nominal and the error part as two separate numpy arrays arr
"""
def separate_uncertainties(uarray : unumpy.uarray):
    nominal=unumpy.nominal_values(uarray)
    error=unumpy.std_devs(uarray)
    return (nominal,error)
def sinusoidal_curve_simple(F,A,w,t):
    return A*np.sin(w*t)

def curve_fit_sinusoidal_with_uncertainties(force_uarray, time_uarray, p0=[1, 1]):
    """
    Ajusta una función sinusoidal a los datos considerando incertidumbres en ambas variables.
    
    Parámetros:
    -----------
    force_uarray : unumpy.uarray
        Array de fuerzas con incertidumbre
    time_uarray : unumpy.uarray
        Array de tiempos con incertidumbre
    p0 : list
        Parámetros iniciales [A, w]
    
    Retorna:
    --------
    popt_uarray : unumpy.uarray
        Parámetros ajustados con incertidumbre [A, w]
    """
    # Separar nominales y errores
    time_nominal, time_error = separate_uncertainties(time_uarray)
    force_nominal, force_error = separate_uncertainties(force_uarray)
    
    # Usar scipy.odr para ajuste considerando errores en ambas variables
    def odr_sin(params, x):
        A, w = params
        return A * np.sin(w * x)
    
    # Crear objeto RealData con errores en ambas variables
    data = odr.RealData(time_nominal, force_nominal, sx=time_error, sy=force_error)
    
    # Crear el modelo ODR
    model = odr.Model(odr_sin)
    
    # Ejecutar el ajuste
    myodr = odr.ODR(data, model, beta0=p0)
    out = myodr.run()
    
    # Extraer parámetros ajustados e incertidumbres
    popt = out.beta
    popt_error = out.sd_beta
    
    # Crear array con incertidumbre
    popt_uarray = unumpy.uarray(popt, popt_error)
    
    return popt_uarray

def print_fit_results(part_number, popt_uarray):
    """
    Imprime los resultados del ajuste con 6 decimales.
    
    Parámetros:
    -----------
    part_number : int
        Número de la parte
    popt_uarray : unumpy.uarray
        Parámetros ajustados con incertidumbre
    """
    print(f"\n=== PARTE {part_number} ===")
    print(f"Amplitud A = {popt_uarray[0]:.6u}")
    print(f"Frecuencia angular ω = {popt_uarray[1]:.6u} rad/s")

def curve_fit_double_sinusoidal_with_uncertainties(force_uarray, time_uarray, w1_init, w2_init):
    """
    Ajusta una función de dos sinusoides con offset a los datos considerando incertidumbres.
    Función: A*sin(w1*t + phi1) + b*sin(w2*t + phi2) + offset
    
    Parámetros:
    -----------
    force_uarray : unumpy.uarray
        Array de fuerzas con incertidumbre
    time_uarray : unumpy.uarray
        Array de tiempos con incertidumbre
    w1_init : float
        Valor inicial para frecuencia angular 1 (generalmente de la parte 2)
    w2_init : float
        Valor inicial para frecuencia angular 2 (generalmente de la parte 3)
    
    Retorna:
    --------
    popt_uarray : unumpy.uarray
        Parámetros ajustados con incertidumbre [A, w1, phi1, b, w2, phi2, offset]
    """
    # Separar nominales y errores
    time_nominal, time_error = separate_uncertainties(time_uarray)
    force_nominal, force_error = separate_uncertainties(force_uarray)
    
    # Definir función modelo para ODR
    def odr_double_sin(params, x):
        A, w1, phi1, b, w2, phi2, offset = params
        return A * np.sin(w1 * x + phi1) + b * np.sin(w2 * x + phi2) + offset
    
    # Valores iniciales: [A, w1, phi1, b, w2, phi2, offset]
    p0 = [1, w1_init, 0, 1, w2_init, 0, 0]
    
    # Crear objeto RealData con errores en ambas variables
    data = odr.RealData(time_nominal, force_nominal, sx=time_error, sy=force_error)
    
    # Crear el modelo ODR
    model = odr.Model(odr_double_sin)
    
    # Ejecutar el ajuste
    myodr = odr.ODR(data, model, beta0=p0)
    out = myodr.run()
    
    # Extraer parámetros ajustados e incertidumbres
    popt = out.beta
    popt_error = out.sd_beta
    
    # Crear array con incertidumbre
    popt_uarray = unumpy.uarray(popt, popt_error)
    
    return popt_uarray

def print_double_fit_results(part_number, popt_uarray):
    """
    Imprime los resultados del ajuste doble sinusoidal con 6 decimales.
    
    Parámetros:
    -----------
    part_number : int
        Número de la parte
    popt_uarray : unumpy.uarray
        Parámetros ajustados con incertidumbre [A, w1, phi1, b, w2, phi2, offset]
    """
    print(f"\n=== PARTE {part_number} (Doble Sinusoide) ===")
    print(f"Amplitud A = {popt_uarray[0]:.6u}")
    print(f"Frecuencia angular ω1 = {popt_uarray[1]:.6u} rad/s")
    print(f"Desfase φ1 = {popt_uarray[2]:.6u} rad")
    print(f"Amplitud b = {popt_uarray[3]:.6u}")
    print(f"Frecuencia angular ω2 = {popt_uarray[4]:.6u} rad/s")
    print(f"Desfase φ2 = {popt_uarray[5]:.6u} rad")
    print(f"Offset = {popt_uarray[6]:.6u}")

def print_fit_results_labeled(label, popt_uarray):
    """
    Imprime los resultados del ajuste con etiqueta personalizada y 6 decimales.
    
    Parámetros:
    -----------
    label : str
        Etiqueta descriptiva (ej: "Parte 2 - Fuerza Izquierda")
    popt_uarray : unumpy.uarray
        Parámetros ajustados con incertidumbre
    """
    print(f"\n=== {label} ===")
    print(f"Amplitud A = {popt_uarray[0]:.6u}")
    print(f"Frecuencia angular ω = {popt_uarray[1]:.6u} rad/s")

def calculate_average_with_uncertainty(values, label):
    """
    Calcula el promedio de múltiples valores con incertidumbre usando uncertainties.
    
    Parámetros:
    -----------
    values : list of unumpy values
        Lista de valores con incertidumbre
    label : str
        Etiqueta para imprimir resultado
    
    Retorna:
    --------
    promedio : ufloat
        Promedio con incertidumbre propagada
    """
    # Usar uncertainties para calcular el promedio
    promedio = sum(values) / len(values)
    print(f"\n=== {label} ===")
    print(f"Promedio = {promedio:.6u}")
    return promedio

data_path_raw_1=Path(__file__).parent / "Fuerzaizda1.txt"
data_user_part_1=pd.read_csv(data_path_raw_1,sep=" ",header=0)
#data_path_raw_2=Path(__file__).parent / "Fuerzader1.txt"
#data_user_part_2=pd.read_csv(data_path_raw_2,sep=" ",header=0)
#data_path_raw_3=Path(__file__).parent / "Fuerzaizda2.txt"
#data_user_part_3=pd.read_csv(data_path_raw_3,sep=" ",header=0)
#data_path_raw_4=Path(__file__).parent / "Fuerzader2.txt"
#data_user_part_4=pd.read_csv(data_path_raw_4,sep=" ",header=0)

# PARTE 1: Fuerza única (sin distinción izquierda/derecha)
force_wunc_1 = unumpy.uarray(data_user_part_1[F],np.std(data_user_part_1[data_user_part_1[F]]))
time_wunc_1 = unumpy.uarray(data_user_part_1[T],0.001)

## PARTE 2: Fuerza izquierda y derecha
#force_wunc_2_izq = unumpy.uarray(data_user_part_2[F_izq],np.std(data_user_part_2[data_user_part_2[F_izq]]))
#force_wunc_2_der = unumpy.uarray(data_user_part_2[F_der],np.std(data_user_part_2[data_user_part_2[F_der]]))
#time_wunc_2 = unumpy.uarray(data_user_part_2[T],0.001)

## PARTE 3: Fuerza izquierda y derecha
#force_wunc_3_izq = unumpy.uarray(data_user_part_3[F_izq],np.std(data_user_part_3[data_user_part_3[F_izq]]))
#force_wunc_3_der = unumpy.uarray(data_user_part_3[F_der],np.std(data_user_part_3[data_user_part_3[F_der]]))
#time_wunc_3 = unumpy.uarray(data_user_part_3[T],0.001)

## PARTE 4: Fuerza izquierda y derecha
#force_wunc_4_izq = unumpy.uarray(data_user_part_4[F_izq],np.std(data_user_part_4[data_user_part_4[F_izq]]))
#force_wunc_4_der = unumpy.uarray(data_user_part_4[F_der],np.std(data_user_part_4[data_user_part_4[F_der]]))
#time_wunc_4 = unumpy.uarray(data_user_part_4[T],0.001)

#mass_rod=3.3

##Calculations
#w_0=unumpy.sqrt(3*k_w_unc/mass_rod)

## CURVE FIT SINUSOIDAL CON INCERTIDUMBRES
## PARTE 1: Ajuste único
popt_1 = curve_fit_sinusoidal_with_uncertainties(force_wunc_1, time_wunc_1, p0=[1, 1])
print_fit_results(1, popt_1)

## PARTE 2: Ajustes separados para izquierda y derecha
#popt_2_izq = curve_fit_sinusoidal_with_uncertainties(force_wunc_2_izq, time_wunc_2, p0=[1, 1])
#popt_2_der = curve_fit_sinusoidal_with_uncertainties(force_wunc_2_der, time_wunc_2, p0=[1, 1])
#print_fit_results_labeled("Parte 2 - Fuerza Izquierda", popt_2_izq)
#print_fit_results_labeled("Parte 2 - Fuerza Derecha", popt_2_der)

## Calcular promedio de frecuencias para parte 2
#w_2 = calculate_average_with_uncertainty([popt_2_izq[1], popt_2_der[1]], "Parte 2 - ω Promedio")

## PARTE 3: Ajustes separados para izquierda y derecha
#popt_3_izq = curve_fit_sinusoidal_with_uncertainties(force_wunc_3_izq, time_wunc_3, p0=[1, 1])
#popt_3_der = curve_fit_sinusoidal_with_uncertainties(force_wunc_3_der, time_wunc_3, p0=[1, 1])
#print_fit_results_labeled("Parte 3 - Fuerza Izquierda", popt_3_izq)
#print_fit_results_labeled("Parte 3 - Fuerza Derecha", popt_3_der)

## Calcular promedio de frecuencias para parte 3
#w_3 = calculate_average_with_uncertainty([popt_3_izq[1], popt_3_der[1]], "Parte 3 - ω Promedio")

## PARTE 4: Ajustes separados para izquierda y derecha (doble sinusoide)
## Usar las frecuencias promediadas de las partes 2 y 3 como valores iniciales
#w2_init_nominal = unumpy.nominal_values(w_2)
#w3_init_nominal = unumpy.nominal_values(w_3)

#popt_4_izq = curve_fit_double_sinusoidal_with_uncertainties(force_wunc_4_izq, time_wunc_4, w2_init_nominal, w3_init_nominal)
#popt_4_der = curve_fit_double_sinusoidal_with_uncertainties(force_wunc_4_der, time_wunc_4, w2_init_nominal, w3_init_nominal)

#print(f"\n=== Parte 4 - Fuerza Izquierda (Doble Sinusoide) ===")
#print(f"Amplitud A = {popt_4_izq[0]:.6u}")
#print(f"Frecuencia angular ω1 = {popt_4_izq[1]:.6u} rad/s")
#print(f"Desfase φ1 = {popt_4_izq[2]:.6u} rad")
#print(f"Amplitud b = {popt_4_izq[3]:.6u}")
#print(f"Frecuencia angular ω2 = {popt_4_izq[4]:.6u} rad/s")
#print(f"Desfase φ2 = {popt_4_izq[5]:.6u} rad")
#print(f"Offset = {popt_4_izq[6]:.6u}")

#print(f"\n=== Parte 4 - Fuerza Derecha (Doble Sinusoide) ===")
#print(f"Amplitud A = {popt_4_der[0]:.6u}")
#print(f"Frecuencia angular ω1 = {popt_4_der[1]:.6u} rad/s")
#print(f"Desfase φ1 = {popt_4_der[2]:.6u} rad")
#print(f"Amplitud b = {popt_4_der[3]:.6u}")
#print(f"Frecuencia angular ω2 = {popt_4_der[4]:.6u} rad/s")
#print(f"Desfase φ2 = {popt_4_der[5]:.6u} rad")
#print(f"Offset = {popt_4_der[6]:.6u}")

## Calcular w_a y w_s usando promedio con propagación de incertidumbre
## w_a: frecuencia antisimétrica (promedio de ω1 de ambos lados)
## w_s: frecuencia simétrica (promedio de ω2 de ambos lados)
#w_a = calculate_average_with_uncertainty([popt_4_izq[1], popt_4_der[1]], "Parte 4 - ωa (Frecuencia Antisimétrica - ω1)")
#w_s = calculate_average_with_uncertainty([popt_4_izq[4], popt_4_der[4]], "Parte 4 - ωs (Frecuencia Simétrica - ω2)")

##Como primer metodo que pide la practica calculo la serie de fourier
#frecuencias_1_fourier=np.fft.fftfreq(len(force_wunc_1), time_wunc_1[1] - time_wunc_1[0])
#frecuencias_2_fourier_izq=np.fft.fftfreq(len(force_wunc_2_izq), time_wunc_2[1] - time_wunc_2[0])
#frecuencias_2_fourier_der=np.fft.fftfreq(len(force_wunc_2_der), time_wunc_2[1] - time_wunc_2[0])
#frecuencias_3_fourier_izq=np.fft.fftfreq(len(force_wunc_3_izq), time_wunc_3[1] - time_wunc_3[0])
#frecuencias_3_fourier_der=np.fft.fftfreq(len(force_wunc_3_der), time_wunc_3[1] - time_wunc_3[0])
#frecuencias_4_fourier_izq=np.fft.fftfreq(len(force_wunc_4_izq), time_wunc_4[1] - time_wunc_4[0])
#frecuencias_4_fourier_der=np.fft.fftfreq(len(force_wunc_4_der), time_wunc_4[1] - time_wunc_4[0])

#"""
#Plotting
#"""


#plt.xlabel('h1 co2 (cm)', fontsize=12)
#plt.ylabel('Coeficiente adiabático', fontsize=12)
##Some options:
#plt.title('Coeficiente adiabático experimental vs h1 co2', fontsize=14)
#plt.legend()
#plt.grid(False)
##Do the plot
#plt.show()


print("Proceso finalizado.")
