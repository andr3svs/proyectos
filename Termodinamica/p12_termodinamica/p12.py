import pandas as pd
import uncertainties
import matplotlib.pyplot as plt
import matplotlib as mpl
from uncertainties import ufloat, unumpy
import numpy as np
from scipy import odr
import ufloat
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
def calculate_theta(params, time):
    """
    Calculates the temperature variation at position 'x' and time 't' for ODR.
    Parameters are first, then independent variable.
    
    Parameters:
    params : [Temperature_mean, amplitude, period, phase_shift]
    time   : Time (in seconds).
    """
    Temperature_mean, amplitude, period, phase_shift = params
    theta = Temperature_mean + amplitude * np.cos((2 * np.pi / period) * time - phase_shift)
    return theta
"""
Fixed parameters for the plot
"""
specific_heat_capacity = 897  # J/(kg*K), specific heat capacity of aluminum IM NOT SURE
density_aluminum = 2700  # kg/m^3, density of aluminum IM NOT SURE 
radius_of_cylinder = 0.01  # meters, radius of the aluminum cylinder IM NOT SURE
distance_between_sensors = ufloat(0.05, 0.001) # meters, distance between the two sensors IM NOT SURE
"""
INTRODUCING DATA
The data for the laboratory practice must be taken into an excel file, and this will read it.
"""
#Excel file location
excel_path_user="C:/Users/Andres/proyectos/p12_termodinamica/p12.xlsx"
data_raw=pd.read_excel(excel_path_user,sheet_name="Sheet")
tiempo  = unumpy.uarray(data_raw["tiempo"],data_raw["u_tiempo"])
theta1= unumpy.uarray(data_raw["theta1"],data_raw["u_theta1"])
theta2= unumpy.uarray(data_raw["theta2"],data_raw["u_theta2"])

"""
Data manipulation
"""
tiempo_nominal,tiempo_error= separate_uncertainties(tiempo)
theta1_nominal,theta1_error= separate_uncertainties(theta1)
theta2_nominal,theta2_error= separate_uncertainties(theta2)

### Mean temperature calculation    
theta1_mean = np.mean(theta1_nominal)
theta2_mean = np.mean(theta2_nominal)
### Amplitude estimation
theta1_amplitude_estimate = (np.max(theta1_nominal) - np.min(theta1_nominal)) / 2
theta2_amplitude_estimate = (np.max(theta2_nominal) - np.min(theta2_nominal)) / 2
""""
Plotting
"""
#h1_aire vs coeficiente adiabatico experimental
plt.figure(dpi=150)  # Adjust dpi value as needed for higher resolution
plt.errorbar(tiempo_nominal, theta1_nominal, yerr=theta1_error, xerr=tiempo_error, fmt='none', color="red",
              label="$\\theta_1$", capsize=3, markersize=4)
plt.errorbar(tiempo_nominal, theta2_nominal, yerr=theta2_error, xerr=tiempo_error, fmt='none', color="red",
              label="$\\theta_2$", capsize=3, markersize=4)

plt.xlabel('tiempo (s)', fontsize=12)
plt.ylabel('Temperatura (°C)', fontsize=12)
#Some options:
plt.title('Temperatura vs tiempo', fontsize=14)
plt.legend()
plt.grid(False)
#Do the plot
plt.show()
"""
3.Fitting the data
"""
# Initial guess for theta1
initial_guess_theta1 = [theta1_mean, theta1_amplitude_estimate, 540, 0.01]
# Create ODR model and fit for theta1, considering errors in both variables
model_theta1 = odr.Model(calculate_theta)
data_theta1 = odr.RealData(tiempo_nominal, theta1_nominal, sx=tiempo_error, sy=theta1_error)
odr_fit_theta1 = odr.ODR(data_theta1, model_theta1, beta0=initial_guess_theta1)
odr_result_theta1 = odr_fit_theta1.run()
# Extract the fitted parameters and their errors for theta1
A_fit_theta1, amp_fit_theta1, tau_fit_theta1, phase_theta1 = odr_result_theta1.beta
A_err_theta1, amp_err_theta1, tau_err_theta1, phase_err_theta1 = odr_result_theta1.sd_beta

# Initial guess for theta2
initial_guess_theta2 = [theta2_mean, theta2_amplitude_estimate, 540, 0.01]
# Create ODR model and fit for theta2, considering errors in both variables
model_theta2 = odr.Model(calculate_theta)
data_theta2 = odr.RealData(tiempo_nominal, theta2_nominal, sx=tiempo_error, sy=theta2_error)
odr_fit_theta2 = odr.ODR(data_theta2, model_theta2, beta0=initial_guess_theta2)
odr_result_theta2 = odr_fit_theta2.run()
# Extract the fitted parameters and their errors for theta2
A_fit_theta2, amp_fit_theta2, tau_fit_theta2, phase_theta2 = odr_result_theta2.beta
A_err_theta2, amp_err_theta2, tau_err_theta2, phase_err_theta2 = odr_result_theta2.sd_beta

