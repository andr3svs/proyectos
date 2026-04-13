import pandas as pd
import uncertainties
import matplotlib.pyplot as plt
import matplotlib as mpl
from uncertainties import unumpy
import numpy as np
from scipy.optimize import curve_fit
from scipy import odr
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
data_path_raw_1=""
data_user_part_1=pd.read_csv(data_path_raw_1,sep=" ",header=)
data_path_raw_2=""
data_user_part_2=pd.read_csv(data_path_raw_2,sep=" ",header=)
data_path_raw_3=""
data_user_part_3=pd.read_csv(data_path_raw_3,sep=" ",header=)
data_path_raw_4=""
data_user_part_4=pd.read_csv(data_path_raw_4,sep=" ",header=)
force_wunc_1 = unumpy.uarray(data_user_part_1[F],np.std(data_user_part_1[data_user_part_1[F]]))
time_wunc_1 = unumpy.uarray(data_user_part_1[T],0.001)
force_wunc_1=unumpy.uarray(data_user_part_1[F],np.std(data_user_part_1[data_user_part_1[F]]))
time_wunc_1=unumpy.uarray(data_user_part_1[T],0.001)
force_wunc_2 = unumpy.uarray(data_user_part_2[F],np.std(data_user_part_2[data_user_part_2[F]]))
time_wunc_2 = unumpy.uarray(data_user_part_2[T],0.001)
force_wunc_3 = unumpy.uarray(data_user_part_3[F],np.std(data_user_part_3[data_user_part_3[F]]))
time_wunc_3 = unumpy.uarray(data_user_part_3[T],0.001)
force_wunc_4 = unumpy.uarray(data_user_part_4[F],np.std(data_user_part_4[data_user_part_4[F]]))
time_wunc_4 = unumpy.uarray(data_user_part_4[T],0.001)
mass_rod=3.3

#Calculations
w_0=unumpy.sqrt(3*k_w_unc/mass_rod)

# CURVE FIT SINUSOIDAL CON INCERTIDUMBRES
# Ajustar la función sinusoidal para cada parte (1-3)
popt_1 = curve_fit_sinusoidal_with_uncertainties(force_wunc_1, time_wunc_1, p0=[1, 1])
popt_2 = curve_fit_sinusoidal_with_uncertainties(force_wunc_2, time_wunc_2, p0=[1, 1])
popt_3 = curve_fit_sinusoidal_with_uncertainties(force_wunc_3, time_wunc_3, p0=[1, 1])

# AJUSTE DOBLE SINUSOIDAL PARA PARTE 4
# Usar las frecuencias de las partes 2 y 3 como valores iniciales
w1_init = unumpy.nominal_values(popt_2)[1]
w2_init = unumpy.nominal_values(popt_3)[1]
popt_4 = curve_fit_double_sinusoidal_with_uncertainties(force_wunc_4, time_wunc_4, w1_init, w2_init)

# Imprimir resultados
print_fit_results(1, popt_1)
print_fit_results(2, popt_2)
print_fit_results(3, popt_3)
print_double_fit_results(4, popt_4)

#Como primer metodo que pide la practica calculo la serie de fourier
frecuencias_1_fourier=np.fft.fftfreq(len(force_wunc_1), time_wunc_1[1] - time_wunc_1[0])
frecuencias_2_fourier=np.fft.fftfreq(len(force_wunc_2), time_wunc_2[1] - time_wunc_2[0])
frecuencias_3_fourier=np.fft.fftfreq(len(force_wunc_3), time_wunc_3[1] - time_wunc_3[0])
frecuencias_4_fourier=np.fft.fftfreq(len(force_wunc_4), time_wunc_4[1] - time_wunc_4[0])

"""
Plotting
"""


plt.xlabel('h1 co2 (cm)', fontsize=12)
plt.ylabel('Coeficiente adiabático', fontsize=12)
#Some options:
plt.title('Coeficiente adiabático experimental vs h1 co2', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()


print("Proceso finalizado.")
