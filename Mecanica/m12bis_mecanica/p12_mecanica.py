import pandas as pd
import uncertainties
import matplotlib.pyplot as plt
import matplotlib as mpl
from uncertainties import unumpy
import numpy as np
from math import sqrt
from scipy.optimize import curve_fit
"""
Functions separate_uncertainties
In: unumpy.array
Returns the nominal and the error part as two separate numpy arrays arr
"""
def separate_uncertainties(uarray : unumpy.uarray):
    nominal=unumpy.nominal_values(uarray)
    error=unumpy.std_devs(uarray)
    return (nominal,error)
def generate_uncertainties_for_chi2_1(data=None, fit=None, num_params=None, x_data=None, y_data=None, x_fit=None, y_fit=None):
    """
    Generate uncertainties that produce chi_squared_red = 1
    We want to make the reduced chi-squared equal to 1,
    which means that the uncertainties should be set such
    that the sum of squared residuals divided by the degrees of freedom equals 1.
    
    Works for single axis or a pair of values (x, y).

    Args (single axis):
        data: measured data points (x or y)
        fit: fitted/theoretical values (x or y)
        num_params: number of parameters in the fit
    
    Args (pair of values):
        x_data: measured x data points
        y_data: measured y data points
        x_fit: fitted x values
        y_fit: fitted y values
        num_params: number of parameters in the fit
        
    Returns:
        uncertainties array or tuple of (x_uncertainties, y_uncertainties) for pairs
    """
    # Case 1: Single axis (original behavior)
    if data is not None and fit is not None and num_params is not None:
        residuals = data - fit
        dof = len(data) - num_params
        
        # Standard deviation of residuals
        sigma = np.sqrt(np.sum(residuals**2) / dof)
        
        # All uncertainties equal to sigma
        uncertainties = np.full_like(data, sigma, dtype=float)
        
        return uncertainties
    
    # Case 2: Pair of values (x, y)
    elif x_data is not None and y_data is not None and x_fit is not None and y_fit is not None and num_params is not None:
        # Calculate residuals in both dimensions
        x_residuals = x_data - x_fit
        y_residuals = y_data - y_fit
        
        # Combined residuals (distance in 2D space)
        combined_residuals = np.sqrt(x_residuals**2 + y_residuals**2)
        
        dof = len(x_data) - num_params
        
        # Standard deviation of combined residuals
        sigma = np.sqrt(np.sum(combined_residuals**2) / dof)
        
        # Uncertainties for each dimension
        x_uncertainties = np.full_like(x_data, sigma, dtype=float)
        y_uncertainties = np.full_like(y_data, sigma, dtype=float)
        
        return (x_uncertainties, y_uncertainties)
    
    else:
        raise ValueError("Provide either (data, fit, num_params) for single axis or (x_data, y_data, x_fit, y_fit, num_params) for pairs")
def calculate_b(X, r_0, k):
    v_0, theta = X
    # Ecuación reordenada para despejar b
    return np.cos(theta/2) * ((k / (mass * v_0**2)) * (1 / np.sin(theta/2)) - r_0)

"""
Fixed parameters for the plot
"""
g= 9.81 #Gravity acceleration, in m/s^2
b_exp=7.5e-2 #Initial distance to the well, in meters
mass=0.1 #Mass of the ball, in kg
uncertainty_constant=0.01 #Relative uncertainty for the measurements, as a fraction (e.g., 0.01 for 1%)

theta_14_exp=np.radians(103.5) #Scattering angle, in radians
theta_07_exp=np.radians(35)
theta_08_exp=np.radians(40)
theta_09_exp=np.radians(45)
theta_10_exp=np.radians(50)
theta_11_exp=np.radians(55)

r_0_exp=0.1 #Distance of the center of the well to the center of forces, in meters