# Print fitted parameters with their errors for theta1
print("\n=== Fitted Parameters for θ₁ ===")
print(f"A (Temperature mean):  {A_fit_theta1:.4f} ± {A_err_theta1:.4f}")
print(f"Amp (Amplitude):       {amp_fit_theta1:.6f} ± {amp_err_theta1:.6f}")
print(f"τ (Period):            {tau_fit_theta1:.4f} ± {tau_err_theta1:.4f}")
print(f"φ (Phase shift):       {phase_theta1:.6f} ± {phase_err_theta1:.6f}")

# Print fitted parameters with their errors for theta2
print("\n=== Fitted Parameters for θ₂ ===")
print(f"A (Temperature mean):  {A_fit_theta2:.4f} ± {A_err_theta2:.4f}")
print(f"Amp (Amplitude):       {amp_fit_theta2:.6f} ± {amp_err_theta2:.6f}")
print(f"τ (Period):            {tau_fit_theta2:.4f} ± {tau_err_theta2:.4f}")
print(f"φ (Phase shift):       {phase_theta2:.6f} ± {phase_err_theta2:.6f}")
#Parameters calculation
temp_mean=ufloat(A_fit_theta1, A_err_theta1)
amp1=ufloat(amp_fit_theta1, amp_err_theta1)
amp2=ufloat(amp_fit_theta2, amp_err_theta2)
tau=ufloat(tau_fit_theta1, tau_err_theta1)  # Assuming the period is the same for both fits, you can also use tau_fit_theta2 if needed
phase1=ufloat(phase_theta1, phase_err_theta1)
phase2=ufloat(phase_theta2, phase_err_theta2)
disphase=abs(phase1-phase2)

m_parameter=abs(unumpy.log(amp1/amp2))/distance_between_sensors
h_parameter=disphase/distance_between_sensors

K_exp=(specific_heat_capacity*density_aluminum*np.pi)/(h_parameter*m_parameter*(tau_fit_theta1+tau_fit_theta2)/2) #we use the average period    #540 is the period of the wave, which is a fixed parameter in this experiment
lambda_exp=K_exp*radius_of_cylinder*(h_parameter**2-m_parameter**2 )/2.0

# Write all parameters to a LaTeX-formatted txt file
with open("results.txt", "w") as f:
    f.write("% Fitted Parameters for θ₁\n")
    f.write(f"A_{{\\theta_1}} = {A_fit_theta1:.4f} \\pm {A_err_theta1:.4f}\n")
    f.write(f"\\text{{Amp}}_{{\\theta_1}} = {amp_fit_theta1:.6f} \\pm {amp_err_theta1:.6f}\n")
    f.write(f"\\tau_{{\\theta_1}} = {tau_fit_theta1:.4f} \\pm {tau_err_theta1:.4f}\n")
    f.write(f"\\phi_{{\\theta_1}} = {phase_theta1:.6f} \\pm {phase_err_theta1:.6f}\n\n")
    
    f.write("% Fitted Parameters for θ₂\n")
    f.write(f"A_{{\\theta_2}} = {A_fit_theta2:.4f} \\pm {A_err_theta2:.4f}\n")
    f.write(f"\\text{{Amp}}_{{\\theta_2}} = {amp_fit_theta2:.6f} \\pm {amp_err_theta2:.6f}\n")
    f.write(f"\\tau_{{\\theta_2}} = {tau_fit_theta2:.4f} \\pm {tau_err_theta2:.4f}\n")
    f.write(f"\\phi_{{\\theta_2}} = {phase_theta2:.6f} \\pm {phase_err_theta2:.6f}\n\n")
    
    f.write("% Derived Parameters\n")
    f.write(f"m = {unumpy.nominal_values(m_parameter):.6f} \\pm {unumpy.std_devs(m_parameter):.6f}\n")
    f.write(f"h = {unumpy.nominal_values(h_parameter):.6f} \\pm {unumpy.std_devs(h_parameter):.6f}\n")
    f.write(f"K_{{\\exp}} = {unumpy.nominal_values(K_exp):.6f} \\pm {unumpy.std_devs(K_exp):.6f}\n")
    f.write(f"\\lambda_{{\\exp}} = {unumpy.nominal_values(lambda_exp):.6f} \\pm {unumpy.std_devs(lambda_exp):.6f}\n")

print("Results saved to results.txt")
