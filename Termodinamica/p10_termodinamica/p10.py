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
temperatura2= ufloat(273.25,0.1)
temperatura1 = ufloat(353.15,0.1)
resistencia2=ufloat(31.5,0.578)
resistencia1=ufloat(1.253,0.215036)

### The report requieres to represent logR in function of 1/T, so we do it here:
resistencia1_log=unumpy.log(resistencia1)
resistencia2_log=unumpy.log(resistencia2)
inverse_temperature=1/temperatura
resistencia_log=unumpy.log(resistencia)
"""
Data manipulation
"""
temperatura1_nominal,temperatura1_error= separate_uncertainties(temperatura1)
temperatura2_nominal,temperatura2_error= separate_uncertainties(temperatura2)
resistencia1_nominal,resistencia1_error= separate_uncertainties(resistencia1)
resistencia2_nominal,resistencia2_error= separate_uncertainties(resistencia2)
temperatura_nominal, temperatura_error = separate_uncertainties(temperatura)
resistencia_nominal, resistencia_error = separate_uncertainties(resistencia)
inverse_temperature_nominal, inverse_temperature_error = separate_uncertainties(1/temperatura)
resistencia_log_nominal, resistencia_log_error = separate_uncertainties(unumpy.log(resistencia))

### Mean temperature calculation   
"""
PART 1: SYSTEM SOLVING
"""
### Based on analytical solution from R(T) = A*exp(B/T):
### From two data points (T1,R1) and (T2,R2):
### B = ln(R1/R2) * (T1*T2)/(T2 - T1)
### A = R1 / exp(B/T1)
### We use uncertainties to propagate the errors in the calculations of A and B.

B = unumpy.log(resistencia1/resistencia2) * (temperatura1*temperatura2)/(temperatura2 - temperatura1)
A = resistencia1 / unumpy.exp(B/temperatura1)
a_nominal,a_error=separate_uncertainties(A)
b_nominal,b_error=separate_uncertainties(B)
print("Parameters calculated from the two data points:")
print(f"A = {a_nominal} ± {a_error}"
      f"\nB = {b_nominal} ± {b_error}")

""""
Plotting
"""
### We plot logR vs 1/T should be somewhat of a straight line, I decided to do it on the same graph
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(inverse_temperature_nominal, resistencia_log_nominal, yerr=resistencia_log_error, xerr=inverse_temperature_error, fmt='--', color="black",
              label="Resistencia ", capsize=3, markersize=4)
plt.xlabel('1/T $K^{-1}$', fontsize=12)
plt.ylabel('log(R)', fontsize=12)
#Some options:
plt.title('log(R) vs 1/T', fontsize=14)
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
data = odr.RealData(temperatura_nominal, resistencia_nominal, sx=temperatura_error, sy=resistencia_error)
odr_fit = odr.ODR(data, model, beta0=initial_guess_temperature)
odr_result = odr_fit.run()
# Extract the fitted parameters and their errors
A_fit_temperature, B_fit_temperature = odr_result.beta
A_err_temperature, B_err_temperature = odr_result.sd_beta
A_fit_temperature_ufloat = ufloat(A_fit_temperature, A_err_temperature)
B_fit_temperature_ufloat = ufloat(B_fit_temperature, B_err_temperature)
# Calculate R² for the fit
y_pred = resistance_temperature_relation(odr_result.beta, temperatura_nominal)
ss_residual = np.sum((resistencia_nominal - y_pred)**2)
ss_total = np.sum((resistencia_nominal - np.mean(resistencia_nominal))**2)
r_squared = 1 - (ss_residual / ss_total)
print(f"\nFitted parameters for temperature-resistance relation:")
print(f"A = {A_fit_temperature} ± {A_err_temperature}")
print(f"B = {B_fit_temperature} ± {B_err_temperature}")
print(f"R² = {r_squared:.6f}") 

"""
4. Calculo temperatura vaso agua
"""
resistencia_vaso=ufloat(11.5,11.5*0.08+0.00001)
temperatura_vaso= B_fit_temperature_ufloat / unumpy.log(resistencia_vaso / A_fit_temperature_ufloat)
print(f"\nCalculated temperature of the water bath:")
print(f"T = {temperatura_vaso-273.15} ºC")