"""
INTRODUCING DATA
The data for the laboratory practice is read from datospozo.txt
"""
# Read the datospozo.txt file
#Tracker has problems due the lenght of the arrays, so we will read each case separately, since they are in the same format
data_14= pd.read_csv("C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\1.4.txt", sep=',', header=None)
data_15=pd.read_csv("C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\1.5.txt", sep=',', header=None)
data_16=pd.read_csv("C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\1.6.txt", sep=',', header=None)
data_17=pd.read_csv("C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\1.7.txt", sep=',', header=None)
data_18=pd.read_csv("C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\1.8.txt", sep=',', header=None)
data_19=pd.read_csv("C:\\Users\\Andres\\proyectos\\Mecanica\\m12bis_mecanica\\1.9.txt", sep=',', header=None)


# The file has 6 cases with columns: t, x, y, v (repeated for each case)
# Cases: 1.4/18.4, 1.5/21.4, 1.6/16, 1.7/13.9, 1.8 12.9, 1.9 12.3
# Column indices: case1: 0(t),1(x),2(y),3(v), case2: 4,5,6,7, ..., case6: 20,21,22,23

# Extract data for each case
x_14=data_14[0].values
y_14=data_14[1].values
x_15=data_15[0].values
y_15=data_15[1].values
x_16=data_16[0].values
y_16=data_16[1].values
x_17=data_17[0].values
y_17=data_17[1].values
x_18=data_18[0].values
y_18=data_18[1].values
x_19=data_19[0].values
y_19=data_19[1].values


###Uncerainri
###INITIAL ANGLES
theta_14=np.radians(90+18.4)
theta_15=np.radians(90+21.4)
theta_16=np.radians(90+16)
theta_17=np.radians(90+13.9)
theta_18=np.radians(90+12.9)
theta_19=np.radians(90+12.3)
###r_0
r_0_exp=0.120e-2 #Distance of the center of the well to the center of forces, in m






### The uncertainties will be chosen artificially to chi reduced square=1, since the theory is already proven 

"""
Fit - For each height, fit and calculate uncertainties
"""
# 2. Agrupar los datos de todos los experimentos en arreglos
v_0_all = np.array([0.317,0.329,0.330,0.339,0.381,0.392])  # Velocidades iniciales para cada caso
theta_all = np.array([theta_14, theta_15, theta_16, theta_17, theta_18, theta_19])

# Las variables independientes en curve_fit para múltiples dimensiones se pasan juntas en una tupla
X_data = (v_0_all, theta_all)

# Variable dependiente. Asumiendo que b_exp (7.5 cm) fue el mismo para todos los tiros
b_all = np.full(6, b_exp) 

# 3. Hacer el ajuste (curve_fit)
popt_all, pcov_all = curve_fit(calculate_b, X_data, b_all, p0=[r_0_exp, 1e-5])
print(f"Valores ajustados: r_0 = {popt_all[0]:.4f}, k = {popt_all[1]:.2e}")
"""
Plotting - Each curve in a separate figure
"""
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(x_14,y_14, fmt='.--', color="black",
              label="h=1.4 cm", capsize=3, markersize=4)
plt.errorbar(x_16,y_16, fmt='.--', color="red",
              label="h=1.6 cm", capsize=3, markersize=4)
plt.errorbar(x_18,y_18,fmt='.--', color="blue",label="h=1.8 cm", capsize=3, markersize=4)
plt.xlabel('x (m)', fontsize=12)
plt.ylabel('y (m)', fontsize=12)
plt.title('Trayectorias experimentales 1', fontsize=14)
plt.legend()
plt.grid(False)
plt.show()

plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(x_15,y_15,fmt='.--', color="black",
              label="h=1.5 cm", capsize=3, markersize=4)
plt.errorbar(x_17,y_17, fmt='.--', color="red",
                label="h=1.7 cm", capsize=3, markersize=4)
plt.errorbar(x_19,y_19, fmt='.--', color="blue", label="h=1.9 cm", capsize=3, markersize=4)
plt.xlabel('x (m)', fontsize=12)
plt.ylabel('y (m)', fontsize=12)
plt.title('Trayectorias experimentales 2', fontsize=14)
plt.legend()
plt.grid(False)
plt.show()



print("Plotting completed!")
