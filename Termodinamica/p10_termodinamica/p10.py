import pandas as pd
from uncertainties import ufloat, unumpy
import matplotlib.pyplot as plt
import numpy as np
from scipy import odr
import openpyxl
import os
"""
Functions separate_uncertainties
In: unumpy.array
Returns the nominal and the error part as two separate numpy arrays arr
"""
def separate_uncertainties(uarray : unumpy.uarray):
    nominal=unumpy.nominal_values(uarray)
    error=unumpy.std_devs(uarray)
    return (nominal,error)
### Functions for data fitting
def resistance_temperature_relation(params, T):
    """
    Exponential relation between resistance and temperature for ODR.
    Parameters are first, then independent variable.
    
    Parameters:
    params : [A, B]
    T : Temperature (in K).
    """
    A, B = params
    return A * np.exp(B / T)
"""
Fixed parameters for the plot
"""

"""
INTRODUCING DATA
The data for the laboratory practice must be taken into an excel file, and this will read it.
"""
# 1. Obtenemos la ruta absoluta de la carpeta donde está guardado este script .py
base_dir = os.path.dirname(os.path.abspath(__file__))

# Función auxiliar para crear la ruta exacta a cada archivo
def ruta(nombre_archivo):
    return os.path.join(base_dir, nombre_archivo)

#Excel file location
excel_path_user=ruta("p10.xlsx")
workbook = openpyxl.load_workbook(excel_path_user)
sheet = workbook["Sheet1"]  # Acceder a la hoja específica
data_raw=pd.read_excel(excel_path_user,sheet_name="Sheet1")
temperatura = unumpy.uarray(data_raw["Temperatura"],data_raw["u_Temperatura"])
resistencia= unumpy.uarray(data_raw["R"],data_raw["u_R"])
#Input of the first two values of the table, which are the ones we will use for the calculations
temperatura1= ufloat(sheet["H2"].value, sheet["I2"].value)
temperatura2= ufloat(sheet["H3"].value, sheet["I3"].value)
resistencia1=ufloat(sheet["K2"].value, sheet["L2"].value)
resistencia2=ufloat(sheet["K3"].value, sheet["L3"].value)
### The report requieres to represent logR in function of 1/T, so we do it here:
resistencia1_log=unumpy.log(resistencia1)
resistencia2_log=unumpy.log(resistencia2)
inverse_temperature_1=1/temperatura1
inverse_temperature_2=1/temperatura2

"""
Data manipulation
"""
temperatura1_nominal,temperatura1_error= separate_uncertainties(temperatura1)
temperatura2_nominal,temperatura2_error= separate_uncertainties(temperatura2)
resistencia1_nominal,resistencia1_error= separate_uncertainties(resistencia1)
resistencia2_nominal,resistencia2_error= separate_uncertainties(resistencia2)
resistencia1_log_nominal,resistencia1_log_error= separate_uncertainties(resistencia1_log)
resistencia2_log_nominal,resistencia2_log_error= separate_uncertainties(resistencia2_log)
inverse_temperature_1_nominal,inverse_temperature_1_error= separate_uncertainties(inverse_temperature_1)
inverse_temperature_2_nominal,inverse_temperature_2_error= separate_uncertainties(inverse_temperature_2)


### Mean temperature calculation   
"""
PART 1: SYSTEM SOLVING
"""
### Based on sympy analytical solution, which is:  
###  A = R1*exp(log((R1/R2)**t2)/(t1 - t2))
### B = log((R2/R1)**(t1*t2))/(t1 - t2)
### We use uncertainties to propagate the errors in the calculations of A and B, which are the parameters of the exponential function that relates resistance and temperature.

A=resistencia1*unumpy.exp(unumpy.log((resistencia1/resistencia2)**temperatura2)/(temperatura1- temperatura2))
B=unumpy.log((resistencia2/resistencia1)**(temperatura1*temperatura2/(temperatura1- temperatura2)))
print(f"A = {A}"
      f"\nB = {B}")
a_nominal,a_error=separate_uncertainties(A)
b_nominal,b_error=separate_uncertainties(B)
print(f"A = {a_nominal} ± {a_error}"
      f"\nB = {b_nominal} ± {b_error}")

""""
Plotting
"""
### We plot logR vs 1/T should be somewhat of a straight line, I decided to do it on the same graph
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(inverse_temperature_1_nominal, resistencia1_log_nominal, yerr=resistencia1_log_error, xerr=inverse_temperature_1_error, fmt='none', color="black",
              label="Resistencia 1", capsize=3, markersize=4)
plt.errorbar(inverse_temperature_2_nominal, resistencia2_log_nominal, yerr=resistencia2_log_error, xerr=inverse_temperature_2_error, fmt='none', color="gray",
              label="Resistencia 2", capsize=3, markersize=4)

plt.xlabel('1/T $K^{-1}$', fontsize=12)
plt.ylabel('log(R)', fontsize=12)
#Some options:
plt.title('Temperatura vs tiempo', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()
"""
3.Fitting the data
"""
# Initial guess for the parameters for temperature fitting
initial_guess_temperature = [a_nominal, b_nominal]
# Create ODR model and fit, considering errors in both variables
model = odr.Model(resistance_temperature_relation)
data = odr.RealData(temperatura1_nominal, resistencia1_nominal, sx=temperatura1_error, sy=resistencia1_error)
odr_fit = odr.ODR(data, model, beta0=initial_guess_temperature)
odr_result = odr_fit.run()
# Extract the fitted parameters and their errors
A_fit_temperature, B_fit_temperature = odr_result.beta
A_err_temperature, B_err_temperature = odr_result.sd_beta
A_fit_temperature_ufloat = ufloat(A_fit_temperature, A_err_temperature)
B_fit_temperature_ufloat = ufloat(B_fit_temperature, B_err_temperature)
print(f"\nFitted parameters for temperature-resistance relation:")
print(f"A = {A_fit_temperature} ± {A_err_temperature}")
print(f"B = {B_fit_temperature} ± {B_err_temperature}") 

"""
Spanish:  Temperatura agua del grifo
En esta parte se pide calcular la temperatura del agua del grifo a partir de la resistencia medida, utilizando los parámetros A y B obtenidos en el ajuste. Sin embargo, no se especifica claramente cuál resistencia corresponde al agua del grifo, por lo que se realizará el cálculo para ambas resistencias y se compararán los resultados.
"""
### Aqui no entiendo del todo lo que pide la practica, entiendo que es el procedimiento inverso, que con los parametros A y B obtenidos, se calcula la temperatura del agua del grifo a partir de la resistencia medida, pero no se especifica cual resistencia es la del agua del grifo, asi que lo hare con ambas resistencias y luego comparo los resultados.
### Calculating the temperature of the tap water using the fitted parameters and the measured resistance   
A_mean=(A_fit_temperature_ufloat+A)/2
B_mean=(b_fit_temperature_ufloat+B)/2

###Calculate the errors in the fitted parameters
A_mean_error_total=np.sqrt(A_err_temperature**2 + a_error**2)
B_mean_error_total=np.sqrt(b_err_temperature**2 + b_error**2)

temperatura_grifo_1 = A_mean * np.exp(B_mean/ resistencia1)
temperatura_grifo_2 = A_mean * np.exp(B_mean / resistencia2)
print(f"\nTemperatura del agua del grifo calculada a partir de resistencia 1: {temperatura_grifo_1} K")
print(f"Temperatura del agua del grifo calculada a partir de resistencia 2: {temperatura_grifo_2} K")

